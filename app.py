import streamlit as st
import sqlite3
import hashlib

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="FoodieHub",
    page_icon="🍴",
    layout="wide"
)

# =========================
# DATABASE
# =========================
DB_NAME = "foodiehub.db"


def get_db():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_db()
    cursor = conn.cursor()

    # USER MODEL
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # RESTAURANT MODEL
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

    # REVIEW MODEL
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            restaurant_id INTEGER NOT NULL,
            rating INTEGER NOT NULL,
            review TEXT NOT NULL
        )
    """)

    # Sample restaurants
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

    conn.commit()
    conn.close()


create_tables()


# =========================
# PASSWORD HASHING
# =========================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# =========================
# CUSTOM DESIGN
# =========================
st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: Arial, sans-serif;
}

.stApp {
    background-color: #f5f7fb;
}

/* Main headings */
h1, h2, h3 {
    color: #172033 !important;
}

/* Normal text */
p, label, span {
    color: #263238;
}

/* Login card */
.login-card {
    background: white;
    padding: 35px;
    border-radius: 18px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.10);
    margin-top: 30px;
}

/* Logo */
.logo {
    font-size: 42px;
    font-weight: bold;
    color: #ff5722;
    text-align: center;
}

.subtitle {
    text-align: center;
    color: #555555;
    font-size: 18px;
    margin-bottom: 25px;
}

/* Restaurant card */
.restaurant-card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    margin-bottom: 15px;
    border: 1px solid #e1e5eb;
    box-shadow: 0 3px 12px rgba(0,0,0,0.07);
}

.restaurant-name {
    color: #172033;
    font-size: 23px;
    font-weight: bold;
}

.restaurant-info {
    color: #555555;
    font-size: 16px;
}

/* Buttons */
.stButton > button {
    background-color: #ff5722 !important;
    color: white !important;
    border-radius: 10px !important;
    border: none !important;
    font-weight: bold !important;
    padding: 10px 20px !important;
}

/* Input boxes */
input {
    color: #172033 !important;
    background-color: white !important;
}

textarea {
    color: #172033 !important;
    background-color: white !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #172033;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)


# =========================
# SESSION
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""


# =========================
# LOGIN / REGISTER
# =========================
if not st.session_state.logged_in:

    st.markdown("<div class='login-card'>", unsafe_allow_html=True)

    st.markdown(
        "<div class='logo'>🍴 FoodieHub</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='subtitle'>Restaurant Discovery & Review Platform</div>",
        unsafe_allow_html=True
    )

    tab1, tab2 = st.tabs(["🔐 Login", "📝 Create Account"])

    # -------------------------
    # LOGIN
    # -------------------------
    with tab1:

        username = st.text_input(
            "Username",
            placeholder="Enter your username",
            key="login_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )

        if st.button("🔐 Login", use_container_width=True):

            conn = get_db()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM users WHERE username=? AND password=?",
                (username, hash_password(password))
            )

            user = cursor.fetchone()
            conn.close()

            if user:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password.")

    # -------------------------
    # REGISTER
    # -------------------------
    with tab2:

        new_username = st.text_input(
            "Create Username",
            placeholder="Choose a username",
            key="register_username"
        )

        new_password = st.text_input(
            "Create Password",
            type="password",
            placeholder="Choose a password",
            key="register_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter your password",
            key="confirm_password"
        )

        if st.button("📝 Create Account", use_container_width=True):

            if not new_username or not new_password:
                st.warning("Please fill all fields.")

            elif new_password != confirm_password:
                st.error("Passwords do not match.")

            else:

                try:
                    conn = get_db()
                    cursor = conn.cursor()

                    cursor.execute(
                        "INSERT INTO users (username, password) VALUES (?, ?)",
                        (new_username, hash_password(new_password))
                    )

                    conn.commit()
                    conn.close()

                    st.success(
                        "Account created successfully! Now login."
                    )

                except sqlite3.IntegrityError:
                    st.error("Username already exists. Choose another.")

    st.markdown("</div>", unsafe_allow_html=True)

    st.stop()


# =========================
# SIDEBAR
# =========================
with st.sidebar:

    st.markdown("## 🍴 FoodieHub")

    st.write(f"👤 Welcome, **{st.session_state.username}**")

    menu = st.radio(
        "Navigation",
        [
            "🏠 Home",
            "🍽️ Restaurants",
            "🔍 Search",
            "⭐ Reviews",
            "👤 Profile"
        ]
    )

    st.divider()

    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()


# =========================
# HOME
# =========================
if menu == "🏠 Home":

    st.title("🍴 Welcome to FoodieHub!")

    st.subheader(
        "Discover great restaurants and share your food experience."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🍽️ Restaurants", "5+")

    with col2:
        st.metric("⭐ Reviews", "Community")

    with col3:
        st.metric("👥 Users", "Multi-User")

    st.markdown("---")

    st.subheader("🔥 Popular Restaurants")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM restaurants ORDER BY rating DESC")
    restaurants = cursor.fetchall()

    conn.close()

    for r in restaurants[:3]:

        st.markdown(f"""
        <div class="restaurant-card">
            <div class="restaurant-name">🍽️ {r[1]}</div>
            <div class="restaurant-info">
                📍 {r[2]} &nbsp; | &nbsp;
                🍴 {r[3]} &nbsp; | &nbsp;
                💰 {r[4]} &nbsp; | &nbsp;
                ⭐ {r[5]}
            </div>
        </div>
        """, unsafe_allow_html=True)


# =========================
# RESTAURANTS
# =========================
elif menu == "🍽️ Restaurants":

    st.title("🍽️ All Restaurants")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM restaurants")
    restaurants = cursor.fetchall()

    conn.close()

    for r in restaurants:

        st.markdown(f"""
        <div class="restaurant-card">
            <div class="restaurant-name">🍴 {r[1]}</div>
            <div class="restaurant-info">
                📍 Location: {r[2]}<br>
                🍽️ Cuisine: {r[3]}<br>
                💰 Price: {r[4]}<br>
                ⭐ Rating: {r[5]}
            </div>
        </div>
        """, unsafe_allow_html=True)


# =========================
# SEARCH
# =========================
elif menu == "🔍 Search":

    st.title("🔍 Search Restaurants")

    search = st.text_input(
        "Search by restaurant, location or cuisine",
        placeholder="Example: Chennai, Cafe, South Indian..."
    )

    if search:

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM restaurants
            WHERE name LIKE ?
            OR location LIKE ?
            OR cuisine LIKE ?
        """, (
            "%" + search + "%",
            "%" + search + "%",
            "%" + search + "%"
        ))

        results = cursor.fetchall()
        conn.close()

        if results:

            for r in results:

                st.markdown(f"""
                <div class="restaurant-card">
                    <div class="restaurant-name">🍴 {r[1]}</div>
                    <div class="restaurant-info">
                        📍 {r[2]} |
                        🍽️ {r[3]} |
                        💰 {r[4]} |
                        ⭐ {r[5]}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        else:
            st.warning("No restaurants found.")


# =========================
# REVIEWS
# =========================
elif menu == "⭐ Reviews":

    st.title("⭐ Write a Review")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM restaurants")
    restaurants = cursor.fetchall()

    conn.close()

    restaurant_names = [r[1] for r in restaurants]

    selected = st.selectbox(
        "Choose Restaurant",
        restaurant_names
    )

    rating = st.slider(
        "Your Rating",
        1,
        5,
        5
    )

    review_text = st.text_area(
        "Your Review",
        placeholder="Share your experience..."
    )

    if st.button("⭐ Submit Review"):

        if not review_text:
            st.warning("Please write a review.")

        else:

            restaurant_id = next(
                r[0] for r in restaurants
                if r[1] == selected
            )

            conn = get_db()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id FROM users WHERE username=?",
                (st.session_state.username,)
            )

            user_id = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO reviews
                (user_id, restaurant_id, rating, review)
                VALUES (?, ?, ?, ?)
            """, (
                user_id,
                restaurant_id,
                rating,
                review_text
            ))

            conn.commit()
            conn.close()

            st.success("Your review has been submitted! ⭐")


# =========================
# PROFILE
# =========================
elif menu == "👤 Profile":

    st.title("👤 My Profile")

    st.success(
        f"You are logged in as **{st.session_state.username}**"
    )

    st.info(
        "Your account is separate from other users."
    )

    st.markdown("""
    ### Account Features

    ✅ Personal username  
    ✅ Secure password storage  
    ✅ Personal login session  
    ✅ Submit restaurant reviews  
    ✅ Multi-user support  
    """)