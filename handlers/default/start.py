from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from database.models import Users

from loader import db


start_router = Router()


@start_router.message(CommandStart())
async def start(message: Message):
    await db.initial()
    if not await db.get_row(Users, tg_user_id=str(message.from_user.id)):
        await db.add_row(Users, tg_username=message.from_user.username,
                         tg_user_id=str(message.from_user.id))
        await message.answer('Привет! Вы успешно зарегистрировались!\nВоспользуйтесь командой /search_channels'
                             'для настройки параметров поиска')
    else:
        await message.answer('Привет!\nВоспользуйтесь командой /search_channels'
                             'для настройки параметров поиска')