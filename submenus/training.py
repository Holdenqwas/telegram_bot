import aiohttp
import os
import json

import app.keyboards.data as data
import app.keyboards.constructor as constructor

headers = {'content-type': "application/json",
                   "Authorization": f"Bearer {os.getenv('TOKEN_BACKEND')}"}

async def get_last_value(name_training, name_exercise):
    async with aiohttp.ClientSession() as session:
        url = os.getenv("BACKEND_URL") + f"training/{name_training}/{name_exercise}"

        async with session.get(url, headers=headers) as response:
            text = await response.text()
            print("Status:", response.status, "Body:", text)
            return text


async def start_training(name, weight):
    async with aiohttp.ClientSession() as session:
        url = os.getenv("BACKEND_URL") + "training/create"
        data = {"weight": weight,
                "name_training": name}
        async with session.post(url, data=json.dumps(data), headers=headers) as response:
            html = await response.text()
            print("Status:", response.status, "Body:", html)


async def write_exercise(name_training, name_exercise, value):
    async with aiohttp.ClientSession() as session:
        url = os.getenv("BACKEND_URL") + "training/write_exercise"
        data = {  "name_training": name_training,
              "name_exercise": name_exercise,
              "value": value}
        async with session.post(url, data=json.dumps(data), headers=headers) as response:
            html = await response.text()
            print("Status:", response.status, "Body:", html)


async def next_func(bot, message, state, uid):
    cur_menu_name = state.get_menu(uid)
    parent_menu_name = state.back_menu(uid)
    parent_menu = getattr(constructor, parent_menu_name)
    index = parent_menu.items.index(cur_menu_name) + 1
    if index < len(parent_menu.items):
        next_menu_name = parent_menu.items[index]
        state.push_menu(uid, next_menu_name)

        prev_value = ""

        if message.text != "Вес":
            print("sending", state.get_menu(uid, 2), state.get_menu(uid))
            val = await get_last_value(state.get_menu(uid, 2), state.get_menu(uid))
            prev_value += f" - {val}"

        await bot.send_message(message.from_user.id, next_menu_name + prev_value)
    else:
        parent_menu_name = state.back_menu(uid)
        parent_menu = getattr(constructor, parent_menu_name)
        await bot.send_message(message.from_user.id, parent_menu.title,
                               reply_markup=parent_menu.markup)


async def training_handler(bot, message, state):
    uid = message.from_user.id

    if message.text == "Грудь":
        state.push_menu(uid, constructor.train_breast_menu.name)
        await bot.send_message(message.from_user.id,
                               constructor.train_breast_menu.title,
                               reply_markup=constructor.train_breast_menu.markup)
    elif message.text == "Спина":
        state.push_menu(uid, constructor.train_beak_menu.name)
        await bot.send_message(message.from_user.id,
                               constructor.train_beak_menu.title,
                               reply_markup=constructor.train_beak_menu.markup)
    elif message.text == "Ноги":
        state.push_menu(uid, constructor.train_leg_menu.name)
        await bot.send_message(message.from_user.id,
                               constructor.train_leg_menu.title,
                               reply_markup=constructor.train_leg_menu.markup)
    elif message.text == "Дальше":
        await next_func(bot, message, state, uid)

    elif (message.text in data.train_breast_menu
          or message.text in data.train_breast_menu
          or message.text in data.train_breast_menu):
        state.push_menu(uid, message.text)
        prev_value = ""
        if message.text != "Вес":
            print("sending", state.get_menu(uid, 2), state.get_menu(uid))
            val = await get_last_value(state.get_menu(uid, 2), state.get_menu(uid))
            prev_value += f" - {val}"
        await bot.send_message(message.from_user.id,
                               message.text + prev_value,
                               reply_markup=constructor.train_exercise_menu.markup)
    else:
        if state.get_menu(uid) == "Вес":
            await start_training(state.get_menu(uid, 2), message.text)
        else:
            await write_exercise(state.get_menu(uid, 2), state.get_menu(uid), message.text)
        print(message.text, state.get_menu(uid))
        await next_func(bot, message, state, uid)
