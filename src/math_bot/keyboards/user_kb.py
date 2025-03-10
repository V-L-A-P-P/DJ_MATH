from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

class MenuCallBack(CallbackData, prefix="menu"):
    button_tag : str


def get_user_main_menu_kb(*, sizes: tuple[int] = (1,)):
    keyboard = InlineKeyboardBuilder()
    btns = {
        "Решать задачи 🤓": "catalog",
        "О нас ℹ️": "about"
    }

    for text, menu_name in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=MenuCallBack(button_tag=menu_name).pack()))

    return keyboard.adjust(*sizes).as_markup()

def get_categories_menu_kb(*, sizes: tuple[int] = (1,)):
    keyboard = InlineKeyboardBuilder()
    btns = {
        "Планиметрия (№17)": "2d",
        "Стереометрия (№14)": "3d",
        "Параметры (№18)": "parametrs",
        "В главное меню 🏠" : "mainmenu"
    }

    for text, menu_name in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=MenuCallBack(button_tag=menu_name).pack()))

    return keyboard.adjust(*sizes).as_markup()

def get_about_menu_kb(*, sizes: tuple[int] = (1,)):
    keyboard = InlineKeyboardBuilder()
    btns = {
        "В главное меню ": "mainmenu"
    }
    for text, menu_name in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=MenuCallBack(button_tag=menu_name).pack()))

    return keyboard.adjust(*sizes).as_markup()

def get_for_task_kb(*, sizes: tuple[int] = (3,), is_first_task=False, is_last_task=False):
    keyboard = InlineKeyboardBuilder()
    if is_first_task and is_last_task:
        btns = {
            "Ответ 💡": "show_answer",
            "В главное меню 🏠": "mainmenu",

        }
    elif is_first_task:
        btns = {
            "Ответ 💡": "show_answer",
            "Следующая": "next_task",
            "В главное меню 🏠": "mainmenu",

        }
    elif is_last_task:
        btns = {
            "Предыдущая": "prev_task",
            "Ответ 💡": "show_answer",
            "В главное меню 🏠": "mainmenu",

        }
    else:
        btns = {
            "Предыдущая": "prev_task",
            "Ответ 💡": "show_answer",
            "Следующая": "next_task",
            "В главное меню 🏠": "mainmenu",

        }
    for text, menu_name in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=MenuCallBack(button_tag=menu_name).pack()))
    if is_first_task and is_last_task:
        return keyboard.adjust(*(1,)).as_markup()
    elif is_first_task or is_last_task:
        return keyboard.adjust(*(2,)).as_markup()
    else:
        return keyboard.adjust(*sizes).as_markup()