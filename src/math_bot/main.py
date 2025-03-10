import asyncio
import os

from aiogram import Bot, Dispatcher

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from handlers.user_private import user_private_router


# ALLOWED_UPDATES = ['message', 'edited_message', 'callback_query']

bot = Bot(token=os.getenv('TOKEN'))
bot.my_admins_list = []

dp = Dispatcher()

dp.include_router(user_private_router)


async def on_startup(bot):

    print('бот стартовал')


async def on_shutdown(bot):
    print('бот лег')

async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


asyncio.run(main())
