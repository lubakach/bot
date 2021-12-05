from random import randint
import sqlite3
from aiogram.types import update

import config
import logging
import asyncio
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

from aiogram import Bot, Dispatcher, executor, types
from sqlighter import SQLighter

# задаем уровень логов
logging.basicConfig(level=logging.INFO)

# инициализируем бота
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

# инициализируем соединение с БД
db = SQLighter('db.db')

button_hi = KeyboardButton('Адрес 🗺')
button_num = KeyboardButton('Контакты 📞')
button_site = KeyboardButton('Сайт 🏪')
button_info = KeyboardButton('Инфо')
greet_kb = ReplyKeyboardMarkup()
greet_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_hi, button_num, button_site, button_info)

# Команда активации подписки
#@dp.message_handler(commands=['subscribe'])
@dp.callback_query_handler(text="subscribe")
async def subscribe(message: types.Message):
    
    if (not db.subscriber_exists(message.from_user.id)):
        # если юзера нет в базе, добавляем его
        db.add_subscriber(message.from_user.id)
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.id, True)

    await message.answer(
        "Вы успешно подписались на рассылку!\nЖдите, скоро выйдут новые обзоры и вы узнаете о них первыми =)")

@dp.message_handler(lambda message: message.text == "Адрес 🗺")
async def with_puree(message: types.Message):
    await message.reply('Адрес: \nКитай, Гималаи, хребет Махалангур-Химал, вершина Эверест, д. 1\nhttps://yandex.ru/maps/org/1179483603')

@dp.message_handler(lambda message: message.text == "Контакты 📞")
async def with_puree(message: types.Message):
    await message.reply('Телефон: +375 (44) 559-00-01')

@dp.message_handler(lambda message: message.text == "Сайт 🏪")
async def with_puree(message: types.Message):
    await message.reply('Сайт:\nhttps://yandex.ru/maps/org/1179483603')

@dp.message_handler(lambda message: message.text == "Инфо")
async def with_puree(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Подписаться на рассылку", callback_data="subscribe"))
    keyboard.add(types.InlineKeyboardButton(text="Отписаться от рассылки", callback_data="unsubscribe"))
    await message.answer("Узнавай про все самые свежие новости и акции первым!", reply_markup=keyboard)

@dp.callback_query_handler(text="random_value")
async def send_random_value(call: types.CallbackQuery):
    await call.message.answer(str(randint(1, 10)))


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет! Я информационный бот компании - Будь здоров!\nДля получения информации можете воспользоваться подсказками ниже!", reply_markup=greet_kb)

# Команда отписки
#@dp.message_handler(commands=['unsubscribe'])
@dp.callback_query_handler(text="unsubscribe")
async def unsubscribe(message: types.Message):
    if (not db.subscriber_exists(message.from_user.id)):
        # если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
        db.add_subscriber(message.from_user.id, False)
        await message.answer("Вы итак не подписаны.")
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.id, False)
        await message.answer("Вы успешно отписаны от рассылки.")



# тест таймер
async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        sqlite_connection = sqlite3.connect('db.db')
        cursor = sqlite_connection.cursor()

        sqlite_select_query = """SELECT * from news"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        str1 = ''.join(records)
        #message = records[1] + records[2] + records[4]

        await bot.send_message(251834774, "ti debil", disable_notification = True)

# Запуск
if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    task1 = loop.create_task(scheduled(10))
    executor.start_polling(dp, skip_updates= True)
