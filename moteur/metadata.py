import requests
from .config import headers
from .utils import clear_text
from bs4 import BeautifulSoup

def get_car_metadata(car_url):
    car_metadata = {}
    required_fields = ["Kilométrage", "Boite de vitesses", "Date", "Puissance fiscale", "Nombre de portes", "Première main", "Véhicule dédouané"]
    en_transmission = {
        "Automatique": "Automatic",
        "Manuelle": "Manual",
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
            car_metadata[trait] = trait_value

    if "Boite de vitesses" in car_metadata:
        if car_metadata["Boite de vitesses"] in en_transmission:
            car_metadata["Boite de vitesses"] = en_transmission.get(car_metadata.get("Boite de vitesses"))
        else:
            car_metadata["Boite de vitesses"] = None

    if "Kilométrage" in car_metadata:
        car_metadata["Kilométrage"] = int(car_metadata["Kilométrage"].replace(" ", ""))

    if "Véhicule dédouané" in car_metadata:
        car_metadata["Véhicule dédouané"] = int(car_metadata["Véhicule dédouané"])

    if "Nombre de portes" in car_metadata:
        car_metadata["Nombre de portes"] = int(car_metadata["Nombre de portes"])

    return car_metadata
