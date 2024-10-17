from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from app.keyboards import menu
from app.states.menu import UserStateMenu
from app.services import train

state = UserStateMenu()


async def train_menu(message: Message, bot: AsyncTeleBot):
    user_id = message.from_user.id
    # print(state.mem)
    if message.text == "Назад":
        cur_menu = getattr(menu, state.back_menu(user_id))
        await bot.send_message(
            message.chat.id, cur_menu.title, reply_markup=cur_menu.markup
        )
        return
    elif message.text == "Начать тренировку":
        state.push_menu(user_id, "Начать тренировку")
        await bot.send_message(
            message.chat.id,
            "Введи свой вес",
            reply_markup=menu.back_menu.markup,
        )
        return
    elif message.text == menu.setup_train_menu.title:
        state.push_menu(user_id, menu.setup_train_menu.title)
        await bot.send_message(
            message.chat.id,
            menu.setup_train_menu.title,
            reply_markup=menu.setup_train_menu.markup,
        )
        return

    if state.get_menu(user_id) == "Начать тренировку":
        try:
            weight = float(message.text)
        except ValueError:
            await bot.send_message(
                message.chat.id,
                "Значение должно быть целым или числом с точкой \
(83 или 83.45). Введи свой вес",
            )
            return
        status, data = await train.create_all_training(user_id, weight)
        if status != 200:
            await bot.send_message(
                message.chat.id,
                "Что-то пошло не так, попробуй снова ввести свой вес",
            )
            return

        if "name_trains" in data and not data["name_trains"]:
            state.back_menu(user_id)
            state.push_menu(user_id, menu.setup_train_menu.title)
            await bot.send_message(
                message.chat.id,
                "Нет ни одной тренировки, сперва их нужно создать",
                reply_markup=menu.setup_train_menu.markup,
            )
            return

        state.back_menu(user_id)
        state.push_menu(user_id, "Выбор тренировки")
        cur_menu = menu.Menu(
            "train_in_process", "Выберете свою тренировку", data["name_trains"]
        )
        state.set_cookie(user_id, "name_trains", data["name_trains"])
        await bot.send_message(
            message.chat.id,
            cur_menu.title,
            reply_markup=cur_menu.markup,
        )
        return
    elif state.get_menu(user_id) == menu.setup_train_menu.title:
        if message.text == "Создать тренировки":
            state.push_menu(user_id, "Создать тренировки")
            await bot.send_message(
                message.chat.id,
                "Введите названия не более 5 тренерировок через запятую. \
Например: грудь, спина, ноги",
            )
            return
        elif message.text == "Сменить названия тренировкам":
            state.push_menu(user_id, "Сменить названия тренировкам")
            await bot.send_message(
                message.chat.id,
                "Введите названия не более 5 тренерировок через запятую. \
Например: грудь, спина, ноги",
            )
            return
        elif message.text == "Удалить тренировки":
            state.push_menu(user_id, "Удалить тренировки")
            await bot.send_message(
                message.chat.id,
                "Вы собираетесь полностью удалить все тренировки. \
Чтобы это сделать напишите в чат без кавычек: \n\n'Удалить все тренировки'",
            )
            return
        elif message.text == "Названия упражнений":
            status, data = await train.get_name_trainings(user_id)
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

            state.back_menu(user_id)
            state.push_menu(user_id, "Названия упражнений")
            cur_menu = menu.Menu(
                "set_name_exers",
                "Выбери тренировку, для которой нужно создать/сменить названия \
упражнений",
                data["name_trains"],
            )
            state.set_cookie(user_id, "name_trains", data["name_trains"])
            await bot.send_message(
                message.chat.id,
                cur_menu.title,
                reply_markup=cur_menu.markup,
            )
            return

    elif state.get_menu(user_id) == "Создать тренировки":
        status = await train.create_trainings(user_id, message.text)
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
        state.back_menu(user_id)
        await bot.send_message(
            message.chat.id,
            menu.setup_train_menu.title,
            reply_markup=menu.setup_train_menu.markup,
        )
        return

    elif state.get_menu(user_id) == "Сменить названия тренировок":
        status = await train.update_name_trainings(user_id, message.text)
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
        state.back_menu(user_id)
        await bot.send_message(
            message.chat.id,
            menu.setup_train_menu.title,
            reply_markup=menu.setup_train_menu.markup,
        )
        return

    elif state.get_menu(user_id) == "Удалить тренировки":
        if message.text == "Удалить все тренировки":
            # TODO дать выбор какую тренировку удалить
            status = await train.delete_training(user_id)
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
            state.back_menu(user_id)
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
    
    elif state.get_menu(user_id) == "Названия упражнений":
        if message.text in state.get_cookie(user_id, "name_trains"):
            state.set_cookie(user_id, "set_for_train", message.text)
            await bot.send_message(
                message.chat.id,
                "Введи названия не более 10 упражнений через запятую. \
Например: жим, разведение гантелей, тяга блока",
                reply_markup=menu.back_menu.markup,
            )
            return
        else:
            name_train = state.get_cookie(user_id, "set_for_train")
            if name_train:
                status = await train.update_name_exercises(user_id, name_train, message.text)
                if status != 200:
                    await bot.send_message(
                        message.chat.id,
                        "Что-то пошло не так, попробуй снова. Нужно отправить \
        сообщение с названиями упражнений через запятую. \
        Например:\n\n жим, разведение гантелей, тяга блока",
                    )
                    return
                else:
                    state.clear_mem(user_id)
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
                
    
    elif state.get_menu(user_id) == "Выбор тренировки":
        if message.text in state.get_cookie(user_id, "name_trains"):
            state.back_menu(user_id)
            await bot.send_message(
                message.chat.id,
                f"Начинаем тренировку {message.text}",
            )
            status, data = await train.get_name_exercises(
                user_id, message.text
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

                state.push_menu(user_id, "Идет тренировка")
                state.set_cookie(user_id, "cur_train", message.text)
                state.set_cookie(
                    user_id, "name_exercises", data["name_exercises"]
                )
                status = await train.start_train(user_id, message.text)
                if status == 200:
                    state.set_cookie(
                        user_id, "name_exercises", data["name_exercises"]
                    )
                    last_value = await train.get_last_value(
                        user_id, message.text, data["name_exercises"][0]
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

    elif state.get_menu(user_id) == "Идет тренировка":
        try:
            value = float(message.text)
        except ValueError:
            await bot.send_message(
                message.chat.id,
                "Новое значение упражнения должно быть целым или числом с \
точкой. Например 99 или 99.5 Отправь сообщение заново",
            )
            return

        all_exers = state.get_cookie(user_id, "name_exercises")
        cur_train = state.get_cookie(user_id, "cur_train")
        await train.write_exercise(user_id, cur_train, all_exers[0], value)
        all_exers.pop(0)
        if all_exers:
            last_value = await train.get_last_value(
                user_id, cur_train, all_exers[0]
            )
            await bot.send_message(
                message.chat.id,
                f"{all_exers[0]}: {last_value}",
                reply_markup=menu.back_menu.markup,
            )
            state.set_cookie(user_id, "name_exercises", all_exers)
            return
        else:
            state.clear_mem(user_id)
            await bot.send_message(
                message.chat.id,
                "Тренировка завершена",
                reply_markup=menu.main_menu.markup,
            )
            return
    await bot.send_message(message.chat.id, "train")