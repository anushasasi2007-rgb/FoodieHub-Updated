import streamlit as st
import sqlite3
import hashlib

DB_NAME = "foodiehub.db"


# ================= DATABASE =================

def get_connection():
    return sqlite3.connect(DB_NAME)


def setup_database():

    connection = get_connection()
    cursor = connection.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Restaurants table
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

    # Reviews table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            restaurant_id INTEGER,
            rating INTEGER,
            review TEXT
        )
    """)

    # Check old reviews table
    cursor.execute("PRAGMA table_info(reviews)")
    columns = [row[1] for row in cursor.fetchall()]

    # Add missing columns automatically
    if "user_id" not in columns:
        cursor.execute(
            "ALTER TABLE reviews ADD COLUMN user_id INTEGER"
        )

    if "restaurant_id" not in columns:
        cursor.execute(
            "ALTER TABLE reviews ADD COLUMN restaurant_id INTEGER"
        )

    if "rating" not in columns:
        cursor.execute(
            "ALTER TABLE reviews ADD COLUMN rating INTEGER"
        )

    if "review" not in columns:
        cursor.execute(
            "ALTER TABLE reviews ADD COLUMN review TEXT"
        )

    # Add sample restaurants
    cursor.execute("SELECT COUNT(*) FROM restaurants")
    count = cursor.fetchone()[0]

    if count == 0:

        restaurants = [
            ("Spice Garden", "Chennai", "South Indian", "₹₹", 4.5),
            ("Urban Bites", "Chennai", "Multi Cuisine", "₹₹₹", 4.2),
            ("Tandoori House", "Coimbatore", "North Indian", "₹₹", 4.4),
            ("Ocean Treat", "Chennai", "Seafood", "₹₹₹", 4.6),
            ("Cafe Aroma", "Madurai", "Cafe", "₹", 4.1)
        ]

        cursor.executemany("""
            INSERT INTO restaurants
            (name, location, cuisine, price, rating)
            VALUES (?, ?, ?, ?, ?)
        """, restaurants)

    connection.commit()
    connection.close()


# ================= PASSWORD =================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ================= REGISTER =================

def register_user(username, password):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO users (username, password)
            VALUES (?, ?)
        """, (username, hash_password(password)))

        connection.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        connection.close()


# ================= LOGIN =================

def login_user(username, password):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, username
        FROM users
        WHERE username = ? AND password = ?
    """, (username, hash_password(password)))

    user = cursor.fetchone()

    connection.close()

    return user


# ================= RESTAURANTS =================

def get_restaurants():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, location, cuisine, price, rating
        FROM restaurants
    """)

    data = cursor.fetchall()

    connection.close()

    return data


def search_restaurants(keyword):

    connection = get_connection()
    cursor = connection.cursor()

    keyword = "%" + keyword + "%"

    cursor.execute("""
        SELECT id, name, location, cuisine, price, rating
        FROM restaurants
        WHERE name LIKE ?
        OR location LIKE ?
        OR cuisine LIKE ?
    """, (keyword, keyword, keyword))

    data = cursor.fetchall()

    connection.close()

    return data


# ================= REVIEWS =================

def add_review(user_id, restaurant_id, rating, review):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO reviews
        (user_id, restaurant_id, rating, review)
        VALUES (?, ?, ?, ?)
    """, (user_id, restaurant_id, rating, review))

    connection.commit()
    connection.close()


def get_reviews(restaurant_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT users.username, reviews.rating, reviews.review
        FROM reviews
        LEFT JOIN users
        ON reviews.user_id = users.id
        WHERE reviews.restaurant_id = ?
        ORDER BY reviews.id DESC
    """, (restaurant_id,))

    data = cursor.fetchall()

    connection.close()

    return data


# ================= PROFILE =================

def get_user_reviews(username):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT restaurants.name, reviews.rating, reviews.review
        FROM reviews
        JOIN users
        ON reviews.user_id = users.id
        JOIN restaurants
        ON reviews.restaurant_id = restaurants.id
        WHERE users.username = ?
        ORDER BY reviews.id DESC
    """, (username,))

    data = cursor.fetchall()

    connection.close()

    return data


# ================= PAGE SETTINGS =================

st.set_page_config(
    page_title="FoodieHub",
    page_icon="🍴",
    layout="wide"
)


# ================= CSS =================

st.markdown("""
<style>

body {
    background-color: #f5f7fb;
}

.stApp {
    background-color: #f5f7fb;
}

h1, h2, h3 {
    color: #172033;
}

p, label {
    color: #263238;
}

.restaurant-card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
    border: 1px solid #eeeeee;
}

.review-card {
    background-color: white;
    padding: 15px;
    border-radius: 12px;
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)


# ================= START DATABASE =================

setup_database()


# ================= SESSION =================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "user_id" not in st.session_state:
    st.session_state.user_id = None


# =================================================
# LOGIN PAGE
# =================================================

if not st.session_state.logged_in:

    st.markdown(
        "<h1 style='text-align:center;'>🍴 FoodieHub</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;'>Restaurant Discovery & Review Platform</p>",
        unsafe_allow_html=True
    )

    login_tab, register_tab = st.tabs(
        ["🔐 Login", "📝 Create Account"]
    )


    # ================= LOGIN =================

    with login_tab:

        st.subheader("Login")

        username = st.text_input(
            "Username",
            key="login_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button("Login", use_container_width=True):

            if username == "" or password == "":
                st.error("Please enter username and password.")

            else:

                user = login_user(username, password)

                if user:

                    st.session_state.logged_in = True
                    st.session_state.username = user[1]
                    st.session_state.user_id = user[0]

                    st.success("Login successful!")

                    st.rerun()

                else:

                    st.error("Invalid username or password.")


    # ================= REGISTER =================

    with register_tab:

        st.subheader("Create Account")

        new_username = st.text_input(
            "Username",
            key="register_username"
        )

        new_password = st.text_input(
            "Password",
            type="password",
            key="register_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="confirm_password"
        )

        if st.button(
            "Create Account",
            use_container_width=True
        ):

            if new_username == "" or new_password == "":
                st.error("Please fill all fields.")

            elif new_password != confirm_password:
                st.error("Passwords do not match.")

            else:

                result = register_user(
                    new_username,
                    new_password
                )

                if result:

                    st.success(
                        "Account created successfully! Please login."
                    )

                else:

                    st.error(
                        "Username already exists."
                    )


# =================================================
# MAIN APPLICATION
# =================================================

else:

    # ================= SIDEBAR =================

    st.sidebar.title("🍴 FoodieHub")

    st.sidebar.write(
        "Welcome, " + st.session_state.username
    )

    page = st.sidebar.radio(
        "Menu",
        [
            "🏠 Home",
            "🍴 Restaurants",
            "🔎 Search",
            "⭐ Reviews",
            "👤 Profile"
        ]
    )

    st.sidebar.divider()

    if st.sidebar.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.user_id = None

        st.rerun()


    # =================================================
    # HOME
    # =================================================

    if page == "🏠 Home":

        st.title("🏠 Welcome to FoodieHub")

        st.write(
            "Discover restaurants, search for food, "
            "and share your reviews."
        )

        st.divider()

        restaurants = get_restaurants()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Restaurants",
                len(restaurants)
            )

        with col2:
            st.metric(
                "Cities",
                len(set(r[2] for r in restaurants))
            )

        with col3:
            st.metric(
                "Cuisines",
                len(set(r[3] for r in restaurants))
            )

        st.divider()

        st.subheader("⭐ Popular Restaurants")

        for restaurant in restaurants:

            st.markdown(
                f"""
                <div class="restaurant-card">
                    <h3>🍴 {restaurant[1]}</h3>
                    <p>📍 {restaurant[2]}</p>
                    <p>🍽️ {restaurant[3]}</p>
                    <p>💰 {restaurant[4]}</p>
                    <p>⭐ {restaurant[5]}</p>
                </div>
                """,
                unsafe_allow_html=True
            )


    # =================================================
    # RESTAURANTS
    # =================================================

    elif page == "🍴 Restaurants":

        st.title("🍴 Restaurants")

        restaurants = get_restaurants()

        for restaurant in restaurants:

            st.markdown(
                f"""
                <div class="restaurant-card">
                    <h3>🍴 {restaurant[1]}</h3>
                    <p>📍 Location: {restaurant[2]}</p>
                    <p>🍽️ Cuisine: {restaurant[3]}</p>
                    <p>💰 Price: {restaurant[4]}</p>
                    <p>⭐ Rating: {restaurant[5]}</p>
                </div>
                """,
                unsafe_allow_html=True
            )


    # =================================================
    # SEARCH
    # =================================================

    elif page == "🔎 Search":

        st.title("🔎 Search Restaurants")

        keyword = st.text_input(
            "Search by restaurant, location or cuisine",
            placeholder="Example: Chennai"
        )

        if keyword:

            results = search_restaurants(keyword)

            if results:

                st.success(
                    str(len(results)) + " restaurant(s) found."
                )

                for restaurant in results:

                    st.markdown(
                        f"""
                        <div class="restaurant-card">
                            <h3>🍴 {restaurant[1]}</h3>
                            <p>📍 {restaurant[2]}</p>
                            <p>🍽️ {restaurant[3]}</p>
                            <p>💰 {restaurant[4]}</p>
                            <p>⭐ {restaurant[5]}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            else:

                st.warning("No restaurants found.")


    # =================================================
    # REVIEWS
    # =================================================

    elif page == "⭐ Reviews":

        st.title("⭐ Restaurant Reviews")

        restaurants = get_restaurants()

        restaurant_names = [
            r[1] for r in restaurants
        ]

        selected_name = st.selectbox(
            "Select Restaurant",
            restaurant_names
        )

        selected_restaurant = None

        for restaurant in restaurants:

            if restaurant[1] == selected_name:
                selected_restaurant = restaurant
                break

        if selected_restaurant:

            restaurant_id = selected_restaurant[0]

            st.subheader(
                "Write a Review for " + selected_name
            )

            rating = st.selectbox(
                "Rating",
                [1, 2, 3, 4, 5]
            )

            review_text = st.text_area(
                "Your Review",
                placeholder="Write your experience..."
            )

            if st.button(
                "Submit Review",
                use_container_width=True
            ):

                if review_text.strip() == "":

                    st.error("Please write a review.")

                else:

                    add_review(
                        st.session_state.user_id,
                        restaurant_id,
                        rating,
                        review_text
                    )

                    st.success(
                        "Review submitted successfully!"
                    )

                    st.rerun()


            st.divider()

            st.subheader("Customer Reviews")

            reviews = get_reviews(restaurant_id)

            if reviews:

                for review in reviews:

                    username = review[0]
                    user_rating = review[1]
                    user_review = review[2]

                    st.markdown(
                        f"""
                        <div class="review-card">
                            <b>👤 {username}</b>
                            <p>⭐ {user_rating}/5</p>
                            <p>{user_review}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            else:

                st.info(
                    "No reviews yet. Be the first to review!"
                )


    # =================================================
    # PROFILE
    # =================================================

    elif page == "👤 Profile":

        st.title("👤 My Profile")

        st.subheader(
            "Welcome, " + st.session_state.username
        )

        st.write(
            "Username: " + st.session_state.username
        )

        st.divider()

        st.subheader("📝 My Reviews")

        my_reviews = get_user_reviews(
            st.session_state.username
        )

        if my_reviews:

            for review in my_reviews:

                restaurant_name = review[0]
                rating = review[1]
                review_text = review[2]

                st.markdown(
                    f"""
                    <div class="review-card">
                        <h4>🍴 {restaurant_name}</h4>
                        <p>⭐ {rating}/5</p>
                        <p>{review_text}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.info(
                "You have not written any reviews yet."
            )