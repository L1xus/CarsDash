import time
import random
import requests
from bs4 import BeautifulSoup
from .car_details import get_car_detail
from .config import base_url, headers


def scrape_avito(car_num):
    page_number = 1
    cars = []

    while len(cars) < car_num:

        url = f"{base_url}{page_number}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        car_soup = soup.find_all("a", class_="sc-1jge648-0 eTbzNs")

        for car_html in car_soup:
            car_url = car_html["href"]
            car_detail = get_car_detail(car_url)
            cars.append(car_detail)
            if len(cars) >= car_num:
                break

        page_number += 1

        if page_number % 2 == 0:
            time.sleep(random.uniform(2, 10))

    return cars
