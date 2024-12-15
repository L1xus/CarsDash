import time
import random
import requests
from bs4 import BeautifulSoup
from .car_details import get_car_detail
from .config import base_url, headers
from db.insert import insert_cars
from db.utils import get_last_announcement_date

BATCH_CARS = 250

def scrape_avito(car_num):
    total_inserted = 0
    total_cars = 0
    page_number = 1
    cars = []
    stop_scraping = False

    last_announcement_date = get_last_announcement_date()

    while total_cars < car_num and not stop_scraping:
        url = f"{base_url}{page_number}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        car_soup = soup.find_all("a", class_="sc-1jge648-0 eTbzNs")

        for car_html in car_soup:
            car_url = car_html["href"]
            car_detail = get_car_detail(car_url)

            car_date = car_detail.get("announcement_date")
            if car_date and car_date <= last_announcement_date:
                stop_scraping = True
                break

            cars.append(car_detail)
            total_cars += 1

            if len(cars) >= BATCH_CARS:
                insert_cars(cars)
                total_inserted += len(cars)
                cars = []  

            if total_cars >= car_num:
                break

        page_number += 1

        if page_number % 2 == 0:
            time.sleep(random.uniform(5, 15))

    if cars:
        insert_cars(cars)
        total_inserted += len(cars)

    return {
        "status": "Avito Cars Scraping Completed",
        "total_cars_inserted": total_inserted,
        "total_scraped_cars": total_cars
    }
