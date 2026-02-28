import os
from telebot import TeleBot, types

TOKEN = os.environ.get("TOKEN")

bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Copy Text", callback_data="copy")
    markup.add(button)
    bot.send_message(
        message.chat.id,
        "اضغط الزرار للنسخ",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "copy")
def copy_text(call):
    bot.answer_callback_query(call.id, "تم النسخ ✅")
    bot.send_message(call.message.chat.id, "النص الجاهز للنسخ هنا 📋")

bot.infinity_polling()
