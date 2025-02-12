from enum import Enum, auto

class OrderType(Enum):
    MARKET = auto()
    LIMIT = auto()
    STOP = auto()

class Side(Enum):
    BUY = auto()
    SELL = auto()

class BaseOrder:
    def __init__(self, order_id, side, quantity, order_type):
        self.order_id = order_id
        self.side = side
        self.quantity = quantity
        self.order_type = order_type
        self.filled_quantity = 0
        self.is_active = True

    def fill(self, fill_qty):
        self.filled_quantity += fill_qty
        if self.filled_quantity >= self.quantity:
            self.is_active = False

    def __repr__(self):
        return (f"BaseOrder(id={self.order_id}, side={self.side}, "
                f"qty={self.quantity}, filled={self.filled_quantity}, "
                f"type={self.order_type}, active={self.is_active})")

class LimitOrder(BaseOrder):
    def __init__(self, order_id, side, quantity, price):
        super().__init__(order_id, side, quantity, OrderType.LIMIT)
        self.price = price

    def __repr__(self):
        return (f"LimitOrder(id={self.order_id}, side={self.side}, "
                f"price={self.price}, qty={self.quantity}, "
                f"filled={self.filled_quantity}, active={self.is_active})")

class MarketOrder(BaseOrder):
    def __init__(self, order_id, side, quantity):
        super().__init__(order_id, side, quantity, OrderType.MARKET)

class StopOrder(BaseOrder):
    def __init__(self, order_id, side, quantity, stop_price):
        super().__init__(order_id, side, quantity, OrderType.STOP)
        self.stop_price = stop_price
