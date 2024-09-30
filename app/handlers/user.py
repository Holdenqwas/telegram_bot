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
    )


async def help_menu(message: Message, bot: AsyncTeleBot):
    await bot.send_message(
        message.chat.id,
        "Здесь подробное описание о работе бота. Об авторе: /author",
    )


async def author_menu(message: Message, bot: AsyncTeleBot):
    await bot.send_message(message.chat.id, "Хорн А.В. 2024 Ссылка на гитхаб")


async def main_menu(message: Message, bot: AsyncTeleBot):
    if message.text == "Тренировка":
        state.push_menu(message.from_user.username, menu.train_menu.name)
        await bot.send_message(
            message.chat.id,
            menu.train_menu.title,
            reply_markup=menu.train_menu.markup,
        )
        return
    await bot.send_message(
        message.chat.id, "Главное меню", reply_markup=menu.main_menu.markup
    )


async def train_menu(message: Message, bot: AsyncTeleBot):
    username = message.from_user.username
    print(state.queue)
    if message.text == "Назад":
        cur_menu = getattr(menu, state.back_menu(username))
        await bot.send_message(
            message.chat.id, cur_menu.title, reply_markup=cur_menu.markup
        )
        return
    elif message.text == "Начать тренировку":
        state.push_menu(username, "Начать тренировку")
        await bot.send_message(
            message.chat.id,
            "Введи свой вес",
            reply_markup=menu.back_menu.markup,
        )
        return
    elif message.text == menu.setup_train_menu.title:
        state.push_menu(username, menu.setup_train_menu.title)
        await bot.send_message(
            message.chat.id,
            menu.setup_train_menu.title,
            reply_markup=menu.setup_train_menu.markup,
        )
        return

    if state.get_menu(username) == "Начать тренировку":
        try:
            weight = float(message.text)
        except ValueError:
            await bot.send_message(
                message.chat.id,
                "Значение должно быть целым или числом с точкой \
(83 или 83.45). Введи свой вес",
            )
            return
        status, data = await train.create_all_training(username, weight)
        if status != 200:
            await bot.send_message(
                message.chat.id,
                "Что-то пошло не так, попробуй снова ввести свой вес",
            )
            return

        if not data.name_trains:
            state.back_menu(username)
            state.push_menu(username, menu.setup_train_menu.title)
            await bot.send_message(
                message.chat.id,
                "Нет ни одной тренировки, сперва их нужно создать",
                reply_markup=menu.setup_train_menu.markup,
            )
            return

        state.push_menu(username, "Идет тренировка")
        cur_menu = menu.Menu(
            "train_in_process", "Выберете свою тренировку", data.name_trains
        )
        await bot.send_message(
            message.chat.id,
            cur_menu.title,
            reply_markup=cur_menu.markup,
        )
        return
    elif state.get_menu(username) == menu.setup_train_menu.title:
        if message.text == "Создать тренировки":
            state.push_menu(username, "Создать тренировки")
            await bot.send_message(
                message.chat.id,
                "Введите названия не более 5 тренерировок через запятую. \
Например: грудь, спина, ноги",
            )
            return
        elif message.text == "Сменить названия тренировкам":
            state.push_menu(username, "Сменить названия тренировкам")
            await bot.send_message(
                message.chat.id,
                "Введите названия не более 5 тренерировок через запятую. \
Например: грудь, спина, ноги",
            )
            return
        elif message.text == "Удалить тренировки":
            state.push_menu(username, "Удалить тренировки")
            await bot.send_message(
                message.chat.id,
                "Вы собираетесь полностью удалить все тренировки. \
Чтобы это сделать напишите в чат без кавычек: \n\n'Удалить все тренировки'",
            )
            return
    elif state.get_menu(username) == "Создать тренировки":
        status = await train.create_trainings(username, message.text)
        if status != 200:
            await bot.send_message(
                message.chat.id,
                "Что-то пошло не так, попробуй снова. Нужно отправить \
сообщение с названиями тренировок через запятую. \
Например:\n\n Верх, Низ, Кардио",
            )
            return
        else:
            await bot.send_message(
                message.chat.id,
                "Отлично, тренировки созданы",
            )
        state.back_menu(username)
        await bot.send_message(
            message.chat.id,
            menu.setup_train_menu.title,
            reply_markup=menu.setup_train_menu.markup,
        )
        return

    elif state.get_menu(username) == "Сменить названия тренировок":
        status = await train.update_name_trainings(username, message.text)
        if status != 200:
            await bot.send_message(
                message.chat.id,
                "Что-то пошло не так, попробуй снова. Нужно отправить \
сообщение с названиями тренировок через запятую. \
Например:\n\n Верх, Низ, Кардио",
            )
            return
        else:
            await bot.send_message(
                message.chat.id,
                "Отлично, тренировки обновлены",
            )
        state.back_menu(username)
        await bot.send_message(
            message.chat.id,
            menu.setup_train_menu.title,
            reply_markup=menu.setup_train_menu.markup,
        )
        return

    elif state.get_menu(username) == "Удалить тренировки":
        if message.text == "Удалить все тренировки":
            status = await train.delete_training(username, message.text)
            if status != 200:
                await bot.send_message(
                    message.chat.id,
                    "Что-то пошло не так, попробуй снова",
                )
                return
            else:
                await bot.send_message(
                    message.chat.id,
                    "Отлично, тренировки удалены",
                )
            state.back_menu(username)
            await bot.send_message(
                message.chat.id,
                menu.setup_train_menu.title,
                reply_markup=menu.setup_train_menu.markup,
            )
            return
        await bot.send_message(
            message.chat.id,
            "Чтобы удалить все тренировки нужно ввести фразу: \n\n\
Удалить все тренировки",
        )
        return
    await bot.send_message(message.chat.id, "train")
