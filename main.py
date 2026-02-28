import os
from telebot import TeleBot

TOKEN = os.environ.get("TOKEN")

bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "✍️ ابعتلي أي كلمة وهخليها جاهزة للنسخ 👇")

@bot.message_handler(func=lambda message: True)
def copy_text(message):
    text = message.text.replace("`", "")  # عشان ميبوظش الفورمات
    bot.send_message(
        message.chat.id,
        f"اضغط على الكلمة لنسخها 👇\n\n`{text}`",
        parse_mode="Markdown"
    )

bot.infinity_polling()
