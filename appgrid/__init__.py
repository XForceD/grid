import requests
from pyramid.config import Configurator
from pyramid.view import view_config
import pyramid_beaker

@view_config(route_name='login', renderer='myapp:templates/login.mako')
def login(request):
	return {}


@view_config(route_name='logged_in', renderer='json')
def logged_in(request):
	token = request.POST['token']
	payload = {'format': 'json', 'token': token}
	response = requests.get(request.host_url + '/velruse/auth_info', params=payload)
	return {'result': response.json}

def main(global_config, **settings):
	""" This function returns a Pyramid WSGI application.
	"""
	config = Configurator(settings=settings)

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
	config.add_route('login', '/login')
	config.add_route('logged_in', '/logged_in')	
	config.include("akhet.pony")
	config.scan(".views")

	# Add static route to overlay static directory onto URL "/".
	config.include("akhet.static")
	config.add_static_route("appgrid", "static", cache_max_age=3600)

	return config.make_wsgi_app()
