from telebot.asyncio_filters import SimpleCustomFilter

from app.states.menu import UserStateMenu

state = UserStateMenu()


class MainMenuFilter(SimpleCustomFilter):
    key = "main_menu"

    async def check(self, message):
        return state.get_menu(message.from_user.username) == "main_menu"


class TrainMenuFilter(SimpleCustomFilter):
    key = "train_menu"

    async def check(self, message):
        return state.check_category(message.from_user.username, "train_menu")
    

class FoodMenuFilter(SimpleCustomFilter):
    key = "food_menu"

    async def check(self, message):
        return state.check_category(message.from_user.username, "food_menu")
