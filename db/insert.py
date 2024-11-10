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
            INSERT INTO cars (title, car_company, car_model, price, year, location, fuel, km, transmission, announcement_date, tax_power, doors, first_hand, nationality_year)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """)

        for car in cars:
            data = (
                car['title'],
                car['car_company'],
                car['car_model'],
                car['price'],
                car['year'],
                car['location'],
                car['fuel'],
                car['km'],
                car['transmission'],
                car['announcement_date'],
                car['tax_power'],
                car['doors'],
                car['first_hand'],
                car['nationality_year'],
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
