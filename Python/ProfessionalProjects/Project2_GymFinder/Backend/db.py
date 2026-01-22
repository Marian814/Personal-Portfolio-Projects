import mysql.connector

DB_CONFIG = {
    "user": "root",
    "password": "",
    "host": "localhost",
    "database": "gymfinderlocal"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)
