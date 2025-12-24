from telebot import types
from config import ADMINS
from database import get_connection

def admin_handlers(bot):

    @bot.message_handler(commands=['admin'])
    def admin_panel(message):
        if message.from_user.id not in ADMINS:
            return

        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add("🔍 بحث عن مستخدم")
        kb.add("📋 كل المستخدمين")
        kb.add("❌ إغلاق")

        bot.send_message(
            message.chat.id,
            "🔐 لوحة تحكم الأدمن",
            reply_markup=kb
        )

    @bot.message_handler(func=lambda m: m.text == "🔍 بحث عن مستخدم")
    def search_user(message):
        if message.from_user.id not in ADMINS:
            return

        msg = bot.send_message(
            message.chat.id,
            "أرسل Telegram ID أو اسم الحساب:"
        )
        bot.register_next_step_handler(msg, process_search)

    def process_search(message):
        conn = get_connection()
        cur = conn.cursor()

        query = message.text.strip()

        if query.isdigit():
            cur.execute("SELECT * FROM users WHERE telegram_id = ?", (int(query),))
        else:
            cur.execute("SELECT * FROM users WHERE account_name = ?", (query,))

        user = cur.fetchone()
        conn.close()

        if not user:
            bot.send_message(message.chat.id, "❌ المستخدم غير موجود")
            return

        text = (
            f"👤 المستخدم:\n"
            f"ID: {user[0]}\n"
            f"Username: @{user[1]}\n"
            f"Account: {user[2]}\n"
            f"Balance: {user[3]}\n"
            f"Status: {user[4]}"
        )

        bot.send_message(message.chat.id, text)
