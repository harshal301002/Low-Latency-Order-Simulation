from collections import deque
from .order import LimitOrder, Side

class OrderBook:
    def __init__(self):
        # We'll maintain deques for the bid (buy) and ask (sell) sides
        self.bids = deque()  # Sorted in descending price
        self.asks = deque()  # Sorted in ascending price

    def add_limit_order(self, order: LimitOrder):
        if order.side == Side.BUY:
            # Insert into self.bids (descending order by price)
            inserted = False
            for i in range(len(self.bids)):
                if order.price > self.bids[i].price:
                    self.bids.insert(i, order)
                    inserted = True
                    break
            if not inserted:
                self.bids.append(order)
        else:  # side == SELL
            # Insert into self.asks (ascending order by price)
            inserted = False
            for i in range(len(self.asks)):
                if order.price < self.asks[i].price:
                    self.asks.insert(i, order)
                    inserted = True
                    break
            if not inserted:
                self.asks.append(order)

    def remove_inactive_orders(self):
        # Filter out inactive (fully filled) orders
        self.bids = deque([o for o in self.bids if o.is_active])
        self.asks = deque([o for o in self.asks if o.is_active])

    def best_bid(self):
        return self.bids[0] if len(self.bids) > 0 else None

    def best_ask(self):
        return self.asks[0] if len(self.asks) > 0 else None

    def __repr__(self):
        bids_str = ", ".join([f"(p={o.price}, q={o.quantity-o.filled_quantity})" for o in self.bids])
        asks_str = ", ".join([f"(p={o.price}, q={o.quantity-o.filled_quantity})" for o in self.asks])
        return f"OrderBook(bids=[{bids_str}], asks=[{asks_str}])"
