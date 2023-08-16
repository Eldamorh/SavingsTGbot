import telebot
from telebot import types
from django.core.exceptions import ObjectDoesNotExist
from .models import User, Savings
from django.conf import settings

bot = telebot.TeleBot(settings.TOKEN_BOT)


@bot.message_handler(commands=['start'])
def handle_start(message):
    try:
        user = User.objects.get(chat_id=message.chat.id)
        bot.send_message(message.chat.id, f"Welcome back, {user.first_name}!")
    except ObjectDoesNotExist:
        user = User.objects.create(
            chat_id=message.chat.id,
            username=message.chat.username,
            first_name=message.chat.first_name,
        )
        bot.send_message(message.chat.id, f"Hello, {user.first_name}! Welcome to the savings bot.")


@bot.message_handler(commands=['add_savings'])
def handle_add_savings(message):
    user_id = message.chat.id
    bot.send_message(user_id, "Select savings type:", reply_markup=get_currency_keyboard())


def get_currency_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(types.KeyboardButton('EUR'), types.KeyboardButton('UAH'), types.KeyboardButton('USD'))
    return keyboard


@bot.message_handler(func=lambda message: message.text in ['EUR', 'UAH', 'USD'])
def add_savings_type(message):
    user_id = message.chat.id
    savings_type = message.text
    bot.send_message(user_id, "Enter savings amount:")
    bot.register_next_step_handler(message, add_savings_amount, savings_type)


def add_savings_amount(message, savings_type):
    user_id = message.chat.id
    amount = float(message.text)
    user = User.objects.get(chat_id=user_id)
    Savings.objects.create(user=user, savings_type=savings_type, amount=amount)
    bot.send_message(user_id, f"Saved {amount} in {savings_type}.")


@bot.message_handler(commands=['delete_savings'])
def handle_delete_savings(message):
    user_id = message.chat.id
    user = User.objects.get(chat_id=user_id)
    savings_list = Savings.objects.filter(user=user)

    if not savings_list:
        bot.send_message(user_id, "You have no savings to delete.")
        return

    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for savings in savings_list:
        keyboard.add(types.KeyboardButton(f"Delete {savings.savings_type} ({savings.amount})"))

    bot.send_message(user_id, "Select the savings to delete:", reply_markup=keyboard)
    bot.register_next_step_handler(message, confirm_delete)


def confirm_delete(message):
    user_id = message.chat.id
    user = User.objects.get(chat_id=user_id)
    savings_to_delete = message.text.split(" ")[1]

    try:
        savings = Savings.objects.get(user=user, savings_type=savings_to_delete)
        savings.delete()
        bot.send_message(user_id, f"Deleted {savings_to_delete} ({savings.amount}).")
    except ObjectDoesNotExist:
        bot.send_message(user_id, "Savings not found.")


@bot.message_handler(commands=['view_savings'])
def handle_view_savings(message):
    user_id = message.chat.id
    user = User.objects.get(chat_id=user_id)
    savings_list = Savings.objects.filter(user=user)

    if not savings_list:
        bot.send_message(user_id, "You have no savings.")
        return

    savings_summary = "\n".join([f"{savings.savings_type}: {savings.amount}" for savings in savings_list])
    response = f"Your savings:\n{savings_summary}"

    bot.send_message(user_id, response)
