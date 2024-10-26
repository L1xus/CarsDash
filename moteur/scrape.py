import requests
from bs4 import BeautifulSoup
import time

base_url = "https://www.moteur.ma/fr/voiture/achat-voiture-occasion/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36"
}


def scrape_moteur(car_num):
    page_number = 1
    cars = []

    while len(cars) < car_num:
        start_index = (page_number - 1) * 30

        url = f"{base_url}{start_index}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        car_soup = soup.find_all("div", class_="content-inner")

        for i in range(len(car_soup)):
            selected_cars = car_soup[i].h3.a.text.strip()
            selected_cars_title = (
                selected_cars.replace("\xa0", " ")
                .replace("\t", "")
                .replace("\n", "")
                .replace("\r", "")
            )
            cars.append(selected_cars_title)

            if len(cars) >= car_num:
                break

        page_number += 1

        if page_number % 3 == 0:
            time.sleep(5)

    return cars
