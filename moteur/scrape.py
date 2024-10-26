import requests
from bs4 import BeautifulSoup
import time
import random
import re

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

        for car_html in car_soup:
            selected_cars = get_car_detail(car_html)
            cars.append(selected_cars)
            if len(cars) >= car_num:
                break

        page_number += 1

        if page_number % 3 == 0:
            time.sleep(random.uniform(2, 10))

    return cars

def get_car_detail(car_html):
    car = {}
    try:
        car_title = car_html.h3.a.text.strip()
        title = clear_text(car_title)
        car_price = car_html.find(class_="price").text if car_html.find(class_="price") else None
        price = clear_text(car_price) if car_price else None
        metadata = car_html.find(lambda tag: tag.has_attr("class") and tag["class"] == ["meta"])
        meta = metadata.find_all("li")
        if len(meta) <= 4:
            car_year = meta[0].text if len(meta) > 0 else None
            car_location = meta[1].text if len(meta) > 1 else None
            car_feul = meta[2].text if len(meta) > 2 else None
            car_meta_url = meta[3].a["href"] if len(meta) > 3 else None
        elif len(meta) > 4: 
            car_year = meta[1].text if len(meta) > 1 else None
            car_location = meta[2].text if len(meta) > 2 else None
            car_feul = meta[3].text if len(meta) > 3 else None
            car_meta_url = meta[4].a["href"] if len(meta) > 4 else None

        year = clear_text(car_year)
        location = clear_text(car_location)
        feul = clear_text(car_feul)
        car_meta = get_car_metadata(car_meta_url)

        car = {
            'title': title,
            'car_company': car_meta.get("car_company"),
            'car_model': car_meta.get("car_model"),
            'price': price,
            'year': year,
            'location': location,
            'feul': feul,
            'km': car_meta.get("Kilométrage"),
            'transmission': car_meta.get("Boite de vitesses"),
            'announcement_date': car_meta.get("Date"),
            'tax_power': car_meta.get("Puissance fiscale"),
            'doors': car_meta.get("Nombre de portes"),
            'first_hand': car_meta.get("Première main"),
            'nationality_year': car_meta.get("Véhicule dédouané")
        }

    except Exception as e:
        print(f"Error getting car details: {e}")

    return car

def get_car_metadata(car_url):
    car_metadata = {}
    required_fields = ["Kilométrage", "Boite de vitesses", "Date", "Puissance fiscale", "Nombre de portes", "Première main", "Véhicule dédouané"]

    response = requests.get(car_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    breadcrumb = soup.find(class_="breadcrumb")
    breadcrumb_items = breadcrumb.find_all("li")
    car_company = clear_text(breadcrumb_items[2].text)
    car_model = clear_text(breadcrumb_items[3].text)
    car_metadata["car_company"] = car_company
    car_metadata["car_model"] = car_model

    car_soup = soup.find(class_="car-detail")
    car_details = car_soup.find_all("div", class_="detail_line")

    for detail in car_details:
        spans = detail.find_all('span')
        trait = spans[0].text
        trait_value = clear_text(spans[1].text)

        if trait in required_fields:
            car_metadata[trait] = trait_value

    return car_metadata



def clear_text(text):
    return re.sub(r"\s+", " ", text).strip()
