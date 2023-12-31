from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
import requests
category_cb = CallbackData('category', 'id', 'action')


def categories_markup():
    global category_cb

    markup = InlineKeyboardMarkup()
    cats = requests.get('https://chtb.onrender.com/bot/category/').json()
    for cat in cats:
        markup.add(InlineKeyboardButton(cat['title'],
                                        callback_data=category_cb.new(id=cat['id'],
                                                                      action='view')))

    return markup
