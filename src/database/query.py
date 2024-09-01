from datetime import timedelta, datetime
from os import getenv, remove
from os.path import join

from dotenv import find_dotenv, load_dotenv
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User, ImageStorage

load_dotenv(find_dotenv())

domen = getenv("DOMEN")


async def orm_add_user(session: AsyncSession, data: dict):
    obj = User(
        tg_id=int(data["id"]),
        user_name=data["user_name"]
    )
    try:
        session.add(obj)
        await session.commit()
    finally:
        print("Новый пользователь ", data["id"], ':', data["user_name"])


async def orm_add_photo(session: AsyncSession, user_id, photo_id):
    obj = ImageStorage(
        user_id=user_id,
        photo_id=photo_id,
        link_id=str(photo_id[0])
    )
    try:
        session.add(obj)
        await session.commit()
        print("Новый запись: ", str(photo_id), ".Идентификатор ", str(photo_id[0]))
    except Exception as error:
        print("Ошибка при добавлении изображения в БД")


async def orm_get_user(session: AsyncSession, user_id: int):
    query = select(User).where(User.tg_id == int(user_id))
    result = await session.execute(query)
    return result.scalar()


async def get_all_users(session: AsyncSession):
    query = select(User)
    res = await session.execute(query)
    users = []
    for user in res.scalars().all():
        users.append(user)
    return users


async def orm_get_photos(session: AsyncSession, id: int):
    query = select(ImageStorage.photo_id).where(ImageStorage.link_id == id)
    result = await session.execute(query)
    return result.scalar()


async def get_links(session: AsyncSession, user_id):
    query = select(ImageStorage.link_id).where(ImageStorage.user_id == int(user_id))
    result = await session.execute(query)
    return result.scalars().all()


async def get_all_links(session: AsyncSession):
    query = select(ImageStorage)
    res = await session.execute(query)
    for obj in res.scalars().all():
        if obj.created + timedelta(days=30) <= datetime.now():
            for item in obj.photo_id:
                remove(join(f'static/image/{item}.jpg'))


async def delete_usr(session: AsyncSession, id):
    query = delete(User).where(User.tg_id == id)
    await session.execute(query)
    await session.commit()
