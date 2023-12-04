from aiogram.types import Message
from loader import dp
from handlers.user.menu import orders
from filters import IsAdmin
import requests


@dp.message_handler(IsAdmin(), text=orders)
async def process_orders(message: Message):
    orders = requests.get('http://localhost:8000/bot/order/').json()
    if len(orders) == 0:
        await message.answer('У вас нет заказов.')
    else:
        await order_answer(message, orders)


async def order_answer(message, orders):
    res = ''

    for order in orders:
        status = ' готовится'
        if order['is_finished']:
            status = ' доставка'

        res += f"Заказ <b>№{order['id']}</b>\nПользователь:{order['name']}\nUsername: @{order['username']}\nTG_id: {order['user_id']}\nАдрес: {order['adress']}\nСумма: {order['total_price']}\nСтатус: {status}\nCard count: {order['cart_count']}\nOrder Products: {order['cart_products']}\n\n"

    await message.answer(res, parse_mode='HTML')


