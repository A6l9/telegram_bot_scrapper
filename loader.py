from config.config import BOT_TOKEN
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from database.controller import BaseInterface
from database.database import DATABASE_URL
from misc.temp_storage import UserManager


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
db = BaseInterface(DATABASE_URL)
user_manager = UserManager()
url_for_channels = 'https://teletarget.com/catalog/{category}/?page={num}'
url_for_categories = 'https://teletarget.com/catalog/'
