from database import create_tables
from auth import register_user, login_user
from restaurants import get_all_restaurants, search_restaurants
from reviews import add_review, get_restaurant_reviews


def start_backend():
    create_tables()
    print("FoodieHub Backend Started")
    print("Database connected successfully")


if __name__ == "__main__":
    start_backend()