from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from app.keyboards import menu


async def start_menu(message: Message, bot: AsyncTeleBot):
    await bot.send_message(message.chat.id, "Вас приветствует личный бот помощник! Чтобы получить помощь воспользуйтейсь командой /help")


async def help_menu(message: Message, bot: AsyncTeleBot):
    await bot.send_message(message.chat.id, "Здесь подробное описание о работе бота. Об авторе: /author")


async def author_menu(message: Message, bot: AsyncTeleBot):
    await bot.send_message(message.chat.id, "Хорн А.В. 2024 Ссылка на гитхаб")


async def main_menu(message: Message, bot: AsyncTeleBot):
    await bot.send_message(message.chat.id, "Главное меню", reply_markup=menu.main_menu.markup)


async def train(message: Message, bot: AsyncTeleBot):
    """
    You can create a function and use parameter pass_bot.
    """
    await bot.send_message(message.chat.id, "train")
# # Handle '/start' and '/help'
# @bot.message_handler(commands=["help", "start"])
# async def send_welcome(message):

#     if message.from_user.username != os.getenv("MY_NAME"):
#         await bot.send_message(
#             message.from_user.id,
#             "Вас приветствует личный бот.\
# К сожалению, работать с Вами он не будет. И вообще, Вы кто такие? Я вас не звал! Идите на х*й!",
#         )
#     state.push_menu(message.from_user.id, menu.main_menu.name)
#     await bot.send_message(
#         message.from_user.id,
#         "Вас приветствует бот.",
#         reply_markup=menu.main_menu.markup,
#     )


# # Handle all other messages with content_type 'text' (content_types defaults to ['text'])
# @bot.message_handler(func=lambda message: True)
# async def echo_message(message):
#     if message.from_user.username != os.getenv("MY_NAME"):
#         await bot.send_message(
#             message.from_user.id, "Вы кто такие? Я вас не звал! Идите на х*й!"
#         )
#         return
#     # print(state.queue)
#     uid = message.from_user.id
#     if message.text == "Назад":
#         cur_menu = getattr(menu, state.back_menu(uid))
#         await bot.send_message(
#             message.from_user.id, cur_menu.title, reply_markup=cur_menu.markup
#         )
#     elif message.text == "Тренировка":
#         state.push_menu(uid, menu.training_menu.name)
#         await bot.send_message(
#             message.from_user.id,
#             menu.training_menu.title,
#             reply_markup=menu.training_menu.markup,
#         )
#     elif state.check_category(uid, menu.training_menu.name):
#         await training_handler(bot, message, state)
#     else:
#         state.push_menu(uid, menu.main_menu.name)
#         await bot.send_message(
#             message.from_user.id,
#             menu.main_menu.title,
#             reply_markup=menu.main_menu.markup,
#         )
