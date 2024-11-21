from loader import bot, dp
import asyncio
from loguru import logger
from utils.set_commands import set_commands
from handlers.default.start import start_router
from handlers.custom.search_channels import search_channels_router


async def main():
    logger.info('The bot starts working')
    dp.include_routers(start_router, search_channels_router)
    await dp.start_polling(bot)
    await set_commands()


if __name__ == '__main__':
    asyncio.run(main())
