import psycopg2
from datetime import datetime
from psycopg2 import sql
from dotenv import load_dotenv
import os

load_dotenv()

db_host = os.getenv("HOST")
db_password = os.getenv("PASSWORD")

def create_backup(cursor):
    # Create a backup of the cars table
    backup_table = f"cars_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    cursor.execute(sql.SQL("CREATE TABLE {} AS TABLE cars;").format(sql.Identifier(backup_table)))
    print(f"Backup created: {backup_table}")

def remove_null_car_companies(cursor):
    # Remove null car companies
    cursor.execute("DELETE FROM cars WHERE car_company IS NULL;")
    print("NULL car companies removed")

def normalize_car_companies(cursor, car_company_mapping):
    # Normalize car company names
    for old_name, new_name in car_company_mapping.items():
        cursor.execute(
            """
            UPDATE cars
            SET car_company = %s
            WHERE car_company = %s;
            """, (new_name, old_name)
        )
    print("Normalized car company names")

def normalize_car_models(cursor, car_model_mapping):
    # Normalize car models
    for company, models in car_model_mapping.items():
        for old_model, new_model in models.items():
            cursor.execute(
                """
                UPDATE cars
                SET car_model = %s
                WHERE car_model = %s AND car_company = %s;
                """, (new_model, old_model, company)
            )
    print("Car model normalization completed!")

def remove_nonsense_prices(cursor):
    # Remove none sense prices
    cursor.execute(
        """
        DELETE FROM cars
        WHERE 
            (price > 4000000 OR price < 7500)
            OR (price < 20000 AND year > 2008)
            OR (car_company IN ('Renault', 'Peugeot', 'Dacia', 'Citroen', 'Mitsubishi') AND price > 400000)
            OR (car_company = 'Volkswagen' AND (price > 760000 OR price < 13000))
            OR (car_company = 'Kia' AND (price > 550000 OR price < 20000))
            OR (car_company = 'Hyundai' AND price > 444444)
            OR (car_company = 'Toyota' AND price > 450000)
            OR (car_company = 'Fiat' AND price > 260000)
            OR (car_company = 'Dacia' AND price < 15000)
            OR (car_company IN ('Hyundai', 'Mitsubishi', 'Toyota', 'Citroen') AND price < 10000)
            OR (car_company = 'Peugeot' AND price < 12000);
        """
    )
    print("None sense cars removed!")

def get_last_announcement_date():
    try:
        conn = psycopg2.connect(
            dbname="carsdb",
            user="postgres",
            host=db_host,
            password=db_password,
            port="5432",
        )
        cursor = conn.cursor()

        cursor.execute("SELECT MAX(announcement_date) FROM cars;")

        last_date = cursor.fetchone()[0]

        return last_date

    except Exception as e:
        print(f"Error fetching last announcement date: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
