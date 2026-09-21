import sqlite3

def connect_database():
    connection = sqlite3.connect("foodiehub.db")
    return connection


def create_tables():
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS restaurants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            cuisine TEXT NOT NULL,
            price TEXT NOT NULL,
            rating REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            restaurant_id INTEGER,
            rating INTEGER,
            review TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
        )
    """)

    connection.commit()
    connection.close()