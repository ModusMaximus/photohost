from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.callback.CallbackUser import Callback_ImageStorage

keyboard_start = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Сохранить фото',
                callback_data='save_photo'
            )
        ]
    ]
)

keyboard_next = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Новое фото',
                callback_data='save_new_photo'
            )
        ],
        [
            InlineKeyboardButton(
                text='В главное меню',
                callback_data='back'
            )
        ]
    ]
)

add_user = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Добавить пользователя',
                callback_data='add'
            )
        ]
    ]
)

images_admin = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='База изображений',
                callback_data='storage'
            )
        ],
        [
            InlineKeyboardButton(
                text='Удалить пользователя',
                callback_data='del_user'
            )
        ]
    ]
)

back_admin = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Вернуться в меню',
                callback_data='back_admin'
            )
        ]
    ]
)

def gen_markup_users(data):
    markup = InlineKeyboardBuilder()
    for i in data:
        markup.button(
            text=i.user_name,
            callback_data=Callback_ImageStorage(btn_name="user_storage", user_id=i.tg_id)
        )
    markup.adjust(1)
    return markup


def delete_user(data):
    markup = InlineKeyboardBuilder()
    for i in data:
        markup.button(
            text=i.user_name,
            callback_data=Callback_ImageStorage(btn_name="delete_user", user_id=i.tg_id)
        )
    markup.adjust(1)
    return markup
