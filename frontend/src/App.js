import React, { useState, useEffect, useCallback, useRef } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Users, Trophy, MessageCircle, LogOut, Play, Plus, 
  Eye, Send, Crown, Bot, Settings, Home, Coins, 
  ChevronRight, X, User, Lock, Unlock, Zap, Star
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

// ============ PARTICLE SYSTEM ============
const Particles = ({ trigger, color = '#ff0055', count = 20 }) => {
  const [particles, setParticles] = useState([]);

  useEffect(() => {
    if (trigger) {
      const newParticles = Array.from({ length: count }, (_, i) => ({
        id: Date.now() + i,
        x: Math.random() * 200 - 100,
        y: Math.random() * 200 - 100,
        color: ['#ff0055', '#00ffff', '#ffd700', '#00ff88'][Math.floor(Math.random() * 4)]
      }));
      setParticles(newParticles);
      setTimeout(() => setParticles([]), 1000);
    }
  }, [trigger, count]);

  return (
    <div className="particle-container">
      {particles.map(p => (
        <div
          key={p.id}
          className="particle"
          style={{
            left: '50%',
            top: '50%',
            backgroundColor: p.color,
            '--x-offset': `${p.x}px`,
            boxShadow: `0 0 10px ${p.color}`
          }}
        />
      ))}
    </div>
  );
};

// ============ SCREEN SHAKE HOOK ============
const useScreenShake = () => {
  const [shaking, setShaking] = useState(false);
  
  const shake = useCallback(() => {
    setShaking(true);
    setTimeout(() => setShaking(false), 500);
  }, []);
  
  return [shaking, shake];
};

// ============ CARD COMPONENT - BALATRO STYLE ============
const Card = ({ card, onClick, playable, disabled, small, played, showBack }) => {
  const [burst, setBurst] = useState(false);
  const isRed = card?.suit === '♥' || card?.suit === '♦';
  
  const handleClick = () => {
    if (playable && !disabled && onClick) {
      setBurst(true);
      setTimeout(() => setBurst(false), 400);
      onClick();
    }
  };
  
  if (showBack) {
    return <div className={`card-back ${small ? 'scale-75' : ''}`} />;
  }
  
  const sizeClass = small ? 'w-16 h-22 text-xl' : 'w-24 h-32 text-3xl';
  
  return (
    <motion.div
      whileHover={playable ? { y: -25, scale: 1.15, rotate: -3 } : {}}
      whileTap={playable ? { scale: 0.95 } : {}}
      onClick={handleClick}
      className={`
        game-card ${sizeClass}
        ${isRed ? 'red' : 'black'}
        ${playable && !disabled ? 'playable' : ''}
        ${disabled ? 'disabled' : ''}
        ${played ? 'played' : ''}
        ${burst ? 'burst' : ''}
      `}
      data-testid={`card-${card?.rank}-${card?.suit}`}
    >
      <span className="text-sm opacity-60">{card?.suit}</span>
      <span className="font-black">{card?.rank}</span>
      <span className="text-sm opacity-60">{card?.suit}</span>
    </motion.div>
  );
};

// ============ CARD BACK COMPONENT ============
const CardBack = ({ small }) => {
  return (
    <div className={`card-back ${small ? 'scale-75' : ''}`}>
      <span className="opacity-0">🂠</span>
    </div>
  );
};

// ============ TRUMP CHIP - BALATRO STYLE ============
const TrumpChip = ({ trump }) => {
  const isRed = trump?.suit === '♥' || trump?.suit === '♦';
  
  return (
    <div className="trump-chip">
      <span className={`suit ${isRed ? 'text-red-500' : 'text-white'}`}>
        {trump?.suit}
      </span>
      <span className="rank">{trump?.rank}</span>
    </div>
  );
};

// ============ AUTH SCREEN ============
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
    <div className="crt-screen min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-[#0a0a0f] via-[#1a0a2e] to-[#0a0a0f]">
      <div className="vignette" />
      <motion.div 
        initial={{ opacity: 0, y: 20, scale: 0.9 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        className="w-full max-w-md relative z-10"
      >
        <div className="modal-content rounded-2xl p-8">
          {/* Title with glitch effect */}
          <h1 className="text-5xl font-black text-center mb-2 neon-yellow neon-text">
            ♠ ALL FOURS ♠
          </h1>
          <p className="text-center neon-cyan mb-8 tracking-widest text-sm">
            // ONLINE MULTIPLAYER //
          </p>

          {/* Tab Switcher */}
          <div className="flex mb-6 bg-black/50 rounded-lg p-1 border border-gray-700">
            <button
              onClick={() => setIsLogin(true)}
              className={`flex-1 py-3 rounded-md font-bold tracking-wider transition-all ${
                isLogin 
                  ? 'bg-gradient-to-r from-pink-600 to-purple-600 text-white shadow-lg shadow-pink-500/30' 
                  : 'text-gray-500 hover:text-gray-300'
              }`}
              data-testid="login-tab"
            >
              LOGIN
            </button>
            <button
              onClick={() => setIsLogin(false)}
              className={`flex-1 py-3 rounded-md font-bold tracking-wider transition-all ${
                !isLogin 
                  ? 'bg-gradient-to-r from-cyan-600 to-blue-600 text-white shadow-lg shadow-cyan-500/30' 
                  : 'text-gray-500 hover:text-gray-300'
              }`}
              data-testid="register-tab"
            >
              REGISTER
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <input
              type="text"
              placeholder="USERNAME"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-4 py-4 rounded-lg bg-black/60 border-2 border-cyan-500/30 focus:border-cyan-400 text-white placeholder-gray-500 outline-none font-mono tracking-wider"
              data-testid="username-input"
            />
            {!isLogin && (
              <input
                type="text"
                placeholder="DISPLAY NAME"
                value={displayName}
                onChange={(e) => setDisplayName(e.target.value)}
                className="w-full px-4 py-4 rounded-lg bg-black/60 border-2 border-pink-500/30 focus:border-pink-400 text-white placeholder-gray-500 outline-none font-mono tracking-wider"
                data-testid="displayname-input"
              />
            )}
            <input
              type="password"
              placeholder="PASSWORD"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-4 rounded-lg bg-black/60 border-2 border-yellow-500/30 focus:border-yellow-400 text-white placeholder-gray-500 outline-none font-mono tracking-wider"
              data-testid="password-input"
            />

            {error && (
              <motion.p 
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                className="neon-pink text-sm text-center font-bold"
              >
                ⚠ {error}
              </motion.p>
            )}

            <motion.button
              type="submit"
              disabled={loading}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="w-full py-5 rounded-lg bg-gradient-to-r from-yellow-500 via-orange-500 to-red-500 text-black font-black text-xl tracking-wider disabled:opacity-50 shadow-lg shadow-yellow-500/30"
              data-testid="auth-submit"
            >
              {loading ? '⏳ LOADING...' : (isLogin ? '🎮 ENTER GAME' : '🚀 CREATE ACCOUNT')}
            </motion.button>
          </form>
        </div>
      </motion.div>
    </div>
  );
};

// ============ LOBBY SCREEN ============
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
    <div className="crt-screen min-h-screen p-4 bg-gradient-to-br from-[#0a0a0f] via-[#1a0a2e] to-[#0a0a0f]">
      <div className="vignette" />
      <div className="max-w-6xl mx-auto relative z-10">
        {/* Header */}
        <div className="modal-content rounded-xl p-4 mb-6">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-4">
              <div className="text-5xl">{user.avatar}</div>
              <div>
                <h2 className="text-2xl font-black neon-yellow">{user.display_name}</h2>
                <div className="flex items-center gap-4 text-sm font-mono">
                  <span className="neon-cyan flex items-center gap-1">
                    <Coins className="w-4 h-4" /> {user.coins}
                  </span>
                  <span className="neon-green">W:{user.wins}</span>
                  <span className="neon-pink">L:{user.losses}</span>
                </div>
              </div>
            </div>
            <div className="flex gap-3">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={onViewLeaderboard}
                className="btn-neon px-6 py-3 rounded-lg text-yellow-400 border-yellow-400 flex items-center gap-2"
                data-testid="leaderboard-btn"
              >
                <Trophy className="w-5 h-5" /> RANKS
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={onLogout}
                className="btn-neon px-6 py-3 rounded-lg text-red-400 border-red-400 flex items-center gap-2"
                data-testid="logout-btn"
              >
                <LogOut className="w-5 h-5" /> EXIT
              </motion.button>
            </div>
          </div>
        </div>

        {/* Quick Join */}
        <div className="mb-6 p-4 bg-black/40 rounded-xl border-2 border-cyan-500/30">
          <h3 className="text-lg font-black neon-cyan mb-3 tracking-wider">// QUICK JOIN //</h3>
          <div className="flex gap-2">
            <input
              type="text"
              placeholder="ENTER ROOM CODE"
              value={joinCode}
              onChange={(e) => setJoinCode(e.target.value.toUpperCase())}
              className="flex-1 px-4 py-3 rounded-lg bg-black/60 border-2 border-cyan-500/50 text-white font-mono uppercase tracking-widest"
              data-testid="join-code-input"
            />
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleJoinByCode}
              className="px-8 py-3 rounded-lg bg-gradient-to-r from-cyan-600 to-blue-600 text-white font-black tracking-wider"
              data-testid="join-code-btn"
            >
              JOIN
            </motion.button>
          </div>
        </div>

        {/* Create Room Modal */}
        <AnimatePresence>
          {showCreate && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 modal-overlay flex items-center justify-center z-50"
              onClick={() => setShowCreate(false)}
            >
              <motion.div
                initial={{ scale: 0.8, y: 50, rotateX: -15 }}
                animate={{ scale: 1, y: 0, rotateX: 0 }}
                exit={{ scale: 0.8, y: 50, rotateX: 15 }}
                onClick={(e) => e.stopPropagation()}
                className="modal-content rounded-2xl p-8 w-full max-w-md"
              >
                <h3 className="text-3xl font-black neon-yellow mb-6 text-center tracking-wider">
                  🎰 NEW GAME 🎰
                </h3>
                <div className="space-y-4">
                  <input
                    type="text"
                    placeholder="ROOM NAME"
                    value={roomName}
                    onChange={(e) => setRoomName(e.target.value)}
                    className="w-full px-4 py-4 rounded-lg bg-black/60 border-2 border-yellow-500/50 text-white font-mono"
                    data-testid="room-name-input"
                  />
                  <div>
                    <label className="neon-cyan text-sm font-mono">BET AMOUNT</label>
                    <input
                      type="number"
                      value={betAmount}
                      onChange={(e) => setBetAmount(parseInt(e.target.value) || 0)}
                      className="w-full px-4 py-4 rounded-lg bg-black/60 border-2 border-cyan-500/50 text-white font-mono"
                      data-testid="bet-amount-input"
                    />
                  </div>
                  <div className="flex items-center gap-3 p-3 bg-black/40 rounded-lg">
                    <input
                      type="checkbox"
                      checked={isPrivate}
                      onChange={(e) => setIsPrivate(e.target.checked)}
                      className="w-6 h-6 accent-pink-500"
                      data-testid="private-checkbox"
                    />
                    <label className="text-white font-mono">🔒 PRIVATE ROOM</label>
                  </div>
                  {isPrivate && (
                    <input
                      type="password"
                      placeholder="ROOM PASSWORD"
                      value={roomPassword}
                      onChange={(e) => setRoomPassword(e.target.value)}
                      className="w-full px-4 py-4 rounded-lg bg-black/60 border-2 border-pink-500/50 text-white font-mono"
                      data-testid="room-password-input"
                    />
                  )}
                  <motion.button
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={handleCreateRoom}
                    className="w-full py-5 rounded-lg bg-gradient-to-r from-green-500 via-emerald-500 to-cyan-500 text-black font-black text-xl tracking-wider"
                    data-testid="create-room-submit"
                  >
                    🚀 CREATE ROOM
                  </motion.button>
                </div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Room List */}
        <div className="grid md:grid-cols-2 gap-4">
          {/* Create Room Card */}
          <motion.div
            whileHover={{ scale: 1.02, boxShadow: '0 0 40px rgba(0, 255, 136, 0.5)' }}
            whileTap={{ scale: 0.98 }}
            onClick={() => setShowCreate(true)}
            className="bg-gradient-to-br from-green-900/40 to-cyan-900/40 rounded-xl p-8 border-3 border-dashed border-green-500/50 cursor-pointer flex items-center justify-center gap-4"
            data-testid="create-room-card"
          >
            <Plus className="w-10 h-10 neon-green" />
            <span className="text-2xl font-black neon-green tracking-wider">CREATE GAME</span>
          </motion.div>

          {/* Available Rooms */}
          {rooms.map((room) => (
            <motion.div
              key={room.id}
              whileHover={{ scale: 1.02, boxShadow: '0 0 40px rgba(255, 0, 85, 0.5)' }}
              whileTap={{ scale: 0.98 }}
              onClick={() => onJoinRoom(room)}
              className="modal-content rounded-xl p-6 cursor-pointer"
              data-testid={`room-${room.id}`}
            >
              <div className="flex justify-between items-start mb-4">
                <h3 className="text-xl font-black neon-yellow">{room.name}</h3>
                <span className="text-xs px-3 py-1 rounded bg-cyan-600/30 border border-cyan-500 text-cyan-300 font-mono">
                  {room.code}
                </span>
              </div>
              <div className="flex justify-between items-center text-sm font-mono">
                <span className="neon-cyan flex items-center gap-2">
                  <Users className="w-4 h-4" />
                  {room.players_count}/{room.max_players}
                </span>
                {room.bet_amount > 0 && (
                  <span className="neon-yellow flex items-center gap-1">
                    <Coins className="w-4 h-4" />
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

// ============ WAITING ROOM SCREEN ============
const WaitingRoomScreen = ({ room, user, onStartGame, onLeave, onUpdate }) => {
  const [chatInput, setChatInput] = useState('');
  const [messages, setMessages] = useState([]);
  const wsRef = useRef(null);
  const chatEndRef = useRef(null);

  useEffect(() => {
    const wsUrl = (API_URL || window.location.origin).replace('http', 'ws') + `/api/ws/${room.id}/${user.id}`;
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
    <div className="crt-screen min-h-screen p-4 bg-gradient-to-br from-[#0a0a0f] via-[#1a0a2e] to-[#0a0a0f]">
      <div className="vignette" />
      <div className="max-w-4xl mx-auto relative z-10">
        {/* Header */}
        <div className="modal-content rounded-xl p-4 mb-6">
          <div className="flex justify-between items-center">
            <div>
              <h2 className="text-3xl font-black neon-yellow tracking-wider">{room.name}</h2>
              <p className="neon-cyan font-mono">
                CODE: <span className="text-white tracking-widest">{room.code}</span>
              </p>
            </div>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={onLeave}
              className="btn-neon px-6 py-3 rounded-lg text-red-400 border-red-400 flex items-center gap-2"
              data-testid="leave-room-btn"
            >
              <X className="w-5 h-5" /> EXIT
            </motion.button>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          {/* Players */}
          <div className="modal-content rounded-xl p-6">
            <h3 className="text-xl font-black neon-pink mb-4 tracking-wider">
              // PLAYERS ({room.players.length}/4) //
            </h3>
            <div className="space-y-3">
              {room.players.map((player, idx) => (
                <motion.div
                  key={player.id}
                  initial={{ x: -50, opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  transition={{ delay: idx * 0.1 }}
                  className={`flex items-center justify-between p-4 rounded-lg border-2 ${
                    player.is_ready || player.is_bot 
                      ? 'bg-green-900/30 border-green-500/50' 
                      : 'bg-black/30 border-gray-700'
                  }`}
                  data-testid={`player-${idx}`}
                >
                  <div className="flex items-center gap-3">
                    <span className="text-3xl">{player.avatar}</span>
                    <div>
                      <div className="font-black text-white flex items-center gap-2">
                        {player.display_name}
                        {player.id === room.host_id && <Crown className="w-5 h-5 text-yellow-400" />}
                        {player.is_bot && <Bot className="w-5 h-5 neon-cyan" />}
                      </div>
                      {player.is_bot && (
                        <div className="text-xs neon-cyan font-mono">SKILL: {player.skill_level}/5</div>
                      )}
                    </div>
                  </div>
                  <span className={`text-sm font-black tracking-wider ${
                    player.is_ready || player.is_bot ? 'neon-green' : 'text-gray-500'
                  }`}>
                    {player.is_bot ? '🤖 READY' : (player.is_ready ? '✓ READY' : '⏳ WAITING')}
                  </span>
                </motion.div>
              ))}
            </div>

            {/* Actions */}
            <div className="mt-6 space-y-3">
              {isHost && room.players.length < 4 && (
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={handleAddBot}
                  className="w-full py-4 rounded-lg bg-gradient-to-r from-cyan-600 to-blue-600 text-white font-black tracking-wider flex items-center justify-center gap-2"
                  data-testid="add-bot-btn"
                >
                  <Bot className="w-6 h-6" /> ADD AI BOT
                </motion.button>
              )}
              {!isHost && (
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={handleReady}
                  className={`w-full py-4 rounded-lg font-black tracking-wider flex items-center justify-center gap-2 ${
                    myPlayer?.is_ready
                      ? 'bg-gray-600 text-white'
                      : 'bg-gradient-to-r from-green-500 to-emerald-500 text-black'
                  }`}
                  data-testid="ready-btn"
                >
                  {myPlayer?.is_ready ? '❌ CANCEL' : '✓ READY UP'}
                </motion.button>
              )}
              {isHost && (
                <motion.button
                  whileHover={canStart ? { scale: 1.02 } : {}}
                  whileTap={canStart ? { scale: 0.98 } : {}}
                  onClick={handleStart}
                  disabled={!canStart}
                  className="w-full py-5 rounded-lg bg-gradient-to-r from-yellow-500 via-orange-500 to-red-500 text-black font-black text-xl tracking-wider disabled:opacity-30 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                  data-testid="start-game-btn"
                >
                  <Zap className="w-6 h-6" /> START GAME
                </motion.button>
              )}
            </div>
          </div>

          {/* Chat */}
          <div className="modal-content rounded-xl p-6">
            <h3 className="text-xl font-black neon-cyan mb-4 tracking-wider flex items-center gap-2">
              <MessageCircle className="w-5 h-5" /> // CHAT //
            </h3>
            <div className="h-64 overflow-y-auto mb-4 bg-black/50 rounded-lg p-3 space-y-2 border border-cyan-500/20">
              {messages.map((msg, idx) => (
                <motion.div 
                  key={idx}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="text-sm font-mono"
                >
                  <span className="neon-yellow">{msg.avatar}</span>
                  <span className="neon-pink ml-1">{msg.username}:</span>
                  <span className="text-white ml-2">{msg.message}</span>
                </motion.div>
              ))}
              <div ref={chatEndRef} />
            </div>
            <div className="flex gap-2">
              <input
                type="text"
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && sendChat()}
                placeholder="TYPE MESSAGE..."
                className="flex-1 px-4 py-3 rounded-lg bg-black/60 border-2 border-cyan-500/50 text-white font-mono"
                data-testid="chat-input"
              />
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={sendChat}
                className="px-6 py-3 rounded-lg bg-cyan-600 text-white"
                data-testid="send-chat-btn"
              >
                <Send className="w-5 h-5" />
              </motion.button>
            </div>
          </div>
        </div>

        {/* Game Rules */}
        <div className="mt-6 modal-content rounded-xl p-6">
          <h3 className="text-xl font-black neon-yellow mb-4 tracking-wider">📋 GAME RULES</h3>
          <div className="grid md:grid-cols-4 gap-4 text-sm font-mono">
            <div className="p-4 bg-black/40 rounded-lg border border-yellow-500/30">
              <div className="text-2xl mb-2">👑</div>
              <div className="neon-yellow font-black">HIGH</div>
              <div className="text-gray-400">4 PTS - Highest trump dealt</div>
            </div>
            <div className="p-4 bg-black/40 rounded-lg border border-cyan-500/30">
              <div className="text-2xl mb-2">⬇️</div>
              <div className="neon-cyan font-black">LOW</div>
              <div className="text-gray-400">1 PT - Lowest trump dealt</div>
            </div>
            <div className="p-4 bg-black/40 rounded-lg border border-pink-500/30">
              <div className="text-2xl mb-2">🃏</div>
              <div className="neon-pink font-black">JACK</div>
              <div className="text-gray-400">3 PTS - Win Jack of trump</div>
            </div>
            <div className="p-4 bg-black/40 rounded-lg border border-green-500/30">
              <div className="text-2xl mb-2">🎮</div>
              <div className="neon-green font-black">GAME</div>
              <div className="text-gray-400">2 PTS - Most card points</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// ============ GAME SCREEN - BALATRO + UNO EDIT STYLE ============
const GameScreen = ({ room, gameState, user, onUpdate, onGameEnd, onLeave }) => {
  const [myHand, setMyHand] = useState([]);
  const [chatInput, setChatInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [showChat, setShowChat] = useState(false);
  const [shaking, shake] = useScreenShake();
  const [particleTrigger, setParticleTrigger] = useState(0);
  const [lastPlayedCard, setLastPlayedCard] = useState(null);
  const wsRef = useRef(null);

  // Fetch hand on mount
  useEffect(() => {
    const fetchHand = async () => {
      try {
        const response = await api.get(`/api/game/${room.id}/hand`);
        setMyHand(response.data.hand);
      } catch (err) {
        console.error('Error fetching hand:', err);
      }
    };
    fetchHand();
  }, [room.id]);

  useEffect(() => {
    const wsUrl = (API_URL || window.location.origin).replace('http', 'ws') + `/api/ws/${room.id}/${user.id}`;
    wsRef.current = new WebSocket(wsUrl);

    wsRef.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      switch (data.type) {
        case 'your_hand':
          setMyHand(data.hand);
          break;
        case 'card_played':
          shake();
          setParticleTrigger(p => p + 1);
          setLastPlayedCard(data.card);
          onUpdate(prev => ({
            ...prev,
            gameState: {
              ...prev.gameState,
              current_trick: data.current_trick || prev.gameState?.current_trick,
              current_player_idx: data.current_player_idx ?? prev.gameState?.current_player_idx
            }
          }));
          break;
        case 'turn_change':
          onUpdate(prev => ({
            ...prev,
            gameState: {
              ...prev.gameState,
              current_player_idx: data.current_player_idx
            }
          }));
          break;
        case 'trick_complete':
          if (data.jack_won) {
            setParticleTrigger(p => p + 10);
          }
          break;
        case 'round_complete':
          shake();
          setParticleTrigger(p => p + 1);
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
  }, [room.id, user.id, shake]);

  const playCard = async (card) => {
    try {
      shake();
      setParticleTrigger(p => p + 1);
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
    <div className={`crt-screen min-h-screen flex flex-col bg-gradient-to-br from-[#0a0a0f] via-[#1a0a2e] to-[#0a0a0f] ${shaking ? 'shake' : ''}`}>
      <div className="vignette" />
      <Particles trigger={particleTrigger} />
      
      {/* Top Info Bar */}
      <div className="p-4 bg-black/60 border-b-2 border-yellow-500/30 relative z-10">
        <div className="max-w-6xl mx-auto flex justify-between items-center">
          <div className="flex items-center gap-8">
            {/* Trump Chip */}
            <div className="flex items-center gap-4">
              <TrumpChip trump={gameState?.trump} />
              <div className="font-mono">
                <div className="text-xs neon-cyan">TRUMP</div>
                <div className="text-lg font-black neon-yellow">
                  {gameState?.trump?.rank}{gameState?.trump?.suit}
                </div>
              </div>
            </div>
            
            {/* Win Score */}
            <div className="score-display">
              <div className="text-xs neon-pink font-mono">WIN AT</div>
              <div className="score-value neon-yellow">14</div>
            </div>
          </div>
          
          <div className="flex gap-3">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setShowChat(!showChat)}
              className={`btn-neon px-4 py-2 rounded-lg ${showChat ? 'neon-cyan border-cyan-400' : 'text-gray-400 border-gray-600'}`}
              data-testid="toggle-chat-btn"
            >
              <MessageCircle className="w-5 h-5" />
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={onLeave}
              className="btn-neon px-4 py-2 rounded-lg text-red-400 border-red-400"
              data-testid="leave-game-btn"
            >
              <X className="w-5 h-5" />
            </motion.button>
          </div>
        </div>
      </div>

      <div className="flex-1 flex gap-4 p-4 relative z-10">
        {/* Main Game Area */}
        <div className="flex-1 flex flex-col">
          {/* Opponent Area */}
          <div className="flex justify-center gap-8 mb-8">
            {room.players.filter(p => p.id !== user.id).map((player, idx) => {
              const isCurrentPlayer = gameState?.players?.[gameState?.current_player_idx] === player.id;
              const handSize = gameState?.hand_sizes?.[player.id] || 0;
              const score = gameState?.scores?.[player.id] || 0;

              return (
                <motion.div
                  key={player.id}
                  animate={isCurrentPlayer ? { scale: [1, 1.02, 1] } : {}}
                  transition={{ repeat: Infinity, duration: 1 }}
                  className={`opponent-card rounded-xl p-4 ${isCurrentPlayer ? 'active' : ''}`}
                  data-testid={`opponent-${idx}`}
                >
                  <div className="text-center mb-3">
                    <div className="text-4xl mb-2">{player.avatar}</div>
                    <div className="font-black text-white flex items-center justify-center gap-2">
                      {player.display_name}
                      {player.is_bot && <Bot className="w-4 h-4 neon-cyan" />}
                    </div>
                    <div className="score-display inline-block mt-2 px-4 py-1">
                      <span className="score-value text-xl neon-cyan">{score}</span>
                    </div>
                  </div>
                  <div className="flex justify-center gap-1">
                    {[...Array(handSize)].map((_, i) => (
                      <CardBack key={i} small />
                    ))}
                  </div>
                </motion.div>
              );
            })}
          </div>

          {/* Turn Indicator */}
          <div className="flex justify-center mb-6">
            <motion.div
              animate={isMyTurn ? { scale: [1, 1.05, 1] } : {}}
              transition={{ repeat: Infinity, duration: 0.5 }}
              className={`turn-indicator ${isMyTurn ? 'your-turn' : 'waiting'}`}
            >
              {isMyTurn ? "🎯 YOUR TURN!" : `⏳ ${currentPlayerName}'s turn...`}
            </motion.div>
          </div>

          {/* Trick Area */}
          <div className="flex-1 flex items-center justify-center">
            <div className="trick-area w-full max-w-2xl flex items-center justify-center gap-6 p-8">
              <AnimatePresence>
                {gameState?.current_trick?.length > 0 ? (
                  gameState.current_trick.map((play, idx) => {
                    const playerName = room.players.find(p => p.id === play.player_id)?.display_name;
                    return (
                      <motion.div
                        key={idx}
                        initial={{ y: -200, scale: 2, rotate: -15, opacity: 0 }}
                        animate={{ y: 0, scale: 1, rotate: 0, opacity: 1 }}
                        transition={{ type: "spring", damping: 15 }}
                        className="text-center"
                      >
                        <Card card={play.card} played />
                        <div className="text-xs font-mono neon-cyan mt-2">{playerName}</div>
                      </motion.div>
                    );
                  })
                ) : (
                  <div className="text-gray-500 font-mono text-lg tracking-wider">
                    // WAITING FOR CARDS //
                  </div>
                )}
              </AnimatePresence>
            </div>
          </div>

          {/* Player's Hand */}
          <div className="player-area rounded-t-2xl p-6">
            <div className="text-center mb-4">
              <span className="neon-yellow font-black tracking-wider">YOUR HAND</span>
              <span className="ml-6 score-display inline-block px-4 py-1">
                <span className="score-value text-xl neon-green">{gameState?.scores?.[user.id] || 0}</span>
              </span>
            </div>
            <div className="flex justify-center gap-4 flex-wrap">
              {myHand.map((card, idx) => (
                <motion.div
                  key={`${card.suit}-${card.rank}-${idx}`}
                  initial={{ y: 100, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ delay: idx * 0.1 }}
                >
                  <Card
                    card={card}
                    playable={isMyTurn}
                    disabled={!isMyTurn}
                    onClick={() => playCard(card)}
                  />
                </motion.div>
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
              className="modal-content rounded-xl flex flex-col overflow-hidden"
            >
              <div className="p-3 border-b border-cyan-500/30">
                <h3 className="font-black neon-cyan tracking-wider">// CHAT //</h3>
              </div>
              <div className="flex-1 overflow-y-auto p-3 space-y-2">
                {messages.map((msg, idx) => (
                  <motion.div 
                    key={idx}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="text-sm font-mono"
                  >
                    <span className="neon-yellow">{msg.avatar}</span>
                    <span className="neon-pink ml-1">{msg.username}:</span>
                    <span className="text-white ml-2">{msg.message}</span>
                  </motion.div>
                ))}
              </div>
              <div className="p-3 border-t border-cyan-500/30 flex gap-2">
                <input
                  type="text"
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && sendChat()}
                  placeholder="MSG..."
                  className="flex-1 px-3 py-2 rounded-lg bg-black/60 border border-cyan-500/50 text-white text-sm font-mono"
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
      <div className="p-4 bg-black/60 border-t-2 border-yellow-500/30 relative z-10">
        <div className="flex justify-center gap-12">
          {room.players.map((player) => (
            <div key={player.id} className="text-center">
              <span className="text-2xl mr-2">{player.avatar}</span>
              <span className={`font-black text-xl ${player.id === user.id ? 'neon-yellow' : 'text-white'}`}>
                {player.display_name}
              </span>
              <span className="score-display inline-block ml-3 px-3 py-1">
                <span className={`score-value text-lg ${player.id === user.id ? 'neon-green' : 'neon-cyan'}`}>
                  {gameState?.scores?.[player.id] || 0}
                </span>
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

// ============ GAME OVER MODAL - JACKPOT STYLE ============
const GameOverModal = ({ data, onClose }) => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="fixed inset-0 modal-overlay flex items-center justify-center z-50"
    >
      <motion.div
        initial={{ scale: 0, rotate: -180 }}
        animate={{ scale: 1, rotate: 0 }}
        transition={{ type: "spring", damping: 10 }}
        className="modal-content rounded-2xl p-10 text-center max-w-md w-full mx-4"
      >
        <motion.div 
          animate={{ rotate: [0, 10, -10, 0] }}
          transition={{ repeat: Infinity, duration: 0.5 }}
          className="text-8xl mb-6"
        >
          🏆
        </motion.div>
        <h2 className="winner-text neon-yellow mb-4">WINNER!</h2>
        <div className="text-6xl mb-4">{data.winner?.avatar}</div>
        <p className="text-2xl font-black neon-cyan mb-6">{data.winner?.display_name}</p>
        
        <div className="bg-black/50 rounded-xl p-4 mb-6 border border-yellow-500/30">
          <h3 className="text-lg font-black neon-pink mb-3 tracking-wider">FINAL SCORES</h3>
          {Object.entries(data.final_scores || {}).map(([playerId, score]) => (
            <div key={playerId} className="flex justify-between text-white font-mono py-1">
              <span>{playerId === data.winner_id ? '👑 ' : ''}{playerId.substring(0, 8)}...</span>
              <span className="neon-yellow font-black">{score}</span>
            </div>
          ))}
        </div>
        
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={onClose}
          className="w-full py-5 rounded-lg bg-gradient-to-r from-cyan-500 via-blue-500 to-purple-500 text-white font-black text-xl tracking-wider"
          data-testid="back-to-lobby-btn"
        >
          🎮 BACK TO LOBBY
        </motion.button>
      </motion.div>
    </motion.div>
  );
};

// ============ LEADERBOARD SCREEN ============
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
    <div className="crt-screen min-h-screen p-4 bg-gradient-to-br from-[#0a0a0f] via-[#1a0a2e] to-[#0a0a0f]">
      <div className="vignette" />
      <div className="max-w-2xl mx-auto relative z-10">
        <div className="flex items-center gap-4 mb-6">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={onBack}
            className="btn-neon p-3 rounded-lg text-cyan-400 border-cyan-400"
            data-testid="back-btn"
          >
            <Home className="w-6 h-6" />
          </motion.button>
          <h1 className="text-4xl font-black neon-yellow neon-text tracking-wider">🏆 LEADERBOARD</h1>
        </div>

        <div className="modal-content rounded-xl overflow-hidden">
          {loading ? (
            <div className="p-8 text-center neon-cyan font-mono">LOADING...</div>
          ) : (
            <table className="w-full">
              <thead>
                <tr className="bg-black/50 border-b border-yellow-500/30">
                  <th className="p-4 text-left neon-yellow font-black">#</th>
                  <th className="p-4 text-left neon-yellow font-black">PLAYER</th>
                  <th className="p-4 text-center neon-green font-black">WINS</th>
                  <th className="p-4 text-center neon-cyan font-black">WIN%</th>
                </tr>
              </thead>
              <tbody>
                {leaderboard.map((player, idx) => (
                  <motion.tr 
                    key={player.id}
                    initial={{ x: -50, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    transition={{ delay: idx * 0.1 }}
                    className="border-b border-purple-700/30 hover:bg-purple-900/20"
                  >
                    <td className="p-4 font-black text-xl">
                      {idx === 0 ? '🥇' : idx === 1 ? '🥈' : idx === 2 ? '🥉' : `${idx + 1}`}
                    </td>
                    <td className="p-4">
                      <div className="flex items-center gap-3">
                        <span className="text-3xl">{player.avatar}</span>
                        <span className="font-black text-white">{player.display_name}</span>
                      </div>
                    </td>
                    <td className="p-4 text-center">
                      <span className="score-display px-4 py-1 inline-block">
                        <span className="score-value text-lg neon-green">{player.wins}</span>
                      </span>
                    </td>
                    <td className="p-4 text-center neon-cyan font-mono">{player.win_rate}%</td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
};

// ============ MAIN APP ============
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
    <>
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
    </>
  );
}

export default App;
