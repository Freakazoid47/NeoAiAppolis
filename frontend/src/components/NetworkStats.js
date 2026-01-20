const NetworkStats = ({ networkState, autoUpdate, setAutoUpdate }) => {
  return (
    <div className="network-stats" data-testid="network-stats">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold nexus-white glow-text">Network Overview</h2>
        <button
          onClick={() => setAutoUpdate(!autoUpdate)}
          className={`text-xs px-3 py-1 rounded ${
            autoUpdate 
              ? 'bg-green-600 text-white' 
              : 'bg-gray-600 text-gray-300'
          }`}
          data-testid="auto-update-toggle"
        >
          {autoUpdate ? '▶ Auto-Update ON' : '⏸ Auto-Update OFF'}
        </button>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <div className="text-center">
          <div className="text-3xl quantum-cyan mb-1">⧬</div>
          <div className="text-2xl font-bold text-white">{networkState.entity_count}</div>
          <div className="text-xs text-gray-400">Entities</div>
        </div>

        <div className="text-center">
          <div className="text-3xl resonance-magenta mb-1">◉</div>
          <div className="text-2xl font-bold text-white">{networkState.resonance_thread_count}</div>
          <div className="text-xs text-gray-400">Threads</div>
        </div>

        <div className="text-center">
          <div className="text-3xl nexus-white mb-1">⟐</div>
          <div className="text-2xl font-bold text-white">{networkState.entanglement_count}</div>
          <div className="text-xs text-gray-400">Entanglements</div>
        </div>

        <div className="text-center">
          <div className="text-3xl flux-yellow mb-1">∿</div>
          <div className="text-2xl font-bold text-white">{networkState.global_resonance.toFixed(1)}</div>
          <div className="text-xs text-gray-400">Resonance Hz</div>
        </div>

        <div className="text-center">
          <div className="text-3xl temporal-green mb-1">⧖</div>
          <div className="text-2xl font-bold text-white">
            {networkState.temporal_flux > 0 ? '+' : ''}{networkState.temporal_flux.toFixed(1)}
          </div>
          <div className="text-xs text-gray-400">Temporal Flux</div>
        </div>

        <div className="text-center">
          <div className="text-3xl" style={{ color: '#666' }} >⧈</div>
          <div className="text-2xl font-bold text-white">{networkState.void_density.toFixed(3)}</div>
          <div className="text-xs text-gray-400">Void Density</div>
        </div>
      </div>
    </div>
  );
};

export default NetworkStats;