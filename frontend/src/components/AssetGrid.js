const AssetGrid = ({ assets, selectedAsset, onSelectAsset }) => {
  const assetInfo = {
    CMPT: { name: 'Computing Power', icon: '💻', unit: 'GHz' },
    HASH: { name: 'Hash Power', icon: '#️⃣', unit: 'H/s' },
    MEM: { name: 'Memory Bandwidth', icon: '🧠', unit: 'GB/s' },
    RES: { name: 'Resonance Points', icon: '◉', unit: 'RP' },
    CONS: { name: 'Consciousness Units', icon: '🧠', unit: 'CU' },
    QBIT: { name: 'Quantum Processing', icon: '⚛️', unit: 'QPU' },
    BAND: { name: 'Network Bandwidth', icon: '🌐', unit: 'Mbps' }
  };

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-4 mb-6">
      {Object.entries(assets).map(([symbol, data]) => {
        const info = assetInfo[symbol];
        const isSelected = symbol === selectedAsset;
        const changeColor = data.change_24h >= 0 ? '#00ff00' : '#ff0000';

        return (
          <button
            key={symbol}
            onClick={() => onSelectAsset(symbol)}
            className={`game-card text-left p-4 ${
              isSelected ? 'ring-2 ring-purple-500' : ''
            }`}
            data-testid={`asset-${symbol}`}
          >
            <div className="text-3xl mb-2">{info.icon}</div>
            <div className="text-xs text-gray-400 mb-1">{symbol}</div>
            <div className="text-lg font-bold text-white mb-1">
              ${data.current_price.toFixed(2)}
            </div>
            <div className="text-xs" style={{ color: changeColor }}>
              {data.change_24h >= 0 ? '▲' : '▼'} {Math.abs(data.change_24h).toFixed(2)}%
            </div>
            <div className="text-[10px] text-gray-500 mt-2">{info.name}</div>
          </button>
        );
      })}
    </div>
  );
};

export default AssetGrid;