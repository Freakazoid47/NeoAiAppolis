// Game State
const gameState = {
    players: [],
    selectedPlayers: [],
    currentPlayerIndex: 0,
    dealer: 0,
    trump: null,
    currentTrick: [],
    tricks: [],
    phase: 'lobby', // lobby, dealing, playing, scoring, gameover
    gameWinScore: 14,
    teamMode: false, // Set to true when 4 players (partnership variant)
    teamScores: { team1: 0, team2: 0 } // Team scores for 4-player game
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    updateLobbyDisplay();
});

// ===== LOBBY FUNCTIONS =====
function togglePlayer(slot) {
    slot = parseInt(slot);
    
    if (gameState.selectedPlayers.includes(slot)) {
        gameState.selectedPlayers = gameState.selectedPlayers.filter(s => s !== slot);
    } else {
        if (gameState.selectedPlayers.length < 4) {
            gameState.selectedPlayers.push(slot);
            gameState.selectedPlayers.sort((a, b) => a - b);
        }
    }
    
    updateLobbyDisplay();
}

function updateLobbyDisplay() {
    for (let i = 1; i <= 4; i++) {
        const slot = document.querySelector(`[data-slot="${i}"]`);
        const btn = slot.querySelector('.slot-btn');
        const status = slot.querySelector('.slot-status');
        
        if (gameState.selectedPlayers.includes(i)) {
            slot.classList.add('active');
            btn.textContent = 'Leave';
            status.textContent = 'Ready';
        } else {
            slot.classList.remove('active');
            btn.textContent = 'Join';
            status.textContent = 'Open';
        }
    }
    
    const startBtn = document.getElementById('startBtn');
    const count = gameState.selectedPlayers.length;
    
    if (count >= 2 && count <= 4) {
        startBtn.disabled = false;
        startBtn.textContent = `Start Game (${count} Players)`;
    } else {
        startBtn.disabled = true;
        startBtn.textContent = 'Start Game (Select 2-4 Players)';
    }
}

function startGame() {
    if (gameState.selectedPlayers.length < 2) return;
    
    // Determine if team mode (4 players = partnership variant)
    gameState.teamMode = gameState.selectedPlayers.length === 4;
    gameState.teamScores = { team1: 0, team2: 0 };
    
    // Setup players with avatars and skill levels (getRandomAvatar from utils.js)
    gameState.players = gameState.selectedPlayers.map(slot => {
    
    gameState.phase = 'dealing';
    
    // Hide lobby, show game
    document.getElementById('lobbyScreen').style.display = 'none';
    document.getElementById('gameScreen').style.display = 'flex';
    
    // Create other player card displays
    createOtherPlayerDisplays();
    
    // Start the game
    dealRound();
}


function createOtherPlayerDisplays() {
    const section = document.getElementById('otherPlayersSection');
    if (!section) return;  // Exit if not in game screen
    section.innerHTML = '';
    
    for (let i = 1; i < gameState.players.length; i++) {
        const playerDiv = document.createElement('div');
        playerDiv.className = 'player-display';
        
        const player = gameState.players[i];
        const avatarDiv = document.createElement('div');
        avatarDiv.style.fontSize = '2em';
        avatarDiv.style.marginBottom = '5px';
        avatarDiv.textContent = player.avatar || '🤖';
        
        const nameDiv = document.createElement('div');
        nameDiv.className = 'player-name';
        nameDiv.textContent = `Player ${player.slot}`;
        
        const cardsDiv = document.createElement('div');
        cardsDiv.className = 'player-cards';
        cardsDiv.id = `player${i}Cards`;
        
        playerDiv.appendChild(avatarDiv);
        playerDiv.appendChild(nameDiv);
        playerDiv.appendChild(cardsDiv);
        section.appendChild(playerDiv);
    }
}

function backToLobby() {
    document.getElementById('lobbyScreen').style.display = 'flex';
    document.getElementById('gameScreen').style.display = 'none';
    gameState.phase = 'lobby';
    gameState.selectedPlayers = [];
    updateLobbyDisplay();
}

// ===== CARD FUNCTIONS (from utils.js) =====
// Note: In browser context, utils functions are already defined globally
// If needed as module, use: const { createDeck, cardToString, ... } = require('./utils');

// ===== SCORING HELPERS =====
function scoreHighCard(players, trump) {
    let highest = null;
    let highPlayer = null;
    for (let player of players) {
        for (let card of player.dealt) {
            if (card.suit === trump) {
                if (!highest || getRankValue(card.rank) > getRankValue(highest.rank)) {
                    highest = card;
                    highPlayer = player;
                }
            }
        }
    }
    return highPlayer;
}

function scoreLowCard(players, trump) {
    let lowest = null;
    let lowPlayer = null;
    for (let player of players) {
        for (let card of player.dealt) {
            if (card.suit === trump) {
                if (!lowest || getRankValue(card.rank) < getRankValue(lowest.rank)) {
                    lowest = card;
                    lowPlayer = player;
                }
            }
        }
    }
    return lowPlayer;
}

function scoreGamePoints(tricks, players, trump) {
    const pointTotals = {};
    players.forEach(p => pointTotals[p.slot] = 0);
    
    for (let trick of tricks) {
        for (let play of trick.cards) {
            pointTotals[players[trick.winner].slot] += getCardPoints(play.card.rank);
        }
    }
    
    let maxSlot = null;
    let maxPoints = -1;
    for (let [slot, points] of Object.entries(pointTotals)) {
        if (points > maxPoints) {
            maxPoints = points;
            maxSlot = slot;
        }
    }
    return maxSlot;
}

// ===== GAME FLOW =====
function dealRound() {
    const deck = createDeck();
    
    // Deal 6 cards (3-3) to each player
    let cardIdx = 0;
    for (let round = 0; round < 2; round++) {
        for (let player of gameState.players) {
            for (let i = 0; i < 3; i++) {
                player.hand.push(deck[cardIdx++]);
            }
        }
    }
    
    // Save original dealt hands for scoring
    gameState.players.forEach(p => p.dealt = JSON.parse(JSON.stringify(p.hand)));
    
    // Trump
    gameState.trump = deck[cardIdx];
    gameState.currentTrick = [];
    gameState.tricks = [];
    
    gameState.phase = 'playing';
    updateDisplay();
    
    // Start playing
    setTimeout(() => playRound(), 800);
}

function playRound() {
    if (gameState.players[0].hand.length === 0) {
        // Round over, score it
        scoreRound();
        return;
    }
    
    gameState.phase = 'playing';
    gameState.currentTrick = [];
    
    // Reset renege flags for new trick
    gameState.players.forEach(p => p.reneged = false);
    
    // Leader leads
    const leader = gameState.dealer === 0 ? 1 : 0;
    gameState.currentPlayerIndex = leader;
    
    playTrick();
}

function playTrick() {
    const player = gameState.players[gameState.currentPlayerIndex];
    
    if (gameState.currentPlayerIndex === 0) {
        // Human player
        updateStatus(`Your turn - ${gameState.currentTrick.length === 0 ? 'Lead' : 'Play'} a card`);
        updateDisplay();
    } else {
        // Computer player
        updateStatus(`Computer ${gameState.currentPlayerIndex} playing...`);
        updateDisplay();
        setTimeout(() => {
            const card = chooseCard(gameState.currentPlayerIndex);
            playCard(gameState.currentPlayerIndex, card);
        }, 800);
    }
}

function chooseCard(playerIdx) {
    const player = gameState.players[playerIdx];
    const isLead = gameState.currentTrick.length === 0;
    
    if (isLead) {
        // Lead: prefer non-trump
        const nonTrump = player.hand.filter(c => c.suit !== gameState.trump.suit);
        return nonTrump.length > 0 ? nonTrump[0] : player.hand[0];
    } else {
        // Follow suit if possible
        const leadSuit = gameState.currentTrick[0].card.suit;
        const same = player.hand.filter(c => c.suit === leadSuit);
        if (same.length > 0) {
            return same[0];
        }
        
        // Otherwise any card
        return player.hand[0];
    }
}

function playCard(playerIdx, card) {
    const player = gameState.players[playerIdx];
    const idx = player.hand.indexOf(card);
    
    if (idx === -1) return;
    
    // Check for renege (failed to follow suit when able)
    if (gameState.currentTrick.length > 0) {
        const leadSuit = gameState.currentTrick[0].card.suit;
        const hasLedSuit = player.hand.some(c => c.suit === leadSuit);
        const isPlayingLedSuit = card.suit === leadSuit;
        
        // If player has the led suit but is playing a different suit, this is a renege violation
        if (hasLedSuit && !isPlayingLedSuit) {
            // Renege detected - player forfeits all points this round
            player.reneged = true;
            player.hand.splice(idx, 1);
            gameState.currentTrick.push({
                playerIdx,
                card
            });
            updateDisplay();
            return 'renege'; // Signal renege to calling function
        }
    }
    
    player.hand.splice(idx, 1);
    gameState.currentTrick.push({
        playerIdx,
        card
    });
    
    // Play card sound
    playCardSound();
    
    // Add flick animation to displayed card
    if (playerIdx === 0) {
        setTimeout(() => {
            const cardElements = document.querySelectorAll('.trick-slot .card');
            if (cardElements.length > 0) {
                cardElements[cardElements.length - 1].classList.add('flick');
            }
        }, 50);
    }
    
    updateDisplay();
    
    // If trick is complete, resolve it
    if (gameState.currentTrick.length === gameState.players.length) {
        setTimeout(() => resolveTrick(), 1000);
    } else {
        // Next player
        gameState.currentPlayerIndex = (gameState.currentPlayerIndex + 1) % gameState.players.length;
        setTimeout(() => playTrick(), 500);
    }
}

function resolveTrick() {
    // Find winner of trick using utility function
    const winnerTrick = determineWinner(gameState.currentTrick, gameState.trump.suit);
    const winner = gameState.currentTrick[winnerTrick];
    const winnerPlayerIdx = winner.playerIdx;
    
    gameState.tricks.push({
        winner: winnerPlayerIdx,
        cards: gameState.currentTrick.slice()
    });
    
    // Check for jack of trump
    if (isJackCard(winner.card, gameState.trump.suit)) {
        playJackSound();
        hangTheJack(winnerPlayerIdx);
        const message = winnerPlayerIdx === 0 ? '🎉 YOU HUNG THE JACK! 🎉' : `🎉 Player ${winnerPlayerIdx + 1} hung the jack!`;
        updateStatus(message);
    } else {
        updateStatus(`Player ${winnerPlayerIdx + 1} wins the trick!`);
    }
    
    // Next trick with winner leading
    gameState.currentPlayerIndex = winnerPlayerIdx;
    gameState.currentTrick = [];
    
    setTimeout(() => playRound(), 1500);
}

function scoreRound() {
    gameState.phase = 'scoring';
    
    const scores = {};
    gameState.players.forEach(p => scores[p.slot] = 0);
    
    const trump = gameState.trump.suit;
    
    // HIGH - highest trump dealt
    const highPlayer = scoreHighCard(gameState.players, trump);
    if (highPlayer) scores[highPlayer.slot]++;
    
    // LOW - lowest trump dealt
    const lowPlayer = scoreLowCard(gameState.players, trump);
    if (lowPlayer) scores[lowPlayer.slot]++;
    
    // JACK - won the jack of trump in tricks (1 point)
    // HANG JACK - bonus 3 points awarded when you win the jack
    for (let trick of gameState.tricks) {
        for (let play of trick.cards) {
            if (isJackCard(play.card, trump)) {
                scores[gameState.players[trick.winner].slot]++;
                scores[gameState.players[trick.winner].slot] += 3; // Hang Jack bonus
            }
        }
    }
    
    // GAME - highest card points in tricks (1 point)
    const maxSlot = scoreGamePoints(gameState.tricks, gameState.players, trump);
    if (maxSlot) scores[maxSlot]++;
    
    // Check for renege violations - player loses all points in the round
    const renegedPlayers = gameState.players.filter(p => p.reneged);
    if (renegedPlayers.length > 0) {
        renegedPlayers.forEach(p => {
            scores[p.slot] = 0;
        });
        updateStatus(`⚠️ Renege! ${renegedPlayers.map(p => `Player ${p.slot}`).join(', ')} forfeits all points this round!`);
    }
    
    // Update scores (individual or team-based)
    if (gameState.teamMode) {
        // Team mode: combine partner scores
        let team1Points = scores[1] + scores[3]; // Players 1 & 3 are team1
        let team2Points = scores[2] + scores[4]; // Players 2 & 4 are team2
        
        gameState.teamScores.team1 += team1Points;
        gameState.teamScores.team2 += team2Points;
        
        // Update individual player scores for display
        gameState.players.forEach(p => {
            p.score = p.team === 'team1' ? gameState.teamScores.team1 : gameState.teamScores.team2;
        });
        
        updateStatus(`Round scores: Team 1 (${team1Points}pts) | Team 2 (${team2Points}pts)`);
    } else {
        // Individual mode
        for (let player of gameState.players) {
            player.score += scores[player.slot];
        }
    }
    
    updateDisplay();
    
    // Check win
    let winner = null;
    let winningTeam = null;
    
    if (gameState.teamMode) {
        // Team mode: check if either team reached 14 points
        if (gameState.teamScores.team1 >= gameState.gameWinScore) {
            winningTeam = 'team1';
            winner = gameState.players.find(p => p.team === 'team1');
        } else if (gameState.teamScores.team2 >= gameState.gameWinScore) {
            winningTeam = 'team2';
            winner = gameState.players.find(p => p.team === 'team2');
        }
        
        if (winner) {
            const team1Players = gameState.players.filter(p => p.team === 'team1').map(p => p.slot).join(' & ');
            const team2Players = gameState.players.filter(p => p.team === 'team2').map(p => p.slot).join(' & ');
            updateStatus(`<strong>Team ${winningTeam === 'team1' ? `1 (Players ${team1Players})` : `2 (Players ${team2Players})`} WINS!</strong>`);
        }
    } else {
        // Individual mode
        winner = gameState.players.find(p => p.score >= gameState.gameWinScore);
        if (winner) {
            updateStatus(`<strong>${winner.isHuman ? 'You' : 'Player ' + winner.slot} WIN!</strong>`);
        }
    }
    
    if (winner) {
        gameState.phase = 'gameover';
        setTimeout(() => {
            backToLobby();
        }, 3000);
    } else {
        // Next round
        gameState.dealer = (gameState.dealer + 1) % gameState.players.length;
        gameState.players[0].tricks = [];
        gameState.players.forEach(p => p.tricks = []);
        
        updateStatus('Next round starting...');
        setTimeout(() => {
            dealRound();
        }, 2000);
    }
}

// ===== UI UPDATES =====
function updateDisplay() {
    updateScores();
    updateTrump();
    updateTrickArea();
    updatePlayerHand();
}

function updateScores() {
    let html = '';
    for (let player of gameState.players) {
        html += `<span>Player ${player.slot}: <strong>${player.score}</strong></span> &nbsp; `;
    }
    document.getElementById('scoresDisplay').innerHTML = html;
}

function updateTrump() {
    if (gameState.trump) {
        const color = isRedSuit(gameState.trump.suit) ? '#e74c3c' : '#000';
        document.getElementById('trumpDisplay').innerHTML = `<span style="color: ${color}">${gameState.trump.rank}${gameState.trump.suit}</span>`;
        document.getElementById('phaseDisplay').textContent = 'Playing';
    }
}

function updateTrickArea() {
    const area = document.getElementById('trickArea');
    area.innerHTML = '';
    
    for (let trick of gameState.currentTrick) {
        const slot = document.createElement('div');
        slot.className = 'trick-slot';
        slot.innerHTML = createCardHtml(trick.card);
        area.appendChild(slot);
    }
}

function updatePlayerHand() {
    const hand = document.getElementById('playerHand');
    if (!hand) return;  // Handle case where playerHand doesn't exist
    const player = gameState.players[0];
    
    hand.innerHTML = '';
    
    for (let i = 0; i < player.hand.length; i++) {
        const card = player.hand[i];
        const div = document.createElement('div');
        div.className = 'card ' + (isRedSuit(card.suit) ? 'red' : 'black');
        
        // Check if playable - only when it's human's turn
        const isHumanTurn = gameState.phase === 'playing' && gameState.currentPlayerIndex === 0;
        if (isHumanTurn) {
            div.classList.add('playable');
            const cardIndex = i;
            div.onclick = () => {
                const selectedCard = player.hand[cardIndex];
                if (selectedCard) {
                    playCard(0, selectedCard);
                }
            };
        } else if (gameState.phase === 'playing') {
            div.classList.add('invalid');
        }
        
        div.textContent = cardToString(card);
        hand.appendChild(div);
    }
    
    updateOtherPlayersHands();
}

function createPlayerDisplay(player, idx) {
    const playerDiv = document.createElement('div');
    playerDiv.className = 'player-display';
    
    const skillColor = getSkillColor(player.skill);
    const reasoningColor = getReasoningColor(player.reasoning);
    
    playerDiv.innerHTML = `
        <div style="font-size: 2em; margin-bottom: 5px;">${player.avatar}</div>
        <div style="font-weight: bold; font-size: 0.9em; color: #FFB703;">Player ${player.slot}</div>
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
    
    return playerDiv;
}

function updateOtherPlayersHands() {
    const container = document.getElementById('otherPlayersSection');
    if (!container) return;  // Return silently if not in game screen
    
    container.innerHTML = '';
    
    gameState.players.forEach((player, idx) => {
        if (!player.isHuman) {
            container.appendChild(createPlayerDisplay(player, idx));
        }
    });
}

function createCardHtml(card) {
    const color = isRedSuit(card.suit) ? 'red' : 'black';
    return `<div class="card ${color}">${cardToString(card)}</div>`;
}

function updateStatus(text) {
    document.getElementById('statusText').innerHTML = text;
}

function playCardSound() {
    // Bird chirp sound effect
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const now = audioContext.currentTime;
    
    // First chirp - ascending
    for (let i = 0; i < 3; i++) {
        const osc = audioContext.createOscillator();
        const gain = audioContext.createGain();
        
        osc.connect(gain);
        gain.connect(audioContext.destination);
        
        const startFreq = 1200 + (i * 200);
        const endFreq = startFreq + 400;
        
        osc.frequency.setValueAtTime(startFreq, now + (i * 0.05));
        osc.frequency.exponentialRampToValueAtTime(endFreq, now + (i * 0.05) + 0.08);
        
        gain.gain.setValueAtTime(0.25, now + (i * 0.05));
        gain.gain.exponentialRampToValueAtTime(0.01, now + (i * 0.05) + 0.08);
        
        osc.start(now + (i * 0.05));
        osc.stop(now + (i * 0.05) + 0.08);
    }
}

function playJackSound() {
    // Excited bird chirping with distortion effect
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const now = audioContext.currentTime;
    
    // Multiple rapid chirps
    const chirpPattern = [1500, 1800, 1600, 2000, 1700];
    
    chirpPattern.forEach((freq, idx) => {
        const osc = audioContext.createOscillator();
        const gain = audioContext.createGain();
        const waveshaper = audioContext.createWaveShaper();
        
        // Create distortion curve for "raspy" bird sound
        const curve = new Float32Array(65536);
        for (let i = 0; i < 65536; i++) {
            const x = (i * 2) / 65536 - 1;
            curve[i] = ((Math.PI + 2) / Math.PI) * x + ((2 / Math.PI) * Math.pow(x, 3));
        }
        waveshaper.curve = curve;
        
        osc.connect(waveshaper);
        waveshaper.connect(gain);
        gain.connect(audioContext.destination);
        
        const startTime = now + (idx * 0.08);
        osc.frequency.setValueAtTime(freq, startTime);
        osc.frequency.exponentialRampToValueAtTime(freq * 1.3, startTime + 0.06);
        
        gain.gain.setValueAtTime(0.2, startTime);
        gain.gain.exponentialRampToValueAtTime(0.01, startTime + 0.06);
        
        osc.start(startTime);
        osc.stop(startTime + 0.06);
    });
}

function hangTheJack(playerIdx) {
    const trickArea = document.getElementById('trickArea');
    
    // Add visual celebration
    const celebration = document.createElement('div');
    celebration.style.position = 'absolute';
    celebration.style.fontSize = '60px';
    celebration.style.pointerEvents = 'none';
    celebration.style.animation = 'celebration 1.5s ease-out forwards';
    celebration.textContent = '♠ 🎊 ♠';
    celebration.style.left = '50%';
    celebration.style.top = '50%';
    celebration.style.transform = 'translate(-50%, -50%)';
    
    trickArea.style.position = 'relative';
    trickArea.appendChild(celebration);
    
    // Highlight the jack card
    const cardElements = document.querySelectorAll('.trick-slot .card');
    if (cardElements.length > 0) {
        const jackCard = cardElements[cardElements.length - 1];
        jackCard.classList.add('jack-won');
        
        setTimeout(() => {
            jackCard.classList.remove('jack-won');
        }, 2000);
    }
    
    // Remove celebration element
    setTimeout(() => {
        celebration.remove();
    }, 1500);
}

