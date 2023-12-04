import requests
BOT_TOKEN = '6810545901:AAG_Iag3bkashNKENTABDNQDBC2YPcjaDQY'


# например, ADMINS = [000000000, 1234567890]
def get_admins():
    return tuple(i['user_id'] for i in requests.get('http://localhost:8000/bot/admins/get_admin/').json())


ADMINS = get_admins()

def get_default_admins():
    return tuple(i['user_id'] for i in requests.get('http://localhost:8000/bot/admins/').json())


DEFAULT_ADMINS = get_default_admins()