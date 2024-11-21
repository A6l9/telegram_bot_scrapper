from aiogram.types import InlineKeyboardButton


parameters_buttons = (InlineKeyboardButton(
    text='Выбрать ключевое слово',
    callback_data='change_keyword'
    ), InlineKeyboardButton(
    text='Ввести кол-во подписчиков',
    callback_data='change_subs_count'
    ),
    InlineKeyboardButton(
    text='Начать поиск',
    callback_data='start_search'
    ),
    )