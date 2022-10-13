from loader import dp, bot
from aiogram.dispatcher.filters import Command
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions, Message, CallbackQuery
from keyboards.inline import choice_buttons as inline
from keyboards.reply import choice_buttons as reply 
from data import db
import asyncio
import random
from aiogram.utils.exceptions import MessageTextIsEmpty
from utils import MainStates
from aiogram.dispatcher import FSMContext
from config import BASE_DIR
import json


@dp.message_handler(Command('start'))  # Начало начал
async def start_command(message):
    photo = open(BASE_DIR/"data/images/hello.jpg", "rb")
    await bot.send_photo(message.chat.id, photo, caption="""Hello, guys! 🖐 Let's determine the level of your emotional intelligence. 🎓
Our emotional intelligence quiz describes situations that we all experience in our lives (like being given difficult feedback).
Be as honest as possible when answering the questions as that will provide you with the most accurate assessment of your level of emotional intelligence.""", reply_markup=reply.menu())


@dp.message_handler()
async def text_msg(message):
    s = message.text
    if s == "Начать тест" or s == "Пройти тест заново":
        db.del_stat(message.chat.id)
        question = db.get_next_question(message.chat.id)
        answers = db.get_answers()
        if question['id'] == 1:
            #db.delete_last(message.chat.id)
            await message.answer(question["text"], reply_markup=reply.answer_btns(answers, False))
        else:
            await message.answer(question["text"], reply_markup=reply.answer_btns(answers))
        with open(BASE_DIR/'tmp.json', 'w') as f:
            json.dump({str(message.chat.id): question["id"]}, f)
        await MainStates.MAIN_STATE.set()


@dp.message_handler(state=MainStates.MAIN_STATE)
async def spare_parts_state(message: Message, state: FSMContext):
    with open(BASE_DIR/'tmp.json') as f:
        data = json.load(f)
    question_id = data[str(message.chat.id)]
    if message.text == "Back":
        db.delete_last(message.chat.id)
        question = db.get_next_question(message.chat.id)
        answers = db.get_answers()
        if question['id'] == 1:
            await message.answer(question["text"], reply_markup=reply.answer_btns(answers, False))
        else:
            await message.answer(question["text"], reply_markup=reply.answer_btns(answers))
        with open(BASE_DIR/'tmp.json', 'w') as f:
            json.dump({str(message.chat.id): question["id"]}, f)
        return
    answer_id = db.get_answer_id(message.text)
    db.add_statistics(message.chat.id, answer_id, question_id)
    question = db.get_next_question(message.chat.id)
    if question is None:
        result = db.get_result(message.chat.id)
        if result >= 8:
            text = """Congratulations! You have high emotional intelligence. This is good news! EQ counts for twice as much as IQ and technical skills combined in determining who will be a star performer. Your level of EQ likely has been and will be a driver of your high performance under pressure for years to come.\nAreas to work on: While you are doing well, don’t forget to take time out of your busy day-to-day activities to stop and reflect on what brings you the greatest meaning in your life. If we fail to do this on a regular basis, we risk becoming tranquilized by the trivial; sedated by the small details. Yes, deadlines need to be met and goals achieved. But if we are working toward goals that are not in alignment with our key values and greater purpose, we face becoming frustrated and cynical when we face pressure – losing sight of the reason we are doing ‘all of this’ in the first place!"""
            path = BASE_DIR/"data/images/first.jpg"
        elif result >= 5:
            text = """You have slightly above average EQ – with room to grow! You are likely sensitive to the emotional climate of the people around you when you and they – peers, friends, family and key clients – are under pressure. You are aware of the effect your behavior has on others. While you may be adept at tuning into others and their needs – you must remember your own. Don’t be afraid to honestly communicate these difficult needs and feelings. This is one of the most important aspects of Emotional Intelligence: being able to skillfully air your grievances."""
            path = BASE_DIR/"data/images/second.jpg"
        else:
            text = """Emotional intelligence can be learned and improved – with big payoffs! Studies of entrepreneurs, leaders and employees at some of the world’s top organizations, show that EQ counts for twice as much as IQ and technical skills combined in defining who will be a star. Improving EQ will result in better relationships, greater health and a happier outlook on life.\nSelf-awareness is the foundation of EQ. Here some things to consider: What situations generally create pressure and stress for you? How are you handling these situations? What negative thoughts play over and over in your mind on a regular basis? Are these a true picture of reality? Are you afraid to share your needs and feelings with others? Are you taking care of everyone else – being a martyr – or acting ‘the strong, silent type’? If we have trouble expressing our emotional needs – if we regularly put others’ needs before our own – that can lead to feeling empty, frustrated, or depressed."""
            path = BASE_DIR/"data/images/third.jpg"
        photo = open(path, "rb")
        await bot.send_photo(message.chat.id, photo, caption=text)
        await state.finish()
        await message.answer("Желаете пройти тест заново?", reply_markup=reply.repeat())
    else:
        answers = db.get_answers()
        await message.answer(question["text"], reply_markup=reply.answer_btns(answers))
        with open(BASE_DIR/'tmp.json', 'w') as f:
            json.dump({str(message.chat.id): question["id"]}, f)


@dp.callback_query_handler(lambda call: "answer" in call.data and "question_id" in call.data)
async def dislike(call: CallbackQuery):
    _, answer_id, _, question_id = map(str, call.data.split("|"))
    db.add_statistics(call.message.chat.id, answer_id, question_id)
    question = db.get_next_question(call.message.chat.id)
    answers = db.get_answers()
    await call.message.answer(question["text"], reply_markup=inline.answer_btns(question["id"], answers))
    await bot.delete_message(call.message.chat.id, call.message.message_id)