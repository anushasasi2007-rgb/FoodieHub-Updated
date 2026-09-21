from database import connect_database


def get_all_restaurants():
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, location, cuisine, price, rating
        FROM restaurants
    """)

    restaurants = cursor.fetchall()

    connection.close()

    return restaurants


def search_restaurants(keyword):
    connection = connect_database()
    cursor = connection.cursor()

    keyword = f"%{keyword}%"

    cursor.execute("""
        SELECT id, name, location, cuisine, price, rating
        FROM restaurants
        WHERE name LIKE ?
           OR location LIKE ?
           OR cuisine LIKE ?
    """, (keyword, keyword, keyword))

    restaurants = cursor.fetchall()

    connection.close()

    return restaurants