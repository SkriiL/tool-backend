import sqlite3


def get_all():
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    c.execute('SELECT * FROM messages')
    messages = c.fetchall()
    conn.close()
    for i in range(len(messages)):
        messages[i] = {'id': messages[i][0], 'byId': messages[i][1], 'text': messages[i][2], 'date': messages[i][3]}
    return messages


def send(msg_str):
    msg = msg_str.split('|')
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    params = (len(get_all()) + 1, msg[0], msg[1], msg[2])
    c.execute('INSERT INTO messages VALUES(?, ?, ?, ?)', params)
    conn.commit()
    conn.close()