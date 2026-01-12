from telebot.types import InlineKeyboardButton,InlineKeyboardMarkup

def payment_button():
    markup = InlineKeyboardMarkup()
    btn = InlineKeyboardButton("Tolovni boshlash",callback_data="pay")
    markup.add(btn)
    return markup
