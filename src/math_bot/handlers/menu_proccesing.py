from src.math_bot.keyboards import user_kb


async def get_main_menu():
    banner_path = 'src/math_bot/handlers/main_banner.jpg'
    kbds = user_kb.get_user_main_menu_kb()
    return banner_path, kbds

async def get_categories_menu():
    banner_path = 'src/math_bot/handlers/categories_banner.jpg'
    kbds = user_kb.get_categories_menu_kb()
    return banner_path, kbds

async def get_about_menu():
    banner_path = 'src/math_bot/handlers/about_banner.jpg'
    kbds = user_kb.get_about_menu_kb()
    return banner_path, kbds

async def get_task_menu(is_first_task=False, is_last_task=False):
    return user_kb.get_for_task_kb(is_first_task=is_first_task, is_last_task=is_last_task)

