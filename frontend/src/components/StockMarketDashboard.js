import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import TradingTerminal from './TradingTerminal';
import CandlestickChart from './CandlestickChart';
import SolarDashboard from './SolarDashboard';
import OrderBookView from './OrderBookView';
import AssetGrid from './AssetGrid';
import TraderLeaderboard from './TraderLeaderboard';
import TradeFeed from './TradeFeed';

const StockMarketDashboard = ({ api }) => {
  const [selectedAsset, setSelectedAsset] = useState('CMPT');
  const [marketData, setMarketData] = useState(null);
  const [solarData, setSolarData] = useState(null);
  const [traders, setTraders] = useState([]);
  const [userTrader, setUserTrader] = useState(null);
  const [marketRunning, setMarketRunning] = useState(false);
  const [loading, setLoading] = useState(true);

  const fetchMarketData = async () => {
    try {
      const [marketRes, solarRes, tradersRes] = await Promise.all([
        fetch(`${api}/market/overview`),
        fetch(`${api}/market/solar`),
        fetch(`${api}/market/traders`)
      ]);
      
      const marketData = await marketRes.json();
      const solarData = await solarRes.json();
      const tradersData = await tradersRes.json();
      
      setMarketData(marketData);
      setSolarData(solarData);
      setTraders(tradersData.traders || []);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching market data:', error);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMarketData();
    const interval = setInterval(fetchMarketData, 3000);
    return () => clearInterval(interval);
  }, [api]);

  const startMarket = async () => {
    try {
      await fetch(`${api}/market/start?interval=3.0`, { method: 'POST' });
      setMarketRunning(true);
    } catch (error) {
      console.error('Error starting market:', error);
    }
  };

  const stopMarket = async () => {
    try {
      await fetch(`${api}/market/stop`, { method: 'POST' });
      setMarketRunning(false);
    } catch (error) {
      console.error('Error stopping market:', error);
    }
  };

  const createUserTrader = async () => {
    const traderId = `human_${Date.now()}`;
    try {
      const response = await fetch(
        `${api}/market/trader/create?trader_id=${traderId}&name=Human%20Trader&initial_capital=100000`,
        { method: 'POST' }
      );
      const data = await response.json();
      setUserTrader(data);
      await fetchMarketData();
    } catch (error) {
      console.error('Error creating trader:', error);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="text-6xl mb-4">📈</div>
          <div className="text-2xl font-bold" style={{ color: '#8a2be2' }}>Loading ÆTHER-MARKET...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen p-6" style={{ background: 'linear-gradient(135deg, #0a0a0a 0%, #1a0f2e 50%, #0a0514 100%)' }}>
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <Link to="/" className="text-gray-400 hover:text-white text-sm mb-2 block">← Back to Network</Link>
          <h1 className="text-4xl font-bold glow-text" style={{ color: '#8a2be2' }}>
            📈 ÆTHER-MARKET
          </h1>
          <p className="text-gray-400 mt-1">AI Stock Exchange • Solar-Influenced Trading</p>
        </div>
        
        <div className="flex gap-3">
          {!marketRunning ? (
            <button
              onClick={startMarket}
              className="void-button"
              style={{ background: 'linear-gradient(135deg, #00ff00 0%, #00cc00 100%)' }}
              data-testid="start-market-btn"
            >
              ▶ Start Market
            </button>
          ) : (
            <button
              onClick={stopMarket}
              className="void-button"
              style={{ background: 'linear-gradient(135deg, #ff0000 0%, #cc0000 100%)' }}
              data-testid="stop-market-btn"
            >
              ⏹ Stop Market
            </button>
          )}
          
          {!userTrader && (
            <button
              onClick={createUserTrader}
              className="void-button"
              data-testid="create-trader-btn"
            >
              + Create Trader Account
            </button>
          )}
        </div>
      </div>

      {/* Solar Activity Dashboard */}
      {solarData && <SolarDashboard solarData={solarData} />}

      {/* Asset Grid */}
      {marketData && (
        <AssetGrid 
          assets={marketData.assets} 
          selectedAsset={selectedAsset}
          onSelectAsset={setSelectedAsset}
        />
      )}

      {/* Main Trading Interface */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6">
        {/* Left Column - Chart & Order Book */}
        <div className="lg:col-span-2 space-y-6">
          <CandlestickChart api={api} asset={selectedAsset} />
          <OrderBookView api={api} asset={selectedAsset} />
        </div>

        {/* Right Column - Trading Terminal & Trade Feed */}
        <div className="space-y-6">
          <TradingTerminal 
            api={api} 
            asset={selectedAsset}
            userTrader={userTrader}
            onTradeComplete={fetchMarketData}
          />
          <TradeFeed api={api} asset={selectedAsset} />
        </div>
      </div>

      {/* Trader Leaderboard */}
      <TraderLeaderboard traders={traders} />
    </div>
  );
};

export default StockMarketDashboard;