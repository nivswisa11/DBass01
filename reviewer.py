import os
import mysql.connector
from dotenv import load_dotenv

# Create a connection
cnx = mysql.connector.connect(
    user='root',
    password=os.getenv('MYSQL_ROOT_PASSWORD'),
    host='127.0.0.1',
    database='sakila'
)
https://code-with-me.global.jetbrains.com/UEJHmnQttb8eq08jXY3pXQ#p=PY&fp=4BB3C2C6934F8B3136052C160878CCE95412A84231198CEFABD5C3AF8024F97F
# Create a cursor
cursor = cnx.cursor()
