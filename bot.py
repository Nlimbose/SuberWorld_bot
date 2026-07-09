import asyncio

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

import os

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
from database import add_user, users_count, get_users


# =========================
# КНОПКИ
# =========================

def main_buttons():

    keyboard = [
        [
            InlineKeyboardButton(
                "📢 Telegram",
                url="https://t.me/SuberWorld"
            )
        ],
        [
            InlineKeyboardButton(
                "💬 Discord",
                url="https://discord.gg/H8wjyqMYk"
            )
        ],
        [
            InlineKeyboardButton(
                "💎 Покупка доната",
                url="https://discord.gg/95y7Pzp6G"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


def admin_button():

    keyboard = [
        [
            KeyboardButton("⚙️ Админ панель")
        ]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


def admin_menu():

    keyboard = [
        [
            InlineKeyboardButton(
                "📊 Статистика",
                callback_data="stats"
            )
        ],
        [
            InlineKeyboardButton(
                "📢 Рассылка",
                callback_data="sendall"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

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


    await update.message.reply_text(
        text,
        reply_markup=main_buttons()
    )


    if user.id == ADMIN_ID:

        await update.message.reply_text(
            "⚙️ Админ доступ включён",
            reply_markup=admin_button()
        )


# =========================
# АДМИНКА
# =========================

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return


    await update.message.reply_text(
        "⚙️ Админ панель:",
        reply_markup=admin_menu()
    )


# =========================
# CALLBACK
# =========================

async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    if query.from_user.id != ADMIN_ID:
        return


    if query.data == "stats":

        await query.message.reply_text(
            f"📊 Статистика:\n\n"
            f"👥 Пользователей: {users_count()}"
        )


    elif query.data == "sendall":

        context.user_data["mailing"] = True

        await query.message.reply_text(
            "📢 Отправь текст рассылки:"
        )


    await query.answer()



# =========================
# РАССЫЛКА
# =========================

async def messages(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return


    if context.user_data.get("mailing"):

        users = get_users()

        sent = 0

        for user in users:

            try:

                await context.bot.send_message(
                    user[0],
                    update.message.text
                )

                sent += 1

            except:
                pass


        context.user_data["mailing"] = False


        await update.message.reply_text(
            f"✅ Отправлено: {sent}"
        )


# =========================
# ЗАПУСК
# =========================

def main():

    app = Application.builder().token(TOKEN).build()


    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    app.add_handler(
        MessageHandler(
            filters.Regex("⚙️ Админ панель"),
            admin_panel
        )
    )


    app.add_handler(
        CallbackQueryHandler(callback)
    )


    app.add_handler(
        MessageHandler(
            filters.TEXT,
            messages
        )
    )


    print("🌍 SuberWorld_bot запущен!")

    app.run_polling()


if __name__ == "__main__":
    main()
