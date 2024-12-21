import time
import random
import requests
from bs4 import BeautifulSoup
from .car_details import get_car_detail
from .config import base_url, headers
from db.insert import insert_cars
from db.utils import get_last_announcement_date

BATCH_CARS = 150

def scrape_moteur(car_num):
    total_inserted = 0
    total_cars = 0
    page_number = 1
    cars = []
    stop_scraping = False

    last_announcement_date = get_last_announcement_date()
    print(last_announcement_date)

    while total_cars < car_num or not stop_scraping:
        start_index = (page_number - 1) * 30

        url = f"{base_url}{start_index}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        car_soup = soup.find_all("div", class_="content-inner")

        for car_html in car_soup:
            selected_cars = get_car_detail(car_html)

            car_date = selected_cars.get("announcement_date")
            print(car_date)
            # if car_date and car_date <= last_announcement_date:
            #     stop_scraping = True
            #     break

            cars.append(selected_cars)
            total_cars += 1

            if len(cars) >= BATCH_CARS:
                # insert_cars(cars)
                total_inserted += len(cars)
                cars = []

            if total_cars >= car_num:
                break

        page_number += 1

        if page_number % 3 == 0:
            time.sleep(random.uniform(5, 15))

    if cars:
        # insert_cars(cars)
        total_inserted += len(cars)

    return {
        "status": "Moteur Scraping Completed",
        "total_cars_inserted": total_inserted,
        "total_scraped_cars": total_cars
    }
