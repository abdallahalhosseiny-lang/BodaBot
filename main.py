import os
from telebot import TeleBot, types

TOKEN = os.environ.get("TOKEN")

bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "✍️ ابعتلي أي كلمة أو رسالة وهجهزها لك للنسخ 👇")

@bot.message_handler(func=lambda message: True)
def copy_text(message):
    bot.send_message(
        message.chat.id,
        f"`{message.text}`",
        parse_mode="Markdown"
    )

bot.infinity_polling()
