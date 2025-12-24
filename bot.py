import telebot
from config import TOKEN
from database import init_db
from handlers.user import user_handlers
from handlers.admin_panel import admin_handlers

bot = telebot.TeleBot(TOKEN)

init_db()

user_handlers(bot)
admin_handlers(bot)

print("Bot is running...")
bot.infinity_polling()
