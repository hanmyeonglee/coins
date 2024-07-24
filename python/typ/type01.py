import requests
from utils.utils import *
from utils.Coin import coin
from utils.trader import trader

from typ.type import type

class type01(type):

    @staticmethod
    def sort_func(C: coin) -> int:
        response = check_request_success(
            requests.get(trader.CDL_CHT_CHK % C.name, params={
                'interval': '1m',
                'size': type01.CDL_size,
            }, headers=trader.headers).json(),
            trader.GET_req_fail % "response of type01.sort_func() by err_code [%s].",
        )

        positive = 0
        negative = 0
        for candle in response['chart']:
            opn, clos = float(candle['open']), float(candle['close'])
            if opn > clos:
                positive += 1
            elif opn < clos:
                negative += 1

        return positive - negative


    @staticmethod
    def select_func(coins: list[coin], n: int) -> list[coin]:
        coins = list(filter(lambda x: x.is_dealible(5000000), coins))
        mid = len(coins) // 2
        return coins[mid - n//2 : mid + n//2 + n % 2]
