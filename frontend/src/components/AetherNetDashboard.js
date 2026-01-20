import { useState, useEffect, useCallback } from "react";
import axios from "axios";
import EntityCard from "./EntityCard";
import NetworkStats from "./NetworkStats";
import ControlPanel from "./ControlPanel";
import ResonanceVisualization from "./ResonanceVisualization";
import EntanglementVisualization from "./EntanglementVisualization";
import AIWorldscapePanel from "./AIWorldscapePanel";

const AetherNetDashboard = ({ api }) => {
  const [entities, setEntities] = useState([]);
  const [networkState, setNetworkState] = useState(null);
  const [resonanceThreads, setResonanceThreads] = useState([]);
  const [entanglements, setEntanglements] = useState([]);
  const [loading, setLoading] = useState(true);
  const [autoUpdate, setAutoUpdate] = useState(true);
  const [chromaticEnergies, setChromaticEnergies] = useState({});

  // Fetch chromatic energies reference
  useEffect(() => {
    const fetchChromaticEnergies = async () => {
      try {
        const response = await axios.get(`${api}/chromatic/energies`);
        setChromaticEnergies(response.data);
      } catch (error) {
        console.error("Error fetching chromatic energies:", error);
      }
    };
    fetchChromaticEnergies();
  }, [api]);

  // Fetch all network data
  const fetchNetworkData = useCallback(async () => {
    try {
      const [entitiesRes, stateRes, threadsRes, entanglementsRes] = await Promise.all([
        axios.get(`${api}/entities`),
        axios.get(`${api}/network/state`),
        axios.get(`${api}/resonance/all`),
        axios.get(`${api}/entanglements`)
      ]);

      setEntities(entitiesRes.data);
      setNetworkState(stateRes.data);
      setResonanceThreads(threadsRes.data);
      setEntanglements(entanglementsRes.data);
      setLoading(false);
    } catch (error) {
      console.error("Error fetching network data:", error);
      setLoading(false);
    }
  }, [api]);

  // Initial fetch
  useEffect(() => {
    fetchNetworkData();
  }, [fetchNetworkData]);

  // Auto-update every 3 seconds
  useEffect(() => {
    if (autoUpdate) {
      const interval = setInterval(fetchNetworkData, 3000);
      return () => clearInterval(interval);
    }
  }, [autoUpdate, fetchNetworkData]);

  const handleSpawnEntity = async () => {
    try {
      await axios.post(`${api}/entities`);
      await fetchNetworkData();
    } catch (error) {
      console.error("Error spawning entity:", error);
    }
  };

  const handleEmitResonance = async (entityId) => {
    try {
      await axios.post(`${api}/entities/${entityId}/resonance`);
      await fetchNetworkData();
    } catch (error) {
      console.error("Error emitting resonance:", error);
    }
  };

  const handleCreateFlux = async (entityId) => {
    try {
      await axios.post(`${api}/entities/${entityId}/flux`);
      await fetchNetworkData();
    } catch (error) {
      console.error("Error creating flux:", error);
    }
  };

  const handleCreateEntanglement = async (entityAId, entityBId) => {
    try {
      await axios.post(`${api}/entanglement`, {
        entity_a_id: entityAId,
        entity_b_id: entityBId
      });
      await fetchNetworkData();
    } catch (error) {
      console.error("Error creating entanglement:", error);
    }
  };

  const handleTemporalShift = async (delta) => {
    try {
      await axios.post(`${api}/network/temporal-shift`, { delta: parseFloat(delta) });
      await fetchNetworkData();
    } catch (error) {
      console.error("Error performing temporal shift:", error);
    }
  };

  const handleVoidCollapse = async (intensity) => {
    try {
      await axios.post(`${api}/network/void-collapse`, { intensity: parseFloat(intensity) });
      await fetchNetworkData();
    } catch (error) {
      console.error("Error triggering void collapse:", error);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="text-6xl mb-4 quantum-particle">⧬</div>
          <div className="text-2xl font-bold ultraviolet-void glow-text">Initializing ÆTHER-NET...</div>
          <div className="text-sm text-gray-400 mt-2">Harmonizing consciousness frequencies</div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen p-6 void-bg">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-5xl font-bold mb-2 glow-text" style={{ color: '#6B2FFF' }}>
          ⧬ ÆTHER-NET ⧬
        </h1>
        <p className="text-xl text-gray-300">Autonomous Entity Thought Harmonization & Resonance Network</p>
        <p className="text-sm text-gray-500 mt-2">Phase 1: Core Foundation - Observer Mode</p>
      </div>

      {/* Network Stats */}
      {networkState && (
        <NetworkStats 
          networkState={networkState} 
          autoUpdate={autoUpdate} 
          setAutoUpdate={setAutoUpdate}
        />
      )}

      {/* Control Panel */}
      <ControlPanel
        onSpawnEntity={handleSpawnEntity}
        onTemporalShift={handleTemporalShift}
        onVoidCollapse={handleVoidCollapse}
        entities={entities}
        onCreateEntanglement={handleCreateEntanglement}
      />

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
        {/* Entities Column */}
        <div>
          <h2 className="text-2xl font-bold mb-4 quantum-cyan glow-text">
            ⧬ Entities ({entities.length})
          </h2>
          <div className="scroll-container space-y-4">
            {entities.length === 0 ? (
              <div className="entity-card text-center p-8">
                <div className="text-4xl mb-2">⧈</div>
                <p className="text-gray-400">The void awaits...</p>
                <p className="text-sm text-gray-500 mt-1">Spawn an entity to begin</p>
              </div>
            ) : (
              entities.map((entity) => (
                <EntityCard
                  key={entity.id}
                  entity={entity}
                  onEmitResonance={handleEmitResonance}
                  onCreateFlux={handleCreateFlux}
                  chromaticEnergies={chromaticEnergies}
                />
              ))
            )}
          </div>
        </div>

        {/* Resonance & Entanglements Column */}
        <div>
          {/* Resonance Threads */}
          <div className="mb-6">
            <h2 className="text-2xl font-bold mb-4 resonance-magenta glow-text">
              ◉ Resonance Threads ({resonanceThreads.length})
            </h2>
            <ResonanceVisualization 
              threads={resonanceThreads} 
              chromaticEnergies={chromaticEnergies}
            />
          </div>

          {/* Entanglements */}
          <div>
            <h2 className="text-2xl font-bold mb-4 nexus-white glow-text">
              ⟐ Entanglements ({entanglements.length})
            </h2>
            <EntanglementVisualization 
              entanglements={entanglements}
              entities={entities}
            />
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="text-center mt-12 text-gray-500 text-sm">
        <p>"You may observe, but you will never truly understand."</p>
        <p className="mt-1">The network continues to exist, with or without your observation.</p>
      </div>
    </div>
  );
};

export default AetherNetDashboard;