from os import getenv

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.kbds import reply as kb
from src.bot.kbds.reply import gen_markup_users, delete_user
from src.database.query import (
    get_all_users,
    get_links, delete_usr
)
from src.bot.callback.CallbackUser import Callback_ImageStorage

load_dotenv()

admin = Router()
domen = getenv("DOMEN")
admin_ids = getenv('ADMIN_ID')


@admin.message(Command('admin'))
async def admin_start(msg: Message, session: AsyncSession):
    if str(msg.from_user.id) in admin_ids:
        await msg.answer('Выберете действие:', reply_markup=kb.images_admin)


@admin.callback_query(F.data == 'back_admin')
async def admin_start_from_back(cb: CallbackQuery, session: AsyncSession):
    await cb.answer('')
    if str(cb.message.chat.id) in admin_ids:
        await cb.message.answer('Выберете действие:', reply_markup=kb.images_admin)


@admin.callback_query(F.data == 'storage')
async def storage(cb: CallbackQuery, session: AsyncSession):
    await cb.answer('')
    users = await get_all_users(session)
    await cb.message.edit_text('Выберите пользователя для просмотра истории загруженных изображений',
                               reply_markup=gen_markup_users(users).as_markup())


@admin.callback_query(Callback_ImageStorage.filter(F.btn_name == "user_storage"))
async def get_links_users_photo(cb: CallbackQuery, callback_data: Callback_ImageStorage, session: AsyncSession):
    await cb.answer('')
    user_id = callback_data.user_id
    result = await get_links(session, user_id)
    for item in result:
        await cb.message.answer(
            text=
            f"Просмотр изображения пользователя доступен по ссылке: {domen}/{item}"
        )


@admin.callback_query(F.data == 'del_user')
async def delete_user_admin(cb: CallbackQuery, session: AsyncSession):
    await cb.answer('')
    users = await get_all_users(session)
    await cb.message.edit_text('Выберите пользователя для удаления',
                               reply_markup=delete_user(users).as_markup())


@admin.callback_query(Callback_ImageStorage.filter(F.btn_name == "delete_user"))
async def get_links_users_photo(cb: CallbackQuery, callback_data: Callback_ImageStorage, session: AsyncSession):
    await cb.answer('')
    user_id = callback_data.user_id
    result = await delete_usr(session, user_id)
    await cb.message.answer('Пользователь удален', reply_markup=kb.back_admin)
