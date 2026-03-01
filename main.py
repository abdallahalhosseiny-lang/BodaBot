import os
import random
from telebot import TeleBot, types

TOKEN = os.environ.get("TOKEN")
CHANNEL_USERNAME = "@BODACHETO"

bot = TeleBot(TOKEN)

participants = {}
available_numbers = list(range(1, 1001))

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

@bot.message_handler(commands=['start'])
def start(message):
    if not check_subscription(message.from_user.id):
        send_subscription_message(message.chat.id)
        return

    bot.send_message(
        message.chat.id,
        "🔥 سحب على 660 شدة ببجي 🔥\n\n"
        "للدخول اكتب:\n"
        "/Entering_the_draw\n\n"
        "لعرض المشاركين اكتب:\n"
        "/participants"
    )

# 🔹 تحقق الاشتراك
@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def verify_subscription(call):
    if check_subscription(call.from_user.id):
        bot.answer_callback_query(call.id, "تم التحقق بنجاح ✅")
        bot.send_message(
            call.message.chat.id,
            "🔥 يمكنك الآن الدخول في السحب\n\n"
            "/Entering_the_draw"
        )
    else:
        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            "عذراً لم يتم الإشتراك في القناه\n"
            "من فضلك إشترك في القناه لإستخدام البوت"
        )

# 🔹 دخول السحب
@bot.message_handler(commands=['Entering_the_draw'])
def enter_draw(message):
    if not check_subscription(message.from_user.id):
        return

    bot.send_message(
        message.chat.id,
        "برجاء إدخال الإسم الذي تريد دخول السحب به 👇"
    )

    bot.register_next_step_handler(message, save_name)

def save_name(message):
    user_id = message.from_user.id

    if user_id in participants:
        bot.send_message(message.chat.id, "❌ لقد دخلت السحب بالفعل.")
        return

    if not available_numbers:
        bot.send_message(message.chat.id, "❌ انتهت أرقام السحب.")
        return

    number = random.choice(available_numbers)
    available_numbers.remove(number)

    participants[user_id] = {
        "name": message.text,
        "number": number
    }

    bot.send_message(
        message.chat.id,
        f"✅ تم دخول السحب بإسم: {message.text}\n"
        f"🎟 رقمك في السحب: {number}"
    )

# 🔹 عرض عدد المشاركين + قائمة الأسماء
@bot.message_handler(commands=['participants'])
def show_participants(message):

    if not participants:
        bot.send_message(message.chat.id, "❌ لا يوجد مشاركين حالياً.")
        return

    count = len(participants)

    text = f"📊 عدد المشتركين في السحب: {count}\n\n"
    text += "📋 قائمة المشاركين:\n\n"

    for data in participants.values():
        text += f"👤 {data['name']} - 🎟 {data['number']}\n"

    bot.send_message(message.chat.id, text)

bot.infinity_polling()
