import os
from telebot import TeleBot, types

TOKEN = os.environ.get("TOKEN")
CHANNEL_USERNAME = "@BODACHETO"  # غيره لو غيرت يوزر القناة

bot = TeleBot(TOKEN)

# 🔹 فحص الاشتراك
def check_subscription(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# 🔹 رسالة الاشتراك
def send_subscription_message(chat_id):
    markup = types.InlineKeyboardMarkup()

    join_btn = types.InlineKeyboardButton(
        "إشتراك",
        url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}"
    )

    check_btn = types.InlineKeyboardButton(
        "تحقق من إشتراكي",
        callback_data="check_sub"
    )

    markup.add(join_btn)
    markup.add(check_btn)

    bot.send_message(
        chat_id,
        "من فضلك إشترك في القناه لإستخدام البوت",
        reply_markup=markup
    )

# 🔹 أمر start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    if not check_subscription(user_id):
        send_subscription_message(message.chat.id)
        return

    bot.send_message(message.chat.id, "مرحباً بك 👑 يمكنك الآن استخدام البوت.")

# 🔹 زرار تحقق
@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def verify_subscription(call):
    user_id = call.from_user.id

    if check_subscription(user_id):
        bot.answer_callback_query(call.id, "تم التحقق بنجاح ✅")
        bot.send_message(call.message.chat.id, "مرحباً بك 👑 يمكنك الآن استخدام البوت.")
    else:
        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            "عذراً لم يتم الإشتراك في القناه\nمن فضلك إشترك في القناه لإستخدام البوت"
        )

bot.infinity_polling()
