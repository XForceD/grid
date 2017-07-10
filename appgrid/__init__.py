from pyramid.config import Configurator
import pyramid_beaker

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    # Configure Beaker sessions and caching.
    config.include("pyramid_beaker")
	config.include('pyramid_mako')
	config.add_mako_renderer('.html')

    # Templates ending in ".html" should be rendered with Mako.
    config.add_renderer(".html", "pyramid.mako_templating.renderer_factory")

    # Configure subscribers: URL generator, renderer globals.
    config.include(".subscribers")

    # Add routes and views.
    config.add_route("home", "/")
    config.include("appgrid.pony")
    config.scan(".views")

    # Add static route to overlay static directory onto URL "/".
    config.include("appgrid.static")
    config.add_static_route("appgrid", "static", cache_max_age=3600)

    return config.make_wsgi_app()
