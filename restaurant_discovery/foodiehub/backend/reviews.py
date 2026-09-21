from database import connect_database


def add_review(user_id, restaurant_id, rating, review):
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO reviews (user_id, restaurant_id, rating, review)
        VALUES (?, ?, ?, ?)
    """, (user_id, restaurant_id, rating, review))

    connection.commit()
    connection.close()

    return True


def get_restaurant_reviews(restaurant_id):
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT users.username, reviews.rating, reviews.review
        FROM reviews
        JOIN users ON reviews.user_id = users.id
        WHERE reviews.restaurant_id = ?
    """, (restaurant_id,))

    reviews = cursor.fetchall()

    connection.close()

    return reviews