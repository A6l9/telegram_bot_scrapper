from aiogram.types import InlineKeyboardMarkup
from keyboards.buttons import parameters_buttons
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_parameters_keyboard():
    kbs_builder = InlineKeyboardBuilder()
    kbs_builder.row(*parameters_buttons)
    kbs_builder.adjust(1)
    return kbs_builder.as_markup()
