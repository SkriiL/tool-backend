import sqlite3


def get_all():
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    c.execute('SELECT * FROM books')
    books = c.fetchall()
    conn.close()
    for i in range(len(books)):
        books[i] = {'id': books[i][0], 'title': books[i][1], 'author': books[i][2], 'price': books[i][3],
                    'own': books[i][4], 'read': books[i][5], 'link': books[i][6], 'userId': books[i][7]}
    return books


def get_all_for_user(id):
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    params = (int(id), )
    c.execute('SELECT * FROM books WHERE userId=?', params)
    books = c.fetchall()
    for i in range(len(books)):
        books[i] = {'id': books[i][0], 'title': books[i][1], 'author': books[i][2], 'price': books[i][3],
                    'own': books[i][4], 'read': books[i][5], 'link': books[i][6], 'userId': books[i][7]}
    return books


def delete(id):
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    params = (int(id), )
    c.execute('DELETE FROM books WHERE id=?', params)
    conn.commit()
    conn.close()


def add(book_str, id_str='-1'):
    book = book_str.split('|')
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    if id_str == '-1':
        params = (len(get_all()) + 1, book[0], book[1], book[2], book[3], book[4], book[5], int(book[6]))
    else:
        params = (int(id_str), book[0], book[1], book[2], book[3], book[4], book[5], int(book[6]))
    c.execute('INSERT INTO books VALUES(?, ?, ?, ?, ?, ?, ?, ?)', params)
    conn.commit()
    conn.close()


def edit(book_str):
    book = book_str.split('|')
    book_str = book[1] + '|' + book[2] + '|' + book[3] + '|' + book[4] + '|' + book[5] + '|' + book[6] + '|' + book[7]
    delete(book[0])
    add(book_str, book[0])
