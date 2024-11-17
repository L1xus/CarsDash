import psycopg2
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

db_host = os.getenv("HOST")
db_password = os.getenv("PASSWORD")


CAR_COMPANY_MAPPING = {
    'Land-rover': 'Land Rover',
    'Mercedes-Benz': 'Mercedes',
    'Bmw': 'BMW',
    'mini': 'Mini',
    'Alfa-romeo': 'Alfa Romeo',
    'Ds': 'DS',
    'Dfsk': 'DFSK',
    'Rolls-royce': 'Rolls-Royce',
    'lancia': 'Lancia',
    'Aston-martin': 'Aston Martin',
    'Gmc': 'GMC'
}

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
        cur = conn.cursor()

        # Create a backup
        backup_table = f"cars_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        cur.execute(f"""
            CREATE TABLE {backup_table} AS TABLE cars;
        """)
        print(f"Backup created: {backup_table}")

        # Remove null car companies
        cur.execute("""
            DELETE FROM cars
            WHERE car_company IS NULL;
        """)
        print("NULL car companies removed")

        # Normalize car company names
        for old_name, new_name in CAR_COMPANY_MAPPING.items():
            cur.execute("""
                UPDATE cars
                SET car_company = %s
                WHERE car_company = %s;
            """, (new_name, old_name))
        print("Normalized car company names")

        conn.commit()
        print("Data inserted successfully!")

    except Exception as e:
        print(f"Error inserting data into PostgreSQL: {e}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
