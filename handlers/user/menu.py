from aiogram.types import Message, ReplyKeyboardMarkup
from loader import dp
from filters import IsAdmin, IsUser

catalog = '🛍️ Все продукты'
cart = '🛒 Корзина'
delivery_status = '🚚 Статус заказа'

continue_message = 'Продолжить покупки'
stop_message = 'Выйти'

settings = '⚙️ Настройка каталога'
orders = '🚚 Заказы'
questions = '❓ Вопросы'


@dp.message_handler(IsAdmin(), commands=['menu'])
async def admin_menu(message: Message):
    markup = ReplyKeyboardMarkup(selective=True)
    markup.add(settings)
    markup.add(questions, orders)

    await message.answer('Меню', reply_markup=markup)


@dp.message_handler(IsUser(), commands='menu')
async def user_menu(message: Message):
    markup = ReplyKeyboardMarkup(selective=True)
    markup.add(catalog)
    markup.add(cart)


    await message.answer('Меню', reply_markup=markup)


@dp.message_handler(IsUser(), commands='cart')
async def user_cart(message: Message):
    markup = ReplyKeyboardMarkup(selective=True)
    markup.add(cart)
    await message.answer('Нажмите внизу на корзину, чтобы посмотреть содержимое', reply_markup=markup)
