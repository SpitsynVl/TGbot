#Модуль для работы с клавиатурами

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import pickle
from random import randint, shuffle

start_kb_buttons = ['📚Цитаты по теме', '🎲Викторина']
start_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(*start_kb_buttons)

clear_kb = ReplyKeyboardRemove()

cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True).add('🔙 Назад')

quizzes = ['Угадай автора по цитате']
choose_quiz_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(*quizzes)
choose_quiz_kb.add('🔙 Назад')

def guess_author_kb(correct_author, quiz_id):
    with open('data_model/authors_for_quiz_1.pickle', 'rb') as f:
        names = list(pickle.load(f))
        names.remove(correct_author)
    
    wrong_authors = set()
    while len(wrong_authors) < 3:
        wrong_authors.add(names[randint(0, len(names) - 1)])
    authors_and_answers = [(correct_author, 'correct')] +\
                         [(wrong_author, 'wrong') for wrong_author in wrong_authors]
    shuffle(authors_and_answers)

    authors_bttns = (InlineKeyboardButton(author, callback_data=answer+' '+str(quiz_id)) for
                    author, answer in authors_and_answers)
    authors_kb = InlineKeyboardMarkup(row_width=3)
    for button in authors_bttns:
        authors_kb.add(button)
    return authors_kb