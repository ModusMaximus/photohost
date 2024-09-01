from os import getenv

from aiogram import Router, Bot, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from dotenv import find_dotenv, load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.kbds import reply as kb
from src.bot.message.builder import StartMessage
from src.database.query import (
    orm_get_user,
    orm_add_user, get_all_links
)

load_dotenv(find_dotenv())

registration = Router()
bot = Bot(getenv("TOKEN"))
admin = getenv("ADMIN_ID")


@registration.message(CommandStart())
async def start(message: Message, session: AsyncSession):
    result = await orm_get_user(session, message.chat.id)
    if result:
        await message.answer(StartMessage.old(result), parse_mode='html', reply_markup=kb.keyboard_start)
    else:
        await message.answer("Ваша заявка находится на проверке. Пожалуйста ожидайте.😊")
        await bot.send_message(chat_id=admin, text=f'Новый пользователь!\n'
                                                   f'ID:{message.from_user.id}\n'
                                                   f'username: @{message.from_user.username}\n',
                               reply_markup=kb.add_user)
    await get_all_links(session)


@registration.callback_query(F.data == 'add')
async def add_user(cb: CallbackQuery, session: AsyncSession):
    await cb.answer('')
    message = cb.message.text
    username_pos = message.find('username')
    user_id = message[message.find('ID') + 3:username_pos - 1]

    obj = {
        'id': user_id,
        'user_name': message[username_pos + 11:],
    }
    await orm_add_user(session, obj)
    result = await orm_get_user(session, user_id)
    await bot.send_message(chat_id=user_id, text=StartMessage.old(result), parse_mode='html',
                           reply_markup=kb.keyboard_start)
