import threading
import queue
from moteur.scrape import scrape_moteur
from avito.scrape import scrape_avito
from datetime import datetime

results_queue = queue.Queue()

def scrape_return(scrape_function, *args):
    result = scrape_function(*args)
    results_queue.put(result)

start_time = datetime.now()

moteur_thread = threading.Thread(target=scrape_return, args=(scrape_moteur, 5))
avito_thread = threading.Thread(target=scrape_return, args=(scrape_avito, 5))

moteur_thread.start()
avito_thread.start()

moteur_thread.join()
avito_thread.join()

moteur_cars = results_queue.get()
print("Moteur cars:", moteur_cars)

avito_cars = results_queue.get()
print("Avito cars:", avito_cars)

end_time = datetime.now()
print("Duration: {}".format(end_time - start_time))
