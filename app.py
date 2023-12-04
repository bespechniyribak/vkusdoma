import os
import sys
import fcntl
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import ReplyKeyboardRemove
from aiogram import executor
from logging import basicConfig, INFO
from aiogram.types import BotCommand
from data.config import ADMINS,DEFAULT_ADMINS
from handlers.user.catalog import process_catalog
from loader import db, bot
import handlers, requests
from handlers import dp
from handlers.user.menu import catalog, cart, delivery_status

LOCK_PATH = "/tmp/bot.lock"
DEFAULT_ADMINS = []  # Замените это на реальный список админов

bot = Bot(token='YOUR_BOT_TOKEN')
dp = Dispatcher(bot)


def acquire_lock():
    try:
        lock_fd = open(LOCK_PATH, 'w')
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return lock_fd
    except (OSError, IOError):
        print("Another instance of the bot is already running. Exiting.")
        sys.exit(1)


def release_lock(lock_fd):
    fcntl.flock(lock_fd, fcntl.LOCK_UN)
    lock_fd.close()


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    print(message.chat.id)

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    if message.chat.id in DEFAULT_ADMINS:
        markup.row('Пользователь', 'Админ')
    else:
        markup.row('Начать покупки')

    await message.answer('''Привет, Hola, Привіт  👋
🤖 Я ваш помощник по заказу всего вкусного и домашнего в магазине VkusDoma

🛍️ Чтобы перейти в каталог продуктов и выбрать их, воспользуйтесь командой /menu.
или нажмите внизу кнопку "Начать покупки".

Синяя кнопка слева всегда поможет вам, если вдруг что-то пошло не так,
например, найти корзину с покупками (на айфонах она иногда сворачивается внизу
и выглядит как 4 кружка в нижнем меню, что не всегда очевидно для пользователя)

❓ По любым вопросам пишите нам, для этого
жмите /sos и спрашивайте о чем угодно.

Добро пожаловать во вкусный мир!''', reply_markup=markup)


@dp.message_handler(text=admin_message)
async def admin_mode(message: types.Message):
    status = True
    res = requests.post('https://chtb.onrender.com/bot/admins/', data={'user_id': message.from_user.id, 'status': status})
    await message.answer('Включен админский режим.',
                         reply_markup=ReplyKeyboardRemove())

@dp.message_handler(text=user_message)
async def user_mode(message: types.Message):
    status = False
    res = requests.post('https://chtb.onrender.com/bot/admins/', data={'user_id': message.from_user.id, 'status': status})
    await message.answer('Включен пользовательский режим.',
                         reply_markup=ReplyKeyboardRemove())

@dp.message_handler(text=menu)
async def menu_handler(message: types.Message):
    markup = ReplyKeyboardMarkup(selective=True)
    markup.add(catalog)
    markup.add(cart)

    await process_catalog(message)
    await message.answer('Меню каталог', reply_markup=markup)


    # await bot.set_chat_menu_buttons(message.chat.id)


async def set_bot_commands():
    commands = [
        BotCommand(command="/menu", description="Все продукты"),
        BotCommand(command="/cart", description="Ваша корзина"),
        BotCommand(command="/sos", description="Отправить вопрос"),
        BotCommand(command="/start", description="Начать сначала")
        # Add more commands as needed
    ]

    await bot.set_my_commands(commands)


async def on_startup(dp):
    basicConfig(level=INFO)
    await set_bot_commands()

pass
    finally:
        release_lock(lock_fd)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
