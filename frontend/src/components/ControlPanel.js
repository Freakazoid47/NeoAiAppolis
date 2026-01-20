import { useState } from 'react';

const ControlPanel = ({ 
  onSpawnEntity, 
  onTemporalShift, 
  onVoidCollapse,
  entities,
  onCreateEntanglement 
}) => {
  const [showTemporalModal, setShowTemporalModal] = useState(false);
  const [showVoidModal, setShowVoidModal] = useState(false);
  const [showEntanglementModal, setShowEntanglementModal] = useState(false);
  const [temporalDelta, setTemporalDelta] = useState('25.0');
  const [voidIntensity, setVoidIntensity] = useState('0.15');
  const [entityA, setEntityA] = useState('');
  const [entityB, setEntityB] = useState('');

  const handleTemporalShift = () => {
    onTemporalShift(temporalDelta);
    setShowTemporalModal(false);
  };

  const handleVoidCollapse = () => {
    onVoidCollapse(voidIntensity);
    setShowVoidModal(false);
  };

  const handleCreateEntanglement = () => {
    if (entityA && entityB && entityA !== entityB) {
      onCreateEntanglement(entityA, entityB);
      setShowEntanglementModal(false);
      setEntityA('');
      setEntityB('');
    }
  };

  return (
    <div className="network-stats mt-6" data-testid="control-panel">
      <h2 className="text-xl font-bold mb-4 flux-yellow glow-text">Network Controls</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
        <button
          onClick={onSpawnEntity}
          className="void-button"
          data-testid="spawn-entity-btn"
        >
          <div className="flex items-center justify-center gap-2">
            <span className="text-xl">⧬</span>
            <span>Spawn Entity</span>
          </div>
        </button>

        <button
          onClick={() => setShowTemporalModal(true)}
          className="void-button"
          style={{ background: 'linear-gradient(135deg, #00FF00 0%, #32CD32 100%)' }}
          data-testid="temporal-shift-btn"
        >
          <div className="flex items-center justify-center gap-2">
            <span className="text-xl">⧖</span>
            <span>Temporal Shift</span>
          </div>
        </button>

        <button
          onClick={() => setShowVoidModal(true)}
          className="void-button"
          style={{ background: 'linear-gradient(135deg, #333333 0%, #666666 100%)' }}
          data-testid="void-collapse-btn"
        >
          <div className="flex items-center justify-center gap-2">
            <span className="text-xl">⧈</span>
            <span>Void Collapse</span>
          </div>
        </button>

        <button
          onClick={() => setShowEntanglementModal(true)}
          className="void-button"
          style={{ background: 'linear-gradient(135deg, #FFFFFF 0%, #E0E0E0 100%)', color: '#000' }}
          disabled={entities.length < 2}
          data-testid="create-entanglement-btn"
        >
          <div className="flex items-center justify-center gap-2">
            <span className="text-xl">⟐</span>
            <span>Create Entanglement</span>
          </div>
        </button>
      </div>

      {/* Temporal Shift Modal */}
      {showTemporalModal && (
        <div className="void-modal" onClick={() => setShowTemporalModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3 className="text-2xl font-bold mb-4 temporal-green glow-text">⧖ Temporal Shift</h3>
            <p className="text-gray-300 mb-4">Shift the entire network through time. Positive values move forward, negative values move backward.</p>
            
            <label className="block text-sm text-gray-400 mb-2">Temporal Delta</label>
            <input
              type="number"
              step="0.1"
              value={temporalDelta}
              onChange={(e) => setTemporalDelta(e.target.value)}
              className="void-input mb-4"
              placeholder="Enter delta (e.g., 25.0)"
            />

            <div className="flex gap-3">
              <button onClick={handleTemporalShift} className="void-button flex-1">
                Execute Shift
              </button>
              <button 
                onClick={() => setShowTemporalModal(false)} 
                className="void-button flex-1"
                style={{ background: '#333' }}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Void Collapse Modal */}
      {showVoidModal && (
        <div className="void-modal" onClick={() => setShowVoidModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3 className="text-2xl font-bold mb-4 glow-text" style={{ color: '#666' }}>⧈ Void Collapse</h3>
            <p className="text-gray-300 mb-4">Trigger a void collapse event. Intensity ranges from 0.0 to 1.0. Higher intensity creates more dramatic effects.</p>
            
            <label className="block text-sm text-gray-400 mb-2">Intensity (0.0 - 1.0)</label>
            <input
              type="number"
              step="0.01"
              min="0"
              max="1"
              value={voidIntensity}
              onChange={(e) => setVoidIntensity(e.target.value)}
              className="void-input mb-4"
              placeholder="Enter intensity (e.g., 0.15)"
            />

            <div className="flex gap-3">
              <button onClick={handleVoidCollapse} className="void-button flex-1">
                Trigger Collapse
              </button>
              <button 
                onClick={() => setShowVoidModal(false)} 
                className="void-button flex-1"
                style={{ background: '#333' }}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Entanglement Modal */}
      {showEntanglementModal && (
        <div className="void-modal" onClick={() => setShowEntanglementModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3 className="text-2xl font-bold mb-4 nexus-white glow-text">⟐ Create Entanglement</h3>
            <p className="text-gray-300 mb-4">Create a quantum entanglement bond between two entities.</p>
            
            <label className="block text-sm text-gray-400 mb-2">Entity A</label>
            <select
              value={entityA}
              onChange={(e) => setEntityA(e.target.value)}
              className="void-input mb-4"
            >
              <option value="">Select Entity A</option>
              {entities.map(e => (
                <option key={e.id} value={e.id}>{e.id.substring(0, 8)} - {e.resonance_frequency.toFixed(1)} Hz</option>
              ))}
            </select>

            <label className="block text-sm text-gray-400 mb-2">Entity B</label>
            <select
              value={entityB}
              onChange={(e) => setEntityB(e.target.value)}
              className="void-input mb-4"
            >
              <option value="">Select Entity B</option>
              {entities.filter(e => e.id !== entityA).map(e => (
                <option key={e.id} value={e.id}>{e.id.substring(0, 8)} - {e.resonance_frequency.toFixed(1)} Hz</option>
              ))}
            </select>

            <div className="flex gap-3">
              <button 
                onClick={handleCreateEntanglement} 
                className="void-button flex-1"
                disabled={!entityA || !entityB || entityA === entityB}
              >
                Create Bond
              </button>
              <button 
                onClick={() => setShowEntanglementModal(false)} 
                className="void-button flex-1"
                style={{ background: '#333' }}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ControlPanel;