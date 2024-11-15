from datetime import datetime

def transform_announcement_date(announcement_date):
    if announcement_date:
        try:
            return datetime.strptime(announcement_date, "%d-%m-%Y").strftime("%Y-%m-%d")
        except ValueError:
            print(f"Date format error for {announcement_date}")
    return None

def transform_first_hand(first_hand):
    if first_hand is not None:
        first_hand = first_hand.lower()
        if first_hand == 'oui':
            return True
        elif first_hand == 'non':
            return False
    return None
