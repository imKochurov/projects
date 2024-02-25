from aiogram import Bot, Dispatcher, F, types
from aiogram.filters.command import Command
import asyncio
import logging
from random import choice
from telegram_bot.configs import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher()


# Хендлер, що реагує на команду /info
@dp.message(Command('info'))
async def cmd_info(message: types.Message):
    await message.answer('Привіт! Це тестовий бот для виконання домашки №39.')


# Хендлер, що реагує на команду /start та кнопку "Розпочати" при першому відкритті боту. Надсилає відповідь з Reply-кнопками
@dp.message(Command('start')) 
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text='🔴 Червона пігулка'),
         types.KeyboardButton(text='🔵 Синя пігулка')]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer('Нео, обери червону або синю пігулку', reply_markup=keyboard)


# Два хендлери, що реагують на натисканя кнопок за допомогою фільтра текстових повідомлень, бо натискання Reply-кнопки сприймається як текстове введення.
@dp.message(F.text == '🔴 Червона пігулка') 
async def but1(message: types.Message):
    await message.reply('Ти дізнаєшся всю правду про Матрицю!', reply_markup=types.ReplyKeyboardRemove())

@dp.message(F.text == '🔵 Синя пігулка')
async def but1(message: types.Message):
    await message.reply('Ти лишишся в Матриці назавжди!', reply_markup=types.ReplyKeyboardRemove())




# Міні-гра "Вгадай, в якій руці" з використанням Inline-кнопок
@dp.message(Command('play'))
async def cmd_info(message: types.Message):

    answer = ['1', '2']
    data1 = choice(answer)
    answer.remove(data1)
    data2 = answer[0]

    kb = [
        [types.InlineKeyboardButton(text='🤛🏼 Ліва рука', callback_data=data1),
         types.InlineKeyboardButton(text='🤜🏼 Права рука', callback_data=data2)]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer('Вгадай, в якій руці монетка?', reply_markup=keyboard)

@dp.callback_query(F.data == '1')
async def game_win(callback: types.CallbackQuery):
    await callback.message.answer('🥳 Перемога! Ви знайшли монетку!')
    await callback.answer()

@dp.callback_query(F.data == '2')
async def game_loose(callback: types.CallbackQuery):
    await callback.message.answer('😒 Невдача... Монетка в іншій руці...')
    await callback.answer()





async def main():
    logging.basicConfig(level=logging.INFO) # логування для виведення подій в термінал
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())