const EntityCard = ({ entity, onEmitResonance, onCreateFlux, chromaticEnergies }) => {
  const getEnergyColor = (energyName) => {
    const energy = chromaticEnergies[energyName];
    return energy ? energy.primary_color : '#FFFFFF';
  };

  const getEnergyDescription = (energyName) => {
    const energy = chromaticEnergies[energyName];
    return energy ? energy.description : '';
  };

  return (
    <div className="entity-card" data-testid="entity-card">
      {/* Header with chromatic blend */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <span className="text-2xl">⧬</span>
          <div>
            <div className="font-mono text-sm text-gray-400">Entity</div>
            <div className="font-mono text-xs" style={{ color: getEnergyColor(entity.chromatic_blend[0]) }}>
              {entity.id.substring(0, 8)}
            </div>
          </div>
        </div>
        <div className="flex gap-1">
          {entity.chromatic_blend.map((energy, idx) => (
            <div
              key={idx}
              className="w-3 h-3 rounded-full"
              style={{ backgroundColor: getEnergyColor(energy) }}
              title={getEnergyDescription(energy)}
            />
          ))}
        </div>
      </div>

      {/* Stats */}
      <div className="space-y-2 mb-3">
        {/* Resonance Frequency */}
        <div>
          <div className="flex justify-between text-xs mb-1">
            <span className="quantum-cyan">Resonance</span>
            <span className="text-gray-400">{entity.resonance_frequency.toFixed(1)} Hz</span>
          </div>
          <div className="chromatic-bar">
            <div
              className="chromatic-fill"
              style={{
                width: `${(entity.resonance_frequency / 1000) * 100}%`,
                background: 'linear-gradient(90deg, #00FFFF, #0080FF)'
              }}
            />
          </div>
        </div>

        {/* Void Depth */}
        <div>
          <div className="flex justify-between text-xs mb-1">
            <span className="void-black" style={{ color: '#999' }}>Void Depth</span>
            <span className="text-gray-400">{entity.void_depth.toFixed(2)}</span>
          </div>
          <div className="chromatic-bar">
            <div
              className="chromatic-fill"
              style={{
                width: `${entity.void_depth * 100}%`,
                background: 'linear-gradient(90deg, #333, #666)'
              }}
            />
          </div>
        </div>

        {/* Temporal Position */}
        <div className="flex justify-between text-xs">
          <span className="temporal-green">Temporal Position</span>
          <span className="text-gray-400">{entity.temporal_position > 0 ? '+' : ''}{entity.temporal_position.toFixed(1)} ⧖</span>
        </div>
      </div>

      {/* Activity Stats */}
      <div className="grid grid-cols-3 gap-2 mb-3 text-center text-xs">
        <div className="bg-black bg-opacity-30 rounded p-2">
          <div className="resonance-magenta">◉</div>
          <div className="text-gray-400 mt-1">{entity.resonance_thread_count}</div>
          <div className="text-gray-500 text-[10px]">Threads</div>
        </div>
        <div className="bg-black bg-opacity-30 rounded p-2">
          <div className="flux-yellow">∿</div>
          <div className="text-gray-400 mt-1">{entity.flux_stream_count}</div>
          <div className="text-gray-500 text-[10px]">Streams</div>
        </div>
        <div className="bg-black bg-opacity-30 rounded p-2">
          <div className="nexus-white">⟐</div>
          <div className="text-gray-400 mt-1">{entity.entanglement_count}</div>
          <div className="text-gray-500 text-[10px]">Bonds</div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex gap-2">
        <button
          onClick={() => onEmitResonance(entity.id)}
          className="flex-1 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white text-xs py-2 px-3 rounded transition-all"
          data-testid="emit-resonance-btn"
        >
          ◉ Emit Resonance
        </button>
        <button
          onClick={() => onCreateFlux(entity.id)}
          className="flex-1 bg-gradient-to-r from-yellow-600 to-green-600 hover:from-yellow-700 hover:to-green-700 text-white text-xs py-2 px-3 rounded transition-all"
          data-testid="create-flux-btn"
        >
          ∿ Create Flux
        </button>
      </div>
    </div>
  );
};

export default EntityCard;