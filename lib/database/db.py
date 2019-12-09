import mysql.connector

from lib.config.config import config

db = mysql.connector.connect(
    host        = config.get_database_host(),
    user        = config.get_database_user(),
    password    = config.get_database_password(),
    database    = config.get_database_name()
)

cursor = db.cursor()

if __name__ == '__main__':
    print(db)
