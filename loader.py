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

headers = {
        'Host': 'teletarget.com',
        'User-Agent': ''
    }

list_user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
                    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
                    'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
                    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.432'
                    '2; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
                    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0;  Trident/5.0)',
                    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0; MDDCJS)',
                    'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTM'
                    'L, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1']