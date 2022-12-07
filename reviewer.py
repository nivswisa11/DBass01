import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()
# Create a connection
cnx = mysql.connector.connect(
    user='root',
    password=os.getenv('MYSQL_ROOT_PASSWORD'),
    host='127.0.0.1',
    database='sakila'
)
# Create a cursor
cursor = cnx.cursor()
# Create the table rating if not exists
cursor.execute("""
    CREATE TABLE if not exists rating (
      film_id smallint,
      review_id INT,
      rating DECIMAL(2,1)
      CHECK (REGEXP_LIKE(film_id,'^([0-9]+)$')),
      CHECK (REGEXP_LIKE(review_id,'^([0-9]+)$')),
      CHECK (REGEXP_LIKE(rating,'^([0-9]\(.[0-9])?)$')),
    );
""")
# Create the table reviewer if not exists
cursor.execute("""
    CREATE TABLE if not exists reviewer (
      review_id INT NOT NULL PRIMARY KEY,
      first_name VARCHAR(45),
      last_name VARCHAR(45),
      CHECK (REGEXP_LIKE(review_id,'^([0-9]+)$')),
      CHECK (REGEXP_LIKE(first_name,'^([A-Za-z]+( [A-Za-z]+)?)$')),
      CHECK (REGEXP_LIKE(last_name,'^([A-Za-z]+( [A-Za-z]+)?)$'))
    );
""")
while True:
    idInput = input("Insert your ID please:\n")
    tableOne = cursor.execute(("""SELECT *
                   FROM reviewer
                    WHERE review_id=%s
    """), (idInput,))
    cursor.fetchall()
    firstName = input("Insert your first name please:\n")
    lastName = input("Insert your last name please:\n")
    try:
        cursor.execute('INSERT INTO reviewer (review_id, first_name,last_name) VALUES (%s, %s,%s)',
                       (idInput, firstName, lastName))
        cnx.commit()
        break
    except:
        continue
if not tableOne:
    print("Hello " + firstName + ' ' + lastName)
else:
    print("Hello " + tableOne.firstName + ' ' + tableOne.lastName)
cursor.fetchall()
while True:
    filmName = input("Please enter a film name:")
    rating = input("Please enter a rating for the film:")
    tableTwo = cursor.execute(("""SELECT *
                                        FROM film 
                                        WHERE title=%s
            """), (filmName,))
    cursor.fetchall()
    filmID=cursor.execute(("""SELECT film.film_id
                                        FROM film 
                                        WHERE title=%s
            """), (filmName,))
    try:
        cursor.execute('INSERT INTO rating (film_id, review_id,rating) VALUES (%s, %s,%s)',
                       (,idInput, rating))
        cnx.commit()
        break
    except:
        continue
cursor.fetchall()

