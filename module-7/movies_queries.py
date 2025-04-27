import mysql.connector  # to connect
from mysql.connector import errorcode
from dotenv import dotenv_values  # to use .env file

# using our .env file
secrets = dotenv_values(".env")

""" database config object """
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True  # not in .env file
}

db = None  # define db in the outer scope

try:
    """ try/catch block for handling potential MySQL database errors """
    db = mysql.connector.connect(**config)  # connect to the database

    # output the connection status
    print("\n  Database user {} connected to MySQL on host {} with database {}".format(
        config["user"], config["host"], config["database"]))
    cursor = db.cursor()

    # 1. Select all fields from the studio table
    print("\n-- DISPLAYING Studio RECORDS --")
    cursor.execute("SELECT * FROM studio;")
    studios = cursor.fetchall()
    for studio in studios:
        print("Studio ID: {}\nStudio Name: {}\n".format(studio[0], studio[1]))

    # 2. Select all fields from the genre table
    print("\n-- DISPLAYING Genre RECORDS --")
    cursor.execute("SELECT * FROM genre;")
    genres = cursor.fetchall()
    for genre in genres:
        print("Genre ID: {}\nGenre Name: {}\n".format(genre[0], genre[1]))

    # 3. Select movie names for movies with runtime less than two hours
    print("\n-- DISPLAYING Short Film RECORDS --")
    cursor.execute("SELECT film_name, film_runtime FROM film WHERE film_runtime < 120;")
    short_films = cursor.fetchall()
    for film in short_films:
        print("Film Name: {}\nRuntime: {} minutes\n".format(film[0], film[1]))

    # 4. Get list of film names and directors, grouped by director
    print("\n-- DISPLAYING Director RECORDS in Grouped Order --")
    cursor.execute("SELECT film_director, film_name FROM film ORDER BY film_director;")
    directors = cursor.fetchall()
    for director in directors:
        print("Director Name: {}\nFilm Name: {}\n".format(director[0], director[1]))

    input("\n\n  Press any key to continue...")

except mysql.connector.Error as err:
    """ on error code """
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")
    else:
        print(err)

finally:
    """ close the connection to MySQL """
    print("  MySQL connection is closed")
    if db:
        print("  Closing connection")
        db.close()
