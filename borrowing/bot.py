import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


async def send_notifications_in_group(notification_message: str):
    await bot.send_message(chat_id=CHAT_ID, text=notification_message)


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply("Hi, it is start message!")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
