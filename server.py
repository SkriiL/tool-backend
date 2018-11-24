from aiohttp import web
import socketio
import users

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)


async def index(request):
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')


@sio.on('connect')
def connect(sid, environ):
    print(sid + " connected")
    sio.enter_room(sid, room='standard')


@sio.on('getUserById')
async def get_user_by_id(sid, id_str):
    user = users.get_single_by_id(id_str)
    await send_user(sid, user)


@sio.on('getUserByUsername')
async def get_user_by_username(sid, username):
    user = users.get_single_by_username(username)
    await send_user(sid, user)


async def send_user(sid, user):
    await sio.emit('user', user, room=sid)


@sio.on('createUser')
async def create_user(sid, user):
    users.create(user)


app.router.add_get('/', index)

if __name__ == '__main__':
    web.run_app(app, port='56789')