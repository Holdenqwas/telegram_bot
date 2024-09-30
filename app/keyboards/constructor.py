from typing import List
from telebot import types


class Menu:
    def __init__(
        self,
        name: str,
        title: str,
        items: List[str],
        isNeedBack: bool = True,
        width: int = 3,
    ):
        self.isNeedBack = isNeedBack
        self.items = items
        self.name = name
        self.title = title
        self.width = width
        self.markup = self._get_markup()

    def __repr__(self) -> str:
        return self.name

    def _get_markup(self):
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, row_width=self.width
        )
        for item in self.items:
            btn = types.KeyboardButton(item)
            markup.add(btn)

        if self.isNeedBack:
            btn = types.KeyboardButton("Назад")
            markup.add(btn)

        return markup
