import sqlite3
import pandas as pd

def create_user_table():
    curr = conn.cursor()
    sql = """CREATE TABLE IF NOT EXISTS users ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    username TEXT NOT NULL UNIQUE, 
    password_hash TEXT NOT NULL 
    ) """
    curr.execute(sql)
    conn.commit()

def add_user(conn, name, hash_password):
    curr = conn.cursor()
    sql = """INSERT INTO users (username, password_hash) VALUES (?, ?)"""
    param = (name, hash_password)
    curr.execute(sql,param)
    conn.commit()

def migrate_users():
    with open('DATA/user.txt')as f:
        users = f.readlines()

    for user in users:
        name, hash = user.strip().split(',')
        add_user(conn, name, hash)
    conn.close()

def get_all_users():
    curr = conn.cursor()
    sql = "SELECT * FROM users"
    curr.execute(sql)
    users = curr.fetchall()
    conn.close()
    return users

def migrate_cyber_incidents():
    cyber = pd.read_csv('DATA/cyber_incidents.csv')
    cyber.to_sql('cyber_incidents', conn, if_exists='append', index=False)

def migrate_datasets_metadata():
    datasets = pd.read_csv('DATA/datasets_metadata.csv')
    datasets.to_sql('datasets_metadata', conn, if_exists='append', index=False)

def migrate_it_tickets():
    tickets = pd.read_csv('DATA/it_tickets.csv')
    tickets.to_sql('it_tickets', conn, if_exists='append', index=False)


conn = sqlite3.connect('DATA/intelligence_platform.db')