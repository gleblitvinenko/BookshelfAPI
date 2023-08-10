import os
from datetime import timedelta

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from django.conf import settings
from django.utils import timezone
from dotenv import load_dotenv

from borrowing.models import Borrowing

load_dotenv()

API_TOKEN = settings.API_TOKEN
CHAT_ID = settings.CHAT_ID

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


async def send_notifications_in_group(notification_message: str):
    await bot.send_message(chat_id=CHAT_ID, text=notification_message)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
