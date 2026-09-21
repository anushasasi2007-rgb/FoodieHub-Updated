import sqlite3
import hashlib

from database import connect_database


def register_user(username, password):
    connection = connect_database()
    cursor = connection.cursor()

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password)
        )

        connection.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        connection.close()


def login_user(username, password):
    connection = connect_database()
    cursor = connection.cursor()

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, hashed_password)
    )

    user = cursor.fetchone()

    connection.close()

    return user is not None