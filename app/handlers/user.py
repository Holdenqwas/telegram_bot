from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from app.keyboards import menu
from app.states.menu import UserStateMenu
from app.services import train, user

state = UserStateMenu()


async def start_menu(message: Message, bot: AsyncTeleBot):
    await user.create_user(message.from_user.username)
    await bot.send_message(
        message.chat.id,
        "Вас приветствует личный бот помощник! Чтобы получить помощь воспользуйтейсь командой /help",
        reply_markup=menu.main_menu.markup
    )


async def help_menu(message: Message, bot: AsyncTeleBot):
    await bot.send_message(
        message.chat.id,
        """Бот помошник в Telegram: Инструкция

Здесь ты найдешь все, что необходимо мне для комфортной жизни и многое другое.

 - Основные функции:

1. Хранилище тренировок:

До 5 различных видов тренировок: создай свои собственные планы тренировок.
До 10 упражнений на каждую тренировку: заполни названия упражнений, которые ты будешь выполнять.
Статистика по весу: бот запоминает твой вес
Отслеживание прогресса: бот напомнит тебе вес, с которым ты работал на прошлой тренировке.


2. Создание тренировки:

Нажми кнопку "Начать тренировку".
Введи свой текущий вес.
Выбери тренировку, которую ты хочешь провести.
Для каждого упражнения введи текущий вес, с которым ты будешь работать.

 - Как пользоваться:

1. Заполнение хранилища тренировок:

Создай новую тренировку:
Нажми кнопку "Настройка тренировок".
Здесь сперва создай тренировки.
Добавь упражнения, нажав кнопку "Названия упражнений" и введя название.
 Важно! "Удалить тренировки" Удалит полностью все записи о тренировках.

2. Проведение тренировки:

Нажми кнопку "Начать тренировку".
Введи свой текущий вес.
Выбери тренировку.
Для каждого упражнения:
Бот напомнит тебе вес, с которым ты работал на прошлой тренировке.
Введи текущий вес, с которым ты будешь работать.
После завершения тренировки бот сохранит твои результаты и обновит статистику.
 Советы:

Удачи в тренировках!

Об авторе: /author""",
    )


async def author_menu(message: Message, bot: AsyncTeleBot):
    await bot.send_message(message.chat.id, 
                           """Обо мне

Я - Антон, создатель этого бота для разного (v1.0.0).

Обратная связь

Если у вас есть пожелания или предложения по доработке моего сайта или проектов, пожалуйста, пишите мне в личку: @akhorn

В ближайших планах по развитию бота:

 - Статистика по тренировка с графиками
 - Список покупок для группы пользователей: разрабатывается функция, которая позволит создавать и управлять списками покупок для групп пользователей.
 - Черный список для продуктов: планируется реализовать функцию черного списка для продуктов, которая позволит блокировать или ограничивать доступ к определенным товарам.

Следите за обновлениями!

Changelog:

09.10.2024 v1.0.0
 - Добавлен раздел тренировок, добавление до 5 тренировок, до 10 упражнений, сохранение веса.
""")


async def get_main_menu(message: Message, bot: AsyncTeleBot):
        state.clear_mem(message.from_user.username)
        await bot.send_message(
            message.chat.id,
            "Главное меню",
            reply_markup=menu.main_menu.markup,
        )
        return


async def main_menu(message: Message, bot: AsyncTeleBot):
    if message.text == "Тренировка":
        state.push_menu(message.from_user.username, menu.train_menu.name)
        await bot.send_message(
            message.chat.id,
            menu.train_menu.title,
            reply_markup=menu.train_menu.markup,
        )
        return
    elif message.text == "Покупки":
        state.push_menu(message.from_user.username, menu.shop_menu.name)
        await bot.send_message(
            message.chat.id,
            menu.shop_menu.title,
            reply_markup=menu.shop_menu.markup,
        )
        return
    await bot.send_message(
        message.chat.id, "Главное меню", reply_markup=menu.main_menu.markup
    )



