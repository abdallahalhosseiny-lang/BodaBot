import os
from telebot import TeleBot, types

TOKEN = os.environ.get("TOKEN")

bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("📋 Tap To Copy", callback_data="copy")
    markup.add(button)
    bot.send_message(message.chat.id, "اضغط الزر
