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

Я - Антон, создатель этого бота для разного.

Обратная связь

Если у вас есть пожелания или предложения по доработке моего сайта или проектов, пожалуйста, пишите мне в личку: @akhorn

В ближайших планах по развитию бота:

 - Статистика по тренировка с графиками
 - Список покупок для группы пользователей: разрабатывается функция, которая позволит создавать и управлять списками покупок для групп пользователей.
 - Черный список для продуктов: планируется реализовать функцию черного списка для продуктов, которая позволит блокировать или ограничивать доступ к определенным товарам.

Следите за обновлениями и новостями о моих проектах!""")


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
    await bot.send_message(
        message.chat.id, "Главное меню", reply_markup=menu.main_menu.markup
    )


async def train_menu(message: Message, bot: AsyncTeleBot):
    username = message.from_user.username
    # print(state.mem)
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

        if "name_trains" in data and not data["name_trains"]:
            state.back_menu(username)
            state.push_menu(username, menu.setup_train_menu.title)
            await bot.send_message(
                message.chat.id,
                "Нет ни одной тренировки, сперва их нужно создать",
                reply_markup=menu.setup_train_menu.markup,
            )
            return

        state.back_menu(username)
        state.push_menu(username, "Выбор тренировки")
        cur_menu = menu.Menu(
            "train_in_process", "Выберете свою тренировку", data["name_trains"]
        )
        state.set_cookie(username, "name_trains", data["name_trains"])
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
        elif message.text == "Названия упражнений":
            status, data = await train.get_name_trainings(username)
            if status != 200:
                await bot.send_message(
                    message.chat.id,
                    "Что-то пошло не так, попробуй снова ввести свой вес",
                )
                return

            if "name_trains" not in data or ("name_trains" in data and not data["name_trains"]):
                await bot.send_message(
                    message.chat.id,
                    "Нет ни одной тренировки, сперва их нужно создать",
                    reply_markup=menu.setup_train_menu.markup,
                )
                return

            state.back_menu(username)
            state.push_menu(username, "Названия упражнений")
            cur_menu = menu.Menu(
                "set_name_exers",
                "Выбери тренировку, для которой нужно создать/сменить названия \
упражнений",
                data["name_trains"],
            )
            state.set_cookie(username, "name_trains", data["name_trains"])
            await bot.send_message(
                message.chat.id,
                cur_menu.title,
                reply_markup=cur_menu.markup,
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
            # TODO дать выбор какую тренировку удалить
            status = await train.delete_training(username)
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
    
    elif state.get_menu(username) == "Названия упражнений":
        if message.text in state.get_cookie(username, "name_trains"):
            state.set_cookie(username, "set_for_train", message.text)
            await bot.send_message(
                message.chat.id,
                "Введи названия не более 10 упражнений через запятую. \
Например: жим, разведение гантелей, тяга блока",
                reply_markup=menu.back_menu.markup,
            )
            return
        else:
            name_train = state.get_cookie(username, "set_for_train")
            if name_train:
                status = await train.update_name_exercises(username, name_train, message.text)
                if status != 200:
                    await bot.send_message(
                        message.chat.id,
                        "Что-то пошло не так, попробуй снова. Нужно отправить \
        сообщение с названиями упражнений через запятую. \
        Например:\n\n жим, разведение гантелей, тяга блока",
                    )
                    return
                else:
                    state.clear_mem(username)
                    await bot.send_message(
                        message.chat.id,
                        "Отлично, упражнения обновлены",
                        reply_markup=menu.main_menu.markup,
                    )
                    return

            await bot.send_message(
                message.chat.id,
                "Нужно выбрать название тренировки",
            )
            return
                
    
    elif state.get_menu(username) == "Выбор тренировки":
        if message.text in state.get_cookie(username, "name_trains"):
            state.back_menu(username)
            await bot.send_message(
                message.chat.id,
                f"Начинаем тренировку {message.text}",
            )
            status, data = await train.get_name_exercises(
                username, message.text
            )
            if status == 200:
                if not data["name_exercises"]:
                    await bot.send_message(
                        message.chat.id,
                        "Для тренировки не создано ни одного упражнения",
                    )
                    await bot.send_message(
                        message.chat.id,
                        menu.setup_train_menu.title,
                        reply_markup=menu.setup_train_menu.markup,
                    )
                    return

                state.push_menu(username, "Идет тренировка")
                state.set_cookie(username, "cur_train", message.text)
                state.set_cookie(
                    username, "name_exercises", data["name_exercises"]
                )
                status = await train.start_train(username, message.text)
                if status == 200:
                    state.set_cookie(
                        username, "name_exercises", data["name_exercises"]
                    )
                    last_value = await train.get_last_value(
                        username, message.text, data["name_exercises"][0]
                    )
                    await bot.send_message(
                        message.chat.id,
                        f"{data['name_exercises'][0]}: {last_value}",
                        reply_markup=menu.back_menu.markup,
                    )
                    return
                else:
                    await bot.send_message(
                        message.chat.id, "Что-то пошло не так, попробуй снова"
                    )
                    return

            else:
                await bot.send_message(
                    message.chat.id, "Что-то пошло не так, попробуй снова"
                )
                return
        else:
            await bot.send_message(
                message.chat.id,
                "Нельзя сейчас ничего писать, нужно выбрать тренировку \
из списка снизу, либо изменить названия тренировок в настройках",
            )

    elif state.get_menu(username) == "Идет тренировка":
        try:
            value = float(message.text)
        except ValueError:
            await bot.send_message(
                message.chat.id,
                "Новое значение упражнения должно быть целым или числом с \
точкой. Например 99 или 99.5 Отправь сообщение заново",
            )
            return

        all_exers = state.get_cookie(username, "name_exercises")
        cur_train = state.get_cookie(username, "cur_train")
        await train.write_exercise(username, cur_train, all_exers[0], value)
        all_exers.pop(0)
        if all_exers:
            last_value = await train.get_last_value(
                username, cur_train, all_exers[0]
            )
            await bot.send_message(
                message.chat.id,
                f"{all_exers[0]}: {last_value}",
                reply_markup=menu.back_menu.markup,
            )
            state.set_cookie(username, "name_exercises", all_exers)
            return
        else:
            state.clear_mem(username)
            await bot.send_message(
                message.chat.id,
                "Тренировка завершена",
                reply_markup=menu.main_menu.markup,
            )
            return
    await bot.send_message(message.chat.id, "train")
