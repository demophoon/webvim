from pyramid.config import Configurator

from webvim.assets.websocket import TerminalClient


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_sockjs')
    config.include('pyramid_chameleon')

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_sockjs_route(prefix='/terminal', session=TerminalClient)
    config.scan()
    return config.make_wsgi_app()
