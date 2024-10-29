from datetime import datetime, timedelta
import re

current_time = datetime.now()

def time_to_time(car_time):
    if "minute" in car_time:
        minutes = int(re.search(r"\d+", car_time).group())
        date_time = current_time - timedelta(minutes=minutes)
    elif "heure" in car_time:
        hours = int(re.search(r"\d+", car_time).group())
        date_time = current_time - timedelta(hours=hours)
    elif "jour" in car_time:
        days = int(re.search(r"\d+", car_time).group())
        date_time = current_time - timedelta(days=days)
    elif "mois" in car_time:
        months = int(re.search(r"\d+", car_time).group())
        date_time = current_time - timedelta(days=30 * months)
    else:
        date_time = current_time

    return date_time.strftime("%d-%m-%Y")

def average_km(km_range):
    start, end = km_range.split(' - ')
    start = int(start.replace(' ', ''))
    end = int(end.replace(' ', ''))

    return (start + end) // 2
