from moteur.scrape import scrape_moteur
from avito.scrape import scrape_avito

from datetime import datetime

start_time = datetime.now()


moteur_cars = scrape_moteur(5)
print(moteur_cars)
avito_cars = scrape_avito(5)
print(avito_cars)

end_time = datetime.now()
print("Duration: {}".format(end_time - start_time))
