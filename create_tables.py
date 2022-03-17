import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def creat_table(conn):
    c=conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS USERS ( user_name varchar(10) primary key
    , password integer not null )""")
    c.execute("""
    CREATE TABLE IF NOT EXISTS GROUPS(user_name varchar(10),
    group_name char not null, 
    foreIgn key (user_name)
    references USER(user_name)
    on update restrict
    on delete restrict
    ,primary key(user_name,group_name))""")
    c.execute("""
    CREATE TABLE IF NOT EXISTS MESSAGE (sender char
    ,resever char ,number integer not null ,status interger
    ,message char not null,time char,primary key(sender,resever,number) 
    ,foreIgn key (sender)
    references USER(user_name)
    on update restrict
    on delete restrict,
    foreIgn key (resever)
    references USER(user_name)
    on update restrict
    on delete restrict)""")

if __name__=='__main__':
    conn=create_connection(r"C:\Users\mostafa\Desktop\messenger\database\sqlite.db")
    creat_table(conn)