from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from app.keyboards import menu
from app.states.menu import UserStateMenu
from app.services import shop as service

state = UserStateMenu()
MARKER_TO_DELETE = "ㅤ"

async def shop_menu(message: Message, bot: AsyncTeleBot):
    user_id = message.from_user.id
    if message.text == "Назад":
        cur_menu = getattr(menu, state.back_menu(user_id))
        await bot.send_message(
            message.chat.id, cur_menu.title, reply_markup=cur_menu.markup
        )
        return
    elif message.text == "Открыть список":
        status, data = await service.get_names_shop_list(user_id)
        if status != 200:
            await bot.send_message(
                message.chat.id,
                "Что-то пошло не так, попробуй снова",
            )
            return

        if "names" in data and not data["names"]:
            await bot.send_message(
                message.chat.id,
                "Нет ни одного списка, сперва их нужно создать или добавить",
            )
            return

        state.push_menu(user_id, "Открыть список")
        cur_menu = menu.Menu("Открыть список", "Выбери список", data["names"])
        await bot.send_message(
            message.chat.id,
            cur_menu.title,
            reply_markup=cur_menu.markup,
        )
        return
    elif message.text == "Добавить новый список":
        state.push_menu(user_id, "Добавить новый список")
        await bot.send_message(
            message.chat.id,
            "Введи название нового списка покупок",
            reply_markup=menu.back_menu.markup,
        )
        return
    elif message.text == "Присоединиться к списку другого пользователя":
        state.push_menu(user_id, "Присоединиться")
        await bot.send_message(
            message.chat.id,
            "Введи ID списка покупок",
            reply_markup=menu.back_menu.markup,
        )
        return
    elif message.text == "Поделиться списком":
        status, data = await service.get_names_shop_list(user_id)
        if status != 200:
            await bot.send_message(
                message.chat.id,
                "Что-то пошло не так, попробуй снова",
            )
            return

        if "names" in data and not data["names"]:
            await bot.send_message(
                message.chat.id,
                "Нет ни одного списка, сперва их нужно создать или добавить",
            )
            return

        state.push_menu(user_id, "Поделиться")
        cur_menu = menu.Menu(
            "Поделиться списком",
            "Выбери список, которым хочешь поделиться",
            data["names"],
        )
        await bot.send_message(
            message.chat.id,
            cur_menu.title,
            reply_markup=cur_menu.markup,
        )
        return
    elif message.text == "Удалить список":
        status, data = await service.get_names_shop_list(user_id)
        if status != 200:
            await bot.send_message(
                message.chat.id,
                "Что-то пошло не так, попробуй снова",
            )
            return

        if "names" in data and not data["names"]:
            await bot.send_message(
                message.chat.id,
                "Нет ни одного списка, сперва их нужно создать или добавить",
            )
            return

        state.push_menu(user_id, "Удалить")
        cur_menu = menu.Menu(
            "Удалить список",
            "Выбери список, который хочешь \
удалить. Если списком кто-то пользуется кроме тебя, у него список не удалится",
            data["names"],
        )
        await bot.send_message(
            message.chat.id,
            cur_menu.title,
            reply_markup=cur_menu.markup,
        )
        return

    if state.get_menu(user_id) == "Открыть список":
        status, data = await service.get_shop_list(user_id, message.text)

        if status != 200:
            await bot.send_message(
                message.chat.id,
                "Что-то пошло не так, попробуй снова выборать свой список",
            )
            return

        state.back_menu(user_id)
        state.push_menu(user_id, "Открыт список")
        state.set_cookie(user_id, "name_shop_list", message.text)
        
        if "items" in data and not data["items"]:
            await bot.send_message(
                message.chat.id,
                f"Список с покупками пустой.\nПоследний раз обновлялся {data['update_time']}\n\n\
Чтобы добавить элементы в список, отправь их в сообщении, каждый эелемент с новой строки. Например:\n\n\
молоко\n\
яйца\n\
хлеб",
                reply_markup=menu.back_menu.markup,
            )
            return


        items = [item + MARKER_TO_DELETE for item in data["items"]]
        cur_menu = menu.Menu(
            "Открыт список",
            f"Список на дату {data['update_time']}",
            items,
        )

        await bot.send_message(
            message.chat.id,
            cur_menu.title,
            reply_markup=cur_menu.markup,
        )
        return
    elif state.get_menu(user_id) == "Добавить новый список":
        status, data = await service.create_shop_list(user_id, message.text)

        if status != 200:
            await bot.send_message(
                message.chat.id,
                "Что-то пошло не так, попробуй снова отправить название \
нового списка, либо позже",
            )
            return

        state.back_menu(user_id)
        await bot.send_message(
            message.chat.id,
            "Список создан",
            reply_markup=menu.shop_menu.markup,
        )
        return

    elif state.get_menu(user_id) == "Присоединиться":
        status, data = await service.user_add_shop_list(user_id, message.text)

        if status != 200:
            await bot.send_message(
                message.chat.id,
                "Что-то пошло не так, попробуй снова отправить ID списка, либо позже",
            )
            return

        state.back_menu(user_id)
        await bot.send_message(
            message.chat.id,
            "Список добавлен",
            reply_markup=menu.shop_menu.markup,
        )
        return
    elif state.get_menu(user_id) == "Поделиться":
        status, data = await service.get_uid_shop_list(user_id, message.text)

        if status != 200:
            await bot.send_message(
                message.chat.id,
                "Что-то пошло не так, попробуй снова отправить ID списка, либо позже",
            )
            return

        state.back_menu(user_id)
        await bot.send_message(
            message.chat.id,
            "Перешли следующее сообщение пользователю, с которым хочешь совместно вести список покупок.",
            reply_markup=menu.shop_menu.markup,
        )
        await bot.send_message(
            message.chat.id,
            f'Чтобы добавить список покупок "{message.text}" нужно:\n\
1. Добавить бота https://t.me/khorn_butler_bot \n\
2. Перейти в меню Покупки -> Присоединиться к списку другого пользователя\n\
3. Ввести следующий ID \n\n{data}\n\n\
4. Готово, теперь вы можете вместе добавлять и удалять элементы от туда',
            reply_markup=menu.shop_menu.markup,
        )
        return
    elif state.get_menu(user_id) == "Удалить":
        status, data = await service.delete_shop_list(user_id, message.text)

        if status != 200:
            await bot.send_message(
                message.chat.id,
                "Что-то пошло не так, попробуй снова выбрать список, либо позже",
            )
            return

        state.back_menu(user_id)
        await bot.send_message(
            message.chat.id,
            "Список успешно удален",
            reply_markup=menu.shop_menu.markup,
        )

        return
    elif state.get_menu(user_id) == "Открыт список":
        name_shop_list = state.get_cookie(user_id, "name_shop_list")

        if message.text.endswith(MARKER_TO_DELETE):
            # Нудно удалить элемент
            status, data = await service.del_item_from_shop_list(user_id, name_shop_list, message.text[:-len(MARKER_TO_DELETE)])
            if status != 200:
                await bot.send_message(
                    message.chat.id,
                    "Что-то пошло не так при удалении из списка, попробуй снова, либо позже",
                )
                return

            if "items" in data and not data["items"]:
                state.back_menu(user_id)
                await bot.send_message(
                    message.chat.id,
                    f"Список с покупками пустой.",
                    reply_markup=menu.shop_menu.markup,
                )
                return

            items = [item + MARKER_TO_DELETE for item in data["items"]]

            cur_menu = menu.Menu(
                "Открыт список",
                "Удален",
                items,
            )
            
            await bot.send_message(
                message.chat.id,
                cur_menu.title,
                reply_markup=cur_menu.markup,
            )
        else:
            # Нужно добавить в список
            status, data = await service.add_items_to_shop_list(user_id, name_shop_list, message.text)
            if status != 200:
                await bot.send_message(
                    message.chat.id,
                    "Что-то пошло не так при добавление в список, попробуй снова, либо позже",
                )
                return

            items = [item + MARKER_TO_DELETE for item in data["items"]]

            cur_menu = menu.Menu(
                "Открыт список",
                "Элементы успешно добавлены",
                items,
            )
            
            await bot.send_message(
                message.chat.id,
                cur_menu.title,
                reply_markup=cur_menu.markup,
            )

        return

    await bot.send_message(message.chat.id, "shop")
