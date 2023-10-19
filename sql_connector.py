import mysql.connector as sql
from mysql.connector import Error
import pandas as pd


CREATE_DATABASE = 'CREATE DATABASE order_log;'
TABLES = {}
def create_table():

    TABLES['Logs'] = (
        "CREATE TABLE `Logs`"
    )


def create_connection(host, user, password):
    try:        
        mydb = sql.connect(
            host = host,
            user = user,
            password = password
        )
        print("Connection succeesfull")
        return mydb
    except Error as er:
        print(f'Error: {er}')

connection = create_connection('localhost', 'root', 'rahul')

cursor = connection.cursor()

cursor.execute(CREATE_DATABASE)


print(cursor.fetchall())
# cursor.execute("CREATE DATABASE coffee")

# for i in cursor:
#     print(i)