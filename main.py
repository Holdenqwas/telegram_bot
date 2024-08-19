import asyncio
import os

from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot

import menu
from state import UserStateMenu
from submenus.training import training_handler

load_dotenv("./.env/all.env")

bot = AsyncTeleBot(os.getenv("TOKEN"))
state = UserStateMenu()


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    if message.from_user.username != 'AKhorn':
        await bot.send_message(message.from_user.id, "Вас приветствует личный бот.\
К сожалению, работать с Вами он не будет. И вообще, Вы кто такие? Я вас не звал! Идите на х*й!")
    state.push_menu(message.from_user.id, menu.main_menu.name)
    await bot.send_message(message.from_user.id, "Вас приветствует бот.",
                           reply_markup=menu.main_menu.markup)


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    if message.from_user.username != 'AKhorn':
        await bot.send_message(message.from_user.id, "Вы кто такие? Я вас не звал! Идите на х*й!")
        return
    # print(state.queue)
    uid = message.from_user.id
    if message.text == "Назад":
        cur_menu = getattr(menu, state.back_menu(uid))
        await bot.send_message(message.from_user.id, cur_menu.title,
                               reply_markup=cur_menu.markup)
    elif message.text == "Тренировка":
        state.push_menu(uid, menu.training_menu.name)
        await bot.send_message(message.from_user.id, menu.training_menu.title,
                               reply_markup=menu.training_menu.markup)
    elif state.check_category(uid, menu.training_menu.name):
        await training_handler(bot, message, state)
    else:
        state.push_menu(uid, menu.main_menu.name)
        await bot.send_message(message.from_user.id, menu.main_menu.title,
                               reply_markup=menu.main_menu.markup)


print("Bot started...")
asyncio.run(bot.polling())
