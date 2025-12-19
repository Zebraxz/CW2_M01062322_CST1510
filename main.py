import bcrypt 
import sqlite3
import pandas as pd

#hashed using bcrypt
def generate_hash(psw):
    byte_psw = psw.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(byte_psw, salt)
    return hash.decode('utf-8')

#validating hash vs psw
def is_valid_hash(psw, hash):
    hash_ = hash.encode('utf-8')
    byte_psw = psw.encode('utf-8')
    is_valid = bcrypt.checkpw(byte_psw, hash_)
    return (is_valid)


#user registration
def register_user():
    name = input('Enter your name: > ')
    password = input('Enter your password: > ')
    hash_password = generate_hash(password)
    role = input('Enter role (admin/user): > ')
    with open('DATA/users.txt', 'a') as f:
        f.write(f'{name},{hash_password},{role}\n')
    print('User Successfully Registered!')

#user log in
def log_in_user():
    name = input('Enter your name: > ')
    password = input('Enter your password: > ')
    with open('DATA/users.txt', 'r') as f:
        users = f.readlines()
    for user in users:
        user_name,user_hash,role = user.strip().split(',')
        if name == user_name and is_valid_hash(password, user_hash):
            return role
    return None

def main():
    while True:
        print('Welcome to the system!')
        print('Please choose from the following options:')
        print('1. To Register With Us')
        print('2. To Log Back in')
        print('3. To Safely Exit:')
        
        choice = input(': > ')

        if choice  == '1':
            register_user()
        elif choice == '2':
            role = log_in_user()
            if role:
                print(f'Logged in successfully! Role: {role}')
            else:
                print('Incorrect Log in. Please Try again')
        elif choice == '3':
            print('Goodbye!')
            break

#if __name__ == '__main__':
    #main()



def create_user_table(conn):
    cur = conn.cursor()
    sql = '''CREATE TABLE users ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    username TEXT NOT NULL UNIQUE, 
    password_hash TEXT NOT NULL, 
    role TEXT DEFAULT 'user' );
    '''
    cur.execute(sql)
    conn.commit()

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
    param = ('user_name',)
    cur.execute(sql, param)
    conn.commit()

def migrate_cyber_incidents(conn):
    data = pd.read_csv('DATA/cyber_incidents.csv')
    data.to_sql('cyber_incidents', conn, if_exists='replace', index=False)

def migrate_datasets_metadata(conn):
    data = pd.read_csv('DATA/datasets_metadata.csv')
    data.to_sql('datasets_metadata', conn, if_exists='replace', index=False)

def migrate_it_tickets(conn):
    data = pd.read_csv('DATA/it_tickets.csv')
    data.to_sql('it_tickets', conn, if_exists='replace', index=False)

def get_all_cyber_incidents(conn):
    sql = 'SELECT * FROM cyber_incidents'
    data = pd.read_sql(sql, conn)
    conn.close()
    return(data)

def get_all_datasets_metadata(conn):
    sql = 'SELECT * FROM datasets_metadata'
    data = pd.read_sql(sql, conn)
    conn.close()
    return(data)

def get_all_it_tickets(conn):
    sql = 'SELECT * FROM it_tickets'
    data = pd.read_sql(sql, conn)
    conn.close()
    return(data)


conn = sqlite3.connect('DATA/project_data.db')
print(get_all_it_tickets(conn))
