import os
from telebot import TeleBot, types

TOKEN = os.environ.get("TOKEN")

bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("عرض الكود", callback_data="copy_code")
    markup.add(button)

    bot.send_message(
        message.chat.id,
        "🔥 دلوقتي نزل كود خصم عالمي\n\nاضغط على الكود لنسخه👇",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "copy_code")
def copy_code(call):
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        "`Gq192nzhee8j`",
        parse_mode="Markdown"
    )

bot.infinity_polling()
