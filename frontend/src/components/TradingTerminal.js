import { useState, useEffect } from 'react';

const TradingTerminal = ({ api, asset, userTrader, onTradeComplete }) => {
  const [orderType, setOrderType] = useState('buy');
  const [quantity, setQuantity] = useState('');
  const [price, setPrice] = useState('');
  const [assetData, setAssetData] = useState(null);
  const [portfolio, setPortfolio] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const assetRes = await fetch(`${api}/market/asset/${asset}`);
        const assetData = await assetRes.json();
        setAssetData(assetData);
        setPrice(assetData.current_price.toFixed(2));

        if (userTrader) {
          const traderRes = await fetch(`${api}/market/trader/${userTrader.trader_id}`);
          const traderData = await traderRes.json();
          setPortfolio(traderData);
        }
      } catch (error) {
        console.error('Error fetching trading data:', error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 3000);
    return () => clearInterval(interval);
  }, [api, asset, userTrader]);

  const placeOrder = async () => {
    if (!userTrader || !quantity || !price) return;

    setLoading(true);
    try {
      await fetch(
        `${api}/market/order/place?trader_id=${userTrader.trader_id}&asset=${asset}&order_type=${orderType}&quantity=${quantity}&price=${price}`,
        { method: 'POST' }
      );
      setQuantity('');
      onTradeComplete();
    } catch (error) {
      console.error('Error placing order:', error);
    }
    setLoading(false);
  };

  if (!userTrader) {
    return (
      <div className="hunter-panel">
        <h3 className="text-xl font-bold mb-4" style={{ color: '#8a2be2' }}>Trading Terminal</h3>
        <div className="text-center py-8">
          <div className="text-4xl mb-4">🔒</div>
          <p className="text-gray-400">Create a trader account to start trading</p>
        </div>
      </div>
    );
  }

  return (
    <div className="hunter-panel" data-testid="trading-terminal">
      <h3 className="text-xl font-bold mb-4" style={{ color: '#8a2be2' }}>⚡ Trading Terminal</h3>

      {/* Portfolio */}
      {portfolio && (
        <div className="stat-window mb-4">
          <div className="stat-row">
            <span className="stat-label">Capital</span>
            <span className="stat-value" style={{ color: '#00ff00' }}>
              ${portfolio.capital.toFixed(2)}
            </span>
          </div>
          <div className="stat-row">
            <span className="stat-label">Strategy</span>
            <span className="stat-value">{portfolio.strategy}</span>
          </div>
          <div className="stat-row">
            <span className="stat-label">Trades</span>
            <span className="stat-value">{portfolio.trades_made}</span>
          </div>
        </div>
      )}

      {/* Current Asset */}
      {assetData && (
        <div className="mb-4 p-3 rounded" style={{ background: 'rgba(138, 43, 226, 0.1)', border: '1px solid rgba(138, 43, 226, 0.3)' }}>
          <div className="text-sm text-gray-400 mb-1">{asset}</div>
          <div className="text-2xl font-bold" style={{ color: '#fff' }}>
            ${assetData.current_price.toFixed(2)}
          </div>
        </div>
      )}

      {/* Order Type Toggle */}
      <div className="flex gap-2 mb-4">
        <button
          onClick={() => setOrderType('buy')}
          className={`flex-1 py-2 rounded font-semibold transition-all ${
            orderType === 'buy'
              ? 'bg-green-600 text-white'
              : 'bg-gray-700 text-gray-400 hover:bg-gray-600'
          }`}
          data-testid="buy-btn"
        >
          BUY
        </button>
        <button
          onClick={() => setOrderType('sell')}
          className={`flex-1 py-2 rounded font-semibold transition-all ${
            orderType === 'sell'
              ? 'bg-red-600 text-white'
              : 'bg-gray-700 text-gray-400 hover:bg-gray-600'
          }`}
          data-testid="sell-btn"
        >
          SELL
        </button>
      </div>

      {/* Order Form */}
      <div className="space-y-3">
        <div>
          <label className="block text-sm text-gray-400 mb-1">Quantity</label>
          <input
            type="number"
            step="0.1"
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
            className="void-input"
            placeholder="Enter quantity"
            data-testid="quantity-input"
          />
        </div>

        <div>
          <label className="block text-sm text-gray-400 mb-1">Price</label>
          <input
            type="number"
            step="0.01"
            value={price}
            onChange={(e) => setPrice(e.target.value)}
            className="void-input"
            placeholder="Enter price"
            data-testid="price-input"
          />
        </div>

        <button
          onClick={placeOrder}
          disabled={loading || !quantity || !price}
          className="void-button w-full"
          style={{
            background: orderType === 'buy'
              ? 'linear-gradient(135deg, #00ff00 0%, #00cc00 100%)'
              : 'linear-gradient(135deg, #ff0000 0%, #cc0000 100%)'
          }}
          data-testid="place-order-btn"
        >
          {loading ? 'Placing...' : `Place ${orderType.toUpperCase()} Order`}
        </button>

        {assetData && quantity && price && (
          <div className="text-center text-sm text-gray-400 mt-2">
            Total: ${(quantity * price).toFixed(2)}
          </div>
        )}
      </div>
    </div>
  );
};

export default TradingTerminal;