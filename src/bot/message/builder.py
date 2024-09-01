from os import getenv

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

support = getenv("SUPPORT_CONTACT_TG")


class StartMessage:
    @staticmethod
    def old(object):
        return (
            f"<b><i>👋 Здравствуйте, @{object.user_name}</i></b>!\n\n"
            f"➖➖➖➖➖➖➖➖➖➖➖➖\n"
            f"<b>ℹ️ Информация о вас:</b>\n\n"
            f"📇 Мой ID: <u>{object.tg_id}</u>\n"
            f"🛡️<b>Поддержка:</b> @{support}"
        )
