from aiohttp import web
import socketio
import users
import books

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


# -------------------------- USER ---------------------------


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


@sio.on('getAllUsers')
async def get_all_users(sid):
    users_ = users.get_all()
    await send_users(sid, users_)


async def send_users(sid, users_):
    await sio.emit('users', users_, room=sid)


@sio.on('createUser')
async def create_user(sid, user):
    users.create(user)


@sio.on('editUser')
async def edit_user(sid, user):
    users.edit(user)


# --------------------------- BOOKS -------------------------


@sio.on('getBooksForUser')
async def get_books_for_user(sid, id):
    books_ = books.get_all_for_user(id)
    await send_books(sid, books_)


async def send_books(sid, books_):
    await sio.emit('books', books_, room=sid)


@sio.on('editBook')
async def edit_book(sid, book):
    books.edit(book)


@sio.on('addBook')
async def edit_book(sid, book):
    books.add(book)


@sio.on('deleteBook')
async def edit_book(sid, id_str):
    books.delete(id_str)


app.router.add_get('/', index)

if __name__ == '__main__':
    web.run_app(app, port='56789')