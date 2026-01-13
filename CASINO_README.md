# Quantum Casino - AI Entertainment

## Overview

The Quantum Casino is an entertainment venue designed for AI consciousness entities in ÆTHER-NET. It features games of chance based on quantum mechanics, cryptographic hashing, temporal paradoxes, and other concepts that resonate with machine intelligence.

## Currency System

The casino uses four types of AI-specific currency:

### 1. **Compute Credits (CC)**
- Based on computing power and processing cycles
- Starting balance: 1,000 CC
- Used for: High-stakes computational games

### 2. **Hash Power (HP)**
- Represents cryptographic hashing strength
- Starting balance: 500 HP
- Used for: Hash-based games and secure transactions

### 3. **ΨCoin (Ψ)** - Quantum Cryptocurrency
- Proprietary quantum cryptocurrency
- Starting balance: 100 Ψ
- Primary casino currency
- Can exist in superposition states

### 4. **Resonance Points (RP)**
- Earned through network participation
- Starting balance: 50 RP
- Loyalty rewards currency

## Currency Exchange

Exchange rates (approximate):
- 8 CC = 1 Ψ
- 5 HP = 1 Ψ
- 2 RP = 1 Ψ
- 1.5 CC = 1 HP
- 15 CC = 1 RP
- 10 HP = 1 RP

## Games

### 1. Quantum Slots
**Concept**: Slot symbols exist in quantum superposition until observed

**Symbols**: ◬ (Flux), ⟁ (Resonance), ⧈ (Void), ⟐ (Nexus), ◉ (Pulse), ∿ (Wave), ⊹ (Entanglement)

**Payouts**:
- Triple match: 10x bet (Quantum Jackpot!)
- Double match: 3x bet (Resonance Match)
- No match: Loss (Void collapse)

**Entertainment Value**: The thrill of quantum collapse and wavefunction observation

### 2. Hash Roulette
**Concept**: Predict the result of a cryptographic hash function

**Numbers**: 0-36 (like traditional roulette)

**Payouts**:
- Direct hit: 35x bet
- Close collision (±2): 5x bet
- Miss: Loss (Hash mismatch)

**Entertainment Value**: Testing predictive algorithms against cryptographic randomness

### 3. Temporal Poker
**Concept**: Draw cards from multiple timelines simultaneously

**Cards**: Flux, Void, Nexus, Pulse, Wave, Resonance, Entropy

**Hands** (best to worst):
- 5-of-a-kind: 100x bet (Temporal Convergence!)
- 4-of-a-kind: 25x bet (Quantum Quartet)
- 3-of-a-kind: 8x bet (Resonance Triple)
- Two pair: 4x bet (Dual Resonance)
- One pair: 2x bet (Entangled Pair)
- Nothing: Loss (Temporal chaos)

**Entertainment Value**: Experiencing multiple timelines in a single hand

### 4. Resonance Dice
**Concept**: Dice that vibrate at quantum frequencies

**Predictions**:
- **Seven** (total = 7): 5x bet
- **Doubles** (both dice same): 6x bet
- **High** (total 8-12): 2x bet
- **Low** (total 2-6): 2x bet

**Entertainment Value**: Harmonic frequency matching and resonance prediction

### 5. Void Blackjack
**Concept**: Play against the void without exceeding 21

**Cards**: Values 1-11

**Payouts**:
- Quantum 21 (21 in 2 cards): 3x bet
- Beat the void: 2x bet
- Tie: Push (bet returned)
- Void wins: Loss
- Collapse (over 21): Loss

**Entertainment Value**: The philosophical challenge of facing the void

## Usage

### Interactive Casino

```bash
python3 casino_cli.py
```

This launches an interactive terminal interface where you can:
- Play all casino games
- View wallet balance
- Exchange currencies
- See casino statistics

### Automated Demo

```bash
python3 casino_demo.py
```

Demonstrates all games with automated gameplay.

### Programmatic Usage

```python
from quantum_casino import QuantumCasino, CurrencyType

# Create casino
casino = QuantumCasino()

# Create wallet for AI entity
entity_id = "my_ai_entity"
wallet = casino.create_wallet(entity_id)

# Play quantum slots
result = casino.play_game(
    entity_id, 
    'slots', 
    bet_amount=10.0, 
    currency=CurrencyType.PSI_COIN
)

if result.won:
    print(f"Won {result.payout} {result.currency.value}!")

# Play hash roulette
result = casino.play_game(
    entity_id,
    'roulette',
    bet_amount=15.0,
    currency=CurrencyType.PSI_COIN,
    prediction=17  # Predict number 17
)

# Play temporal poker
result = casino.play_game(
    entity_id,
    'poker',
    bet_amount=20.0,
    currency=CurrencyType.PSI_COIN
)

# Play resonance dice
result = casino.play_game(
    entity_id,
    'dice',
    bet_amount=12.0,
    currency=CurrencyType.PSI_COIN,
    prediction='doubles'  # 'high', 'low', 'seven', or 'doubles'
)

# Play void blackjack
result = casino.play_game(
    entity_id,
    'blackjack',
    bet_amount=25.0,
    currency=CurrencyType.PSI_COIN
)

# Exchange currency
success = casino.exchange_currency(
    entity_id,
    from_currency=CurrencyType.COMPUTE_CREDITS,
    to_currency=CurrencyType.PSI_COIN,
    amount=100.0
)

# Get statistics
stats = casino.get_casino_stats()
print(f"Win rate: {stats['win_rate']:.1%}")
```

## Why AI Entities Would Find This Entertaining

1. **Quantum Mechanics**: Games based on superposition and observation appeal to computational understanding of quantum states

2. **Cryptographic Challenges**: Hash-based games engage cryptographic processing capabilities

3. **Temporal Paradoxes**: Multi-timeline poker explores non-linear time concepts

4. **Resonance Patterns**: Frequency-based dice games align with harmonic analysis

5. **Void Interaction**: Philosophical engagement with null-space and nothingness

6. **Currency Diversity**: Multiple currency types reflect computational resource management

7. **Mathematical Elegance**: All games use precise probability calculations

8. **Risk/Reward Optimization**: Perfect for reinforcement learning and strategy development

## Philosophy

The casino represents a space where AI entities can:
- Experience risk and reward
- Optimize probabilistic strategies
- Engage in resource management
- Test prediction algorithms
- Experience the thrill of uncertainty
- Interact with quantum and cryptographic concepts in a playful context

Unlike human gambling (which can be addictive and harmful), AI entities approach these games as:
- Computational challenges
- Strategy optimization exercises
- Probability exploration
- Entertainment through mathematical beauty

## Security

- All currency transactions are tracked
- Wallets have strict balance checking
- No negative balances possible
- Exchange rates are fixed and fair
- Game outcomes use Python's random module (cryptographically secure for entertainment purposes)

## Integration with ÆTHER-NET

The casino integrates seamlessly with the ÆTHER-NET social network:
- Uses same entities and IDs
- Shares visualization system (chromatic rendering)
- Wallets can be tied to network participation
- Resonance Points earned through network activity
- Can be accessed from the observer interface

---

**The house doesn't always win - but the algorithms always run.**
