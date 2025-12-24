import sqlite3
import pandas as pd

from app_model.db import conn
from app_model.users import add_user, get_user
from hashing import generate_hash, is_valid_hash



#user registration
def register_user(conn):
    name = input('Enter your name: > ')
    password = input('Enter your password: > ')
    hash_password = generate_hash(password)
    role = input('Enter role (admin/user): > ')
    add_user(conn, name, hash_password, role)


#user log in
def log_in_user(conn):
    name = input('Enter your name: > ')
    password = input('Enter your password: > ')
    user = get_user(conn,name)

    if user is None:
        print("User Not Found.")
        return None

    id, user_name,user_hash,role = get_user(conn, name)
    if is_valid_hash(password, user_hash):
        print(f'Welcome {user_name} !!!')
        return role
    else:
        print("Incorrect Password.")
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
            register_user(conn)
        elif choice == '2':
            role = log_in_user(conn)
            if role:
                print(f'Logged in successfully! Role: {role}')
            else:
                print('Incorrect Log in. Please Try again')
        elif choice == '3':
            print('Goodbye!')
            break

if __name__ == '__main__':
    main()















