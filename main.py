
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram import F
from dotenv import load_dotenv
from service import *
from connection import *
import asyncio
import os

load_dotenv()
token = os.getenv("BOT_TOKEN")

bot = Bot(token=token)
dp = Dispatcher()


main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📦 Склад"), KeyboardButton(text="🆘 Помощь")],
        [KeyboardButton(text="⚠️ Заканчивается")],
    ],
    resize_keyboard=True,
)

@dp.message(CommandStart())
async def start_bot(message: Message):
    if await  get_user_by_id(message.from_user.id):
        await message.answer(f"👋Привет @{message.from_user.username} я бот для учёта товаров на складе.", reply_markup=main_kb)
    else:
        user = message.from_user
        await create_user(user.username, user.full_name, user.id)
        await message.answer(f"👋Привет @{message.from_user.username} я бот для учёта товаров на складе.", reply_markup=main_kb)
        

@dp.message(F.text == "🆘 Помощь")
@dp.message(Command("help"))
async def help(message: Message):
    await message.answer(
        """
        Я помогаю вести учёт товаров на складе.
        📦 /products - показать все товары
        🆘 /help - помощь
        ⚠️ /low_stock-показать товары,  которые меньше порога
        ➕ /add_product название/количество/порог
        📦 /sell продать id/количество
        📦 /restock добавить id/количество
        """
    )






async def main():
    await create_table()
    print("Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
