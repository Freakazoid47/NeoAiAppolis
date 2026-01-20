import React, { useState, useEffect, useCallback, useRef } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Users, Trophy, MessageCircle, LogOut, Play, Plus, 
  Eye, Send, Crown, Bot, Settings, Home, Coins, 
  ChevronRight, X, User, Lock, Unlock
} from 'lucide-react';

// Get backend URL from environment or use empty string (relative path for proxy)
const API_URL = process.env.REACT_APP_BACKEND_URL || '';

// API Helper
const api = axios.create({
  baseURL: API_URL,
  headers: { 'Content-Type': 'application/json' }
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Card Component
const Card = ({ card, onClick, playable, disabled, small }) => {
  const isRed = card?.suit === '♥' || card?.suit === '♦';
  const sizeClasses = small ? 'w-14 h-20 text-lg' : 'w-20 h-28 text-2xl';
  
  return (
    <motion.div
      whileHover={playable ? { y: -10, scale: 1.05 } : {}}
      whileTap={playable ? { scale: 0.95 } : {}}
      onClick={playable && !disabled ? onClick : undefined}
      className={`
        ${sizeClasses} rounded-lg flex items-center justify-center font-bold
        bg-gradient-to-br from-yellow-50 to-orange-50 border-2
        shadow-lg cursor-pointer transition-all
        ${isRed ? 'text-red-500' : 'text-gray-900'}
        ${playable ? 'border-yellow-400 hover:border-pink-500 hover:shadow-pink-500/30' : 'border-gray-600'}
        ${disabled ? 'opacity-50 cursor-not-allowed grayscale' : ''}
      `}
      data-testid={`card-${card?.rank}-${card?.suit}`}
    >
      {card?.rank}{card?.suit}
    </motion.div>
  );
};

// Card Back Component
const CardBack = ({ small }) => {
  const sizeClasses = small ? 'w-10 h-14 text-sm' : 'w-14 h-20 text-lg';
  return (
    <div className={`${sizeClasses} rounded-lg bg-gradient-to-br from-purple-900 to-pink-900 border-2 border-yellow-500/50 flex items-center justify-center shadow-lg`}>
      🂠
    </div>
  );
};

// Auth Screen
const AuthScreen = ({ onLogin }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const endpoint = isLogin ? '/api/auth/login' : '/api/auth/register';
      const payload = isLogin 
        ? { username, password }
        : { username, password, display_name: displayName || username };
      
      const response = await api.post(endpoint, payload);
      localStorage.setItem('token', response.data.token);
      onLogin(response.data.user);
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-md"
      >
        <div className="bg-gradient-to-br from-purple-900/90 to-pink-900/90 rounded-2xl p-8 border-2 border-cyan-400 shadow-2xl shadow-pink-500/20">
          <h1 className="text-4xl font-bold text-center mb-2 text-yellow-400">♠ All Fours ♠</h1>
          <p className="text-center text-cyan-300 mb-8">Online Multiplayer Card Game</p>

          <div className="flex mb-6 bg-black/30 rounded-lg p-1">
            <button
              onClick={() => setIsLogin(true)}
              className={`flex-1 py-2 rounded-md transition-all ${isLogin ? 'bg-pink-600 text-white' : 'text-gray-400'}`}
              data-testid="login-tab"
            >
              Login
            </button>
            <button
              onClick={() => setIsLogin(false)}
              className={`flex-1 py-2 rounded-md transition-all ${!isLogin ? 'bg-pink-600 text-white' : 'text-gray-400'}`}
              data-testid="register-tab"
            >
              Register
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-4 py-3 rounded-lg bg-black/40 border-2 border-cyan-500/50 focus:border-cyan-400 text-white placeholder-gray-400 outline-none"
              data-testid="username-input"
            />
            {!isLogin && (
              <input
                type="text"
                placeholder="Display Name (optional)"
                value={displayName}
                onChange={(e) => setDisplayName(e.target.value)}
                className="w-full px-4 py-3 rounded-lg bg-black/40 border-2 border-cyan-500/50 focus:border-cyan-400 text-white placeholder-gray-400 outline-none"
                data-testid="displayname-input"
              />
            )}
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-3 rounded-lg bg-black/40 border-2 border-cyan-500/50 focus:border-cyan-400 text-white placeholder-gray-400 outline-none"
              data-testid="password-input"
            />

            {error && <p className="text-red-400 text-sm text-center">{error}</p>}

            <button
              type="submit"
              disabled={loading}
              className="w-full py-4 rounded-lg bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-500 hover:to-purple-500 text-white font-bold text-lg transition-all disabled:opacity-50"
              data-testid="auth-submit"
            >
              {loading ? 'Loading...' : (isLogin ? 'Login' : 'Create Account')}
            </button>
          </form>
        </div>
      </motion.div>
    </div>
  );
};

// Lobby Screen
const LobbyScreen = ({ user, onJoinRoom, onCreateRoom, onLogout, onViewLeaderboard }) => {
  const [rooms, setRooms] = useState([]);
  const [showCreate, setShowCreate] = useState(false);
  const [roomName, setRoomName] = useState('');
  const [betAmount, setBetAmount] = useState(0);
  const [isPrivate, setIsPrivate] = useState(false);
  const [roomPassword, setRoomPassword] = useState('');
  const [joinCode, setJoinCode] = useState('');

  useEffect(() => {
    const fetchRooms = async () => {
      try {
        const response = await api.get('/api/rooms');
        setRooms(response.data.rooms);
      } catch (err) {
        console.error('Error fetching rooms:', err);
      }
    };

    fetchRooms();
    const interval = setInterval(fetchRooms, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleCreateRoom = async () => {
    try {
      const response = await api.post('/api/rooms/create', {
        name: roomName || `${user.display_name}'s Game`,
        bet_amount: betAmount,
        is_private: isPrivate,
        password: isPrivate ? roomPassword : null
      });
      onCreateRoom(response.data.room);
    } catch (err) {
      console.error('Error creating room:', err);
    }
  };

  const handleJoinByCode = async () => {
    try {
      const response = await api.post('/api/rooms/join', { room_id: joinCode.toUpperCase() });
      onJoinRoom(response.data.room);
    } catch (err) {
      alert(err.response?.data?.detail || 'Could not join room');
    }
  };

  return (
    <div className="min-h-screen p-4">
      {/* Header */}
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8 bg-gradient-to-r from-purple-900/80 to-pink-900/80 rounded-xl p-4 border border-cyan-500/30">
          <div className="flex items-center gap-4">
            <div className="text-4xl">{user.avatar}</div>
            <div>
              <h2 className="text-xl font-bold text-yellow-400">{user.display_name}</h2>
              <div className="flex items-center gap-4 text-sm">
                <span className="text-cyan-300"><Coins className="inline w-4 h-4" /> {user.coins}</span>
                <span className="text-green-400">W: {user.wins}</span>
                <span className="text-red-400">L: {user.losses}</span>
              </div>
            </div>
          </div>
          <div className="flex gap-2">
            <button
              onClick={onViewLeaderboard}
              className="px-4 py-2 rounded-lg bg-yellow-600 hover:bg-yellow-500 text-white flex items-center gap-2"
              data-testid="leaderboard-btn"
            >
              <Trophy className="w-4 h-4" /> Leaderboard
            </button>
            <button
              onClick={onLogout}
              className="px-4 py-2 rounded-lg bg-red-600 hover:bg-red-500 text-white flex items-center gap-2"
              data-testid="logout-btn"
            >
              <LogOut className="w-4 h-4" /> Logout
            </button>
          </div>
        </div>

        {/* Quick Join */}
        <div className="mb-6 bg-gradient-to-r from-purple-900/60 to-pink-900/60 rounded-xl p-4 border border-pink-500/30">
          <h3 className="text-lg font-bold text-pink-400 mb-3">Quick Join</h3>
          <div className="flex gap-2">
            <input
              type="text"
              placeholder="Enter Room Code"
              value={joinCode}
              onChange={(e) => setJoinCode(e.target.value.toUpperCase())}
              className="flex-1 px-4 py-2 rounded-lg bg-black/40 border border-cyan-500/50 text-white uppercase"
              data-testid="join-code-input"
            />
            <button
              onClick={handleJoinByCode}
              className="px-6 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white font-bold"
              data-testid="join-code-btn"
            >
              Join
            </button>
          </div>
        </div>

        {/* Create Room Modal */}
        <AnimatePresence>
          {showCreate && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black/70 flex items-center justify-center z-50"
              onClick={() => setShowCreate(false)}
            >
              <motion.div
                initial={{ scale: 0.9, y: 20 }}
                animate={{ scale: 1, y: 0 }}
                exit={{ scale: 0.9, y: 20 }}
                onClick={(e) => e.stopPropagation()}
                className="bg-gradient-to-br from-purple-900 to-pink-900 rounded-2xl p-6 w-full max-w-md border-2 border-yellow-400"
              >
                <h3 className="text-2xl font-bold text-yellow-400 mb-4">Create Game Room</h3>
                <div className="space-y-4">
                  <input
                    type="text"
                    placeholder="Room Name"
                    value={roomName}
                    onChange={(e) => setRoomName(e.target.value)}
                    className="w-full px-4 py-3 rounded-lg bg-black/40 border border-cyan-500/50 text-white"
                    data-testid="room-name-input"
                  />
                  <div>
                    <label className="text-cyan-300 text-sm">Bet Amount (Coins)</label>
                    <input
                      type="number"
                      value={betAmount}
                      onChange={(e) => setBetAmount(parseInt(e.target.value) || 0)}
                      className="w-full px-4 py-3 rounded-lg bg-black/40 border border-cyan-500/50 text-white"
                      data-testid="bet-amount-input"
                    />
                  </div>
                  <div className="flex items-center gap-2">
                    <input
                      type="checkbox"
                      checked={isPrivate}
                      onChange={(e) => setIsPrivate(e.target.checked)}
                      className="w-5 h-5"
                      data-testid="private-checkbox"
                    />
                    <label className="text-white">Private Room</label>
                  </div>
                  {isPrivate && (
                    <input
                      type="password"
                      placeholder="Room Password"
                      value={roomPassword}
                      onChange={(e) => setRoomPassword(e.target.value)}
                      className="w-full px-4 py-3 rounded-lg bg-black/40 border border-cyan-500/50 text-white"
                      data-testid="room-password-input"
                    />
                  )}
                  <button
                    onClick={handleCreateRoom}
                    className="w-full py-4 rounded-lg bg-gradient-to-r from-green-600 to-cyan-600 hover:from-green-500 hover:to-cyan-500 text-white font-bold text-lg"
                    data-testid="create-room-submit"
                  >
                    Create Room
                  </button>
                </div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Room List */}
        <div className="grid md:grid-cols-2 gap-4">
          {/* Create Room Card */}
          <motion.div
            whileHover={{ scale: 1.02 }}
            onClick={() => setShowCreate(true)}
            className="bg-gradient-to-br from-green-900/60 to-cyan-900/60 rounded-xl p-6 border-2 border-dashed border-green-500/50 cursor-pointer hover:border-green-400 transition-all flex items-center justify-center gap-3"
            data-testid="create-room-card"
          >
            <Plus className="w-8 h-8 text-green-400" />
            <span className="text-xl font-bold text-green-400">Create New Game</span>
          </motion.div>

          {/* Available Rooms */}
          {rooms.map((room) => (
            <motion.div
              key={room.id}
              whileHover={{ scale: 1.02 }}
              className="bg-gradient-to-br from-purple-900/60 to-pink-900/60 rounded-xl p-6 border border-pink-500/30 cursor-pointer hover:border-pink-400 transition-all"
              onClick={() => onJoinRoom(room)}
              data-testid={`room-${room.id}`}
            >
              <div className="flex justify-between items-start mb-3">
                <h3 className="text-lg font-bold text-yellow-400">{room.name}</h3>
                <span className="text-xs px-2 py-1 rounded bg-cyan-600 text-white">{room.code}</span>
              </div>
              <div className="flex justify-between items-center text-sm">
                <span className="text-cyan-300">
                  <Users className="inline w-4 h-4 mr-1" />
                  {room.players_count}/{room.max_players}
                </span>
                {room.bet_amount > 0 && (
                  <span className="text-yellow-400">
                    <Coins className="inline w-4 h-4 mr-1" />
                    {room.bet_amount}
                  </span>
                )}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
};

// Waiting Room Screen
const WaitingRoomScreen = ({ room, user, onStartGame, onLeave, onUpdate }) => {
  const [chatInput, setChatInput] = useState('');
  const [messages, setMessages] = useState([]);
  const wsRef = useRef(null);
  const chatEndRef = useRef(null);

  useEffect(() => {
    // Connect WebSocket
    const wsUrl = API_URL.replace('http', 'ws') + `/api/ws/${room.id}/${user.id}`;
    wsRef.current = new WebSocket(wsUrl);

    wsRef.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'chat_message') {
        setMessages(prev => [...prev, data.message]);
      } else if (data.type === 'player_joined' || data.type === 'player_ready') {
        onUpdate({ ...room, players: data.players });
      } else if (data.type === 'game_started') {
        onStartGame(data.game_state, data.room);
      }
    };

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [room.id, user.id]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleAddBot = async () => {
    try {
      const response = await api.post(`/api/rooms/${room.id}/add-bot`);
      onUpdate(response.data.room);
    } catch (err) {
      alert(err.response?.data?.detail || 'Could not add bot');
    }
  };

  const handleReady = async () => {
    try {
      const response = await api.post(`/api/rooms/${room.id}/ready`);
      onUpdate(response.data.room);
    } catch (err) {
      console.error('Error toggling ready:', err);
    }
  };

  const handleStart = async () => {
    try {
      const response = await api.post(`/api/rooms/${room.id}/start`);
      onStartGame(response.data.game_state, response.data.room);
    } catch (err) {
      alert(err.response?.data?.detail || 'Could not start game');
    }
  };

  const sendChat = () => {
    if (chatInput.trim() && wsRef.current) {
      wsRef.current.send(JSON.stringify({ type: 'chat', message: chatInput }));
      setChatInput('');
    }
  };

  const isHost = room.host_id === user.id;
  const myPlayer = room.players.find(p => p.id === user.id);
  const canStart = room.players.length >= 2 && room.players.every(p => p.is_ready || p.id === user.id || p.is_bot);

  return (
    <div className="min-h-screen p-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="bg-gradient-to-r from-purple-900/80 to-pink-900/80 rounded-xl p-4 border border-yellow-500/30 mb-6">
          <div className="flex justify-between items-center">
            <div>
              <h2 className="text-2xl font-bold text-yellow-400">{room.name}</h2>
              <p className="text-cyan-300">Room Code: <span className="font-bold text-white">{room.code}</span></p>
            </div>
            <button
              onClick={onLeave}
              className="px-4 py-2 rounded-lg bg-red-600 hover:bg-red-500 text-white flex items-center gap-2"
              data-testid="leave-room-btn"
            >
              <X className="w-4 h-4" /> Leave
            </button>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          {/* Players */}
          <div className="bg-gradient-to-br from-purple-900/60 to-pink-900/60 rounded-xl p-6 border border-pink-500/30">
            <h3 className="text-xl font-bold text-pink-400 mb-4">Players ({room.players.length}/4)</h3>
            <div className="space-y-3">
              {room.players.map((player, idx) => (
                <div
                  key={player.id}
                  className={`flex items-center justify-between p-3 rounded-lg ${
                    player.is_ready || player.is_bot ? 'bg-green-900/40 border border-green-500/30' : 'bg-black/30'
                  }`}
                  data-testid={`player-${idx}`}
                >
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">{player.avatar}</span>
                    <div>
                      <div className="font-bold text-white flex items-center gap-2">
                        {player.display_name}
                        {player.id === room.host_id && <Crown className="w-4 h-4 text-yellow-400" />}
                        {player.is_bot && <Bot className="w-4 h-4 text-cyan-400" />}
                      </div>
                      {player.is_bot && (
                        <div className="text-xs text-cyan-300">Skill: {player.skill_level}/5</div>
                      )}
                    </div>
                  </div>
                  <span className={`text-sm ${player.is_ready || player.is_bot ? 'text-green-400' : 'text-gray-400'}`}>
                    {player.is_bot ? 'Ready' : (player.is_ready ? 'Ready' : 'Not Ready')}
                  </span>
                </div>
              ))}
            </div>

            {/* Actions */}
            <div className="mt-6 space-y-3">
              {isHost && room.players.length < 4 && (
                <button
                  onClick={handleAddBot}
                  className="w-full py-3 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white font-bold flex items-center justify-center gap-2"
                  data-testid="add-bot-btn"
                >
                  <Bot className="w-5 h-5" /> Add AI Bot
                </button>
              )}
              {!isHost && (
                <button
                  onClick={handleReady}
                  className={`w-full py-3 rounded-lg font-bold flex items-center justify-center gap-2 ${
                    myPlayer?.is_ready
                      ? 'bg-gray-600 hover:bg-gray-500 text-white'
                      : 'bg-green-600 hover:bg-green-500 text-white'
                  }`}
                  data-testid="ready-btn"
                >
                  {myPlayer?.is_ready ? 'Cancel Ready' : 'Ready Up'}
                </button>
              )}
              {isHost && (
                <button
                  onClick={handleStart}
                  disabled={!canStart}
                  className="w-full py-4 rounded-lg bg-gradient-to-r from-yellow-600 to-orange-600 hover:from-yellow-500 hover:to-orange-500 text-white font-bold text-lg disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                  data-testid="start-game-btn"
                >
                  <Play className="w-5 h-5" /> Start Game
                </button>
              )}
            </div>
          </div>

          {/* Chat */}
          <div className="bg-gradient-to-br from-purple-900/60 to-pink-900/60 rounded-xl p-6 border border-cyan-500/30">
            <h3 className="text-xl font-bold text-cyan-400 mb-4">
              <MessageCircle className="inline w-5 h-5 mr-2" /> Chat
            </h3>
            <div className="h-64 overflow-y-auto mb-4 bg-black/30 rounded-lg p-3 space-y-2">
              {messages.map((msg, idx) => (
                <div key={idx} className="text-sm">
                  <span className="text-yellow-400">{msg.avatar} {msg.username}: </span>
                  <span className="text-white">{msg.message}</span>
                </div>
              ))}
              <div ref={chatEndRef} />
            </div>
            <div className="flex gap-2">
              <input
                type="text"
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && sendChat()}
                placeholder="Type a message..."
                className="flex-1 px-4 py-2 rounded-lg bg-black/40 border border-cyan-500/50 text-white"
                data-testid="chat-input"
              />
              <button
                onClick={sendChat}
                className="px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white"
                data-testid="send-chat-btn"
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>

        {/* Game Rules */}
        <div className="mt-6 bg-gradient-to-br from-purple-900/40 to-pink-900/40 rounded-xl p-6 border border-yellow-500/20">
          <h3 className="text-xl font-bold text-yellow-400 mb-4">📋 Game Rules</h3>
          <div className="grid md:grid-cols-2 gap-4 text-sm text-gray-300">
            <div>
              <h4 className="font-bold text-cyan-400 mb-2">Scoring</h4>
              <ul className="space-y-1">
                <li>• <span className="text-yellow-400">HIGH (4 pts)</span> - Highest trump dealt</li>
                <li>• <span className="text-yellow-400">LOW (1 pt)</span> - Lowest trump dealt</li>
                <li>• <span className="text-yellow-400">JACK (3 pts)</span> - Win Jack of trump</li>
                <li>• <span className="text-yellow-400">GAME (2 pts)</span> - Most card points</li>
              </ul>
            </div>
            <div>
              <h4 className="font-bold text-cyan-400 mb-2">Card Points (for GAME)</h4>
              <ul className="space-y-1">
                <li>• 10 = 10 points</li>
                <li>• Ace = 4 points</li>
                <li>• King = 3, Queen = 2, Jack = 1</li>
                <li>• First to 14 points wins!</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Game Screen
const GameScreen = ({ room, gameState, user, onUpdate, onGameEnd, onLeave }) => {
  const [myHand, setMyHand] = useState([]);
  const [chatInput, setChatInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [showChat, setShowChat] = useState(false);
  const wsRef = useRef(null);

  useEffect(() => {
    const wsUrl = API_URL.replace('http', 'ws') + `/api/ws/${room.id}/${user.id}`;
    wsRef.current = new WebSocket(wsUrl);

    wsRef.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      switch (data.type) {
        case 'your_hand':
          setMyHand(data.hand);
          break;
        case 'card_played':
        case 'turn_change':
        case 'trick_complete':
          onUpdate(prev => ({
            ...prev,
            gameState: {
              ...prev.gameState,
              current_trick: data.current_trick || prev.gameState?.current_trick,
              current_player_idx: data.current_player_idx ?? prev.gameState?.current_player_idx
            }
          }));
          break;
        case 'round_complete':
          onUpdate(prev => ({
            ...prev,
            gameState: {
              ...prev.gameState,
              scores: data.total_scores
            }
          }));
          break;
        case 'new_round':
          onUpdate(prev => ({
            ...prev,
            gameState: data.game_state
          }));
          break;
        case 'game_over':
          onGameEnd(data);
          break;
        case 'chat_message':
          setMessages(prev => [...prev, data.message]);
          break;
        default:
          break;
      }
    };

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [room.id, user.id]);

  const playCard = async (card) => {
    try {
      await api.post('/api/game/play-card', {
        room_id: room.id,
        card: card
      });
      setMyHand(prev => prev.filter(c => !(c.suit === card.suit && c.rank === card.rank)));
    } catch (err) {
      alert(err.response?.data?.detail || 'Cannot play that card');
    }
  };

  const sendChat = () => {
    if (chatInput.trim() && wsRef.current) {
      wsRef.current.send(JSON.stringify({ type: 'chat', message: chatInput }));
      setChatInput('');
    }
  };

  const currentPlayerId = gameState?.players?.[gameState?.current_player_idx];
  const isMyTurn = currentPlayerId === user.id;
  const currentPlayerName = room.players.find(p => p.id === currentPlayerId)?.display_name;

  return (
    <div className="min-h-screen p-4 flex flex-col">
      {/* Top Info Bar */}
      <div className="bg-gradient-to-r from-purple-900/80 to-pink-900/80 rounded-xl p-4 border border-yellow-500/30 mb-4">
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-6">
            <div>
              <span className="text-gray-400 text-sm">Trump</span>
              <div className={`text-3xl font-bold ${
                gameState?.trump?.suit === '♥' || gameState?.trump?.suit === '♦' ? 'text-red-500' : 'text-white'
              }`}>
                {gameState?.trump?.rank}{gameState?.trump?.suit}
              </div>
            </div>
            <div>
              <span className="text-gray-400 text-sm">Win at</span>
              <div className="text-xl font-bold text-yellow-400">14 pts</div>
            </div>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => setShowChat(!showChat)}
              className="px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white"
              data-testid="toggle-chat-btn"
            >
              <MessageCircle className="w-5 h-5" />
            </button>
            <button
              onClick={onLeave}
              className="px-4 py-2 rounded-lg bg-red-600 hover:bg-red-500 text-white"
              data-testid="leave-game-btn"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>

      <div className="flex-1 flex gap-4">
        {/* Main Game Area */}
        <div className="flex-1 flex flex-col">
          {/* Other Players */}
          <div className="flex justify-center gap-6 mb-6">
            {room.players.filter(p => p.id !== user.id).map((player, idx) => {
              const playerIdx = room.players.findIndex(p => p.id === player.id);
              const isCurrentPlayer = gameState?.players?.[gameState?.current_player_idx] === player.id;
              const handSize = gameState?.hand_sizes?.[player.id] || 0;
              const score = gameState?.scores?.[player.id] || 0;

              return (
                <div
                  key={player.id}
                  className={`bg-gradient-to-br from-purple-900/60 to-pink-900/60 rounded-xl p-4 border-2 transition-all ${
                    isCurrentPlayer ? 'border-yellow-400 shadow-lg shadow-yellow-500/30' : 'border-pink-500/30'
                  }`}
                  data-testid={`opponent-${idx}`}
                >
                  <div className="text-center mb-2">
                    <div className="text-3xl mb-1">{player.avatar}</div>
                    <div className="font-bold text-yellow-400 flex items-center justify-center gap-1">
                      {player.display_name}
                      {player.is_bot && <Bot className="w-4 h-4 text-cyan-400" />}
                    </div>
                    <div className="text-sm text-cyan-300">Score: {score}</div>
                  </div>
                  <div className="flex justify-center gap-1">
                    {[...Array(handSize)].map((_, i) => (
                      <CardBack key={i} small />
                    ))}
                  </div>
                </div>
              );
            })}
          </div>

          {/* Trick Area */}
          <div className="flex-1 flex flex-col items-center justify-center">
            <div className={`text-lg font-bold mb-4 px-6 py-2 rounded-full ${
              isMyTurn ? 'bg-green-600 text-white' : 'bg-purple-900/60 text-cyan-300'
            }`}>
              {isMyTurn ? "🎯 Your Turn!" : `${currentPlayerName}'s turn...`}
            </div>
            
            <div className="flex gap-4 min-h-36 items-center justify-center p-4 rounded-xl bg-black/30 border-2 border-dashed border-yellow-500/30">
              {gameState?.current_trick?.length > 0 ? (
                gameState.current_trick.map((play, idx) => {
                  const playerName = room.players.find(p => p.id === play.player_id)?.display_name;
                  return (
                    <div key={idx} className="text-center">
                      <Card card={play.card} />
                      <div className="text-xs text-gray-400 mt-1">{playerName}</div>
                    </div>
                  );
                })
              ) : (
                <div className="text-gray-500 text-lg">Waiting for cards...</div>
              )}
            </div>
          </div>

          {/* My Hand */}
          <div className="bg-gradient-to-r from-purple-900/80 to-pink-900/80 rounded-xl p-4 border-2 border-yellow-500/50">
            <div className="text-center mb-2">
              <span className="text-yellow-400 font-bold">Your Hand</span>
              <span className="text-cyan-300 ml-4">Score: {gameState?.scores?.[user.id] || 0}</span>
            </div>
            <div className="flex justify-center gap-3 flex-wrap">
              {myHand.map((card, idx) => (
                <Card
                  key={idx}
                  card={card}
                  playable={isMyTurn}
                  disabled={!isMyTurn}
                  onClick={() => playCard(card)}
                />
              ))}
            </div>
          </div>
        </div>

        {/* Chat Panel */}
        <AnimatePresence>
          {showChat && (
            <motion.div
              initial={{ width: 0, opacity: 0 }}
              animate={{ width: 300, opacity: 1 }}
              exit={{ width: 0, opacity: 0 }}
              className="bg-gradient-to-br from-purple-900/80 to-pink-900/80 rounded-xl border border-cyan-500/30 flex flex-col overflow-hidden"
            >
              <div className="p-3 border-b border-cyan-500/30">
                <h3 className="font-bold text-cyan-400">Chat</h3>
              </div>
              <div className="flex-1 overflow-y-auto p-3 space-y-2">
                {messages.map((msg, idx) => (
                  <div key={idx} className="text-sm">
                    <span className="text-yellow-400">{msg.avatar} {msg.username}: </span>
                    <span className="text-white">{msg.message}</span>
                  </div>
                ))}
              </div>
              <div className="p-3 border-t border-cyan-500/30 flex gap-2">
                <input
                  type="text"
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && sendChat()}
                  placeholder="Message..."
                  className="flex-1 px-3 py-2 rounded-lg bg-black/40 border border-cyan-500/50 text-white text-sm"
                />
                <button onClick={sendChat} className="px-3 py-2 rounded-lg bg-cyan-600 text-white">
                  <Send className="w-4 h-4" />
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Scores Bar */}
      <div className="mt-4 bg-gradient-to-r from-purple-900/80 to-pink-900/80 rounded-xl p-3 border border-yellow-500/30">
        <div className="flex justify-center gap-8">
          {room.players.map((player) => (
            <div key={player.id} className="text-center">
              <span className={`font-bold ${player.id === user.id ? 'text-yellow-400' : 'text-white'}`}>
                {player.display_name}: {gameState?.scores?.[player.id] || 0}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

// Game Over Modal
const GameOverModal = ({ data, onClose }) => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="fixed inset-0 bg-black/80 flex items-center justify-center z-50"
    >
      <motion.div
        initial={{ scale: 0.5, y: 50 }}
        animate={{ scale: 1, y: 0 }}
        className="bg-gradient-to-br from-purple-900 to-pink-900 rounded-2xl p-8 border-4 border-yellow-400 text-center max-w-md w-full mx-4 shadow-2xl shadow-yellow-500/30"
      >
        <div className="text-6xl mb-4">🏆</div>
        <h2 className="text-3xl font-bold text-yellow-400 mb-2">Game Over!</h2>
        <div className="text-2xl mb-4">
          <span className="text-4xl">{data.winner?.avatar}</span>
          <p className="text-cyan-300 font-bold">{data.winner?.display_name} Wins!</p>
        </div>
        
        <div className="bg-black/30 rounded-xl p-4 mb-6">
          <h3 className="text-lg font-bold text-pink-400 mb-3">Final Scores</h3>
          {Object.entries(data.final_scores || {}).map(([playerId, score]) => (
            <div key={playerId} className="flex justify-between text-white">
              <span>{playerId === data.winner_id ? '👑 ' : ''}{playerId.substring(0, 8)}...</span>
              <span className="font-bold text-yellow-400">{score}</span>
            </div>
          ))}
        </div>
        
        <button
          onClick={onClose}
          className="w-full py-4 rounded-lg bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white font-bold text-lg"
          data-testid="back-to-lobby-btn"
        >
          Back to Lobby
        </button>
      </motion.div>
    </motion.div>
  );
};

// Leaderboard Screen
const LeaderboardScreen = ({ onBack }) => {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        const response = await api.get('/api/leaderboard');
        setLeaderboard(response.data.leaderboard);
      } catch (err) {
        console.error('Error fetching leaderboard:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchLeaderboard();
  }, []);

  return (
    <div className="min-h-screen p-4">
      <div className="max-w-2xl mx-auto">
        <div className="flex items-center gap-4 mb-6">
          <button
            onClick={onBack}
            className="px-4 py-2 rounded-lg bg-purple-600 hover:bg-purple-500 text-white"
            data-testid="back-btn"
          >
            <Home className="w-5 h-5" />
          </button>
          <h1 className="text-3xl font-bold text-yellow-400">🏆 Leaderboard</h1>
        </div>

        <div className="bg-gradient-to-br from-purple-900/80 to-pink-900/80 rounded-xl border border-yellow-500/30 overflow-hidden">
          {loading ? (
            <div className="p-8 text-center text-gray-400">Loading...</div>
          ) : (
            <table className="w-full">
              <thead>
                <tr className="bg-black/30 text-yellow-400">
                  <th className="p-4 text-left">#</th>
                  <th className="p-4 text-left">Player</th>
                  <th className="p-4 text-center">Wins</th>
                  <th className="p-4 text-center">Win Rate</th>
                </tr>
              </thead>
              <tbody>
                {leaderboard.map((player, idx) => (
                  <tr key={player.id} className="border-t border-purple-700/30 hover:bg-purple-900/30">
                    <td className="p-4">
                      {idx === 0 ? '🥇' : idx === 1 ? '🥈' : idx === 2 ? '🥉' : idx + 1}
                    </td>
                    <td className="p-4">
                      <div className="flex items-center gap-3">
                        <span className="text-2xl">{player.avatar}</span>
                        <span className="font-bold text-white">{player.display_name}</span>
                      </div>
                    </td>
                    <td className="p-4 text-center text-green-400 font-bold">{player.wins}</td>
                    <td className="p-4 text-center text-cyan-300">{player.win_rate}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
};

// Main App
function App() {
  const [user, setUser] = useState(null);
  const [currentScreen, setCurrentScreen] = useState('auth');
  const [currentRoom, setCurrentRoom] = useState(null);
  const [gameState, setGameState] = useState(null);
  const [gameOverData, setGameOverData] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      api.get('/api/auth/me')
        .then(response => {
          setUser(response.data);
          setCurrentScreen('lobby');
        })
        .catch(() => {
          localStorage.removeItem('token');
        });
    }
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
    setCurrentScreen('lobby');
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setUser(null);
    setCurrentScreen('auth');
  };

  const handleJoinRoom = async (room) => {
    try {
      const response = await api.post('/api/rooms/join', { room_id: room.id });
      setCurrentRoom(response.data.room);
      setCurrentScreen('waiting');
    } catch (err) {
      alert(err.response?.data?.detail || 'Could not join room');
    }
  };

  const handleCreateRoom = (room) => {
    setCurrentRoom(room);
    setCurrentScreen('waiting');
  };

  const handleStartGame = (gameState, room) => {
    setGameState(gameState);
    setCurrentRoom(room);
    setCurrentScreen('game');
  };

  const handleUpdateRoom = (room) => {
    setCurrentRoom(room);
  };

  const handleGameEnd = (data) => {
    setGameOverData(data);
  };

  const handleLeaveRoom = () => {
    setCurrentRoom(null);
    setGameState(null);
    setCurrentScreen('lobby');
  };

  const handleCloseGameOver = () => {
    setGameOverData(null);
    setCurrentRoom(null);
    setGameState(null);
    setCurrentScreen('lobby');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-game-dark via-game-purple to-blue-900">
      {currentScreen === 'auth' && (
        <AuthScreen onLogin={handleLogin} />
      )}
      
      {currentScreen === 'lobby' && user && (
        <LobbyScreen
          user={user}
          onJoinRoom={handleJoinRoom}
          onCreateRoom={handleCreateRoom}
          onLogout={handleLogout}
          onViewLeaderboard={() => setCurrentScreen('leaderboard')}
        />
      )}

      {currentScreen === 'waiting' && currentRoom && user && (
        <WaitingRoomScreen
          room={currentRoom}
          user={user}
          onStartGame={handleStartGame}
          onLeave={handleLeaveRoom}
          onUpdate={handleUpdateRoom}
        />
      )}

      {currentScreen === 'game' && currentRoom && gameState && user && (
        <GameScreen
          room={currentRoom}
          gameState={gameState}
          user={user}
          onUpdate={(updater) => {
            if (typeof updater === 'function') {
              setGameState(prev => updater({ gameState: prev }).gameState);
            }
          }}
          onGameEnd={handleGameEnd}
          onLeave={handleLeaveRoom}
        />
      )}

      {currentScreen === 'leaderboard' && (
        <LeaderboardScreen onBack={() => setCurrentScreen('lobby')} />
      )}

      {gameOverData && (
        <GameOverModal data={gameOverData} onClose={handleCloseGameOver} />
      )}
    </div>
  );
}

export default App;
