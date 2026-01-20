import { useState, useEffect } from 'react';

const CandlestickChart = ({ api, asset }) => {
  const [candlesticks, setCandlesticks] = useState([]);
  const [priceHistory, setPriceHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchChartData = async () => {
      try {
        const [candleRes, assetRes] = await Promise.all([
          fetch(`${api}/market/asset/${asset}/candlesticks?limit=50`),
          fetch(`${api}/market/asset/${asset}`)
        ]);
        
        const candleData = await candleRes.json();
        const assetData = await assetRes.json();
        
        setCandlesticks(candleData.candlesticks || []);
        setPriceHistory(assetData.price_history || []);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching chart data:', error);
        setLoading(false);
      }
    };

    fetchChartData();
    const interval = setInterval(fetchChartData, 5000);
    return () => clearInterval(interval);
  }, [api, asset]);

  if (loading || priceHistory.length === 0) {
    return (
      <div className="hunter-panel">
        <h3 className="text-xl font-bold mb-4" style={{ color: '#8a2be2' }}>📊 Price Chart</h3>
        <div className="text-center py-8 text-gray-400">Loading chart data...</div>
      </div>
    );
  }

  const minPrice = Math.min(...priceHistory);
  const maxPrice = Math.max(...priceHistory);
  const priceRange = maxPrice - minPrice;

  return (
    <div className="hunter-panel" data-testid="candlestick-chart">
      <h3 className="text-xl font-bold mb-4" style={{ color: '#8a2be2' }}>📊 {asset} Price Chart</h3>

      {/* Simple Line Chart */}
      <div className="relative" style={{ height: '300px', background: 'rgba(0, 0, 0, 0.4)', borderRadius: '8px', padding: '1rem' }}>
        <svg width="100%" height="100%" style={{ overflow: 'visible' }}>
          {/* Price Line */}
          <polyline
            points={priceHistory
              .map((price, i) => {
                const x = (i / (priceHistory.length - 1)) * 100;
                const y = 100 - ((price - minPrice) / priceRange) * 90;
                return `${x},${y}`;
              })
              .join(' ')}
            fill="none"
            stroke="#8a2be2"
            strokeWidth="2"
            vectorEffect="non-scaling-stroke"
          />
          
          {/* Price Points */}
          {priceHistory.slice(-20).map((price, i) => {
            const totalPoints = priceHistory.length;
            const actualIndex = totalPoints - 20 + i;
            const x = (actualIndex / (totalPoints - 1)) * 100;
            const y = 100 - ((price - minPrice) / priceRange) * 90;
            
            return (
              <circle
                key={i}
                cx={`${x}%`}
                cy={`${y}%`}
                r="3"
                fill="#8a2be2"
                className="pulse"
              />
            );
          })}
        </svg>

        {/* Price Labels */}
        <div className="absolute top-2 left-2 text-xs text-gray-400">
          High: ${maxPrice.toFixed(2)}
        </div>
        <div className="absolute bottom-2 left-2 text-xs text-gray-400">
          Low: ${minPrice.toFixed(2)}
        </div>
        <div className="absolute top-2 right-2 text-lg font-bold" style={{ color: '#8a2be2' }}>
          ${priceHistory[priceHistory.length - 1].toFixed(2)}
        </div>
      </div>

      {/* EM Index Indicator (NEW!) */}
      <div className="mt-4 p-3 rounded" style={{ background: 'rgba(255, 165, 0, 0.1)', border: '1px solid rgba(255, 165, 0, 0.3)' }}>
        <div className="flex items-center justify-between">
          <div>
            <div className="text-xs text-gray-400">☀️ Solar EM Influence</div>
            <div className="text-sm mt-1">
              {candlesticks.length > 0 && (
                <span style={{ color: '#ffa500' }}>
                  EM Index: {candlesticks[candlesticks.length - 1]?.electromagnetic_index.toFixed(1)}
                </span>
              )}
            </div>
          </div>
          <div className="text-2xl">☀️</div>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-3 mt-4 text-center text-sm">
        <div>
          <div className="text-gray-400">Data Points</div>
          <div className="text-white font-semibold mt-1">{priceHistory.length}</div>
        </div>
        <div>
          <div className="text-gray-400">Change</div>
          <div className="text-white font-semibold mt-1">
            {((priceHistory[priceHistory.length - 1] - priceHistory[0]) / priceHistory[0] * 100).toFixed(2)}%
          </div>
        </div>
        <div>
          <div className="text-gray-400">Volatility</div>
          <div className="text-white font-semibold mt-1">
            {((priceRange / minPrice) * 100).toFixed(1)}%
          </div>
        </div>
      </div>
    </div>
  );
};

export default CandlestickChart;