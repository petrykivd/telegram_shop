# - *- coding: utf- 8 - *-
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from tgbot.data.config import get_admins
from tgbot.services.api_sqlite import get_settingsx


# Проверка на диалог в ЛС бота
class IsPrivate(BoundFilter):
    async def check(self, message):
        if "id" in message:
            return message.message.chat.type == types.ChatType.PRIVATE
        else:
            return message.chat.type == types.ChatType.PRIVATE


# Проверка на админа
class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        if message.from_user.id in get_admins():
            return True
        else:
            return False

class IsDimkevich(BoundFilter):
    async def check(self, message: types.Message):
        if str(message.from_user.id) == "346783362": # 950467953 346783362
            return True
        else:
            return False

# Проверка на технические работы
class IsWork(BoundFilter):
    async def check(self, message: types.Message):
        get_settings = get_settingsx()

        if get_settings['status_work'] == "False" or message.from_user.id in get_admins():
            return False
        else:
            return True


# Проверка на возможность пополнения
class IsRefill(BoundFilter):
    async def check(self, message: types.Message):
        get_settings = get_settingsx()

        if get_settings['status_refill'] == "True" or message.from_user.id in get_admins():
            return False
        else:
            return True


# Проверка на возможность покупки товара
class IsBuy(BoundFilter):
    async def check(self, message: types.Message):
        get_settings = get_settingsx()

        if get_settings['status_buy'] == "True" or message.from_user.id in get_admins():
            return False
        else:
            return True
