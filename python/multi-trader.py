from requests.exceptions import ConnectionError, ReadTimeout
from utils.trader import trader
from utils.log import print

from python.typ.typ import *

import traceback
from time import sleep

import sys


Trader: trader = None
type_selector = {
    'type01': type01,
    'type02': type02,
    'type03': type03,
}


def main(name:str, balance: float, n: int, main_type: type):
    global Trader
    Trader = trader(name, balance, n)
    flag = False
    while True:
        try:
            if not flag:
                Trader.update() \
                      .select_coins_and_buy(main_type.sort_func, main_type.select_func)
            
            nof_sold_coins = 0
            
            while nof_sold_coins < max(n // 2, 1):
                nof_sold_coins += Trader.supervise_price_of_dealing_coins(main_type.decide_func)
                flag = True
                sleep(1.25)

            print(Trader)
            flag = False

            main_type.wait_func()
        except ConnectionError or ReadTimeout:
            print('connection error...')
            sleep(10)
            continue


if __name__ == "__main__":
    name, bal, n, typ = sys.argv[1:5]

    try:
        main(name, int(bal), int(n), type_selector[typ])
    except Exception:
        bt = traceback.format_exc()
        print(bt)
        print(Trader)
        print("process exited...")
        exit(0)
