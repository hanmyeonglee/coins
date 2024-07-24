import requests
from utils.utils import *
from utils.Coin import coin
from utils.trader import trader

from type.type import type

class type03(type):
    @staticmethod
    def select_func(coins: list[coin], n: int) -> list[coin]:
        for C in coins:
            if C.name == 'BTC':
                return [C]
