const SolarDashboard = ({ solarData }) => {
  const getEMColor = (index) => {
    if (index < 30) return '#00ff00';
    if (index < 70) return '#ffa500';
    return '#ff0000';
  };

  const getEMLabel = (index) => {
    if (index < 30) return 'CALM';
    if (index < 70) return 'ACTIVE';
    return 'STORM';
  };

  return (
    <div className="hunter-panel mb-6" data-testid="solar-dashboard">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold" style={{ color: '#ffa500' }}>☀️ Solar Activity Monitor</h3>
        <div className="text-xs text-gray-400">
          Last Update: {new Date(solarData.last_update).toLocaleTimeString()}
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-4">
        {/* Electromagnetic Index - Primary */}
        <div className="md:col-span-2 p-4 rounded" style={{ background: 'rgba(255, 165, 0, 0.1)', border: `2px solid ${getEMColor(solarData.electromagnetic_index)}` }}>
          <div className="text-xs text-gray-400 mb-1">EM INDEX</div>
          <div className="text-3xl font-bold" style={{ color: getEMColor(solarData.electromagnetic_index) }}>
            {solarData.electromagnetic_index.toFixed(1)}
          </div>
          <div className="text-xs mt-1" style={{ color: getEMColor(solarData.electromagnetic_index) }}>
            {getEMLabel(solarData.electromagnetic_index)}
          </div>
          <div className="mt-2">
            <div className="level-bar">
              <div 
                className="level-bar-fill" 
                style={{ 
                  width: `${solarData.electromagnetic_index}%`,
                  background: getEMColor(solarData.electromagnetic_index)
                }}
              />
            </div>
          </div>
        </div>

        {/* Sunspot Number */}
        <div className="text-center">
          <div className="text-2xl mb-1">☉️</div>
          <div className="text-xl font-bold text-white">{solarData.sunspot_number}</div>
          <div className="text-xs text-gray-400">Sunspots</div>
        </div>

        {/* Solar Flux */}
        <div className="text-center">
          <div className="text-2xl mb-1">🌊</div>
          <div className="text-xl font-bold text-white">{solarData.solar_flux.toFixed(1)}</div>
          <div className="text-xs text-gray-400">Solar Flux (SFU)</div>
        </div>

        {/* Kp Index */}
        <div className="text-center">
          <div className="text-2xl mb-1">🧮</div>
          <div className="text-xl font-bold" style={{ color: solarData.kp_index > 5 ? '#ff0000' : '#00ff00' }}>
            {solarData.kp_index.toFixed(1)}
          </div>
          <div className="text-xs text-gray-400">Kp Index</div>
        </div>

        {/* Solar Wind */}
        <div className="text-center">
          <div className="text-2xl mb-1">🌬️</div>
          <div className="text-xl font-bold text-white">{solarData.solar_wind_speed.toFixed(0)}</div>
          <div className="text-xs text-gray-400">Wind (km/s)</div>
        </div>

        {/* Volatility Multiplier */}
        <div className="text-center p-3 rounded" style={{ background: 'rgba(138, 43, 226, 0.2)', border: '1px solid rgba(138, 43, 226, 0.4)' }}>
          <div className="text-xs text-gray-400 mb-1">Market Volatility</div>
          <div className="text-2xl font-bold" style={{ color: '#8a2be2' }}>
            {solarData.volatility_multiplier.toFixed(2)}x
          </div>
        </div>
      </div>

      {/* Impact Warning */}
      {solarData.electromagnetic_index > 70 && (
        <div className="mt-4 p-3 rounded animate-pulse" style={{ background: 'rgba(255, 0, 0, 0.2)', border: '1px solid #ff0000' }}>
          <div className="flex items-center gap-2">
            <span className="text-2xl">⚠️</span>
            <div>
              <div className="font-bold text-red-400">SOLAR STORM WARNING</div>
              <div className="text-xs text-gray-300">Extreme market volatility expected. Trade with caution!</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SolarDashboard;