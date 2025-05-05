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
def show_films(cursor, title):
    print("\n-- {} --".format(title))
    cursor.execute("SELECT film_name, film_director, genre_name, studio_name FROM film JOIN genre ON film.genre_id = genre.genre_id JOIN studio ON film.studio_id = studio.studio_id")
    films = cursor.fetchall()
    for film in films:
        print("Film: {}, Director: {}, Genre: {}, Studio: {}".format(film[0], film[1], film[2], film[3]))
try:
    """ try/catch block for handling potential MySQL database errors """
    db = mysql.connector.connect(**config)  # connect to the database

    # output the connection status
    print("\n  Database user {} connected to MySQL on host {} with database {}".format(
        config["user"], config["host"], config["database"]))
    cursor = db.cursor()
    show_films(cursor, "DISPLAYING FILMS")



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



