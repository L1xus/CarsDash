from .transform import transform_announcement_date, transform_first_hand
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

load_dotenv()

db_host = os.getenv("HOST")
db_password = os.getenv("PASSWORD")


def insert_cars(cars):
    print("HOLA!")
    try:
        conn = psycopg2.connect(
            dbname="carsdb",
            user="postgres",
            host=db_host,
            password=db_password,
            port="5432",
        )
        cur = conn.cursor()

        insert_query = sql.SQL("""
            INSERT INTO cars (title, car_company, car_model, price, year, location, fuel, km, transmission, announcement_date, tax_power, doors, first_hand, nationality_year, announcement_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """)

        for car in cars:
            announcement_date = transform_announcement_date(car.get('announcement_date'))
            first_hand = transform_first_hand(car.get('first_hand'))

            data = (
                car.get('title'),
                car.get('car_company'),
                car.get('car_model'),
                car.get('price'),
                car.get('year'),
                car.get('location'),
                car.get('fuel'),
                car.get('km'),
                car.get('transmission'),
                announcement_date,
                car.get('tax_power'),
                car.get('doors'),
                first_hand,
                car.get('nationality_year'),
                car.get('announcement_url')
            )

            cur.execute(insert_query, data)
        conn.commit()
        print("Data inserted successfully!")

    except Exception as e:
        print(f"Error inserting data into PostgreSQL: {e}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
