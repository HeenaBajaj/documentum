
import sqlite3
from sqlite3 import Error
import os


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
##########################    Create Database Connection and table  ##########################
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        print("Table created successfully")
    except Error as e:
        print(e)


sql ='''CREATE TABLE if not exists FileDetails(
 file_name varchar(200),
 original_file varchar(200),
 pdf_file varchar(200),
 tags varchar(200),
 created_date datetime,
 modified_date datetime,
 document_dates datetime,
 username varchar(200),
 usertags varchar(max)
)'''

droptable ='''drop  TABLE  FileDetails'''
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


global conn
db_conn = BASE_DIR + '\\' + r"pythonsqlite.db"
conn = create_connection(db_conn)
