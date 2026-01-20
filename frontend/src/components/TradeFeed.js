import { useState, useEffect } from 'react';

const TradeFeed = ({ api, asset }) => {
  const [assetData, setAssetData] = useState(null);
  const [trades, setTrades] = useState([]);

  useEffect(() => {
    const fetchTrades = async () => {
      try {
        const response = await fetch(`${api}/market/asset/${asset}`);
        const data = await response.json();
        setAssetData(data);
        
        // Simulate trade feed from order book activity
        // In production, this would come from actual trade history
      } catch (error) {
        console.error('Error fetching trade feed:', error);
      }
    };

    fetchTrades();
    const interval = setInterval(fetchTrades, 3000);
    return () => clearInterval(interval);
  }, [api, asset]);

  return (
    <div className="hunter-panel" data-testid="trade-feed">
      <h3 className="text-xl font-bold mb-4" style={{ color: '#00ffff' }}>📰 Live Market Feed</h3>

      {/* Asset Stats */}
      {assetData && (
        <div className="space-y-2 mb-4">
          <div className="stat-window">
            <div className="stat-row">
              <span className="stat-label">Best Bid</span>
              <span className="stat-value" style={{ color: '#00ff00' }}>
                {assetData.best_bid ? `$${assetData.best_bid.toFixed(2)}` : 'N/A'}
              </span>
            </div>
            <div className="stat-row">
              <span className="stat-label">Best Ask</span>
              <span className="stat-value" style={{ color: '#ff0000' }}>
                {assetData.best_ask ? `$${assetData.best_ask.toFixed(2)}` : 'N/A'}
              </span>
            </div>
            <div className="stat-row">
              <span className="stat-label">Spread</span>
              <span className="stat-value">
                {assetData.spread ? `$${assetData.spread.toFixed(2)}` : 'N/A'}
              </span>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-2 text-xs text-center">
            <div className="p-2 rounded" style={{ background: 'rgba(0, 255, 0, 0.1)' }}>
              <div className="text-gray-400">Buy Orders</div>
              <div className="text-green-400 font-bold mt-1">{assetData.pending_buy_orders}</div>
            </div>
            <div className="p-2 rounded" style={{ background: 'rgba(255, 0, 0, 0.1)' }}>
              <div className="text-gray-400">Sell Orders</div>
              <div className="text-red-400 font-bold mt-1">{assetData.pending_sell_orders}</div>
            </div>
          </div>
        </div>
      )}

      {/* Market Activity Indicators */}
      <div className="space-y-2">
        <div className="p-3 rounded" style={{ background: 'rgba(138, 43, 226, 0.1)', border: '1px solid rgba(138, 43, 226, 0.3)' }}>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
            <div className="text-sm text-gray-300">Market Active</div>
          </div>
        </div>

        {assetData && assetData.pending_buy_orders + assetData.pending_sell_orders > 0 && (
          <div className="p-3 rounded" style={{ background: 'rgba(0, 255, 255, 0.1)', border: '1px solid rgba(0, 255, 255, 0.3)' }}>
            <div className="flex items-center gap-2">
              <div className="text-lg">📊</div>
              <div className="text-sm text-gray-300">
                {assetData.pending_buy_orders + assetData.pending_sell_orders} orders pending
              </div>
            </div>
          </div>
        )}

        {assetData && assetData.spread && assetData.spread > 0 && (
          <div className="p-3 rounded" style={{ background: 'rgba(255, 165, 0, 0.1)', border: '1px solid rgba(255, 165, 0, 0.3)' }}>
            <div className="flex items-center gap-2">
              <div className="text-lg">⚡</div>
              <div>
                <div className="text-xs text-gray-400">Liquidity</div>
                <div className="text-sm" style={{ color: '#ffa500' }}>
                  {assetData.spread < 1 ? 'High' : assetData.spread < 5 ? 'Medium' : 'Low'}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Recent Activity (placeholder) */}
      <div className="mt-4">
        <div className="text-xs text-gray-400 mb-2">Recent Activity</div>
        <div className="space-y-1">
          {[...Array(5)].map((_, i) => (
            <div
              key={i}
              className="text-xs p-2 rounded"
              style={{ background: 'rgba(0, 0, 0, 0.3)' }}
            >
              <div className="flex items-center justify-between">
                <span className="text-gray-500">Monitoring...</span>
                <span className="text-gray-600">•</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default TradeFeed;