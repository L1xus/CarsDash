import requests
from .config import headers
from .utils import time_to_time, average_km
from bs4 import BeautifulSoup

def get_car_detail(car_url):
    car_metadata = {}
    required_fields = ["Kilométrage", "Marque", "Modèle", "Puissance fiscale", "Nombre de portes", "Première main"]
    en_fuel = {
        "Diesel": "Diesel",
        "Electrique": "Electric",
        "Essence": "Essence",
        "Hybride": "Hybrid",
        "LPG": "LPG"
    }
    en_tran = {
        "Automatique": "Automatic",
        "Manuelle": "Manual"
    }
    en_first = {
        "Oui": "Yes",
        "Non": "No"
    }
    try:
        response = requests.get(car_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find("h1", class_="sc-1g3sn3w-12 jUtCZM").text
        price = soup.find("div", class_="sc-1x0vz2r-0 lnEFFR sc-1g3sn3w-13 czygWQ").text if soup.find("div", class_="sc-1x0vz2r-0 lnEFFR sc-1g3sn3w-13 czygWQ") else None
        location = soup.find_all("span", class_="sc-1x0vz2r-0 iotEHk")[0].text
        date_time = soup.find("time").text

        meta_icon = soup.find_all("span", class_="sc-1x0vz2r-0 kQHNss")

        year = meta_icon[0].text.strip() if len(meta_icon) > 0 else None
        transmission = meta_icon[1].text.strip() if len(meta_icon) > 1 else None
        if transmission in en_tran:
            transmission = en_tran[transmission]
        else:
            transmission = None
        fuel = meta_icon[2].text.strip() if len(meta_icon) > 2 else None
        if fuel in en_fuel:
            fuel = en_fuel[fuel]
        else: 
            fuel = None

        meta_soup = soup.find_all("li", class_="sc-qmn92k-1 jJjeGO")
        for meta in meta_soup:
            spans = meta.find_all('span')
            trait = spans[0].text
            trait_value = spans[1].text

            if trait in required_fields:
                car_metadata[trait] = trait_value

        first_hand = car_metadata.get("Première main")
        if first_hand in en_first:
            first_hand = en_first[first_hand]

        return {
            "title": title,
            "car_company": car_metadata.get("Marque"),
            "car_model": car_metadata.get("Modèle"),
            "price": price,
            "year": year,
            "location": location,
            "fuel": fuel,
            "km": average_km(car_metadata.get("Kilométrage")),
            "transmission": transmission,
            "announcement_date": time_to_time(date_time),
            "tax_power": car_metadata.get("Puissance fiscale"),
            "doors": car_metadata.get("Nombre de portes"),
            "first_hand": first_hand
        }

    except Exception as e:
        print(f"Error extracting car details: {e}")
        return {}
