from aiogram.types import Message
from loader import dp
from .menu import delivery_status
from filters import IsUser
import requests


@dp.message_handler(IsUser(), text=delivery_status)
async def process_delivery_status(message: Message):
    orders = requests.get(f'http://localhost:8000/bot/order/{message.from_user.id}/get_order/').json()

    if len(orders) == 0:
        await message.answer('У вас нет активных заказов.')
    else:
        await delivery_status_answer(message, orders)

async def delivery_status_answer(message, orders):
    res = ''

    for order in orders:
        res += f'Заказ <b>№{order["id"]}  {order["name"]}</b>'
        status = ' готовится'
        if order['is_finished']:
            status = ' доставка'


        res += status
        res += '\n\n'

    await message.answer(res)
