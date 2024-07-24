import requests
from utils.utils import *
from utils.log import print
from utils.Coin import coin

class trader:
    pass

class trader:
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"}

    ALL_COIN_INFO_CHK = 'https://api.coinone.co.kr/public/v2/markets/KRW'
    ONE_COIN_INFO_CHK = 'https://api.coinone.co.kr/public/v2/markets/KRW/%s'

    ALL_TICK_INFO_CHK = 'https://api.coinone.co.kr/public/v2/ticker_new/KRW'
    ONE_TICK_INFO_CHK = 'https://api.coinone.co.kr/public/v2/ticker_new/KRW/%s'

    LAST_TRANSACTION_CHK = 'https://api.coinone.co.kr/public/v2/trades/KRW/%s'

    ORDER_BOOK_CHK = 'https://api.coinone.co.kr/public/v2/orderbook/KRW/%s'

    CDL_CHT_CHK = 'https://api.coinone.co.kr/public/v2/chart/KRW/%s'

    GET_req_fail = 'GET request is failed in %s'
    POST_req_fail = 'POST request is failed in %s'
    

    def __init__(self, name: str, balance: float, n: int):
        print('Start Trading')

        self.name: str = name
        self.balance: float = balance
        self.nof_coins_to_deal_atonce = n
        self.coins: dict = {}
        self.coin_names: list = []
        self.current_dealing_coins: list = []


    def update(self) -> trader:
        coins_info = check_request_success(
            requests.get(self.ALL_COIN_INFO_CHK, headers=self.headers).json(),
            self.GET_req_fail % "coins_info of trader.initialize() by err_code [%s].",
        )

        tick_infos = check_request_success(
            requests.get(self.ALL_TICK_INFO_CHK, headers=self.headers).json(),
            self.GET_req_fail % "tick_info of trader.initialize() by err_code [%s]."
        )


        self.coin_names = map(
            lambda x: x['target_currency'],
            coins_info['markets'],
        )


        for ind, coin_name in enumerate(self.coin_names):
            if coin_name in self.coins:
                self.coins[coin_name].update(
                    coin_info = coins_info['markets'][ind],
                    tick_info = tick_infos['tickers'][ind],
                )
                continue

            self.coins[coin_name] = coin(
                coin_info = coins_info['markets'][ind],
                tick_info = tick_infos['tickers'][ind],
            )

        
        return self
    

    def select_coins_and_buy(self, sort_func: function, select_func: function) -> trader:
        nof_dificient_coins = self.nof_coins_to_deal_atonce - len(self.current_dealing_coins)
        
        sorted_coin_list: list = list(self.coins.values())
        sorted_coin_list.sort(
            key = sort_func
        )

        selected_coins: list = select_func(sorted_coin_list, nof_dificient_coins)

        for C in selected_coins:
            self.buy(C)

        self.current_dealing_coins.extend(selected_coins)

        return self
    

    def supervise_price_of_dealing_coins(self, decide_func: function) -> int:
        selling_coin_number = 0

        for coin in self.current_dealing_coins:
            if decide_func(coin):
                self.sell(coin)
                selling_coin_number += 1
        
        return selling_coin_number
    

    def buy(self, coin: coin) -> trader:
        order_book = check_request_success(
            requests.get(self.ORDER_BOOK_CHK % coin.name, headers=self.headers).json(),
            self.GET_req_fail % 'order_book_info of trader.buy() by err_code [%s].',
        )

        budget = self.balance / (self.nof_coins_to_deal_atonce - len(self.current_dealing_coins))
        buying_qty_and_price = []
        total_qty = 0
        total_price = 0


        for order in order_book['asks']:
            price = float(order['price'])
            qty = float(order['qty'])

            buying_price = price * qty
            buying_price = floor(buying_price, coin.min_info['price'])

            if buying_price >= budget:
                qty = floor(budget / price, coin.min_info['qty'])
                buying_price = floor(qty * price, coin.min_info['price'])
                budget = 0
            else:
                budget -= buying_price

            self.balance -= buying_price
            total_price += buying_price

            buying_qty_and_price.append((price, qty))
            total_qty += qty

            if not budget:
                break

        
        crit_price = sum(
            map(
                lambda x: floor(x[0] * (x[1] / total_qty),  coin.min_info['price']),
                buying_qty_and_price,
            )
        )

        coin.crit_price = crit_price
        coin.total_qty = total_qty


        print(
            "Trader: buys %s by qty %f and price %f." % (coin.name, total_qty, crit_price)
        )


        return self
    

    def sell(self, coin: coin) -> trader:
        order_book = check_request_success(
            requests.get(self.ORDER_BOOK_CHK % coin.name, headers=self.headers).json(),
            self.GET_req_fail % 'order_book_info of trader.sell() by err_code [%s].',
        )

        total_qty = 0
        before_bal = coin.total_qty * coin.crit_price


        for order in order_book['bids'][::-1]:
            price = float(order['price'])
            qty = float(order['qty'])

            if qty >= coin.total_qty:
                qty = coin.total_qty
                coin.total_qty = 0
            else:
                coin.total_qty -= qty
            
            selling_price = floor(qty * price, coin.min_info['price'])

            self.balance += selling_price
            total_qty += qty

            if not coin.total_qty:
                coin.sold()
                self.current_dealing_coins.remove(coin)
                break


        print(
            "Trader: sells %s by qty %f and profit %f." % (coin.name, total_qty, self.balance - before_bal)
        )


        return self


    def __str__(self) -> str:
        return f"trader {self.name}(bal={self.balance}, dealing coins currently={self.current_dealing_coins})"
    
    
    def __repr__(self) -> str:
        return self.__str__()