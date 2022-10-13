from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def menu():
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
	keyboard.row(KeyboardButton('Начать тест'))
	return keyboard


def answer_btns(answers, back=True):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = KeyboardButton(answers[1])
    btn2 = KeyboardButton(answers[2])
    keyboard.row(btn1, btn2)
    btn = KeyboardButton(answers[3])
    keyboard.row(btn)
    btn1 = KeyboardButton(answers[4])
    btn2 = KeyboardButton(answers[5])
    keyboard.row(btn1, btn2)
    if back:
        btn = KeyboardButton("Back")
        keyboard.row(btn)
    return keyboard


def repeat():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row(KeyboardButton('Пройти тест заново'))
    return keyboard