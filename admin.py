from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from config import ADMIN_ID
from database import users_count, get_users


admin_router = Router()


# Кнопка админ панели

@admin_router.message(F.text == "⚙️ Админ панель")
async def open_admin(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "⚙️ Админ панель:\n\n"
        "📊 Статистика\n"
        "📢 Рассылка\n"
    )


# Статистика

@admin_router.callback_query(F.data == "stats")
async def stats(callback: CallbackQuery):

    if callback.from_user.id != ADMIN_ID:
        return

    count = users_count()

    await callback.message.answer(
        f"📊 Статистика:\n\n"
        f"👥 Всего пользователей: {count}"
    )

    await callback.answer()


# Рассылка

@admin_router.callback_query(F.data == "sendall")
async def send_all(callback: CallbackQuery):

    if callback.from_user.id != ADMIN_ID:
        return

    await callback.message.answer(
        "📢 Отправь текст рассылки следующим сообщением."
    )

    await callback.answer()
