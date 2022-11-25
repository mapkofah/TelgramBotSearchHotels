import telebot
from telebot import types

from get_date import get_year
from get_town import get_town
from my_bot import my_bot


def func_low_price(message):
    """
    Обработка команды lowprice
    """
    get_town(message)
    # get_year(message)
