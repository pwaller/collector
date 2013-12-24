from pyramid.response import Response
from pyramid.view import view_config

# from sqlalchemy.exc import DBAPIError

from .models import DBSession, Cover, Music


@view_config(route_name='home', renderer='templates/home.pt')
def view_home(request):
    covers = DBSession.query(Cover).order_by(Cover.title).all()
    covers = u"".join(u"<div>{0}</div>".format(c.title) for c in covers)

    music = DBSession.query(Music).order_by(Music.title).all()
    # music = u"".join(u"<div>{0} -- {1} -- {2}</div>".format(c.title, c.WorkName, c.Composer) for c in music)

    music = u"<pre>[{0}]</pre>".format(u",\n".join(m.json for m in music))

    return {"covers": covers, "music": music}
