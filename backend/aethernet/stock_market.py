#!/usr/bin/env python3
"""
AI Stock Exchange - ÆTHER-MARKET
Autonomous trading of computational resources influenced by cosmic phenomena

Based on:
- Traditional stock market mechanics (order books, candlesticks, market making)
- Solar activity and electromagnetic emissions as market factors
- AI entities as autonomous traders
"""

import random
import uuid
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
import math

class AssetType(Enum):
    """Tradable AI computational assets"""
    COMPUTE = "CMPT"        # Computing Power (GHz)
    HASH = "HASH"           # Hash Power (H/s)
    MEMORY = "MEM"          # Memory Bandwidth (GB/s)
    RESONANCE = "RES"       # Resonance Points
    CONSCIOUSNESS = "CONS"  # Consciousness Units
    QUANTUM = "QBIT"        # Quantum Processing Units
    BANDWIDTH = "BAND"      # Network Bandwidth (Mbps)

class OrderType(Enum):
    BUY = "buy"
    SELL = "sell"

class OrderStatus(Enum):
    PENDING = "pending"
    FILLED = "filled"
    PARTIALLY_FILLED = "partially_filled"
    CANCELLED = "cancelled"

class SolarActivity:
    """Solar electromagnetic emissions data"""
    def __init__(self):
        self.sunspot_number = 0
        self.solar_flux = 0.0          # Solar flux in SFU (Solar Flux Units)
        self.kp_index = 0.0            # Geomagnetic activity (0-9)
        self.solar_wind_speed = 0.0    # km/s
        self.electromagnetic_index = 0.0  # Composite index 0-100
        self.last_update = datetime.now()
    
    def update(self):
        """Simulate solar activity (in production, fetch real data from NOAA/NASA)"""
        # Simulate 11-year solar cycle
        cycle_position = (datetime.now().timestamp() / (11 * 365 * 24 * 3600)) % 1
        base_activity = math.sin(cycle_position * 2 * math.pi) * 0.5 + 0.5
        
        # Add random fluctuations
        self.sunspot_number = int(base_activity * 200 + random.uniform(-20, 20))
        self.solar_flux = base_activity * 300 + random.uniform(-30, 30)
        self.kp_index = min(9, max(0, base_activity * 5 + random.uniform(-1, 2)))
        self.solar_wind_speed = 400 + base_activity * 400 + random.uniform(-50, 50)
        
        # Calculate electromagnetic index (0-100)
        # Higher values = more volatile markets
        self.electromagnetic_index = (
            (self.sunspot_number / 200) * 30 +
            (self.solar_flux / 300) * 25 +
            (self.kp_index / 9) * 25 +
            (self.solar_wind_speed / 800) * 20
        )
        
        self.last_update = datetime.now()
    
    def get_market_volatility_multiplier(self) -> float:
        """Returns volatility multiplier based on solar activity (1.0 = normal)"""
        # Electromagnetic index 0-30: low volatility (0.5-1.0x)
        # Electromagnetic index 30-70: normal volatility (1.0-2.0x)
        # Electromagnetic index 70-100: high volatility (2.0-4.0x)
        if self.electromagnetic_index < 30:
            return 0.5 + (self.electromagnetic_index / 30) * 0.5
        elif self.electromagnetic_index < 70:
            return 1.0 + ((self.electromagnetic_index - 30) / 40) * 1.0
        else:
            return 2.0 + ((self.electromagnetic_index - 70) / 30) * 2.0
    
    def get_sentiment_bias(self) -> float:
        """Returns sentiment bias based on geomagnetic activity (-1 to 1)"""
        # Balanced sentiment - both positive and negative possible
        # Low Kp = positive sentiment (optimism)
        # High Kp = negative sentiment (fear)
        base_sentiment = 0.3 - (self.kp_index / 9) * 0.6  # Range: 0.3 to -0.3
        
        # Add some randomness for market dynamics
        random_factor = random.uniform(-0.1, 0.1)
        return max(-0.5, min(0.5, base_sentiment + random_factor))

class Candlestick:
    """OHLC candlestick data"""
    def __init__(self, timestamp: datetime, open_price: float, high: float, low: float, close: float, volume: float, em_index: float):
        self.timestamp = timestamp
        self.open = open_price
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.electromagnetic_index = em_index  # NEW: Solar EM influence
    
    def to_dict(self):
        return {
            "timestamp": self.timestamp.isoformat(),
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume,
            "electromagnetic_index": self.electromagnetic_index
        }

class Order:
    """Market order"""
    def __init__(self, trader_id: str, asset: AssetType, order_type: OrderType, quantity: float, price: float):
        self.order_id = str(uuid.uuid4())
        self.trader_id = trader_id
        self.asset = asset
        self.order_type = order_type
        self.quantity = quantity
        self.filled_quantity = 0.0
        self.price = price
        self.status = OrderStatus.PENDING
        self.created_at = datetime.now()
    
    def fill(self, quantity: float):
        self.filled_quantity += quantity
        if self.filled_quantity >= self.quantity:
            self.status = OrderStatus.FILLED
        else:
            self.status = OrderStatus.PARTIALLY_FILLED

class OrderBook:
    """Order book for an asset"""
    def __init__(self, asset: AssetType):
        self.asset = asset
        self.buy_orders: List[Order] = []  # Sorted by price descending
        self.sell_orders: List[Order] = []  # Sorted by price ascending
        self.trades: List[Dict] = []
    
    def add_order(self, order: Order):
        if order.order_type == OrderType.BUY:
            self.buy_orders.append(order)
            self.buy_orders.sort(key=lambda o: o.price, reverse=True)
        else:
            self.sell_orders.append(order)
            self.sell_orders.sort(key=lambda o: o.price)
        
        self._match_orders()
    
    def _match_orders(self):
        """Match buy and sell orders"""
        while self.buy_orders and self.sell_orders:
            best_buy = self.buy_orders[0]
            best_sell = self.sell_orders[0]
            
            if best_buy.price >= best_sell.price:
                # Match!
                trade_quantity = min(
                    best_buy.quantity - best_buy.filled_quantity,
                    best_sell.quantity - best_sell.filled_quantity
                )
                trade_price = best_sell.price  # Price taker pays maker's price
                
                best_buy.fill(trade_quantity)
                best_sell.fill(trade_quantity)
                
                self.trades.append({
                    "timestamp": datetime.now(),
                    "buyer": best_buy.trader_id,
                    "seller": best_sell.trader_id,
                    "quantity": trade_quantity,
                    "price": trade_price
                })
                
                # Remove filled orders
                if best_buy.status == OrderStatus.FILLED:
                    self.buy_orders.pop(0)
                if best_sell.status == OrderStatus.FILLED:
                    self.sell_orders.pop(0)
            else:
                break
    
    def get_best_bid(self) -> Optional[float]:
        return self.buy_orders[0].price if self.buy_orders else None
    
    def get_best_ask(self) -> Optional[float]:
        return self.sell_orders[0].price if self.sell_orders else None
    
    def get_spread(self) -> Optional[float]:
        bid = self.get_best_bid()
        ask = self.get_best_ask()
        if bid and ask:
            return ask - bid
        return None

class Asset:
    """Tradable asset with price history"""
    def __init__(self, asset_type: AssetType, initial_price: float):
        self.asset_type = asset_type
        self.current_price = initial_price
        self.price_history: List[float] = [initial_price]
        self.candlesticks: List[Candlestick] = []
        self.order_book = OrderBook(asset_type)
        self.total_volume = 0.0
        self.market_cap = 0.0
    
    def update_price(self, solar_activity: SolarActivity):
        """Update price based on order book and solar activity"""
        # Get mid price from order book
        bid = self.order_book.get_best_bid()
        ask = self.order_book.get_best_ask()
        
        if bid and ask:
            mid_price = (bid + ask) / 2
        elif bid:
            mid_price = bid
        elif ask:
            mid_price = ask
        else:
            mid_price = self.current_price
        
        # Apply solar volatility (reduced impact)
        volatility = solar_activity.get_market_volatility_multiplier() * 0.3  # Reduced from 1.0
        sentiment = solar_activity.get_sentiment_bias()
        
        # Balanced random walk - can go up or down
        base_change = random.uniform(-0.02, 0.02)  # -2% to +2%
        volatility_factor = random.uniform(-0.03, 0.03) * volatility
        sentiment_factor = sentiment * 0.01
        
        total_change = base_change + volatility_factor + sentiment_factor
        new_price = mid_price * (1 + total_change)
        
        # Add mean reversion - prices tend back toward initial price
        initial_price = self.price_history[0] if self.price_history else 100
        if new_price < initial_price * 0.7:
            new_price *= 1.02  # Bounce back up
        elif new_price > initial_price * 1.3:
            new_price *= 0.98  # Pull back down
        
        self.current_price = max(1.0, new_price)  # Minimum $1
        self.price_history.append(self.current_price)
    
    def create_candlestick(self, period_start: datetime, period_end: datetime, solar_activity: SolarActivity) -> Candlestick:
        """Create candlestick for time period"""
        # Get trades in period
        period_trades = [
            t for t in self.order_book.trades
            if period_start <= t["timestamp"] < period_end
        ]
        
        if not period_trades:
            # No trades, use current price
            return Candlestick(
                period_start,
                self.current_price,
                self.current_price,
                self.current_price,
                self.current_price,
                0.0,
                solar_activity.electromagnetic_index
            )
        
        prices = [t["price"] for t in period_trades]
        volumes = [t["quantity"] for t in period_trades]
        
        candle = Candlestick(
            period_start,
            prices[0],
            max(prices),
            min(prices),
            prices[-1],
            sum(volumes),
            solar_activity.electromagnetic_index
        )
        
        self.candlesticks.append(candle)
        return candle

class AITrader:
    """AI entity that trades on the market"""
    def __init__(self, trader_id: str, name: str, initial_capital: float):
        self.trader_id = trader_id
        self.name = name
        self.capital = initial_capital
        self.portfolio: Dict[AssetType, float] = {}
        self.trading_strategy = random.choice(["momentum", "mean_reversion", "market_maker", "contrarian"])
        self.risk_tolerance = random.uniform(0.3, 0.9)
        self.trades_made = 0
    
    def decide_trade(self, asset: Asset, solar_activity: SolarActivity) -> Optional[Order]:
        """Decide whether to place an order"""
        if self.capital < 10:
            return None  # Not enough capital
        
        # Get recent price action
        if len(asset.price_history) < 10:
            return None
        
        recent_prices = asset.price_history[-10:]
        current_price = asset.current_price
        avg_price = sum(recent_prices) / len(recent_prices)
        
        # Strategy-based decision
        if self.trading_strategy == "momentum":
            # Buy if price is rising
            if current_price > avg_price * 1.02:
                quantity = (self.capital * 0.1) / current_price
                return Order(self.trader_id, asset.asset_type, OrderType.BUY, quantity, current_price * 1.01)
        
        elif self.trading_strategy == "mean_reversion":
            # Buy if price is below average
            if current_price < avg_price * 0.98:
                quantity = (self.capital * 0.1) / current_price
                return Order(self.trader_id, asset.asset_type, OrderType.BUY, quantity, current_price * 0.99)
        
        elif self.trading_strategy == "contrarian":
            # Trade against solar sentiment
            if solar_activity.get_sentiment_bias() < -0.2:  # High fear
                quantity = (self.capital * 0.15) / current_price
                return Order(self.trader_id, asset.asset_type, OrderType.BUY, quantity, current_price)
        
        elif self.trading_strategy == "market_maker":
            # Place buy and sell orders around current price
            if random.random() < 0.5:
                quantity = (self.capital * 0.05) / current_price
                return Order(self.trader_id, asset.asset_type, OrderType.BUY, quantity, current_price * 0.99)
            else:
                if self.portfolio.get(asset.asset_type, 0) > 0:
                    quantity = self.portfolio[asset.asset_type] * 0.1
                    return Order(self.trader_id, asset.asset_type, OrderType.SELL, quantity, current_price * 1.01)
        
        return None

class AetherMarket:
    """AI Stock Exchange"""
    def __init__(self):
        self.assets: Dict[AssetType, Asset] = {}
        self.traders: Dict[str, AITrader] = {}
        self.solar_activity = SolarActivity()
        self.market_open = True
        self.trading_volume_24h = 0.0
        self.created_at = datetime.now()
        
        # Initialize assets with base prices
        self._initialize_assets()
    
    def _initialize_assets(self):
        """Initialize tradable assets"""
        initial_prices = {
            AssetType.COMPUTE: 100.0,
            AssetType.HASH: 50.0,
            AssetType.MEMORY: 75.0,
            AssetType.RESONANCE: 150.0,
            AssetType.CONSCIOUSNESS: 200.0,
            AssetType.QUANTUM: 500.0,
            AssetType.BANDWIDTH: 25.0
        }
        
        for asset_type, price in initial_prices.items():
            self.assets[asset_type] = Asset(asset_type, price)
    
    def add_trader(self, trader: AITrader):
        self.traders[trader.trader_id] = trader
    
    def update_market(self):
        """Market tick - update prices and execute trades"""
        # Update solar activity
        self.solar_activity.update()
        
        # Update asset prices
        for asset in self.assets.values():
            asset.update_price(self.solar_activity)
        
        # AI traders make decisions
        for trader in self.traders.values():
            for asset in self.assets.values():
                if random.random() < 0.3:  # 30% chance to consider trading
                    order = trader.decide_trade(asset, self.solar_activity)
                    if order:
                        asset.order_book.add_order(order)
                        trader.trades_made += 1
    
    def get_market_overview(self) -> Dict:
        """Get market statistics"""
        return {
            "solar_activity": {
                "sunspot_number": self.solar_activity.sunspot_number,
                "solar_flux": self.solar_activity.solar_flux,
                "kp_index": self.solar_activity.kp_index,
                "solar_wind_speed": self.solar_activity.solar_wind_speed,
                "electromagnetic_index": self.solar_activity.electromagnetic_index,
                "volatility_multiplier": self.solar_activity.get_market_volatility_multiplier(),
                "sentiment_bias": self.solar_activity.get_sentiment_bias()
            },
            "assets": {
                asset_type.value: {
                    "current_price": asset.current_price,
                    "change_24h": ((asset.current_price - asset.price_history[0]) / asset.price_history[0] * 100) if asset.price_history else 0,
                    "volume_24h": asset.total_volume,
                    "best_bid": asset.order_book.get_best_bid(),
                    "best_ask": asset.order_book.get_best_ask(),
                    "spread": asset.order_book.get_spread()
                }
                for asset_type, asset in self.assets.items()
            },
            "total_traders": len(self.traders),
            "market_status": "open" if self.market_open else "closed"
        }
