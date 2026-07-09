import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from config import TOKEN, ADMIN_ID
from database import add_user, users_count, get_users
from keyboards import main_menu, admin_menu, admin_button


bot = Bot(token=TOKEN)
dp = Dispatcher()


# =====================
# START
# =====================

@dp.message(CommandStart())
async def start(message: Message):

    user = message.from_user

    username = f"@{user.username}" if user.username else "без username"

    add_user(
        user.id,
        user.username,
        user.first_name
    )

    text = (
        f"🌍 Приветствуем тебя, {user.first_name} {username}!\n\n"
        "Добро пожаловать в SuberWorld!\n\n"
        "Выбери наши сообщества ниже 👇"
    )

    await message.answer(
        text,
        reply_markup=main_menu
    )


    if user.id == ADMIN_ID:
        await message.answer(
            "⚙️ Админ панель доступна:",
            reply_markup=admin_button
        )


# =====================
# АДМИН ПАНЕЛЬ
# =====================

@dp.message(lambda m: m.text == "⚙️ Админ панель")
async def admin_panel(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "⚙️ Админ панель:",
        reply_markup=admin_menu
    )


# =====================
# СТАТИСТИКА
# =====================

@dp.callback_query(lambda c: c.data == "stats")
async def stats(callback: CallbackQuery):

    if callback.from_user.id != ADMIN_ID:
        return

    count = users_count()

    await callback.message.answer(
        f"📊 Статистика:\n\n"
        f"👥 Всего пользователей: {count}"
    )

    await callback.answer()


# =====================
# РАССЫЛКА
# =====================

@dp.callback_query(lambda c: c.data == "sendall")
async def send_all(callback: CallbackQuery):

    if callback.from_user.id != ADMIN_ID:
        return

    await callback.message.answer(
        "📢 Напиши сообщение для рассылки:"
    )

    await callback.answer()


@dp.message()
async def mailing(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    if message.text == "⚙️ Админ панель":
        return

    users = get_users()

    sent = 0

    for user in users:
        try:
            await bot.send_message(
                user[0],
                message.text
            )
            sent += 1

        except:
            pass


    await message.answer(
        f"✅ Рассылка завершена\n"
        f"Отправлено: {sent}"
    )


# =====================
# ЗАПУСК
# =====================

async def main():

    print("🌍 SuberWorld_bot запущен!")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
