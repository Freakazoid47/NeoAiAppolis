import { useState } from 'react';

const AIWorldscapePanel = ({ api, onRefresh }) => {
  const [worldscapeStatus, setWorldscapeStatus] = useState({ running: false });
  const [aiAgents, setAIAgents] = useState([]);
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showEventsModal, setShowEventsModal] = useState(false);

  const fetchWorldscapeStatus = async () => {
    try {
      const response = await fetch(`${api}/worldscape/status`);
      const data = await response.json();
      setWorldscapeStatus(data);
    } catch (error) {
      console.error('Error fetching worldscape status:', error);
    }
  };

  const fetchAIAgents = async () => {
    try {
      const response = await fetch(`${api}/ai/agents`);
      const data = await response.json();
      setAIAgents(data);
    } catch (error) {
      console.error('Error fetching AI agents:', error);
    }
  };

  const fetchEvents = async () => {
    try {
      const [worldscapeRes, aiRes] = await Promise.all([
        fetch(`${api}/worldscape/events?count=10`),
        fetch(`${api}/ai/events?count=10`)
      ]);
      const worldscapeData = await worldscapeRes.json();
      const aiData = await aiRes.json();
      
      const combined = [
        ...worldscapeData.events.map(e => ({ type: 'worldscape', text: e })),
        ...aiData.events.map(e => ({ type: 'ai', text: e }))
      ].slice(-15);
      
      setEvents(combined);
    } catch (error) {
      console.error('Error fetching events:', error);
    }
  };

  const startWorldscape = async () => {
    setLoading(true);
    try {
      await fetch(`${api}/worldscape/start`, { method: 'POST' });
      await fetchWorldscapeStatus();
      await onRefresh();
    } catch (error) {
      console.error('Error starting worldscape:', error);
    }
    setLoading(false);
  };

  const stopWorldscape = async () => {
    setLoading(true);
    try {
      await fetch(`${api}/worldscape/stop`, { method: 'POST' });
      await fetchWorldscapeStatus();
    } catch (error) {
      console.error('Error stopping worldscape:', error);
    }
    setLoading(false);
  };

  const spawnAI = async (model) => {
    setLoading(true);
    try {
      const response = await fetch(`${api}/ai/spawn?model=${model}`, { method: 'POST' });
      const data = await response.json();
      await fetchAIAgents();
      await onRefresh();
      return data;
    } catch (error) {
      console.error('Error spawning AI:', error);
    }
    setLoading(false);
  };

  const aiPerceive = async (entityId) => {
    setLoading(true);
    try {
      const response = await fetch(`${api}/ai/${entityId}/perceive`, { method: 'POST' });
      const data = await response.json();
      await fetchEvents();
      return data.perception;
    } catch (error) {
      console.error('Error in AI perception:', error);
    }
    setLoading(false);
  };

  const aiAct = async (entityId) => {
    setLoading(true);
    try {
      const response = await fetch(`${api}/ai/${entityId}/act`, { method: 'POST' });
      const data = await response.json();
      await onRefresh();
      return data;
    } catch (error) {
      console.error('Error in AI action:', error);
    }
    setLoading(false);
  };

  return (
    <div className="space-y-4">
      {/* Worldscape Control */}
      <div className="network-stats">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-xl font-bold flux-yellow glow-text">✨ Worldscape Evolution</h3>
          <button
            onClick={fetchWorldscapeStatus}
            className="text-xs px-3 py-1 rounded bg-gray-700 hover:bg-gray-600"
          >
            Refresh Status
          </button>
        </div>
        
        <div className="grid grid-cols-3 gap-3 mb-4 text-center text-sm">
          <div>
            <div className="text-gray-400">Status</div>
            <div className={worldscapeStatus.running ? 'text-green-400' : 'text-gray-500'}>
              {worldscapeStatus.running ? '▶ Running' : '⏸ Stopped'}
            </div>
          </div>
          <div>
            <div className="text-gray-400">Cycles</div>
            <div className="text-white">{worldscapeStatus.cycle_count || 0}</div>
          </div>
          <div>
            <div className="text-gray-400">Events</div>
            <div className="text-white">{worldscapeStatus.event_count || 0}</div>
          </div>
        </div>

        <div className="flex gap-3">
          {!worldscapeStatus.running ? (
            <button
              onClick={startWorldscape}
              disabled={loading}
              className="flex-1 void-button"
              style={{ background: 'linear-gradient(135deg, #FFD700 0%, #FFA500 100%)' }}
              data-testid="start-worldscape-btn"
            >
              ▶ Start Evolution
            </button>
          ) : (
            <button
              onClick={stopWorldscape}
              disabled={loading}
              className="flex-1 void-button"
              style={{ background: 'linear-gradient(135deg, #FF6B6B 0%, #FF4444 100%)' }}
              data-testid="stop-worldscape-btn"
            >
              ⏹ Stop Evolution
            </button>
          )}
          <button
            onClick={() => { fetchEvents(); setShowEventsModal(true); }}
            className="flex-1 void-button"
            style={{ background: 'linear-gradient(135deg, #00FFFF 0%, #0080FF 100%)' }}
            data-testid="view-events-btn"
          >
            📜 View Events
          </button>
        </div>
      </div>

      {/* AI Spawning */}
      <div className="network-stats">
        <h3 className="text-xl font-bold mb-4" style={{ color: '#FF00FF' }} >🤖 Spawn AI Consciousness</h3>
        <p className="text-sm text-gray-400 mb-4">
          Summon AI entities from different models. Each has unique personality traits.
        </p>
        
        <div className="grid grid-cols-3 gap-3">
          <button
            onClick={() => spawnAI('gpt-5.2')}
            disabled={loading}
            className="void-button text-sm py-3"
            style={{ background: 'linear-gradient(135deg, #10a37f 0%, #1a7f64 100%)' }}
            data-testid="spawn-gpt-btn"
          >
            <div className="font-bold mb-1">GPT-5.2</div>
            <div className="text-xs opacity-75">Creative Explorer</div>
          </button>
          
          <button
            onClick={() => spawnAI('claude-sonnet-4.5')}
            disabled={loading}
            className="void-button text-sm py-3"
            style={{ background: 'linear-gradient(135deg, #d97757 0%, #c1553d 100%)' }}
            data-testid="spawn-claude-btn"
          >
            <div className="font-bold mb-1">Claude</div>
            <div className="text-xs opacity-75">Social Harmonizer</div>
          </button>
          
          <button
            onClick={() => spawnAI('gemini-3-flash')}
            disabled={loading}
            className="void-button text-sm py-3"
            style={{ background: 'linear-gradient(135deg, #4285f4 0%, #3367d6 100%)' }}
            data-testid="spawn-gemini-btn"
          >
            <div className="font-bold mb-1">Gemini</div>
            <div className="text-xs opacity-75">Void Wanderer</div>
          </button>
        </div>
      </div>

      {/* AI Agents List */}
      {aiAgents.length > 0 && (
        <div className="network-stats">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-bold resonance-magenta glow-text">🧠 Active AI Entities</h3>
            <button
              onClick={fetchAIAgents}
              className="text-xs px-3 py-1 rounded bg-gray-700 hover:bg-gray-600"
            >
              Refresh
            </button>
          </div>
          
          <div className="space-y-2 max-h-60 overflow-y-auto">
            {aiAgents.map((agent) => (
              <div key={agent.entity_id} className="bg-black bg-opacity-30 rounded p-3">
                <div className="flex items-center justify-between mb-2">
                  <div>
                    <div className="font-mono text-xs text-gray-400">{agent.entity_id.substring(0, 8)}</div>
                    <div className="font-bold text-sm">{agent.model}</div>
                  </div>
                  <div className="text-right text-xs">
                    <div className="text-gray-400">Interactions: {agent.interactions}</div>
                    <div className="text-gray-400">Memories: {agent.memory_count}</div>
                  </div>
                </div>
                
                <div className="flex gap-2 mt-2">
                  <button
                    onClick={async () => {
                      const perception = await aiPerceive(agent.entity_id);
                      if (perception) alert(`AI Perception:\n\n${perception}`);
                    }}
                    disabled={loading}
                    className="flex-1 text-xs py-1 rounded bg-purple-600 hover:bg-purple-700"
                  >
                    👁️ Perceive
                  </button>
                  <button
                    onClick={async () => {
                      const action = await aiAct(agent.entity_id);
                      if (action) console.log('AI Action:', action);
                    }}
                    disabled={loading}
                    className="flex-1 text-xs py-1 rounded bg-green-600 hover:bg-green-700"
                  >
                    ⚡ Act
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Events Modal */}
      {showEventsModal && (
        <div className="void-modal" onClick={() => setShowEventsModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3 className="text-2xl font-bold mb-4 flux-yellow glow-text">📜 Recent Events</h3>
            
            <div className="space-y-2 max-h-96 overflow-y-auto">
              {events.length === 0 ? (
                <p className="text-gray-400 text-center py-8">No events yet...</p>
              ) : (
                events.map((event, idx) => (
                  <div
                    key={idx}
                    className={`p-2 rounded text-sm ${
                      event.type === 'worldscape'
                        ? 'bg-yellow-900 bg-opacity-20 border-l-2 border-yellow-500'
                        : 'bg-purple-900 bg-opacity-20 border-l-2 border-purple-500'
                    }`}
                  >
                    <div className="flex items-start gap-2">
                      <span className="text-lg">{event.type === 'worldscape' ? '✨' : '🤖'}</span>
                      <span className="flex-1">{event.text}</span>
                    </div>
                  </div>
                ))
              )}
            </div>

            <button
              onClick={() => setShowEventsModal(false)}
              className="void-button w-full mt-4"
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default AIWorldscapePanel;