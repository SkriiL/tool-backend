from aiohttp import web
import socketio
import users
import books
import messages
import maths

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
    await send_user_id(sid, user)


async def send_user_id(sid, user):
    event = 'user' + str(user['id'])
    await sio.emit(event, user, room=sid)


@sio.on('getUserByUsername')
async def get_user_by_username(sid, username):
    user = users.get_single_by_username(username)
    await send_user_username(sid, user)


async def send_user_username(sid, user):
    await sio.emit('user', user, room=sid)


@sio.on('getAllUsers')
async def get_all_users(sid, arg):
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


@sio.on('deleteUser')
async def delete_user(sid, id_str):
    users.delete(id_str)


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


@sio.on('searchBook')
async def search_book(sid, search_str):
    books_ = books.search(search_str)
    await send_searched_books(sid, books_)


async def send_searched_books(sid, books_):
    await sio.emit('searchedBook', books_, room=sid)


# --------------------------- MESSAGES ---------------------


@sio.on('sendMessage')
async def send_msg(sid, msg_str):
    messages.send(msg_str)
    msgs = messages.get_all()
    await send_messages(-1, msgs)


@sio.on('getAllMessages')
async def get_messages(sid, arg):
    msgs = messages.get_all()
    await send_messages(sid, msgs)


async def send_messages(sid, msgs):
    if sid == -1:
        await sio.emit('allMessages', msgs)
    else:
        await sio.emit('allMessages', msgs, room=sid)


# --------------------------- MATHS ---------------------


@sio.on('getDeriv')
async def get_deriv(sid, args):
    deriv = maths.get_deriv(args)
    await send_expression(sid, deriv)


async def send_expression(sid, expr):
    await sio.emit('mathExpression', expr, room=sid)


app.router.add_get('/', index)

if __name__ == '__main__':
    web.run_app(app, port='56789')