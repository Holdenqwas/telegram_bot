from telebot.asyncio_filters import SimpleCustomFilter

from app.states.menu import UserStateMenu

state = UserStateMenu()


class MainMenuFilter(SimpleCustomFilter):
    key = "main_menu"

    async def check(self, message):
        return state.get_menu(message.from_user.id) == "main_menu"


class TrainMenuFilter(SimpleCustomFilter):
    key = "train_menu"

    async def check(self, message):
        return state.check_category(message.from_user.id, "train_menu")
    

class ShopMenuFilter(SimpleCustomFilter):
    key = "shop_menu"

    async def check(self, message):
        return state.check_category(message.from_user.id, "shop_menu")
