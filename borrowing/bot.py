import os
from datetime import timedelta

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from django.utils import timezone
from dotenv import load_dotenv

from borrowing.models import Borrowing

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


async def send_notifications_in_group(notification_message: str):
    await bot.send_message(chat_id=CHAT_ID, text=notification_message)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
