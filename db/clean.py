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

        # Remove none sense prices
        cur.execute("""
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
        """)
        print("None sense cars removed!")

        conn.commit()
        print("Database cleanup completed successfully!")

    except Exception as e:
        print(f"Error during database cleanup: {e}")
    

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    clean_database()

