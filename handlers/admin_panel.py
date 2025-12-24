from config import ADMINS
from database import get_connection

def admin_handlers(bot):

    @bot.message_handler(commands=['admin'])
    def admin_panel(message):
        if message.from_user.id not in ADMINS:
            return

        bot.send_message(
            message.chat.id,
            "لوحة تحكم الأدمن 🔐\n"
            "/users - عرض المستخدمين\n"
            "/search ID - البحث عن مستخدم\n"
        )
