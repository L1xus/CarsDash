from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from bs4 import BeautifulSoup

from datetime import datetime

start_time = datetime.now()

from moteur.scrape import scrape_moteur
from avito.scrape import scrape_avito


def get_cars_html(num):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    driver.maximize_window()  # try deleting this!
    wait = WebDriverWait(driver, 10)
    cars = []

    try:
        url = "https://www.moteur.ma/fr/voiture/achat-voiture-occasion/"
        # url_expand =
        driver.get(url)

        iteration = 0
        last_car_index = 0

        while len(cars) < num:
            cars_html = wait.until(
                EC.visibility_of_all_elements_located(
                    (By.XPATH, "//div[contains(@class, 'content-inner')]")
                )
            )

            for i in range(last_car_index, len(cars_html)):
                element = cars_html[i]
                cars.append(element)

                if len(cars) >= num:
                    break

            # Load next page
            # last_car_index = len(movies)
            # if last_car_index < num:
            #     try:
    finally:
        driver.quit()

    return cars


tojot = scrape_moteur(5)
print(tojot)
print(len(tojot))
ikhan = scrape_avito(5)
print(ikhan)
print(len(ikhan))

end_time = datetime.now()
print("Duration: {}".format(end_time - start_time))

# def get_cars(car_html):
#     return print("Helllo")
#
