import re

from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from sqlalchemy import and_, func

from database.models import TgChannels
from storage.states import States
from aiogram.fsm.context import FSMContext
from loader import bot, db, user_manager
import asyncio
from keyboards.inline.inline_kbs import create_parameters_keyboard


search_channels_router = Router()


@search_channels_router.message(Command('search_channels'))
async def search_channels(message: Message):
    temp_storage = user_manager.get_user(message.chat.id)
    await message.answer('Параметры поиска:\n'
                         'Ключевое слово: {keyword}\n'
                         'Кол-во подписчиков: {count_subs}'.format(keyword=temp_storage.keyword,
                                                                   count_subs=temp_storage.range_subs),
                         reply_markup=create_parameters_keyboard())



@search_channels_router.callback_query(F.data=='change_keyword')
async def change_keyword(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Напишите ключевое слово:')
    await state.set_state(States.write_keyword)


@search_channels_router.message(States.write_keyword)
async def write_keyword_take_answer(message: Message, state: FSMContext):
    temp_storage = user_manager.get_user(message.chat.id)
    temp_storage.keyword = message.text
    await state.clear()
    await search_channels(message)


@search_channels_router.callback_query(F.data=='change_subs_count')
async def change_subs_count(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Введите диапазон подписчиков в формате "от-до", если вы'
                                     'хотите указать определенный диапазон введите диапазон в формате "10-10"')
    await state.set_state(States.write_subs_count)


@search_channels_router.message(States.write_subs_count)
async def write_subs_count_take_answer(message: Message, state: FSMContext):
    temp_storage = user_manager.get_user(message.chat.id)
    pattern = r'^\d+-\d+$'
    match = re.match(pattern=pattern, string=message.text)
    if match:
        if int(message.text.split('-')[1]) > int(message.text.split('-')[0]):
            low, high = message.text.split('-')
            temp_storage.amount_min = int(low)
            temp_storage.amount_max = int(high)
            temp_storage.range_subs = str(message.text)
            await state.clear()
            await search_channels(message)
        else:
            await message.answer('Ошибка ввода. Пожалуйста, введите диапазон в формате "от-до".')
    else:
        await message.answer('Ошибка ввода. Пожалуйста, введите диапазон в формате "от-до".')


@search_channels_router.callback_query(F.data=='start_search')
async def write_keyword_take_answer(call: CallbackQuery, state: FSMContext):
    temp_storage = user_manager.get_user(call.message.chat.id)
    sql_filter = and_(func.lower(TgChannels.tg_channel_name).ilike(f'%{temp_storage.keyword.lower()}%'),
                      int(temp_storage.amount_min) < TgChannels.subscribers_count,
                      TgChannels.subscribers_count < int(temp_storage.amount_max))
    result = await db.get_row(TgChannels, to_many=True, filter={'filter': sql_filter})
    for i_elem in result[:10]:
        await bot.send_photo(caption=f'Название: {i_elem.tg_channel_name}\n'
                       f'Количество подписчиков: {i_elem.subscribers_count}\n'
                       f'Ссылка на канал: {i_elem.tg_link}\n', photo=i_elem.channel_photo, chat_id=call.message.chat.id)
        await asyncio.sleep(2)
    if not result:
        await call.message.answer('Ничего не было найдено, '
                                  'извините, моя база каналов пока не достаточно большая.')
    await state.clear()
