import os
from telebot import TeleBot, types

TOKEN = os.environ.get("TOKEN")

bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("انسخ الكلمة", callback_data="copy_word")
    markup.add(button)
    bot.send_message(message.chat.id, "اضغط الزرار لنسخ الكلمة 👇", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "copy_word")
def copy_word(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "`اكتب_هنا_الكلمة_بتاعتك`", parse_mode="Markdown")

bot.infinity_polling()
