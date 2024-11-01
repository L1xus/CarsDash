import time
import random
import requests
from bs4 import BeautifulSoup
from .car_details import get_car_detail
from .config import base_url, headers

def scrape_moteur(car_num):
    page_number = 1
    cars = []

    while len(cars) < car_num:
        start_index = (page_number - 1) * 30

        url = f"{base_url}{start_index}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        car_soup = soup.find_all("div", class_="content-inner")

        for car_html in car_soup:
            selected_cars = get_car_detail(car_html)
            cars.append(selected_cars)
            if len(cars) >= car_num:
                break

        page_number += 1

        if page_number % 3 == 0:
            time.sleep(random.uniform(2, 10))

    return cars
