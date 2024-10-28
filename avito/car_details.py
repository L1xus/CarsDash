import requests
from .config import headers
from .utils import time_to_time
from bs4 import BeautifulSoup

def get_car_detail(car_url):
    try:
        print(f"Here is your Car: {car_url}")
        response = requests.get(car_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find("h1", class_="sc-1g3sn3w-12 jUtCZM").text
        price = soup.find("div", class_="sc-1x0vz2r-0 lnEFFR sc-1g3sn3w-13 czygWQ").text if soup.find("div", class_="sc-1x0vz2r-0 lnEFFR sc-1g3sn3w-13 czygWQ") else None
        location = soup.find_all("span", class_="sc-1x0vz2r-0 iotEHk")[0].text
        date_time = soup.find("time").text

        return {
            "title": title,
            "price": price,
            "location": location,
            "announcement_date": time_to_time(date_time)
        }

    except Exception as e:
        print(f"Error extracting car details: {e}")
        return {}
