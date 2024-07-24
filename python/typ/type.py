import requests
from utils.utils import *
from utils.Coin import coin
from utils.trader import trader

from time import sleep
from random import randint

class type:

    profit_ratio = 0.005
    loss_ratio = 0.2

    TRANS_size = 10
    CDL_size = 250

    @staticmethod
    def sort_func(C: coin) -> int:
        return C.quote_volume

    @staticmethod
    def select_func(coins: list[coin], n: int) -> list[coin]:
        return coins[-n:]
    
    @staticmethod
    def decide_func(C: coin):
        orderbook = check_request_success(
            requests.get(trader.ORDER_BOOK_CHK % C.name, headers=trader.headers).json(),
            trader.GET_req_fail % "orderbook of type.decide_func() by err_code [%s].",
        )

        transactions = check_request_success(
            requests.get(trader.LAST_TRANSACTION_CHK % C.name, params={
                'size': type.TRANS_size,
            }, headers=trader.headers).json(),
            trader.GET_req_fail % "transactions of type.decide_func() by err_code [%s].",
        )


        lowest_price = float(orderbook['bids'][-1]['price'])
        sell_price = []
        

        for trans in transactions['transactions']:
            if not trans['is_seller_maker']:
                sell_price.append(float(trans['price']))


        if not len(sell_price):
            return lowest_price >= C.crit_price * (1 + type.profit_ratio)


        avg_sell_price = sum(sell_price) / len(sell_price)


        return lowest_price >= C.crit_price * (1 + type.profit_ratio) or \
               avg_sell_price <= C.crit_price * (1 - type.loss_ratio)
    

    @staticmethod
    def wait_func():
        sleep(randint(5, 20) * 60)