from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

API_TOKEN = "6671991384:AAHgJGgXG24YBQ146W1PWIYxIgRfo8FUeAE"
CHAT_ID = -931563366

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


async def send_notifications_in_group():
    await bot.send_message(chat_id=CHAT_ID, text="HELLO")


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    print(message)
    await message.reply("Привет, это тестовое уведомление от вашего бота!")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
