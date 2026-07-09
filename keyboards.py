from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from config import CHANNEL_URL, DISCORD_URL, DONATE_URL


# Кнопки для пользователей

main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📢 Telegram",
                url=CHANNEL_URL
            )
        ],
        [
            InlineKeyboardButton(
                text="💬 Discord",
                url=DISCORD_URL
            )
        ],
        [
            InlineKeyboardButton(
                text="💎 Покупка доната",
                url=DONATE_URL
            )
        ]
    ]
)


# Кнопка администратора

admin_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="⚙️ Админ панель"
            )
        ]
    ],
    resize_keyboard=True
)


# Меню админ панели

admin_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📊 Статистика",
                callback_data="stats"
            )
        ],
        [
            InlineKeyboardButton(
                text="📢 Рассылка",
                callback_data="sendall"
            )
        ]
    ]
)
