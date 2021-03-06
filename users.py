import sqlite3


def get_all():
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    users = c.fetchall()
    conn.close()
    for i in range(len(users)):
        users[i] = {'id': users[i][0], 'username': users[i][1], 'email': users[i][2], 'password': users[i][3], 'imgUrl': users[i][4], 'rights': users[i][5]}
    return users


def get_single_by_id(id_str):
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    params = (int(id_str), )
    c.execute('SELECT * FROM users WHERE id=?', params)
    user = c.fetchone()
    conn.close()
    user = {'id': user[0], 'username': user[1], 'email': user[2], 'password': user[3], 'imgUrl': user[4], 'rights': user[5]}
    return user


def get_single_by_username(username):
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    params = (username, )
    try:
        c.execute('SELECT * FROM users WHERE username=?', params)
        user = c.fetchone()
        conn.close()
        user = {'id': user[0], 'username': user[1], 'email': user[2], 'password': user[3], 'imgUrl': user[4], 'rights': user[5]}
        return user
    except:
        return {'id': -1, 'username': '', 'email': '', 'password': '', 'imgUrl': ''}


def create(user_str, id='-1'):
    user = user_str.split('|')
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    if id == '-1':
        params = (len(get_all()) + 1, user[0], user[1], user[2], user[3], int(user[4]))
    else:
        params = (int(id), user[0], user[1], user[2], user[3], int(user[4]))
    c.execute('INSERT INTO users VALUES(?, ?, ?, ?, ?, ?)', params)
    conn.commit()
    conn.close()


def delete(id):
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    params = (int(id), )
    c.execute('DELETE FROM users WHERE id=?', params)
    conn.commit()
    conn.close()


def edit(user_str):
    user = user_str.split('|')
    user_str = user[1] + '|' + user[2] + '|' + user[3] + '|' + user[4] + '|' + user[5]
    delete(user[0])
    create(user_str, user[0])