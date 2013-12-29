import json

from itertools import groupby

from pyramid.response import FileIter, Response
from pyramid.view import view_config
from pyramid.url import urlencode

import sqlalchemy as S
# from sqlalchemy.exc import DBAPIError

from sqlalchemy.orm import eagerload

from .models import DBSession, Cover, Music

from contextlib import contextmanager
from time import time


@contextmanager
def t(what):
    start = time()
    try:
        yield
    finally:
        print("Took {:.2f} to {}".format(time() - start, what))


@view_config(route_name='home', renderer='templates/home.pt')
def view_home(request):
    return {"base": base()}

    covers = DBSession.query(Cover).order_by(Cover.title).all()
    covers = u"".join(u"<div>{0}</div>".format(c.title) for c in covers)

    music = DBSession.query(Music).order_by(Music.title).all()
    # music = u"".join(u"<div>{0} -- {1} -- {2}</div>".format(
        # c.title, c.WorkName, c.Composer) for c in music)

    music = u"<pre>[{0}]</pre>".format(u",\n".join(m.json for m in music))

    # return {"covers": covers, "music": music}


@view_config(route_name='query', renderer='json')
def view_query(request):

    what = request.params.get("w", "title")
    query = request.params.get("term", None)

    attr = getattr(Music, what)

    q = DBSession.query(Music.id, attr, Cover.id, Cover.title).join(Cover)

    if query:
        terms = query.split()
        like_terms = [attr.like("%{}%".format(term))
                      for term in terms]  # if len(term) > 2]
        q = q.filter(S.and_(*like_terms))

    print("count({}) = {}".format(query, q.count()))

    with t("get vs for {!r}".format(query)):
        vs = q.all()

    def mk_value(v):
        music_id, attr, cover_id, cover_title = v
        return dict(
            music_id=music_id,
            attr=attr,
            cover_id=cover_id,
            cover_title=cover_title,
        )

    values = [mk_value(v) for v in vs]

    # values = [{"music_": v, "value": i, "cover": c} for (i, v, c) in vs]

    # TODO: natsort values
    # (sorting of flat vs sharp?)

    # TODO: sort vs by edit distance to query
    # with t("sort by edit distance"):
        # values.sort(key=lambda v: (edit_distance(query, v), v), reverse=True)

    # Limit to a max of 100 responses
    values = values[:100]

    return values


from sqlalchemy.sql import func


@view_config(route_name="composers", renderer="templates/composers.pt")
def view_composers(request):
    composers = DBSession.query(Music.Composer, func.count(Music.Composer)
                                ).group_by(Music.Composer
                                           ).order_by(Music.Composer).all()

    return {"base": base(), u"composers": composers}


def table_group(records, key):

    rowspans = []
    evens = []

    for i, (cover, cs) in enumerate(groupby(records, key=key)):

        n = len(list(cs))
        evens.extend("" if i % 2 else "tr-even" for _ in xrange(n))

        rowspans.append(n)
        for i in xrange(n - 1):
            # Use rowspan=0 for non-present items
            rowspans.append(0)

    return zip(records, rowspans, evens)


@view_config(route_name="composer", renderer="templates/list_music.pt")
def view_composer(request):
    composer = request.matchdict["composer"]

    music = DBSession.query(Music).filter(
        Music.Composer == composer)

    music = music.options(eagerload(Music.cover))

    music = music.all()

    result = table_group(music, key=lambda v: v.cover)

    return {
        u"base": base(),
        u"title": u"Music composed by {}".format(composer),
        u"music": result,
    }


from pyramid.renderers import get_renderer


def base():
    return get_renderer("templates/base.pt").implementation()


@view_config(route_name="cover", renderer="templates/cover.pt")
def view_cover(request):
    cover_id = request.matchdict["cover_id"]

    cover = DBSession.query(Cover).filter(Cover.id == cover_id).one()
    return {"cover": cover, "base": base()}


@view_config(route_name="download")
def view_download(request):
    # TODO(pwaller): safe backup
    # raise RuntimeError
    # return Response("", content_type="text/plain")
    # return FileResponse(DBSession.bind.url.database)
    fd = open(DBSession.bind.url.database)
    cd = 'attachment; filename="collector.sqlite"'
    return Response(app_iter=FileIter(fd), content_disposition=cd)


@view_config(route_name="soloists", renderer="templates/list_music.pt")
def view_soloists(request):
    # return NotImplementedError("Soloist = {}".format()

    soloist = request.matchdict["soloist"]

    expr = S.or_(Music.Solo1.like("%{}%".format(soloist)))
    music = DBSession.query(Music)
    music = music.options(eagerload(Music.cover))

    music = music.filter(expr)

    music = music.limit(100)
    music = music.all()

    return {
        "base": base(),
        "music": table_group(music, lambda m: m.cover),
        "title": u"Soloist {}".format(soloist)
    }
