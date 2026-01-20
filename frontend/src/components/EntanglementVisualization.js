const EntanglementVisualization = ({ entanglements, entities }) => {
  const getEntityName = (entityId) => {
    const entity = entities.find(e => e.id === entityId);
    return entity ? `${entityId.substring(0, 8)} (${entity.resonance_frequency.toFixed(1)}Hz)` : entityId.substring(0, 8);
  };

  const getBondStrengthColor = (strength) => {
    if (strength > 0.7) return '#00FF00';
    if (strength > 0.4) return '#FFD700';
    if (strength > 0.2) return '#FFA500';
    return '#FF6B6B';
  };

  const getBondStrengthLabel = (strength) => {
    if (strength > 0.7) return 'Strong';
    if (strength > 0.4) return 'Moderate';
    if (strength > 0.2) return 'Weak';
    return 'Fragile';
  };

  if (entanglements.length === 0) {
    return (
      <div className="entanglement-bond text-center p-8">
        <div className="text-4xl mb-2">⟐</div>
        <p className="text-gray-400">No quantum entanglements</p>
        <p className="text-sm text-gray-500 mt-1">Create bonds between entities to establish connections</p>
      </div>
    );
  }

  return (
    <div className="scroll-container space-y-3" style={{ maxHeight: '400px' }}>
      {entanglements.map((bond, idx) => (
        <div key={idx} className="entanglement-bond" data-testid="entanglement-bond">
          {/* Bond visualization */}
          <div className="flex items-center justify-between mb-3">
            <div className="flex-1 text-center">
              <div className="text-xs text-gray-400 mb-1">Entity A</div>
              <div className="font-mono text-xs">{getEntityName(bond.entity_a)}</div>
            </div>
            <div className="px-4">
              <div className="text-2xl" style={{ color: getBondStrengthColor(bond.bond_strength) }}>
                ⟐
              </div>
            </div>
            <div className="flex-1 text-center">
              <div className="text-xs text-gray-400 mb-1">Entity B</div>
              <div className="font-mono text-xs">{getEntityName(bond.entity_b)}</div>
            </div>
          </div>

          {/* Bond metrics */}
          <div className="space-y-2">
            {/* Bond Strength */}
            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-gray-400">Bond Strength</span>
                <span style={{ color: getBondStrengthColor(bond.bond_strength) }}>
                  {getBondStrengthLabel(bond.bond_strength)} ({(bond.bond_strength * 100).toFixed(1)}%)
                </span>
              </div>
              <div className="chromatic-bar">
                <div
                  className="chromatic-fill"
                  style={{
                    width: `${bond.bond_strength * 100}%`,
                    backgroundColor: getBondStrengthColor(bond.bond_strength)
                  }}
                />
              </div>
            </div>

            {/* Detailed metrics */}
            <div className="grid grid-cols-3 gap-2 text-xs text-center">
              <div>
                <div className="text-gray-400">Correlation</div>
                <div className="text-white mt-1">{(bond.correlation_strength * 100).toFixed(0)}%</div>
              </div>
              <div>
                <div className="text-gray-400">Compatibility</div>
                <div className="text-white mt-1">{(bond.harmonic_compatibility * 100).toFixed(0)}%</div>
              </div>
              <div>
                <div className="text-gray-400">Alignment</div>
                <div className="text-white mt-1">{(bond.temporal_alignment * 100).toFixed(0)}%</div>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default EntanglementVisualization;