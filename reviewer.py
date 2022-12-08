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

# This is a while loop that will keep asking the user to input their ID until they input a valid ID.
while True:
    idInput = input("Insert your ID please:\n")
    # This is checking if the user enters a valid ID number.
    try:
        cursor.execute("""SELECT *
                   FROM reviewer
                    WHERE reviewer_id=%s
    """, (int(idInput),))
    except:
        continue
    # Fetching all the rows from the table `reviewer` and storing them in the variable `tableOne`.
    tableOne = cursor.fetchall()
    # This is checking if the user has already been in the database. If they have, it will print out their name.
    if len(tableOne) == 1:
        print("Hello, " + tableOne[0][1] + ' ' + tableOne[0][2])
        break
    firstName = input("Insert your first name please: \n")
    lastName = input("Insert your last name please: \n")
    try:
        # This is inserting the user's ID, first name, and last name into the table `reviewer`.
        cursor.execute('INSERT INTO reviewer (reviewer_id, first_name,last_name) VALUES (%s, %s,%s)',
                       (idInput, firstName, lastName))
        cnx.commit()
        break
    except:
        continue

# This is checking if the user has already been in the database. If they have, it will print out their name.
if not tableOne:
    print("Hello, " + firstName + ' ' + lastName)
cursor.fetchall()
flag = True
while flag:
    # This is asking the user to input a film name and then it is searching the database for the film name.
    filmName = input("Please enter a film name: \n")
    cursor.execute(("""SELECT film_id, title, release_year
                       FROM film 
                       WHERE title=%s
    """), (filmName,))
    # Fetching all the rows from the table `film` and storing them in the variable `tableTwo`.
    tableTwo = cursor.fetchall()
    # This is checking if the user has input a valid film name. If they have not, it will ask them to input a film name
    # again.
    if not tableTwo:
        continue
    if len(tableTwo) == 1:
        while True:
            rating = input("Please enter a rating for the film: \n")
            # This is checking if the user has already rated the film. If they have, it will update the rating.
            cursor.execute(("""SELECT rating.reviewer_id, rating.rating
                               FROM rating
                               WHERE reviewer_id=%s AND rating.film_id=%s
                """), (idInput, tableTwo[0][0]))
            # Fetching all the rows from the table `rating` and storing them in the variable `originalRating`.
            originalRating = cursor.fetchall()
            # This is checking if the user has already rated the film. If they have, it will update the rating.
            if len(originalRating) == 1:
                cursor.execute('UPDATE rating SET rating = %s WHERE reviewer_id = %s AND film_id = %s',
                               [rating, idInput, tableTwo[0][0]])
                cnx.commit()
                break
            else:
                # This is inserting the user's rating into the table `rating`.
                try:
                    cursor.execute('INSERT INTO rating (film_id,reviewer_id,rating) VALUES (%s,%s,%s)',
                                   (tableTwo[0][0], idInput, rating))
                    cnx.commit()
                    break
                except:
                    continue
        break
    if len(tableTwo) > 1:
        # This is printing out the film ID, film name, and release year of all the films that have the same name as the
        # film the user has input.
        for x in tableTwo:
            print('Film ID: ' + str(x[0]) + ' Film Name: ' + str(x[1]) + ' Release Year: ' + str(x[2]))
        choice = input("Insert the ID of the movie you would like to rate: \n")
        for x in tableTwo:
            try:
                if int(choice) == x[0]:
                    flag = False
                    while True:
                        try:
                            rating = input("Please enter a rating for the film: \n")
                            # This is checking if the user has already rated the film. If they have, it will update the
                            # rating.
                            cursor.execute(("""SELECT reviewer_id
                                               FROM rating
                                               WHERE reviewer_id=%s AND film_id=%s
                                            """), (idInput, choice))
                            originalRating = cursor.fetchall()
                            # This is checking if the user has already rated the film. If they have, it will update the
                            # rating.
                            if len(originalRating) == 1:
                                cursor.execute('UPDATE rating SET rating = %s WHERE reviewer_id = %s AND film_id = %s',
                                               [rating, idInput, choice])
                                cnx.commit()
                                break
                            # This is inserting the user's rating into the table `rating`.
                            else:
                                cursor.execute('INSERT INTO rating (film_id,reviewer_id,rating) VALUES (%s,%s,%s)',
                                               (choice, idInput, rating))
                                cnx.commit()
                                break
                        except:
                            continue
            except:
                break
# This is selecting all the ratings inserted so far by reviewers
cursor.execute(("""SELECT film.title, CONCAT(reviewer.first_name, ' ', reviewer.last_name), rating.rating
                   FROM reviewer, rating, film 
                   WHERE rating.film_id = film.film_id AND rating.reviewer_id = reviewer.reviewer_id
                   LIMIT 100
    """))
ratingTable = cursor.fetchall()
# This is printing out the film title, reviewer name, and rating of all the ratings inserted so far by reviewers.
for x in ratingTable:
    print('Film Title: ' + str(x[0]) + ' Reviewer Name: ' + str(x[1]) + ' Rating: ' + str(x[2]))
