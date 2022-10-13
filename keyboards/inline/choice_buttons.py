from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def example_btns(url):
    keyboard = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('Example url', url=url)
    btn2 = InlineKeyboardButton('Example button', callback_data=f"example")
    keyboard.row(btn1)
    keyboard.row(btn2)
    return keyboard


def answer_btns(question_id, answers):
    keyboard = InlineKeyboardMarkup()
    for id, name in answers.items():
        btn = InlineKeyboardButton(name, callback_data=f"answer|{id}|question_id|{question_id}")
        keyboard.row(btn)
    return keyboard


def repeat(user_id):
    keyboard = InlineKeyboardMarkup()
    btn = InlineKeyboardButton('Перепройти', callback_data=f"user_id|{user_id}")
    keyboard.row(btn)
    return keyboard