from os import getenv

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from dotenv import find_dotenv, load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.FSM.user_fsm import Photo
from src.bot.kbds import reply as kb
from src.bot.message.builder import StartMessage
from src.database.query import (
    orm_get_user,
    orm_add_photo
)

load_dotenv(find_dotenv())

user_private_router = Router()
bot = Bot(getenv("TOKEN"))
domen = getenv("DOMEN")
List_photo = {}


@user_private_router.callback_query(F.data == "back")
async def back(callback: CallbackQuery, session: AsyncSession):
    await callback.answer("")
    result = await orm_get_user(session, callback.message.chat.id)
    await callback.message.answer(StartMessage.old(result), parse_mode='html', reply_markup=kb.keyboard_start)


@user_private_router.callback_query(F.data == "save_photo")
@user_private_router.callback_query(F.data == "save_new_photo")
async def read_count_photo(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.answer("Укажите количество добавляемых фото: ")
    await state.set_state(Photo.Count)


@user_private_router.message(Photo.Count, F.text)
async def get_photo(message: Message, session: AsyncSession, state: FSMContext):
    if int(message.text) > 10:
        await message.answer(
            text=f"⚠️Вы можете загрузить за раз не более 10 изображений.",
            reply_markup=kb.keyboard_start
        )
        await state.clear()
    else:
        await state.update_data(count=message.text)
        print(message.text)
        print(await state.get_data())
        await message.answer(
            text=f"Пришлите изображение(я) одним сообщением."
        )
        await state.set_state(Photo.photo_id)


@user_private_router.message(Photo.photo_id, F.photo)
async def get_photo(message: Message, session: AsyncSession, state: FSMContext):
    global List_photo
    data = await state.get_data()
    key = str(message.from_user.id)
    List_photo.setdefault(key, [])
    if message.content_type == 'photo':
        List_photo[key].append(message.photo[-1].file_id)
        if len(List_photo[key]) == int(data["count"]):
            await orm_add_photo(session, message.chat.id, List_photo[str(message.chat.id)])
            for item in List_photo[str(message.chat.id)]:
                file = await bot.get_file(item)
                file_path = file.file_path
                await bot.download_file(file_path, destination=f"static/image/{item}.jpg")
            await message.answer(
                text=
                "✅Изображение успешно сохранено!\n\n"
                f"Для доступа перейдите по ссылке {domen}/{List_photo[str(message.chat.id)][0]}",
                reply_markup=kb.keyboard_next)
            await state.clear()
            List_photo = {}


@user_private_router.message(Photo.photo_id, F.document)
async def get_photo(message: Message, session: AsyncSession, state: FSMContext):
    global List_photo
    data = await state.get_data()
    key = str(message.from_user.id)
    List_photo.setdefault(key, [])
    if message.content_type == 'document':
        List_photo[key].append(message.document.file_id)
    if len(List_photo[key]) == int(data["count"]):
        await orm_add_photo(session, message.chat.id, List_photo[str(message.chat.id)])
        for item in List_photo[str(message.chat.id)]:
            file = await bot.get_file(item)
            file_path = file.file_path
            await bot.download_file(file_path, destination=f"static/image/{item}.jpg")
        await message.answer(
            text=
            "✅Изображение успешно сохранено!\n\n"
            f"Для доступа перейдите по ссылке {domen}/{List_photo[str(message.chat.id)][0]}",
            reply_markup=kb.keyboard_next)
        await state.clear()
        List_photo = {}
