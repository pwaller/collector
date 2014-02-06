import json

from collections import defaultdict
from itertools import groupby

from pyramid.httpexceptions import HTTPFound
from pyramid.response import FileIter, Response
from pyramid.view import view_config
from pyramid.url import urlencode

import sqlalchemy as S
# from sqlalchemy.exc import DBAPIError

from sqlalchemy.orm import eagerload

from .models import DBSession, Cover, Music

from contextlib import contextmanager
from time import time


from pyramid.renderers import get_renderer


# TODO: Use a subscriber instead
def base():
    return get_renderer("templates/base.pt").implementation()

# from repoze.events import subscriber
from pyramid.interfaces import IBeforeRender


# @subscriber(IBeforeRender)
def add_global(event):
    event['testglob'] = 'foo'


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
    q = DBSession.query(Music.Composer, func.count(Music.Composer))

    title = "Composers"

    if "type" in request.params:
        title = request.params["type"]
        q = q.filter(Music.MusicType == request.params["type"])

    composers = q.group_by(Music.Composer).order_by(Music.Composer).all()

    return {
        u"base": base(),
        u"routename": "composer",
        u"people": composers,
        u"title": title,
        u"_query": {},
    }


@view_config(route_name="conductors", renderer="templates/composers.pt")
def view_conductors(request):
    conductors = DBSession.query(Music.Conductor, func.count(Music.Conductor)
                                 ).group_by(Music.Conductor
                                            ).order_by(Music.Conductor).all()

    return {
        u"base": base(),
        u"people": conductors,
        u"title": u"Conductors",
        u"routename": u"conductor",
        u"_query": {},
    }


@view_config(route_name="ensembles", renderer="templates/composers.pt")
def view_ensembles(request):
    ensembles = DBSession.query(Music.Ensemble, func.count(Music.Ensemble)
                                ).group_by(Music.Ensemble
                                           ).order_by(Music.Ensemble).all()

    return {
        u"base": base(),
        u"people": ensembles,
        u"title": u"Ensembles",
        u"routename": u"ensemble",
        u"_query": {},
    }


@view_config(route_name="soloists", renderer="templates/composers.pt")
def view_soloists(request):

    def get_s(what):
        return DBSession.query(what, func.count(what)).group_by(what).all()

    ss = Music.Solo1, Music.Solo2, Music.Solo3, Music.Solo4

    soloists = defaultdict(int)

    for s in ss:
        for key, value in get_s(s):
            soloists[key] += value

    return {
        u"base": base(),
        u"people": sorted(soloists.items()),
        u"title": u"Soloists",
        u"routename": u"soloist",
        u"_query": {},
    }


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


def composer_query(composer):
    """
    Return music by `composer`
    """

    music = DBSession.query(Music).filter(
        Music.Composer == composer)

    music = music.options(eagerload(Music.cover))

    return music


@view_config(route_name="composer", renderer="templates/list_music.pt")
def view_composer(request):
    composer = request.matchdict["who"]

    fmt = u"Music composed by {}"

    music = composer_query(composer)

    if "type" in request.params:
        music = music.filter(Music.MusicType == request.params["type"])

    if "q" in request.params:
        music = music.filter(Music.title.like("%{}%".format(request.params["q"])))

    music = music.all()

    result = table_group(music, key=lambda v: v.cover)

    return {
        u"base": base(),
        u"title": fmt.format(composer),
        u"music": result,
    }


@view_config(route_name="composer_type", renderer="templates/list_music.pt")
def view_composer_type(request):
    composer = request.matchdict["who"]
    type_ = request.matchdict["type"]

    fmt = u"{} composed by {}"

    music = composer_query(composer)
    music = music.all()

    result = table_group(music, key=lambda v: v.cover)

    return {
        u"base": base(),
        u"title": fmt.format(type_, composer),
        u"music": result,
    }

    if "type" in request.params:
        music = music.filter(Music.MusicType == request.params["type"])
        fmt = u"{} composed by {{}}".format(request.params["type"])


@view_config(route_name="conductor", renderer="templates/list_music.pt")
def view_conductor(request):
    conductor = request.matchdict["who"]

    music = DBSession.query(Music).filter(
        Music.Conductor == conductor)

    music = music.options(eagerload(Music.cover))

    music = music.all()

    result = table_group(music, key=lambda v: v.cover)

    return {
        u"base": base(),
        u"title": u"Music conducted by {}".format(conductor),
        u"music": result,
    }


@view_config(route_name="ensemble", renderer="templates/list_music.pt")
def view_ensemble(request):
    ensemble = request.matchdict["who"]

    # TODO(pwaller): query covers which have a music.ensemble

    music = DBSession.query(Music).filter(
        Music.Ensemble == ensemble).order_by(Music.title)

    music = music.options(eagerload(Music.cover))

    music = music.all()

    result = table_group(music, key=lambda v: v.cover)

    return {
        u"base": base(),
        u"title": u"Music performed by {}".format(ensemble),
        u"music": result,
    }


@view_config(route_name="cover_put", renderer="json")
def update_cover(request):
    p = request.params

    if "cover_id" in p:
        # cover specific updates
        cover_id = p["cover_id"]
        c = DBSession.query(Cover).get(cover_id)
        if p["field"] == "title":
            c.title = p["value"]
        elif p["field"] == "notes":
            c.CommentsC = p["value"]
            print "Updated CommentsC: ", c.CommentsC
        else:
            raise NotImplementedError
        return {"status": "success"}

    music_id, field, value = p["music_id"], p["field"], p["value"]

    if p["field"] == "Soloists":
        raise NotImplementedError

    m = DBSession.query(Music).get(music_id)

    setattr(m, p["field"], p["value"])

    # DBSession.commit()

    return {"status": "success"}


@view_config(route_name="cover_new", renderer="json")
def cover_new(request):
    c = Cover(request.params["title"])
    DBSession.add(c)
    DBSession.flush()
    return HTTPFound(request.route_url("cover", cover_id=c.id))
    return request.params["title"]


@view_config(route_name="cover_post", renderer="json")
def cover_add_music(request):
    p = request.params

    cover_id = request.matchdict["cover_id"]

    # m = Music()
    # c.musi
    # music_id = p["music_id"]

    c = DBSession.query(Cover).get(cover_id)

    m = Music()
    c.music.append(m)

    # c = Cover()
    # DBSession.add(c)

    # m.music.append(c)

    print "Added new music to cover: {}".format(c, m)

    # DBSession.commit()

    return {"status": "success", "newId": m.id}


@view_config(route_name="cover", renderer="templates/cover.pt")
def view_cover(request):
    cover_id = request.matchdict["cover_id"]

    cover = DBSession.query(Cover).filter(Cover.id == cover_id).one()

    def complete_distinct(what):
        values = DBSession.query(what).distinct().order_by(what).all()
        return json.dumps([{"value": x} for (x,) in values])

    # Used so that the "Add new row" button can copy this record if the cover
    # is otherwise empty.
    # class Placeholder(object):
    #     id = None
    #     title = ""
    #     PerfDateX = ""

    placeholder = Music()

    # <td><div contenteditable class="input-soloists">
    # <td><div contenteditable class="input-conductor">
    # <td><div contenteditable class="input-chorus">
    # <td><div contenteditable class="input-ensemble">
    # <td><div contenteditable class="input-musicclass">
    return {
        "base": base(),
        "cover": cover,
        "composers": complete_distinct(Music.Composer),
        "musicTypes": complete_distinct(Music.MusicType),
        "instruments": complete_distinct(Music.Instrument),
        # "soloists": Music.complete_soloists(),
        "soloists": [],
        "conductors": complete_distinct(Music.Conductor),
        "choruses": complete_distinct(Music.Chorus),
        "ensembles": complete_distinct(Music.Ensemble),
        "musicClasses": complete_distinct(Music.MusicClass),
        "placeholder": placeholder,
    }


@view_config(route_name="download")
def view_download(request):
    # TODO(pwaller): safe backup
    # raise RuntimeError
    # return Response("", content_type="text/plain")
    # return FileResponse(DBSession.bind.url.database)
    fd = open(DBSession.bind.url.database)
    cd = 'attachment; filename="collector.sqlite"'
    return Response(app_iter=FileIter(fd), content_disposition=cd)


@view_config(route_name="soloist", renderer="templates/list_music.pt")
def view_soloist(request):
    # return NotImplementedError("Soloist = {}".format()

    soloist = request.matchdict["who"]

    ss = Music.Solo1, Music.Solo2, Music.Solo3, Music.Solo4
    expr = S.or_(*(s.like("%{}%".format(soloist)) for s in ss))

    music = DBSession.query(Music)

    music = music.filter(expr)
    music = music.options(eagerload(Music.cover))

    # music = music.limit(100)
    music = music.all()

    return {
        "base": base(),
        "music": table_group(music, lambda m: m.cover),
        "title": u"Soloist {}".format(soloist)
    }


@view_config(route_name="types", renderer="templates/composers.pt")
def view_types(request):
    types = DBSession.query(Music.MusicType, func.count(Music.MusicType)
                            ).group_by(Music.MusicType
                                       ).order_by(Music.MusicType).all()

    return {
        u"base": base(),
        u"people": types,
        u"title": u"Music types",
        u"routename": u"type",
        u"_query": {},
    }


@view_config(route_name="type", renderer="templates/composers.pt")
def view_type(request):

    what = request.matchdict["who"]

    q = DBSession.query(Music.Composer, func.count(
        Music.Composer)).filter(Music.MusicType == what)

    composers = q.group_by(Music.Composer).order_by(Music.Composer).all()

    return {
        u"base": base(),
        u"routename": "composer",
        u"people": composers,
        u"title": "Composers of {}".format(what),
        u"_query": {"type": what},
    }
