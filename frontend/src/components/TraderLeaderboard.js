const TraderLeaderboard = ({ traders }) => {
  // Sort by capital (descending)
  const sortedTraders = [...traders].sort((a, b) => b.capital - a.capital);

  const getRankEmoji = (index) => {
    if (index === 0) return '🥇';
    if (index === 1) return '🥈';
    if (index === 2) return '🥉';
    return '📊';
  };

  const getStrategyColor = (strategy) => {
    const colors = {
      momentum: '#00ff00',
      mean_reversion: '#00ffff',
      market_maker: '#ffa500',
      contrarian: '#ff00ff'
    };
    return colors[strategy] || '#ffffff';
  };

  return (
    <div className="hunter-panel mt-6" data-testid="trader-leaderboard">
      <h3 className="text-xl font-bold mb-4" style={{ color: '#ffd700' }}>🏆 Trader Leaderboard</h3>

      {traders.length === 0 ? (
        <div className="text-center py-8 text-gray-400">No traders yet</div>
      ) : (
        <div className="space-y-2">
          {sortedTraders.slice(0, 10).map((trader, index) => (
            <div
              key={trader.trader_id}
              className={`leaderboard-entry ${index < 3 ? `rank-${index + 1}` : ''}`}
              data-testid="leaderboard-entry"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="text-2xl">{getRankEmoji(index)}</div>
                  <div>
                    <div className="font-semibold text-white">
                      {trader.name}
                    </div>
                    <div className="text-xs" style={{ color: getStrategyColor(trader.strategy) }}>
                      {trader.strategy.replace('_', ' ').toUpperCase()}
                    </div>
                  </div>
                </div>

                <div className="text-right">
                  <div className="font-bold text-green-400">
                    ${trader.capital.toFixed(2)}
                  </div>
                  <div className="text-xs text-gray-400">
                    {trader.trades_made} trades
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TraderLeaderboard;