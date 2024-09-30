from app.keyboards.constructor import Menu
from app.keyboards import data


main_menu = Menu("main_menu", "Главное меню", data.main_menu, isNeedBack=False)
back_menu = Menu("back_menu", "Назад", data.back_menu, isNeedBack=False)

training_menu = Menu("training_menu", "Тренировка", data.train_menu)
train_breast_menu = Menu("train_breast_menu", "Грудь", data.train_breast_menu)
train_beak_menu = Menu("train_beak_menu", "Спина", data.train_beak_menu)
train_leg_menu = Menu("train_leg_menu", "Ноги", data.train_leg_menu)
train_exercise_menu = Menu("train_exercise_menu", "", data.train_exercise_menu)
