from django.core.management.base import BaseCommand
from django.conf import settings
from telebot import TeleBot
import asyncio

from core.main_bot import bot


class Command(BaseCommand):
    help = 'Implemented to Django application telegram bot setup command'

    def handle(self, *args, **kwargs):
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        bot.infinity_polling()
