from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import keyboards as kb
import messages as msgs
import calls_to_data as data
from CLI import Quote


bot = Bot(token='5159766100:AAGcbFAXDIuYzaiJVFfDgmoYYV9orNYUdj8')
dp = Dispatcher(bot, storage=MemoryStorage())
quote = Quote('data_model/big_data.csv', 'data_model/pure_q_35k.csv', 
              'data_model/d2v_35k_exp.model')
quote.Q_NUMBER = 5

logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await message.reply(msgs.start_message, reply_markup=kb.start_kb)


@dp.message_handler(commands=['help'])
async def command_help(message: types.Message):
    await message.reply(msgs.help_message)



@dp.message_handler(state='*', regexp='🔙 Назад')
async def cancel(message: types.Message):
    await dp.current_state(user=message.from_user.id).reset_state()
    await bot.send_message(message.from_user.id, msgs.cancel_message,
                           reply_markup=kb.start_kb)


@dp.message_handler(commands=['quotes_by_topic'])
@dp.message_handler(regexp='📚Цитаты по теме')
async def get_topic(message: types.Message):
    await dp.current_state(user=message.from_user.id).set_state('get_topic')
    await bot.send_message(message.from_user.id, msgs.choose_topic_message,
                           reply_markup=kb.cancel_kb)


@dp.message_handler(state='get_topic')
async def send_quotes_by_topic(message: types.Message):
    quote.preprocess_text(message.text)
    quotes_and_authors_list = quote.basic_model()
    final_message = '\n\n📝'.join(quote_ + '\n' + '© ' + author 
                                   for quote_, author in quotes_and_authors_list)
    await bot.send_message(message.from_user.id, '📝' + final_message,
                           reply_markup=kb.cancel_kb)
    await bot.send_message(message.from_user.id, 'Какая ещё тема тебя интересует? 👇',
                           reply_markup=kb.cancel_kb)


@dp.message_handler(commands=['quiz'])
@dp.message_handler(regexp='🎲Викторина')
async def start_quiz(message: types.Message):
    await dp.current_state(user=message.from_user.id).set_state('quiz')
    await bot.send_message(message.from_user.id, msgs.start_quiz, 
                           reply_markup=kb.cancel_kb)
    quiz_quote, correct_author = data.take_random_quote()
    await bot.send_message(message.from_user.id, msgs.who_is_author + '📝' + quiz_quote, 
                           reply_markup=kb.guess_author_kb(correct_author))


@dp.callback_query_handler(text='correct', state='quiz')
@dp.callback_query_handler(text='wrong', state='quiz')
async def check_quiz_answer(query: types.CallbackQuery):
    answer = query.data
    if answer == 'correct':
        is_correct = '✅ Верно!\n\n'
    else:
        is_correct = '❌ Неправильно\n\n'

    quiz_quote, correct_author = data.take_random_quote()

    await bot.send_message(query.from_user.id, is_correct + msgs.who_is_author + '📝' +\
                        quiz_quote, reply_markup=kb.guess_author_kb(correct_author))


@dp.callback_query_handler(state='*')
async def incorrect_inline_behaviour(query: types.CallbackQuery):
    await bot.answer_callback_query(query.id, text='Ты уже вышел из Викторины',
                                    show_alert=True)


if __name__ == '__main__':
    executor.start_polling(dp)