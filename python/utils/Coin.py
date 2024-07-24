class coin:
    def __init__(self, coin_info: dict, tick_info: dict):
        self.name = coin_info['target_currency']
        self.price_unit = coin_info['price_unit']
        self.qty_unit = coin_info['qty_unit']

        self.max_info = {
            "order_amount": coin_info['max_order_amount'],
            "price": coin_info['max_price'],
            "qty": coin_info['max_qty'],
        }

        self.min_info = {
            "order_amount": coin_info['min_order_amount'], 
            "price": coin_info['min_price'].count('0'), 
            "qty": coin_info['min_qty'].count('0'), 
        }

        self.maintenance_status = coin_info['maintenance_status']
        self.trade_status = coin_info['trade_status']


        self.quote_volume = float(tick_info['quote_volume'])
        self.target_volume = float(tick_info['target_volume'])


        self.crit_price = 0
        self.total_qty = 0


    def is_dealible(self, crit: float) -> bool:
        return self.maintenance_status == 0 and \
               self.trade_status == 1 and \
               self.quote_volume > crit
    

    def sold(self) -> None:
        self.crit_price = 0
        self.total_qty = 0

    
    def issold(self) -> bool:
        return self.total_qty == 0
    

    def update(self, coin_info: dict, tick_info: dict):
        cur_crit_price = self.crit_price
        cur_total_qty = self.total_qty

        self.__init__(coin_info, tick_info)
        self.crit_price = cur_crit_price
        self.total_qty = cur_total_qty


    def __str__(self) -> str:
        return f"Coin {self.name}(status={'dealible' if self.is_dealible(0) else 'indealible'}, info={self.crit_price} * {self.total_qty})"
    
    
    def __repr__(self) -> str:
        return self.__str__()