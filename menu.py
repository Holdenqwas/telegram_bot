from typing import List

from telebot import types

import data


class Menu:
    def __init__(self, name: str, title: str, items: List[str],
                 isNeedBack: bool = True, width: int = 3):
        self.name = name
        self.title = title
        self.items = items
        self.isNeedBack = isNeedBack
        self.width = width
        self.markup = self._get_markup()

    def __repr__(self) -> str:
        return self.name

    def _get_markup(self):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                           row_width=self.width)
        for item in self.items:
            btn = types.KeyboardButton(item)
            markup.add(btn)

        if self.isNeedBack:
            btn = types.KeyboardButton("Назад")
            markup.add(btn)

        return markup


main_menu = Menu("main_menu", "Главное меню", data.main_menu, isNeedBack=False)
back_menu = Menu("back_menu", "Назад", data.back_menu, isNeedBack=False)

training_menu = Menu("training_menu", "Тренировка", data.train_menu)
train_breast_menu = Menu("train_breast_menu", "Грудь", data.train_breast_menu)
train_beak_menu = Menu("train_beak_menu", "Спина", data.train_beak_menu)
train_leg_menu = Menu("train_leg_menu", "Ноги", data.train_leg_menu)
train_exercise_menu = Menu("train_exercise_menu", "", data.train_exercise_menu)
