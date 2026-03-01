import os
from telebot import TeleBot, types

TOKEN = os.environ.get("TOKEN")
CHANNEL_USERNAME = "@BODACHETO"

bot = TeleBot(TOKEN)

def check_subscription(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

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

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    if not check_subscription(user_id):
        send_subscription_message(message.chat.id)
        return

    bot.send_message(
        message.chat.id,
        "مرحباً بك 👑\n\n✍️ ابعت أي كود وهخليه جاهز للنسخ."
    )

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def verify_subscription(call):
    user_id = call.from_user.id

    if check_subscription(user_id):
        bot.answer_callback_query(call.id, "تم التحقق بنجاح ✅")
        bot.send_message(
            call.message.chat.id,
            "مرحباً بك 👑\n\n✍️ ابعت أي كود وهخليه جاهز للنسخ."
        )
    else:
        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            "عذراً لم يتم الإشتراك في القناه\nمن فضلك إشترك في القناه لإستخدام البوت"
        )

# 👇 ده الجزء اللي كان ناقص
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if not check_subscription(message.from_user.id):
        return

    code = message.text.replace("`", "")
    bot.send_message(
        message.chat.id,
        f"اضغط على الكود لنسخه 👇\n\n`{code}`",
        parse_mode="Markdown"
    )

bot.infinity_polling()
