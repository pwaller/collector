from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import Base, DBSession


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('home', '/')
    config.add_route('download', '/download')
    config.add_route('query', '/query')

    config.add_route('cover', '/covers/{cover_id}', request_method="GET")
    config.add_route('cover_put', '/covers/{cover_id}', request_method="PUT")
    config.add_route('cover_post', '/covers/{cover_id}', request_method="POST")
    config.add_route('cover_new', '/covers', request_method="POST")

    config.add_route('type', '/type/{who}')
    config.add_route('types', '/types/')

    config.add_route('composer', '/composers/{who}')
    config.add_route('composer_type', '/composers/{who}/type/{type}')
    config.add_route('composers', '/composers/')

    config.add_route('conductor', '/conductors/{who}')
    config.add_route('conductors', '/conductors/')

    config.add_route('soloist', '/soloists/{who}')
    config.add_route('soloists', '/soloists/')

    config.add_route('ensemble', '/ensembles/{who}')
    config.add_route('ensembles', '/ensembles/')

    config.scan()

    return config.make_wsgi_app()
