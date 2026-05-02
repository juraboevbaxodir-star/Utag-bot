from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import asyncio
import os

API_TOKEN = os.getenv("TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

users = set()
running = False
delay = 1.0

@dp.message_handler()
async def save_user(message: types.Message):
    users.add(message.from_user.id)

async def is_admin(chat_id, user_id):
    member = await bot.get_chat_member(chat_id, user_id)
    return member.status in ["administrator", "creator"]

@dp.message_handler(commands=['speed'])
async def set_speed(message: types.Message):
    global delay
    if not await is_admin(message.chat.id, message.from_user.id):
        return

    try:
        delay = float(message.get_args())
        if delay < 0.1:
            delay = 0.1
    except:
        pass

@dp.message_handler(commands=['utag'])
async def utag(message: types.Message):
    global running

    if not await is_admin(message.chat.id, message.from_user.id):
        return

    running = True

    for user in list(users):
        if not running:
            break

        await message.answer(f"<a href='tg://user?id={user}'>user</a>", parse_mode="HTML")
        await asyncio.sleep(delay)

@dp.message_handler(commands=['stoputag'])
async def stop_utag(message: types.Message):
    global running

    if not await is_admin(message.chat.id, message.from_user.id):
        return

    running = False


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
