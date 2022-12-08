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
# Create the table reviewer if not exists
cursor.execute("""
    CREATE TABLE if not exists reviewer (
      reviewer_id INT NOT NULL PRIMARY KEY,
      first_name VARCHAR(45),
      last_name VARCHAR(45),
      CHECK (REGEXP_LIKE(reviewer_id,'^([0-9]+)$')),
      CHECK (REGEXP_LIKE(first_name,'^([A-Za-z]+( [A-Za-z]+)?)$')),
      CHECK (REGEXP_LIKE(last_name,'^([A-Za-z]+( [A-Za-z]+)?)$'))
    );
""")
# Create the table rating if not exists
cursor.execute("""
    CREATE TABLE if not exists rating (
      film_id smallint unsigned,
      reviewer_id INT,
      rating DECIMAL(2,1),
      CHECK (rating >= 0 AND rating <= 9.9),
      PRIMARY KEY(film_id,reviewer_id),
      FOREIGN KEY (film_id) REFERENCES film(film_id) ON UPDATE CASCADE ON DELETE CASCADE,
      FOREIGN KEY (reviewer_id) REFERENCES reviewer(reviewer_id) ON UPDATE CASCADE ON DELETE CASCADE
    );
""")

while True:
    idInput = input("Insert your ID please:\n")
    cursor.execute(("""SELECT *
                   FROM reviewer
                    WHERE reviewer_id=%s
    """), (idInput,))
    tableOne=cursor.fetchall()
    firstName = input("Insert your first name please:\n")
    lastName = input("Insert your last name please:\n")
    try:
        cursor.execute('INSERT INTO reviewer (reviewer_id, first_name,last_name) VALUES (%s, %s,%s)',
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
    cursor.execute(("""SELECT title
                                        FROM film 
                                        WHERE title=%s
    """), (filmName,))
    tableTwo = cursor.fetchall()
    if not tableTwo:
        continue
    cursor.execute(("""SELECT film.film_id
                                FROM film 
                                WHERE title=%s
    """), (filmName,))
    filmId = cursor.fetchall()
    if len(tableTwo) == 1:
        rating = input("Please enter a rating for the film:")
        try:
            cursor.execute('INSERT INTO rating (film_id,reviewer_id,rating) VALUES (%s,%s,%s)',
                               (filmId[0][0], idInput, rating))
            cnx.commit()
            break
        except:
            continue

