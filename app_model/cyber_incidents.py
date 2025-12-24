import pandas as pd
from app_model.db import get_connection

def migrate_cyber_incidents():
    conn = get_connection()
    data = pd.read_csv('DATA/cyber_incidents.csv')
    data.to_sql('cyber_incidents', conn, if_exists='replace', index=False)
    conn.close

def get_all_cyber_incidents():
    conn = get_connection()
    sql = 'SELECT * FROM cyber_incidents'
    data = pd.read_sql(sql, conn)
    conn.close
    return data

