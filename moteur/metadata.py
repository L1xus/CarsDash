import requests
from .config import headers
from .utils import clear_text
from bs4 import BeautifulSoup

def get_car_metadata(car_url):
    car_metadata = {}
    required_fields = ["Kilométrage", "Boite de vitesses", "Date", "Puissance fiscale", "Nombre de portes", "Première main", "Véhicule dédouané"]
    fr_to_en = {
        "Oui": "Yes",
        "Non": "No",
        "Automatique": "Automatic",
        "Manuelle": "Manual",
        "Electrique": "Electric"
    }

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
            if trait_value in fr_to_en:
                trait_value = fr_to_en[trait_value]
            car_metadata[trait] = trait_value

    return car_metadata
