from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config


@view_config(
	route_name='video_post'
)
def video_post():
	lst = 0.0; msg = []
	room = get_post('room')
	user_id= get_post('user_id')
	last= float(get_post('last', 0))
	mess= get_post('mess')
#	doc = db.chat.find_one({'_id':room})
	if mess:
		doc['mess'].append((time.time(), mess, user_id))
#		db.chat.save(doc)
	for i_time, i_msg, i_user in doc['mess']:
		if i_user != user_id and i_time > last:
			lst = i_time
			msg.append((i_time, i_user, i_msg))
	if not lst: lst = last
	return json.dumps({'result': 'ok', 'last': lst, 'msg': msg})

#def connect():
#	mongo = Connection('localhost', 27017)
#	db = mongo['db']
#	db.authenticate('user', 'pass')
#	return db

#db = connect()

	
def get_post(name, default = None):
	return request.POST[name] if name in request.POST else default	

def chat(room):
#	doc = db.chat.find_one({'_id':room})
	initiator = 1
	if not doc:
		initiator = 0
		doc = {'_id':room, 'mess': []}
		db.chat.save(doc)
	return templ('rtc.tpl', initiator = initiator, room=room)
	
def hello_world(request):
    return Response('Hello Force!' )	

if __name__ == '__main__':
	config = Configurator()
	config.add_route('post_grid', '/post_grid')
	config.add_view(hello_world, route_name='post_grid')	
	app = config.make_wsgi_app()
	server = make_server('0.0.0.0', 8080, app)
	server.serve_forever()