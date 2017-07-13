import requests
from pyramid.config import Configurator
from pyramid.view import view_config
import pyramid_beaker

def includeme(config):
    """Add the Velruse standalone app configuration to a Pyramid app."""
    settings = config.registry.settings
    config.add_directive('register_velruse_store', register_velruse_store)

    # setup application
    setup = settings.get('setup') or default_setup
    if setup:
        config.include(setup)

    # include supported providers
    for provider in settings_adapter:
        config.include('velruse.providers.%s' % provider)

    # configure requested providers
    for provider in find_providers(settings):
        load_provider(config, provider)

    # check for required settings
    if not settings.get('endpoint'):
        raise ConfigurationError(
            'missing required setting "endpoint"')

    # add views
    config.add_view(
        auth_complete_view,
        context='velruse.AuthenticationComplete')
    config.add_view(
        auth_denied_view,
        context='velruse.AuthenticationDenied')
    config.add_view(
        auth_info_view,
        name='auth_info',
        request_param='format=json',
        renderer='json')

def main(global_config, **settings):
	""" This function returns a Pyramid WSGI application.
	"""
    config = Configurator(settings=settings)
    config.include('pyramid_debugtoolbar')
    config.add_route('login', '/login')
    config.add_route('logged_in', '/logged_in')
	# Configure Beaker sessions and caching.
	config.include("pyramid_beaker")
	config.include('pyramid_mako')
	config.add_mako_renderer('.html')

	# Templates ending in ".html" should be rendered with Mako.
	#config.add_renderer(".html", "pyramid.mako_templating.renderer_factory")

	# Configure subscribers: URL generator, renderer globals.
	config.include(".subscribers")

	# Add routes and views.
	config.add_route("home", "/")
	config.add_route("grid_video", "/grid")
	config.include("akhet.pony")
	
	config.scan(".views")

	# Add static route to overlay static directory onto URL "/".
	config.include("akhet.static")
	config.add_static_route("appgrid", "static", cache_max_age=3600)
	config.include(includeme)

	return config.make_wsgi_app()
