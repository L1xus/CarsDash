import psycopg2
import os
from dotenv import load_dotenv
from config import car_company_mapping, car_model_mapping
from utils import (
    create_backup,
    remove_null_car_companies,
    normalize_car_companies,
    normalize_car_models,
    remove_nonsense_prices
)

load_dotenv()

db_host = os.getenv("HOST")
db_password = os.getenv("PASSWORD")

def clean_database():
    print("Starting database cleanup...")
    
    try:
        conn = psycopg2.connect(
            dbname="carsdb",
            user="postgres",
            host=db_host,
            password=db_password,
            port="5432",
        )
        cursor = conn.cursor()

        # Cleaning
        create_backup(cursor)
        remove_null_car_companies(cursor)
        normalize_car_companies(cursor, car_company_mapping)
        normalize_car_models(cursor, car_model_mapping)
        remove_nonsense_prices(cursor)

        conn.commit()
        print("Database cleanup completed successfully!")

    except Exception as e:
        print(f"Error during database cleanup: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    clean_database()
