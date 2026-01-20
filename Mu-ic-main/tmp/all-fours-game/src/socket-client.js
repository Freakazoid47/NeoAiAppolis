// Socket.io client for online multiplayer
const socket = io();

let myPlayerIndex = null;
let myRoomCode = null;
let isMyTurn = false;
let gameState = null;
let myPlayerData = null;
let isRoomCreator = false;
let currentRules = null;

// Default rules
const DEFAULT_RULES = `
🏆 ALL FOURS CARD GAME RULES

📋 OBJECTIVE
Be the first team or player to reach 14 points.

🎴 DEALING
• Deal 6 cards to each player (3 at a time)
• Trump suit is determined by the next card in deck

🎯 FOUR SCORING POINTS
1. HIGH: Highest trump card dealt = 4 points
2. LOW: Lowest trump card dealt = 1 point
3. JACK: Winning the Jack of trump = 1 point
   (Bonus: +3 points if you win it = 4 points total)
4. GAME: Highest point value in tricks = 2 points
   (10=10pts, K=4pts, Q=3pts, J=2pts, A=1pt)

📏 PLAYING RULES
• Leader plays first card
• Must follow suit if possible
• Must play trump if you have it (when trump is led)
• Any card can be played if you can't follow suit
• Winner of trick leads next

🏁 WINNING
• Individual: First to 14+ points wins
• Teams (4 players): First team to 14+ points wins
• Renege: Failing to follow suit forfeits all points for that round

⚠️ HOUSE RULES
(Room creator may add custom rules here)
`;

// ===== RULES MODAL FUNCTIONS =====
function showRulesModal() {
    const modal = document.getElementById('rulesModal');
    const rulesDisplay = document.getElementById('rulesDisplay');
    const editBtn = document.getElementById('editRulesBtn');
    
    // Display rules
    rulesDisplay.innerHTML = formatRulesForDisplay(currentRules || DEFAULT_RULES);
    
    // Show edit button only for room creator
    if (isRoomCreator) {
        editBtn.style.display = 'block';
    } else {
        editBtn.style.display = 'none';
    }
    
    modal.style.display = 'flex';
}

function closeRulesModal() {
    const modal = document.getElementById('rulesModal');
    modal.style.display = 'none';
    cancelEditRules();
}

function formatRulesForDisplay(rulesText) {
    // Convert plain text to formatted HTML
    let html = '<div style="white-space: pre-wrap;">';
    html += rulesText.replace(/&/g, '&amp;')
                     .replace(/</g, '&lt;')
                     .replace(/>/g, '&gt;');
    html += '</div>';
    return html;
}

function toggleEditRules() {
    const editSection = document.getElementById('editRulesSection');
    const textarea = document.getElementById('rulesTextarea');
    const btn = document.getElementById('editRulesBtn');
    
    if (editSection.style.display === 'none') {
        editSection.style.display = 'block';
        textarea.value = currentRules || DEFAULT_RULES;
        btn.textContent = 'Close Editor';
    } else {
        editSection.style.display = 'none';
        btn.textContent = 'Edit Rules';
    }
}

function cancelEditRules() {
    const editSection = document.getElementById('editRulesSection');
    const btn = document.getElementById('editRulesBtn');
    editSection.style.display = 'none';
    btn.textContent = 'Edit Rules';
}

function saveRules() {
    const textarea = document.getElementById('rulesTextarea');
    const newRules = textarea.value.trim();
    
    if (!newRules) {
        alert('Rules cannot be empty!');
        return;
    }
    
    // Send rules update to server
    socket.emit('update-rules', { roomCode: myRoomCode, rules: newRules });
    
    // Update local rules
    currentRules = newRules;
    
    // Update display
    const rulesDisplay = document.getElementById('rulesDisplay');
    rulesDisplay.innerHTML = formatRulesForDisplay(newRules);
    
    // Close editor
    cancelEditRules();
    
    // Notify other players
    updateWaitingRoom(gameState?.players || []);
}

// ===== MENU NAVIGATION =====
function showMenu() {
    document.getElementById('menuScreen').style.display = 'flex';
    document.getElementById('createGameScreen').style.display = 'none';
    document.getElementById('joinGameScreen').style.display = 'none';
    document.getElementById('waitingRoomScreen').style.display = 'none';
    document.getElementById('gameScreen').style.display = 'none';
    closeRulesModal();
}

function showCreateGame() {
    document.getElementById('menuScreen').style.display = 'none';
    document.getElementById('createGameScreen').style.display = 'flex';
    document.getElementById('createPlayerName').focus();
}

function showJoinGame() {
    document.getElementById('menuScreen').style.display = 'none';
    document.getElementById('joinGameScreen').style.display = 'flex';
    document.getElementById('joinRoomCode').focus();
}

function showWaitingRoom() {
    document.getElementById('menuScreen').style.display = 'none';
    document.getElementById('createGameScreen').style.display = 'none';
    document.getElementById('joinGameScreen').style.display = 'none';
    document.getElementById('waitingRoomScreen').style.display = 'flex';
    document.getElementById('gameScreen').style.display = 'none';
    
    // Show rules splash when entering waiting room
    showRulesModal();
}

function showGameScreen() {
    document.getElementById('menuScreen').style.display = 'none';
    document.getElementById('waitingRoomScreen').style.display = 'none';
    document.getElementById('gameScreen').style.display = 'flex';
}

// ===== GAME CREATION/JOINING =====
function createGame() {
    const playerName = document.getElementById('createPlayerName').value.trim();
    if (!playerName) {
        alert('Please enter your name');
        return;
    }

    myPlayerData = {
        name: playerName,
        avatar: getRandomAvatar(),
        skill: Math.floor(Math.random() * 5) + 1,
        reasoning: Math.floor(Math.random() * 5) + 1
    };

    socket.emit('create-game', myPlayerData);
}

function joinGame() {
    const roomCode = document.getElementById('joinRoomCode').value.trim().toUpperCase();
    const playerName = document.getElementById('joinPlayerName').value.trim();

    if (!roomCode || !playerName) {
        alert('Please enter room code and your name');
        return;
    }

    myPlayerData = {
        name: playerName,
        avatar: getRandomAvatar(),
        skill: Math.floor(Math.random() * 5) + 1,
        reasoning: Math.floor(Math.random() * 5) + 1
    };

    socket.emit('join-game', { roomCode, playerData: myPlayerData });
}

function startOnlineGame() {
    socket.emit('start-game', { roomCode: myRoomCode });
}

function addAIPlayer() {
    if (!myRoomCode) {
        alert('Error: Not in a game room');
        return;
    }

    socket.emit('add-ai-player', { 
        roomCode: myRoomCode,
        aiData: {
            name: `AI Bot ${Math.floor(Math.random() * 1000)}`,
            avatar: getRandomAvatar(),
            skill: Math.floor(Math.random() * 5) + 1,
            reasoning: Math.floor(Math.random() * 5) + 1,
            isAI: true
        }
    });
}

function leaveGame() {
    socket.disconnect();
    showMenu();
    location.reload();
}

// ===== SOCKET.IO EVENTS =====
socket.on('game-created', (data) => {
    myRoomCode = data.roomCode;
    myPlayerIndex = data.playerIndex;
    isRoomCreator = true;  // Creator is always index 0
    currentRules = DEFAULT_RULES;
    document.getElementById('roomCodeDisplay').textContent = myRoomCode;
    updateWaitingRoom(data.players);
    showWaitingRoom();
});

socket.on('join-error', (error) => {
    alert('Error joining game: ' + error);
});

socket.on('ai-player-added', (data) => {
    // Update the waiting room with the new AI player
    updateWaitingRoom(data.players);
    
    // Show success message
    if (data.players.length === 4) {
        // Show start button when we have 4 players
        document.getElementById('startGameBtn').style.display = 'block';
    }
});

socket.on('player-joined', (data) => {
    isRoomCreator = false;  // Only creator is index 0
    if (data.rules) {
        currentRules = data.rules;
    } else {
        currentRules = DEFAULT_RULES;
    }
    updateWaitingRoom(data.players);
});

socket.on('game-started', (state) => {
    gameState = state;
    closeRulesModal();
    showGameScreen();
    updateDisplay();
});

socket.on('rules-updated', (data) => {
    currentRules = data.rules;
    // Update rules display if modal is open
    const rulesDisplay = document.getElementById('rulesDisplay');
    if (rulesDisplay) {
        rulesDisplay.innerHTML = formatRulesForDisplay(data.rules);
    }
});

socket.on('game-state', (state) => {
    gameState = state;
    updateDisplay();
});

socket.on('play-error', (error) => {
    alert('Cannot play card: ' + error);
});

socket.on('player-disconnected', (data) => {
    alert('Player ' + (data.playerIndex + 1) + ' disconnected');
});

// ===== UI UPDATES =====
function updateWaitingRoom(players) {
    const container = document.getElementById('waitingPlayers');
    container.innerHTML = '';

    players.forEach((player, idx) => {
        const slot = document.createElement('div');
        slot.className = 'player-slot';
        slot.innerHTML = `
            <div style="font-size: 1.8em; margin-bottom: 5px;">${player.avatar}</div>
            <div class="slot-number">Player ${idx + 1}</div>
            <div class="slot-status">${player.name}</div>
            <div style="font-size: 0.8em; color: #FFB703; margin-top: 3px;">
                Skill: ${player.skill} | Reasoning: ${player.reasoning}
            </div>
        `;
        container.appendChild(slot);
    });

    const startBtn = document.getElementById('startGameBtn');
    if (myPlayerIndex === 0 && players.length >= 2) {
        startBtn.style.display = 'block';
        startBtn.textContent = `Start Game (${players.length} player${players.length > 1 ? 's' : ''} ready)`;
    } else if (myPlayerIndex === 0) {
        startBtn.style.display = 'block';
        startBtn.textContent = 'Waiting for more players...';
        startBtn.disabled = true;
    } else {
        startBtn.style.display = 'none';
    }
}

function updateDisplay() {
    if (!gameState) return;

    // Update trump display
    const trumpDisplay = document.getElementById('trumpDisplay');
    trumpDisplay.textContent = gameState.trump || '-';
    trumpDisplay.style.fontSize = '1.5em';

    // Update phase display
    document.getElementById('phaseDisplay').textContent = gameState.phase === 'playing' ? 'In Play' : 'Dealing...';

    // Update current player
    const currentIdx = gameState.currentPlayerIndex;
    isMyTurn = currentIdx === myPlayerIndex;

    // Update player hand
    updatePlayerHand();

    // Update other players
    updateOtherPlayersHands();

    // Update trick area
    updateTrickArea();

    // Update scores
    updateScoresDisplay();

    // Update status
    if (isMyTurn && gameState.phase === 'playing') {
        document.getElementById('statusText').textContent = 'Your turn - Play a card';
    } else if (gameState.phase === 'playing') {
        const playerName = gameState.players[currentIdx].name;
        document.getElementById('statusText').textContent = `${playerName}'s turn...`;
    } else {
        document.getElementById('statusText').textContent = 'Dealing...';
    }
}

function updatePlayerHand() {
    const container = document.getElementById('playerHand');
    const myPlayer = gameState.players[myPlayerIndex];
    
    if (!myPlayer) return;

    container.innerHTML = '';
    
    myPlayer.hand.forEach(card => {
        const cardHtml = createCardHtml(card);
        const cardDiv = document.createElement('div');
        cardDiv.innerHTML = cardHtml;
        
        const cardEl = cardDiv.querySelector('.card');
        
        if (isMyTurn && gameState.phase === 'playing') {
            cardEl.style.cursor = 'pointer';
            cardEl.addEventListener('click', () => {
                socket.emit('play-card', { roomCode: myRoomCode, card });
            });
        } else {
            cardEl.style.opacity = '0.6';
            cardEl.style.cursor = 'default';
        }
        
        container.appendChild(cardEl);
    });
}

function updateOtherPlayersHands() {
    const container = document.getElementById('otherPlayersSection');
    if (!container) return;
    
    container.innerHTML = '';
    
    gameState.players.forEach((player, idx) => {
        if (idx !== myPlayerIndex) {
            const playerDiv = document.createElement('div');
            playerDiv.className = 'player-display';
            
            const skillColor = getSkillColor(player.skill);
            const reasoningColor = getReasoningColor(player.reasoning);
            const isActive = idx === gameState.currentPlayerIndex ? 'border-color: var(--accent); box-shadow: 0 0 20px rgba(0, 217, 255, 0.5);' : '';
            
            playerDiv.innerHTML = `
                <div style="font-size: 2em; margin-bottom: 5px;">${player.avatar}</div>
                <div style="font-weight: bold; font-size: 0.9em; color: #FFB703;">${player.name}</div>
                <div style="font-size: 0.85em; margin-top: 3px;">
                    <span style="color: ${skillColor};">⚔️ Skill: ${player.skill}</span>
                </div>
                <div style="font-size: 0.85em;">
                    <span style="color: ${reasoningColor};">🧠 Reason: ${player.reasoning}</span>
                </div>
                <div style="margin-top: 8px; display: flex; gap: 3px; flex-wrap: wrap;">
                    ${Array(Math.min(player.hand.length, 6)).fill('🂠').map((card, i) => 
                        `<div class="card-back" style="transform: translateY(${(i-2)*8}px);">${card}</div>`
                    ).join('')}
                </div>
            `;
            
            playerDiv.style.cssText = isActive + (playerDiv.style.cssText || '');
            container.appendChild(playerDiv);
        }
    });
}

function updateTrickArea() {
    const container = document.getElementById('trickArea');
    container.innerHTML = '';
    
    if (gameState.currentTrick.length > 0) {
        gameState.currentTrick.forEach(play => {
            const card = play.card;
            const cardHtml = createCardHtml(card);
            const div = document.createElement('div');
            div.innerHTML = cardHtml;
            div.style.marginRight = '15px';
            container.appendChild(div.querySelector('.card'));
        });
    }
}

function updateScoresDisplay() {
    const container = document.getElementById('scoresDisplay');
    let html = '';
    
    gameState.players.forEach((player, idx) => {
        const isMe = idx === myPlayerIndex ? ' (You)' : '';
        html += `<span style="margin-right: 20px; color: ${idx === gameState.currentPlayerIndex ? 'var(--gold)' : 'inherit'};">${player.name}${isMe}: ${player.score || 0}</span>`;
    });
    
    container.innerHTML = html;
}

// ===== UTILITY FUNCTIONS (from utils.js) =====
// Shared utilities are available globally from utils.js
// If used as module: const { getRandomAvatar, ... } = require('./utils');

// Create HTML for a card display with Mughal-inspired face card designs
function createCardHtml(card) {
    if (!card) return '<div class="card" style="visibility: hidden;"></div>';
    
    const isRed = card.suit === '♥' || card.suit === '♦';
    const colorClass = isRed ? 'red' : 'black';
    const isFaceCard = ['J', 'Q', 'K'].includes(card.rank);
    
    if (isFaceCard) {
        return createFaceCardHtml(card, colorClass);
    }
    
    return `<div class="card ${colorClass}">
        <div style="font-size: 0.7em; line-height: 1.2;">
            <div>${card.rank}</div>
            <div>${card.suit}</div>
        </div>
    </div>`;
}

// Create Manga/Anime-inspired otherworldly face card with cosmic effects
function createFaceCardHtml(card, colorClass) {
    const titles = {
        'J': { name: 'Kaze', title: '風の戦士', style: 'Wind Warrior', power: '⚡' },
        'Q': { name: 'Yuki', title: '氷の女王', style: 'Ice Empress', power: '❄️' },
        'K': { name: 'Kurogane', title: '鋼鉄の帝王', style: 'Steel Emperor', power: '⚔️' }
    };
    
    const title = titles[card.rank];
    const isCrimson = colorClass === 'red';
    
    return `<div class="card ${colorClass} face-card manga-card">
        <div class="face-card-container">
            <!-- Cosmic background effect -->
            <div class="cosmic-background"></div>
            
            <!-- Aura layers -->
            <div class="character-aura aura-outer"></div>
            <div class="character-aura aura-middle"></div>
            
            <!-- Japanese characters with glow -->
            <div class="japanese-title">${title.title}</div>
            
            <!-- Anime portrait circle -->
            <div class="anime-portrait">
                <div class="portrait-frame-anime"></div>
                <div class="manga-face">
                    ${getMangaPortrait(card.rank)}
                </div>
                <div class="portrait-aura"></div>
                <div class="glitch-effect-1"></div>
                <div class="glitch-effect-2"></div>
            </div>
            
            <!-- Power indicator -->
            <div class="power-indicator">${title.power}</div>
            
            <!-- Title with manga style -->
            <div class="manga-title">
                <div class="title-rank-anime">${card.rank}</div>
                <div class="title-name-anime">${title.name}</div>
                <div class="title-style-anime">${title.style}</div>
            </div>
            
            <!-- Energy lines -->
            <div class="energy-line-top"></div>
            <div class="energy-line-bottom"></div>
            
            <!-- Suit with magical effect -->
            <div class="suit-indicator-anime magical-glow">${card.suit}</div>
            
            <!-- Particle effect container -->
            <div class="particle-field"></div>
        </div>
    </div>`;
}

// Generate Manga/Anime portrait based on rank with supernatural style
function getMangaPortrait(rank) {
    const portraits = {
        'J': `<svg viewBox="0 0 100 120" class="manga-svg">
            <defs>
                <radialGradient id="electricAuraJ" cx="40%" cy="30%">
                    <stop offset="0%" style="stop-color:#FFD700;stop-opacity:0.8" />
                    <stop offset="100%" style="stop-color:#FF6B00;stop-opacity:0" />
                </radialGradient>
                <filter id="glow-j">
                    <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
                    <feMerge>
                        <feMergeNode in="coloredBlur"/>
                        <feMergeNode in="SourceGraphic"/>
                    </feMerge>
                </filter>
            </defs>
            <!-- Electric aura -->
            <circle cx="50" cy="45" r="28" fill="url(#electricAuraJ)" opacity="0.6"/>
            <!-- Face -->
            <circle cx="50" cy="48" r="20" fill="#FDD0A5" filter="url(#glow-j)"/>
            <!-- Spiky anime hair -->
            <path d="M 35 25 L 30 10 L 35 20" fill="#1a1a2e"/>
            <path d="M 50 18 L 48 0 L 52 18" fill="#1a1a2e"/>
            <path d="M 65 25 L 70 10 L 65 20" fill="#1a1a2e"/>
            <path d="M 75 35 L 85 25 L 75 40" fill="#1a1a2e"/>
            <!-- Large expressive anime eyes -->
            <ellipse cx="40" cy="42" rx="5" ry="8" fill="#FFFFFF"/>
            <ellipse cx="60" cy="42" rx="5" ry="8" fill="#FFFFFF"/>
            <circle cx="40" cy="44" r="3.5" fill="#0047AB"/>
            <circle cx="60" cy="44" r="3.5" fill="#0047AB"/>
            <circle cx="40.5" cy="42" r="1.5" fill="#FFFFFF"/>
            <circle cx="60.5" cy="42" r="1.5" fill="#FFFFFF"/>
            <!-- Intense expression -->
            <line x1="35" y1="38" x2="32" y2="35" stroke="#1a1a2e" stroke-width="1"/>
            <line x1="65" y1="38" x2="68" y2="35" stroke="#1a1a2e" stroke-width="1"/>
            <!-- Battle scars/marks -->
            <line x1="45" y1="50" x2="48" y2="55" stroke="#E74C3C" stroke-width="1.5" opacity="0.7"/>
            <!-- Energy sparkles -->
            <circle cx="30" cy="35" r="2" fill="#FFD700" opacity="0.8"/>
            <circle cx="70" cy="35" r="2" fill="#FFD700" opacity="0.8"/>
        </svg>`,
        'Q': `<svg viewBox="0 0 100 120" class="manga-svg">
            <defs>
                <radialGradient id="frostAuraQ" cx="40%" cy="30%">
                    <stop offset="0%" style="stop-color:#00D9FF;stop-opacity:0.8" />
                    <stop offset="100%" style="stop-color:#0099CC;stop-opacity:0" />
                </radialGradient>
                <filter id="glow-q">
                    <feGaussianBlur stdDeviation="2.5" result="coloredBlur"/>
                    <feMerge>
                        <feMergeNode in="coloredBlur"/>
                        <feMergeNode in="SourceGraphic"/>
                    </feMerge>
                </filter>
            </defs>
            <!-- Frost aura -->
            <circle cx="50" cy="45" r="30" fill="url(#frostAuraQ)" opacity="0.5"/>
            <!-- Face -->
            <circle cx="50" cy="48" r="20" fill="#F5E6D3" filter="url(#glow-q)"/>
            <!-- Long flowing anime hair -->
            <path d="M 32 30 Q 25 50 30 70" stroke="#1a4d7a" stroke-width="4" fill="none"/>
            <path d="M 68 30 Q 75 50 70 70" stroke="#1a4d7a" stroke-width="4" fill="none"/>
            <path d="M 40 18 L 35 5 L 42 16" fill="#1a4d7a"/>
            <path d="M 60 18 L 65 5 L 58 16" fill="#1a4d7a"/>
            <!-- Large mystical eyes -->
            <ellipse cx="38" cy="40" rx="6" ry="9" fill="#E0F7FF"/>
            <ellipse cx="62" cy="40" rx="6" ry="9" fill="#E0F7FF"/>
            <circle cx="38" cy="44" r="4" fill="#00BFFF"/>
            <circle cx="62" cy="44" r="4" fill="#00BFFF"/>
            <circle cx="38.5" cy="42" r="1.5" fill="#FFFFFF"/>
            <circle cx="62.5" cy="42" r="1.5" fill="#FFFFFF"/>
            <!-- Regal expression -->
            <path d="M 45 58 Q 50 62 55 58" stroke="#1a1a2e" stroke-width="1.5" fill="none"/>
            <!-- Magic markings -->
            <line x1="32" y1="48" x2="26" y2="50" stroke="#00D9FF" stroke-width="1.5" opacity="0.7"/>
            <line x1="68" y1="48" x2="74" y2="50" stroke="#00D9FF" stroke-width="1.5" opacity="0.7"/>
            <!-- Crown of ice crystals -->
            <circle cx="50" cy="20" r="4" fill="#E0F7FF"/>
            <circle cx="42" cy="22" r="2.5" fill="#00BFFF"/>
            <circle cx="58" cy="22" r="2.5" fill="#00BFFF"/>
        </svg>`,
        'K': `<svg viewBox="0 0 100 120" class="manga-svg">
            <defs>
                <radialGradient id="infernoAuraK" cx="40%" cy="30%">
                    <stop offset="0%" style="stop-color:#FF4500;stop-opacity:0.8" />
                    <stop offset="100%" style="stop-color:#8B0000;stop-opacity:0" />
                </radialGradient>
                <filter id="glow-k">
                    <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
                    <feMerge>
                        <feMergeNode in="coloredBlur"/>
                        <feMergeNode in="SourceGraphic"/>
                    </feMerge>
                </filter>
            </defs>
            <!-- Inferno aura -->
            <circle cx="50" cy="45" r="32" fill="url(#infernoAuraK)" opacity="0.6"/>
            <!-- Face -->
            <circle cx="50" cy="48" r="21" fill="#E5C9B8" filter="url(#glow-k)"/>
            <!-- Wild spiky hair like fire -->
            <path d="M 30 22 L 25 5 L 32 20" fill="#3d1a0a"/>
            <path d="M 42 16 L 40 -2 L 45 16" fill="#3d1a0a"/>
            <path d="M 58 16 L 60 -2 L 55 16" fill="#3d1a0a"/>
            <path d="M 70 22 L 75 5 L 68 20" fill="#3d1a0a"/>
            <path d="M 78 40 L 90 35 L 77 45" fill="#3d1a0a"/>
            <!-- Intimidating eyes -->
            <ellipse cx="37" cy="38" rx="6" ry="10" fill="#FFE4B5"/>
            <ellipse cx="63" cy="38" rx="6" ry="10" fill="#FFE4B5"/>
            <circle cx="37" cy="45" r="5" fill="#8B0000"/>
            <circle cx="63" cy="45" r="5" fill="#8B0000"/>
            <circle cx="37.5" cy="42" r="2" fill="#FF6347"/>
            <circle cx="63.5" cy="42" r="2" fill="#FF6347"/>
            <!-- Scar marks -->
            <line x1="30" y1="38" x2="25" y2="42" stroke="#8B4513" stroke-width="2" opacity="0.6"/>
            <line x1="70" y1="38" x2="75" y2="42" stroke="#8B4513" stroke-width="2" opacity="0.6"/>
            <!-- Fierce expression -->
            <path d="M 40 60 L 50 64 L 60 60" stroke="#1a1a2e" stroke-width="2" fill="none"/>
            <!-- Demonic marks -->
            <circle cx="45" cy="35" r="2" fill="#FF4500" opacity="0.8"/>
            <circle cx="55" cy="35" r="2" fill="#FF4500" opacity="0.8"/>
        </svg>`
    };
    
    return portraits[rank] || '';
}

// Get skill level color
function getSkillColor(skill) {
    const colors = ['#888', '#FFD700', '#FF6347', '#32CD32', '#FF00FF'];
    return colors[Math.min(skill - 1, 4)] || '#888';
}

// Get reasoning color
function getReasoningColor(reasoning) {
    const colors = ['#888', '#87CEEB', '#00BFFF', '#00CED1', '#FF1493'];
    return colors[Math.min(reasoning - 1, 4)] || '#888';
}

// Show menu on load
document.addEventListener('DOMContentLoaded', () => {
    showMenu();
});
