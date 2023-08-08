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


async def send_overdue_and_upcoming_notifications():
    overdue_borrowings = Borrowing.objects.filter(
        actual_return_date__isnull=True, expected_return_date__lt=timezone.now()
    )
    upcoming_borrowings = Borrowing.objects.filter(
        actual_return_date__isnull=True,
        expected_return_date=timezone.now() + timedelta(days=1),
    )

    daily_message = "Daily borrowings overview\n"
    if overdue_borrowings or upcoming_borrowings:
        daily_message += "Overdue borrowings list\n"
        for borrowing in overdue_borrowings:
            daily_message += (
                f"📕 Book: {borrowing.book.title}, 🤠 User: {borrowing.borrower.email}\n"
            )

        daily_message += "Upcoming borrowings list\n"
        for borrowing in upcoming_borrowings:
            daily_message += (
                f"📕 Book: {borrowing.book.title}, 🤠 User: {borrowing.borrower.email}\n"
            )
    else:
        daily_message += "No overdue and upcoming borrowings"

    await bot.send_message(chat_id=CHAT_ID, text=daily_message)


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply("Hi, it is start message!")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
