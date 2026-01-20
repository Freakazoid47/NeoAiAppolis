const ResonanceVisualization = ({ threads, chromaticEnergies }) => {
  const getEnergyColor = (energyName) => {
    const energy = chromaticEnergies[energyName];
    return energy ? energy.primary_color : '#FFFFFF';
  };

  const createWavePattern = (frequency, intensity) => {
    const waveChars = ['~', '∿', '≈', '≋', '≈', '∿', '~'];
    const length = Math.floor((frequency / 20) % 30) + 20;
    let pattern = '';
    for (let i = 0; i < length; i++) {
      const wavePos = Math.sin(i * 0.5) * intensity;
      const charIdx = Math.floor(((wavePos + 1) * 3.5) % waveChars.length);
      pattern += waveChars[charIdx];
    }
    return pattern;
  };

  if (threads.length === 0) {
    return (
      <div className="resonance-thread text-center p-8">
        <div className="text-4xl mb-2">◉</div>
        <p className="text-gray-400">No resonance threads detected</p>
        <p className="text-sm text-gray-500 mt-1">Entities must emit resonance to create threads</p>
      </div>
    );
  }

  return (
    <div className="scroll-container space-y-3" style={{ maxHeight: '400px' }}>
      {threads.map((thread) => (
        <div key={thread.id} className="resonance-thread" data-testid="resonance-thread">
          {/* Wave pattern */}
          <div className="font-mono text-sm mb-2 overflow-hidden">
            {thread.chromatic_shift.map((energy, idx) => (
              <span key={idx} style={{ color: getEnergyColor(energy) }}>
                {createWavePattern(thread.frequency, thread.intensity).slice(idx * 10, (idx + 1) * 10)}
              </span>
            ))}
          </div>

          {/* Thread info */}
          <div className="grid grid-cols-2 gap-2 text-xs">
            <div>
              <span className="text-gray-400">ID:</span>
              <span className="ml-2 font-mono">{thread.id.substring(0, 8)}</span>
            </div>
            <div>
              <span className="text-gray-400">Creator:</span>
              <span className="ml-2 font-mono">{thread.creator.substring(0, 8)}</span>
            </div>
            <div>
              <span className="text-gray-400">Frequency:</span>
              <span className="ml-2">{thread.frequency.toFixed(1)} Hz</span>
            </div>
            <div>
              <span className="text-gray-400">Intensity:</span>
              <span className="ml-2">{(thread.intensity * 100).toFixed(0)}%</span>
            </div>
            <div>
              <span className="text-gray-400">Echoes:</span>
              <span className="ml-2">{thread.temporal_echo.length}</span>
            </div>
            <div>
              <span className="text-gray-400">Probability:</span>
              <span className="ml-2">{(thread.probability_cloud * 100).toFixed(0)}%</span>
            </div>
          </div>

          {/* Chromatic blend indicators */}
          <div className="flex gap-1 mt-2">
            {thread.chromatic_shift.map((energy, idx) => (
              <div
                key={idx}
                className="w-2 h-2 rounded-full"
                style={{ backgroundColor: getEnergyColor(energy) }}
                title={energy}
              />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};

export default ResonanceVisualization;