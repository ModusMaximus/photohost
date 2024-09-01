from aiogram.filters.callback_data import CallbackData

class Callback_ImageStorage(CallbackData, prefix="my"):
    btn_name:str
    user_id:int