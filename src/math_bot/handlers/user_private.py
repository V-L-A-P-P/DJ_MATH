from src.math_bot.keyboards.user_kb import MenuCallBack
from src.math_bot.teacher.math_teacher import teacher
from aiogram import types, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InputMediaPhoto, FSInputFile
from pprint import pprint
from src.math_bot.handlers import menu_proccesing
import os


class CleintState(StatesGroup):
    #Шаги состояний
    main_menu_choosing = State()
    category_choosing = State()
    task_solving = State()
    reading_about = State()

user_private_router = Router()

@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message, state: FSMContext):
    print(f'*{message.from_user.id} {message.from_user.username} нажал кнопку старта*')
    image_path, reply_markup = await menu_proccesing.get_main_menu()
    now_dir = os.path.dirname(__file__).replace("\\", "/")
    await message.answer_photo(types.FSInputFile(path=now_dir + image_path), reply_markup=reply_markup)
    await state.set_state(CleintState.main_menu_choosing)


@user_private_router.callback_query(MenuCallBack.filter(), CleintState.main_menu_choosing)
async def user_menu(callback: types.CallbackQuery, callback_data: MenuCallBack, state: FSMContext):

    if callback_data.button_tag == 'catalog':
        print(f'*{callback.from_user.id} нажал кнопку "Решать задачи" из главного меню*')
        image_path, reply_markup = await menu_proccesing.get_categories_menu()
        now_dir = os.path.dirname(__file__).replace("\\", "/")
        await callback.message.edit_media(media=InputMediaPhoto(media=FSInputFile(now_dir+image_path), caption='Выберите тип задач: '), reply_markup=reply_markup)
        await callback.answer()
        await state.set_state(CleintState.category_choosing)
    elif callback_data.button_tag == 'about':
        print(f'*{callback.from_user.id} нажал кнопку "О нас" из главного меню*')
        image_path, reply_markup = await menu_proccesing.get_about_menu()
        '''
        await callback.message.edit_media(
            media=InputMediaPhoto(media=FSInputFile(image_path), caption='*Всё, что необходимо знать о нас*:\n'
                                                                         'Владик - очень хорош 😏\n'
                                                                         'Женя - лапуся 😘\n'
                                                                         'Мама Жени - красотуля 💋\n'
                                                                         '+79262305879 📞', parse_mode= 'Markdown'),
            reply_markup=reply_markup)
        '''
        now_dir = os.path.dirname(__file__).replace("\\", "/")
        await callback.message.edit_media(
            media=InputMediaPhoto(media=FSInputFile(now_dir + image_path), caption='*Что умеет бот?*\n'
                                                                         '✅Присылать задачи по разным темам\n'
                                                                         '✅Показывать правильные ответы\n'
                                                                         '✅ Показывать решения и пояснения\n'
                                                                         '✅ Присылать уведомления\n'
                                                                         '*Контакты*\n'
                                                                         'Если у вас есть вопросы, предложения или пожелания, пишите нам:\n'
                                                                         '📩 [drakinajenea@gmail.com]\n'
                                                                         '💬 [@dr_evgenya]', parse_mode='Markdown'),
            reply_markup=reply_markup)
        await callback.answer()
        await state.set_state(CleintState.reading_about)
    elif callback_data.button_tag == 'theory':
        print(f'*{callback.from_user.id} нажал кнопку "Теория" из главного меню*')
        now_dir = os.path.dirname(__file__).replace("\\", "/")
        path = now_dir + await menu_proccesing.get_theory_doc()
        document = FSInputFile(path=path, filename="Теория(тестовая часть).pdf")
        await callback.message.bot.send_document(chat_id=callback.from_user.id, document=document)

@user_private_router.callback_query(MenuCallBack.filter(), CleintState.category_choosing)
async def categories_menu(callback: types.CallbackQuery, callback_data: MenuCallBack, state: FSMContext):

    if callback_data.button_tag == 'mainmenu':
        print(f'*{callback.from_user.id} нажал кнопку "В главное меню" из меню категорий*')
        image_path, reply_markup = await menu_proccesing.get_main_menu()
        now_dir = os.path.dirname(__file__).replace("\\", "/")
        await callback.message.edit_media(
            media=InputMediaPhoto(media=FSInputFile(now_dir + image_path)),
            reply_markup=reply_markup)
        await callback.answer()
        await state.set_state(CleintState.main_menu_choosing)
    else:
        print(f'*{callback.from_user.id} нажал кнопку "<{callback_data.button_tag}>" из меню категорий*')
        task_id, task_image = teacher.create_task_order(callback.from_user.id, callback_data.button_tag)
        await callback.message.edit_media(media=InputMediaPhoto(media=task_image,
                                                                caption='Задача ' + task_id),
                                          reply_markup=await menu_proccesing.get_task_menu(is_first_task=True))
        pprint(teacher.get_task_order_copy())
        pprint(teacher.get_task_now_copy())
        await callback.answer()
        await state.set_state(CleintState.task_solving)


@user_private_router.callback_query(MenuCallBack.filter(), CleintState.task_solving)
async def categories_menu(callback: types.CallbackQuery, callback_data: MenuCallBack, state: FSMContext):
    if callback_data.button_tag == 'mainmenu':
        print(f'*{callback.from_user.id} нажал кнопку "В главное меню" из меню решения задач*')
        image_path, reply_markup = await menu_proccesing.get_main_menu()
        now_dir = os.path.dirname(__file__).replace("\\", "/")
        await callback.message.edit_media(
            media=InputMediaPhoto(media=FSInputFile(now_dir + image_path)),
            reply_markup=reply_markup)
        await callback.answer()
        await state.set_state(CleintState.main_menu_choosing)
    elif callback_data.button_tag == 'next_task':
        print(f'*{callback.from_user.id} нажал кнопку "Следующая задача" из меню решения задач*')
        task_id, task_image = teacher.get_next_task(callback.from_user.id)
        if task_id:
            await callback.message.edit_media(media=InputMediaPhoto(media=task_image,
                                                                    caption='Задача ' + task_id),
                                              reply_markup=await menu_proccesing.get_task_menu(is_last_task=teacher.is_last_task(callback.from_user.id)))
        await callback.answer()
    elif callback_data.button_tag == 'prev_task':
        print(f'{callback.from_user.id} нажал кнопку "Предыдущая задача" из меню решения задач')
        task_id, task_image = teacher.get_prev_task(callback.from_user.id)
        if task_id:
            await callback.message.edit_media(media=InputMediaPhoto(media=task_image,
                                                                    caption='Задача ' + task_id),
                                              reply_markup=await menu_proccesing.get_task_menu(
                                                  is_first_task=teacher.is_first_task(callback.from_user.id)))
        await callback.answer()
    elif callback_data.button_tag == 'show_answer':
        print(f'*{callback.from_user.id} нажал кнопку "Показать ответ" из меню решения задач*')
        await callback.answer(teacher.get_answer(callback.from_user.id), show_alert=True)
    else:
        await callback.answer()
    pprint(teacher.get_task_order_copy())
    pprint(teacher.get_task_now_copy())


@user_private_router.callback_query(MenuCallBack.filter())
async def user_menu(callback: types.CallbackQuery, callback_data: MenuCallBack, state: FSMContext):
    print(f'!!! {callback.from_user.id} return to main menu')

    if callback_data.button_tag == 'mainmenu':
        image_path, reply_markup = await menu_proccesing.get_main_menu()
        now_dir = os.path.dirname(__file__).replace("\\", "/")
        await callback.message.edit_media(
            media=InputMediaPhoto(media=FSInputFile(now_dir + image_path)),
            reply_markup=reply_markup)
        await callback.answer()
    await state.set_state(CleintState.main_menu_choosing)

if __name__ == '__main__':
    print(__file__)
    print(InputMediaPhoto(media=FSInputFile('src/math_bot/handlers/main_banner.jpg')))






