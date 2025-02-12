from .order import MarketOrder, LimitOrder, Side
from .logger import logger

class MatchingEngine:
    def __init__(self, order_book):
        self.order_book = order_book
        self.last_trade_price = None

    def handle_order(self, order):
        """Process an incoming order (Market or Limit) against the order book."""
        if isinstance(order, MarketOrder):
            self._match_market_order(order)
        elif isinstance(order, LimitOrder):
            # Place the limit order into the order book *after* attempting immediate match.
            # We attempt to match only if it crosses the spread (for partial immediate fills).
            self._match_crossed_limit_order(order)
            if order.is_active:
                self.order_book.add_limit_order(order)
        else:
            # STOP orders might convert to MARKET or LIMIT once triggered. Simplified here.
            logger.debug(f"Received STOP order, ignoring advanced logic in this demo: {order}")

    def _match_market_order(self, market_order):
        """Executes the entire quantity of the market order immediately at the best price."""
        if market_order.side == Side.BUY:
            # Match against asks from lowest price to highest
            self._match_buy_order(market_order, self.order_book.asks)
        else:  # SELL
            # Match against bids from highest price to lowest
            self._match_sell_order(market_order, self.order_book.bids)

        self.order_book.remove_inactive_orders()

    def _match_crossed_limit_order(self, limit_order):
        """Matches a newly arrived limit order if it crosses the best price on the other side."""
        if limit_order.side == Side.BUY:
            self._match_buy_order(limit_order, self.order_book.asks)
        else:
            self._match_sell_order(limit_order, self.order_book.bids)

        self.order_book.remove_inactive_orders()

    def _match_buy_order(self, buy_order, ask_deque):
        i = 0
        # While we have quantity left to fill and there are asks
        while buy_order.is_active and i < len(ask_deque):
            best_ask = ask_deque[i]
            # Check if we can trade
            # For a market order or a crossing limit order, price check might be different
            if isinstance(buy_order, MarketOrder) or (isinstance(buy_order, LimitOrder) and buy_order.price >= best_ask.price):
                # Determine matched quantity
                trade_qty = min(buy_order.quantity - buy_order.filled_quantity,
                                best_ask.quantity - best_ask.filled_quantity)

                # Execute trade
                buy_order.fill(trade_qty)
                best_ask.fill(trade_qty)
                self.last_trade_price = best_ask.price
                logger.info(f"Trade executed: BUY {trade_qty} @ {best_ask.price}")

                if not best_ask.is_active:
                    # The ask is fully filled, move on
                    i += 1
            else:
                # No more crossing possible
                break

        # Remove filled asks from the front
        # We'll let remove_inactive_orders handle it or
        # we can do it manually after the loop
        # but we must ensure 'i' tracks how many were fully filled
        pass

    def _match_sell_order(self, sell_order, bid_deque):
        i = 0
        # While we have quantity left to fill and there are bids
        while sell_order.is_active and i < len(bid_deque):
            best_bid = bid_deque[i]
            # For a market order or crossing limit order, price check:
            if isinstance(sell_order, MarketOrder) or (isinstance(sell_order, LimitOrder) and sell_order.price <= best_bid.price):
                trade_qty = min(sell_order.quantity - sell_order.filled_quantity,
                                best_bid.quantity - best_bid.filled_quantity)

                sell_order.fill(trade_qty)
                best_bid.fill(trade_qty)
                self.last_trade_price = best_bid.price
                logger.info(f"Trade executed: SELL {trade_qty} @ {best_bid.price}")

                if not best_bid.is_active:
                    i += 1
            else:
                # No more crossing possible
                break

        pass
