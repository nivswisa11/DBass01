import os
import mysql.connector

# Create a connection
cnx = mysql.connector.connect(
    user='root',
    password=os.getenv('MYSQL_ROOT_PASSWORD'),
    host='127.0.0.1',
    database='sakila'
)

# Create a cursor
cursor = cnx.cursor()
