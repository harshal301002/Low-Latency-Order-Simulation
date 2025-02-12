import random
from .order_book import OrderBook
from .matching_engine import MatchingEngine
from .order import MarketOrder, LimitOrder, Side
from .logger import logger

class MarketSimulator:
    def __init__(self):
        self.order_book = OrderBook()
        self.matching_engine = MatchingEngine(self.order_book)
        self.order_id_counter = 0
        self.tick_count = 0

    def initialize(self):
        """Initialize any data sources, historical data, etc."""
        logger.info("Initializing MarketSimulator with empty order book...")

    def run_tick(self):
        """Simulate a single tick of market activity:
           - Randomly generate an order
           - Pass it to the matching engine
           - Possibly random order cancellations or partial fills
        """
        self.tick_count += 1
        logger.debug(f"--- Tick {self.tick_count} ---")

        # Randomly choose an order type
        order_type = random.choice(["MARKET", "LIMIT"])
        side = random.choice([Side.BUY, Side.SELL])
        quantity = random.randint(1, 5) * 100  # e.g., multiples of 100 shares

        self.order_id_counter += 1
        if order_type == "MARKET":
            new_order = MarketOrder(self.order_id_counter, side, quantity)
        else:
            # random price around a notional mid-level
            price = random.randint(90, 110)
            new_order = LimitOrder(self.order_id_counter, side, quantity, price)

        logger.debug(f"New order generated: {new_order}")
        self.matching_engine.handle_order(new_order)

        # Log best bid/ask
        best_bid = self.order_book.best_bid()
        best_ask = self.order_book.best_ask()
        logger.debug(f"Best Bid: {best_bid.price if best_bid else None}")
        logger.debug(f"Best Ask: {best_ask.price if best_ask else None}")
        logger.debug(str(self.order_book))

    def shutdown(self):
        """Cleanup resources."""
        logger.info("Shutting down MarketSimulator.")
