from aiogram.types import BotCommand, BotCommandScopeDefault
from loader import bot


async def set_commands():
    commands = [
        BotCommand(command='start', description='Начать работу с ботом'),
        BotCommand(command='search_channels', description='Поиск телеграмм каналов')
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
