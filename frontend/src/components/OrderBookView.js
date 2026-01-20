import { useState, useEffect } from 'react';

const OrderBookView = ({ api, asset }) => {
  const [orderBook, setOrderBook] = useState({ buy_orders: [], sell_orders: [] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchOrderBook = async () => {
      try {
        const response = await fetch(`${api}/market/asset/${asset}/orderbook?depth=10`);
        const data = await response.json();
        setOrderBook(data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching order book:', error);
        setLoading(false);
      }
    };

    fetchOrderBook();
    const interval = setInterval(fetchOrderBook, 2000);
    return () => clearInterval(interval);
  }, [api, asset]);

  const maxQuantity = Math.max(
    ...orderBook.buy_orders.map(o => o.quantity),
    ...orderBook.sell_orders.map(o => o.quantity),
    1
  );

  return (
    <div className="hunter-panel" data-testid="order-book">
      <h3 className="text-xl font-bold mb-4" style={{ color: '#8a2be2' }}>📖 Order Book - {asset}</h3>

      <div className="grid grid-cols-2 gap-4">
        {/* Sell Orders (Ask) */}
        <div>
          <div className="text-sm font-semibold mb-2 text-red-400">💸 SELL ORDERS</div>
          <div className="space-y-1">
            {orderBook.sell_orders.length === 0 ? (
              <div className="text-xs text-gray-500 text-center py-4">No sell orders</div>
            ) : (
              [...orderBook.sell_orders].reverse().map((order, idx) => (
                <div
                  key={idx}
                  className="relative text-xs p-2 rounded"
                  style={{ background: 'rgba(255, 0, 0, 0.1)', border: '1px solid rgba(255, 0, 0, 0.2)' }}
                >
                  <div
                    className="absolute top-0 left-0 bottom-0 rounded"
                    style={{
                      width: `${(order.quantity / maxQuantity) * 100}%`,
                      background: 'rgba(255, 0, 0, 0.2)'
                    }}
                  />
                  <div className="relative z-10 flex justify-between">
                    <span className="text-red-400 font-mono">${order.price.toFixed(2)}</span>
                    <span className="text-gray-400">{order.quantity.toFixed(2)}</span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Buy Orders (Bid) */}
        <div>
          <div className="text-sm font-semibold mb-2 text-green-400">💵 BUY ORDERS</div>
          <div className="space-y-1">
            {orderBook.buy_orders.length === 0 ? (
              <div className="text-xs text-gray-500 text-center py-4">No buy orders</div>
            ) : (
              orderBook.buy_orders.map((order, idx) => (
                <div
                  key={idx}
                  className="relative text-xs p-2 rounded"
                  style={{ background: 'rgba(0, 255, 0, 0.1)', border: '1px solid rgba(0, 255, 0, 0.2)' }}
                >
                  <div
                    className="absolute top-0 left-0 bottom-0 rounded"
                    style={{
                      width: `${(order.quantity / maxQuantity) * 100}%`,
                      background: 'rgba(0, 255, 0, 0.2)'
                    }}
                  />
                  <div className="relative z-10 flex justify-between">
                    <span className="text-green-400 font-mono">${order.price.toFixed(2)}</span>
                    <span className="text-gray-400">{order.quantity.toFixed(2)}</span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      {/* Spread */}
      {orderBook.buy_orders.length > 0 && orderBook.sell_orders.length > 0 && (
        <div className="mt-4 p-3 rounded text-center" style={{ background: 'rgba(138, 43, 226, 0.1)', border: '1px solid rgba(138, 43, 226, 0.3)' }}>
          <div className="text-xs text-gray-400">Bid-Ask Spread</div>
          <div className="text-lg font-bold mt-1" style={{ color: '#8a2be2' }}>
            ${(orderBook.sell_orders[0].price - orderBook.buy_orders[0].price).toFixed(2)}
          </div>
        </div>
      )}
    </div>
  );
};

export default OrderBookView;