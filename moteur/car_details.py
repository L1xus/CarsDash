from .utils import clear_text
from .metadata import get_car_metadata

def get_car_detail(car_html):
    try:
        car_title = clear_text(car_html.h3.a.text)
        car_price = car_html.find(class_="price").text if car_html.find(class_="price") else None
        price = clear_text(car_price) if car_price else None

        metadata = car_html.find(lambda tag: tag.has_attr("class") and tag["class"] == ["meta"])
        metadata_items = metadata.find_all("li") if metadata else []

        if len(metadata_items) <= 4:
            car_year = metadata_items[0].text if len(metadata_items) > 0 else None
            car_location = metadata_items[1].text if len(metadata_items) > 1 else None
            car_feul = metadata_items[2].text if len(metadata_items) > 2 else None
            car_meta_url = metadata_items[3].a["href"] if len(metadata_items) > 3 else None
        else: 
            car_year = metadata_items[1].text if len(metadata_items) > 1 else None
            car_location = metadata_items[2].text if len(metadata_items) > 2 else None
            car_feul = metadata_items[3].text if len(metadata_items) > 3 else None
            car_meta_url = metadata_items[4].a["href"] if len(metadata_items) > 4 else None

        year = clear_text(car_year) if car_year else None
        location = clear_text(car_location) if car_location else None
        fuel = clear_text(car_feul) if car_feul else None

        car_meta = get_car_metadata(car_meta_url) if car_meta_url else {}

        return {
            "title": car_title,
            "car_company": car_meta.get("car_company"),
            "car_model": car_meta.get("car_model"),
            "price": price,
            "year": year,
            "location": location,
            "fuel": fuel,
            "km": car_meta.get("Kilométrage"),
            "transmission": car_meta.get("Boite de vitesses"),
            "announcement_date": car_meta.get("Date"),
            "tax_power": car_meta.get("Puissance fiscale"),
            "doors": car_meta.get("Nombre de portes"),
            "first_hand": car_meta.get("Première main"),
            "nationality_year": car_meta.get("Véhicule dédouané"),
        }

    except Exception as e:
        print(f"Error extracting car details: {e}")
        return {}
