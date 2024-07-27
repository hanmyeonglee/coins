import requests
from utils.utils import *
from utils.Coin import coin
from utils.trader import trader

from time import sleep
from random import randint

class typ:

    profit_ratio = 0.005
    loss_ratio = 0.2

    TRANS_size = 10
    CDL_size = 250

    @staticmethod
    def sort_func(C: coin) -> int:
        return C.quote_volume

    @staticmethod
    def select_func(coins: list, n: int) -> list:
        return coins[-n:]
    
    @staticmethod
    def decide_func(C: coin):
        orderbook = check_request_success(
            requests.get(trader.ORDER_BOOK_CHK % C.name, headers=trader.headers).json(),
            trader.GET_req_fail % "orderbook of typ.decide_func() by err_code [%s].",
        )

        transactions = check_request_success(
            requests.get(trader.LAST_TRANSACTION_CHK % C.name, params={
                'size': typ.TRANS_size,
            }, headers=trader.headers).json(),
            trader.GET_req_fail % "transactions of typ.decide_func() by err_code [%s].",
        )


        lowest_price = float(orderbook['bids'][-1]['price'])
        sell_price = []
        

        for trans in transactions['transactions']:
            if not trans['is_seller_maker']:
                sell_price.append(float(trans['price']))


        if not len(sell_price):
            return lowest_price >= C.crit_price * (1 + typ.profit_ratio)


        avg_sell_price = sum(sell_price) / len(sell_price)


        return lowest_price >= C.crit_price * (1 + typ.profit_ratio) or \
               avg_sell_price <= C.crit_price * (1 - typ.loss_ratio)
    

    @staticmethod
    def wait_func():
        sleep(randint(120, 240) * 60)


class type01(typ):

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
    def select_func(coins: list, n: int) -> list:
        coins = list(filter(lambda x: x.is_dealible(5000000), coins))
        mid = len(coins) // 2
        return coins[mid - n//2 : mid + n//2 + n % 2]


class type02(typ): pass


class type03(typ):
    @staticmethod
    def select_func(coins: list, n: int) -> list:
        for C in coins:
            if C.name == 'BTC':
                return [C]
