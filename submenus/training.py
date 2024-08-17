import data
import menu


async def next_func(bot, message, state, uid):
    cur_menu_name = state.get_menu(uid)
    parent_menu_name = state.back_menu(uid)
    parent_menu = getattr(menu, parent_menu_name)
    index = parent_menu.items.index(cur_menu_name) + 1
    if index < len(parent_menu.items):
        next_menu_name = parent_menu.items[index]
        state.push_menu(uid, next_menu_name)
        await bot.send_message(message.from_user.id, next_menu_name)
    else:
        parent_menu_name = state.back_menu(uid)
        parent_menu = getattr(menu, parent_menu_name)
        await bot.send_message(message.from_user.id, parent_menu.title,
                               reply_markup=parent_menu.markup)


async def training_handler(bot, message, state):
    uid = message.from_user.id

    if message.text == "Грудь":
        state.push_menu(uid, menu.train_breast_menu.name)
        await bot.send_message(message.from_user.id,
                               menu.train_breast_menu.title,
                               reply_markup=menu.train_breast_menu.markup)
    elif message.text == "Спина":
        state.push_menu(uid, menu.train_beak_menu.name)
        await bot.send_message(message.from_user.id,
                               menu.train_beak_menu.title,
                               reply_markup=menu.train_beak_menu.markup)
    elif message.text == "Ноги":
        state.push_menu(uid, menu.train_leg_menu.name)
        await bot.send_message(message.from_user.id,
                               menu.train_leg_menu.title,
                               reply_markup=menu.train_leg_menu.markup)
    elif message.text == "Дальше":
        await next_func(bot, message, state, uid)

    elif (message.text in data.train_breast_menu
          or message.text in data.train_breast_menu
          or message.text in data.train_breast_menu):
        state.push_menu(uid, message.text)
        await bot.send_message(message.from_user.id,
                               message.text,
                               reply_markup=menu.train_exercise_menu.markup)
    else:
        print(message.text, state.get_menu(uid))
        await next_func(bot, message, state, uid)
