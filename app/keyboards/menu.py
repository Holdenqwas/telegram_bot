from app.keyboards.constructor import Menu
from app.keyboards import data


main_menu = Menu("main_menu", "Главное меню", data.main_menu, isNeedBack=False)
back_menu = Menu("back_menu", "Назад", data.back_menu, isNeedBack=False)

train_menu = Menu("train_menu", "Тренировка", data.train_menu)
setup_train_menu = Menu(
    "setup_train_menu", "Настройка тренировок", data.setup_train_menu
)

shop_menu = Menu("shop_menu", "Списки покупок", data.shop_menu)
