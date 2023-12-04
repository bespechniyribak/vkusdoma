import requests
BOT_TOKEN = '6810545901:AAG_Iag3bkashNKENTABDNQDBC2YPcjaDQY'


# например, ADMINS = [000000000, 1234567890]
def get_admins():
    response = requests.get('https://chtb.onrender.com/bot/admins/get_admin/')
    if response.status_code == 200:
        try:
            data = response.json()
            return tuple(i['user_id'] for i in data)
        except json.JSONDecodeError as e:
            print(f"Ошибка декодирования JSON: {e}")
            # Обработка ошибки декодирования
    else:
        print(f"Ошибка запроса. Код статуса: {response.status_code}")
        # Обработка ошибки HTTP
    return ()  # Возвращаем пустой кортеж в случае ошибки

ADMINS = get_admins()

def get_default_admins():
    response = requests.get('https://chtb.onrender.com/bot/admins/')
    if response.status_code == 200:
        try:
            data = response.json()
            return tuple(i['user_id'] for i in data)
        except json.JSONDecodeError as e:
            print(f"Ошибка декодирования JSON: {e}")
            # Обработка ошибки декодирования
    else:
        print(f"Ошибка запроса. Код статуса: {response.status_code}")
        # Обработка ошибки HTTP
    return ()  # Возвращаем пустой кортеж в случае ошибки

DEFAULT_ADMINS = get_default_admins()
