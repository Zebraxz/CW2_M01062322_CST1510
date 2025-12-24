import sqlite3

def add_user(conn, name, hash, role='user'):
    cur = conn.cursor()
    sql = '''INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)'''
    param = (name, hash, role)
    try:
        cur.execute(sql, param)
        conn.commit()
        print(f"User '{name}' added successfully with role '{role}'!")
    except sqlite3.IntegrityError:
        print(f"Username '{param[0]}' already exists. Choose a different name.")



def migrate_users(conn):
    with open(r'DATA\users.txt', 'r') as f:
        users = f.readlines()

    for user in users:
        name, hash, role = user.strip().split(',')
        add_user(conn, name, hash, role)



def get_all_users(conn):
    cur = conn.cursor()
    sql = '''SELECT * FROM users'''
    cur.execute(sql)
    users = cur.fetchall()
    return(users)


def get_user(conn,name):
    cur = conn.cursor()
    sql = '''SELECT * FROM users WHERE username = ?'''
    param = (name,)
    cur.execute(sql, param)
    user = cur.fetchone()
    return(user)


def update_user_role(conn, username, new_role):
    cur = conn.cursor()
    sql = 'UPDATE users SET role = ? WHERE username = ?'
    param = (new_role, username)
    cur.execute(sql, param)
    conn.commit()

def delete_user(conn, user_name):
    cur = conn.cursor()
    sql = 'DELETE FROM users WHERE username = ?'
    param = (user_name,)
    cur.execute(sql, param)
    conn.commit()