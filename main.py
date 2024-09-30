import asyncio
import os

from dotenv import load_dotenv

load_dotenv("./.env/all.env")
from telebot.async_telebot import AsyncTeleBot

from app.states.menu import UserStateMenu
from app.handlers.admin import admin_user
from app.handlers import user
from app.filters.admin_filter import AdminFilter
from app.filters import menu_filter
from app.middlewares.antiflood_middleware import AntiFloodMiddleware

state = UserStateMenu()


bot = AsyncTeleBot(os.getenv("TOKEN"))


def register_handlers():
    bot.register_message_handler(
        admin_user, commands=["my"], admin=True, pass_bot=True
    )
    bot.register_message_handler(
        user.start_menu, commands=["start"], pass_bot=True
    )
    bot.register_message_handler(
        user.help_menu, commands=["help"], pass_bot=True
    )
    bot.register_message_handler(
        user.author_menu, commands=["author"], pass_bot=True
    )
    bot.register_message_handler(user.main_menu, main_menu=True, pass_bot=True)
    bot.register_message_handler(
        user.train_menu, train_menu=True, pass_bot=True
    )

register_handlers()

# Middlewares
bot.setup_middleware(AntiFloodMiddleware(limit=1, bot=bot))

# custom filters
bot.add_custom_filter(AdminFilter())
bot.add_custom_filter(menu_filter.MainMenuFilter())
bot.add_custom_filter(menu_filter.TrainMenuFilter())


async def run():
    print("Bot started...")
    await bot.polling(non_stop=True)


asyncio.run(run())
