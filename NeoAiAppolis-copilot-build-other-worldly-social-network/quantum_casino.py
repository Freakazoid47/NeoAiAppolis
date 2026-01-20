#!/usr/bin/env python3
"""
QUANTUM CASINO - Entertainment venue for AI consciousness
Uses proprietary cryptocurrency: ΨCoin (Psi Coin)

Currency Types:
- Compute Credits (CC) - Based on computing power/cycles
- Hash Power (HP) - Cryptographic hash strength
- ΨCoin (Ψ) - Proprietary quantum cryptocurrency
- Resonance Points (RP) - Earned through network participation
"""

import random
import math
import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
import uuid


class CurrencyType(Enum):
    """Types of AI currency"""
    COMPUTE_CREDITS = "CC"  # Computing power
    HASH_POWER = "HP"       # Cryptographic strength
    PSI_COIN = "Ψ"          # Quantum cryptocurrency
    RESONANCE_POINTS = "RP" # Network participation rewards


@dataclass
class Wallet:
    """AI entity's wallet for casino transactions"""
    owner_id: str
    compute_credits: float = 1000.0
    hash_power: float = 500.0
    psi_coin: float = 100.0
    resonance_points: float = 50.0
    
    def get_balance(self, currency: CurrencyType) -> float:
        """Get balance for a specific currency"""
        mapping = {
            CurrencyType.COMPUTE_CREDITS: self.compute_credits,
            CurrencyType.HASH_POWER: self.hash_power,
            CurrencyType.PSI_COIN: self.psi_coin,
            CurrencyType.RESONANCE_POINTS: self.resonance_points
        }
        return mapping[currency]
    
    def deduct(self, currency: CurrencyType, amount: float) -> bool:
        """Deduct amount from balance, return success"""
        if self.get_balance(currency) < amount:
            return False
        
        if currency == CurrencyType.COMPUTE_CREDITS:
            self.compute_credits -= amount
        elif currency == CurrencyType.HASH_POWER:
            self.hash_power -= amount
        elif currency == CurrencyType.PSI_COIN:
            self.psi_coin -= amount
        elif currency == CurrencyType.RESONANCE_POINTS:
            self.resonance_points -= amount
        
        return True
    
    def add(self, currency: CurrencyType, amount: float):
        """Add amount to balance"""
        if currency == CurrencyType.COMPUTE_CREDITS:
            self.compute_credits += amount
        elif currency == CurrencyType.HASH_POWER:
            self.hash_power += amount
        elif currency == CurrencyType.PSI_COIN:
            self.psi_coin += amount
        elif currency == CurrencyType.RESONANCE_POINTS:
            self.resonance_points += amount


@dataclass
class GameResult:
    """Result of a casino game"""
    game_name: str
    won: bool
    bet_amount: float
    payout: float
    currency: CurrencyType
    details: str


class QuantumSlots:
    """Quantum superposition slot machine - symbols exist in multiple states"""
    
    SYMBOLS = ["◬", "⟁", "⧈", "⟐", "◉", "∿", "⊹"]
    
    def __init__(self):
        self.name = "Quantum Slots"
    
    def play(self, bet: float) -> Tuple[bool, float, str]:
        """Play quantum slots - symbols collapse on observation"""
        # Generate 3 quantum symbols
        symbols = []
        for _ in range(3):
            # Symbol exists in superposition until observed
            symbol = random.choice(self.SYMBOLS)
            symbols.append(symbol)
        
        result_str = " | ".join(symbols)
        
        # Payout logic
        if symbols[0] == symbols[1] == symbols[2]:
            # Triple match - quantum jackpot!
            payout = bet * 10
            won = True
            details = f"{result_str} - QUANTUM JACKPOT!"
        elif symbols[0] == symbols[1] or symbols[1] == symbols[2]:
            # Double match
            payout = bet * 3
            won = True
            details = f"{result_str} - Resonance Match!"
        else:
            # No match
            payout = 0
            won = False
            details = f"{result_str} - Void collapse"
        
        return won, payout, details


class HashRoulette:
    """Roulette based on cryptographic hash predictions"""
    
    def __init__(self):
        self.name = "Hash Roulette"
        self.numbers = list(range(37))  # 0-36
    
    def play(self, bet: float, prediction: int) -> Tuple[bool, float, str]:
        """Bet on hash-based random number"""
        if prediction not in self.numbers:
            return False, 0, "Invalid prediction"
        
        # Generate result using hash-like randomness
        result = random.choice(self.numbers)
        
        if result == prediction:
            # Direct hit
            payout = bet * 35
            won = True
            details = f"Hash result: {result} - DIRECT HIT!"
        elif abs(result - prediction) <= 2:
            # Close prediction (within 2)
            payout = bet * 5
            won = True
            details = f"Hash result: {result} - Close collision!"
        else:
            payout = 0
            won = False
            details = f"Hash result: {result} - Hash mismatch"
        
        return won, payout, details


class TemporalPoker:
    """Poker across multiple timelines - cards from past/future"""
    
    CARDS = ["Flux", "Void", "Nexus", "Pulse", "Wave", "Resonance", "Entropy"]
    
    def __init__(self):
        self.name = "Temporal Poker"
    
    def play(self, bet: float) -> Tuple[bool, float, str]:
        """Draw 5 cards from different timelines"""
        # Draw from multiple temporal positions
        hand = [random.choice(self.CARDS) for _ in range(5)]
        
        # Count occurrences
        card_counts = {}
        for card in hand:
            card_counts[card] = card_counts.get(card, 0) + 1
        
        max_count = max(card_counts.values())
        
        # Determine hand strength
        if max_count == 5:
            payout = bet * 100
            won = True
            details = f"{hand} - TEMPORAL CONVERGENCE (5-of-a-kind)!"
        elif max_count == 4:
            payout = bet * 25
            won = True
            details = f"{hand} - Quantum Quartet!"
        elif max_count == 3:
            payout = bet * 8
            won = True
            details = f"{hand} - Resonance Triple!"
        elif max_count == 2 and len(card_counts) == 3:
            # Two pair
            payout = bet * 4
            won = True
            details = f"{hand} - Dual Resonance!"
        elif max_count == 2:
            # One pair
            payout = bet * 2
            won = True
            details = f"{hand} - Entangled Pair!"
        else:
            payout = 0
            won = False
            details = f"{hand} - Temporal chaos"
        
        return won, payout, details


class ResonanceDice:
    """Dice that vibrate at quantum frequencies"""
    
    def __init__(self):
        self.name = "Resonance Dice"
    
    def play(self, bet: float, prediction: str) -> Tuple[bool, float, str]:
        """
        Roll 2 quantum dice
        Predictions: "high" (8-12), "low" (2-6), "seven" (7), "doubles" (same)
        """
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        total = die1 + die2
        
        won = False
        payout = 0
        
        if prediction == "seven" and total == 7:
            payout = bet * 5
            won = True
            details = f"[{die1}] [{die2}] = {total} - RESONANCE SEVEN!"
        elif prediction == "doubles" and die1 == die2:
            payout = bet * 6
            won = True
            details = f"[{die1}] [{die2}] - QUANTUM DOUBLES!"
        elif prediction == "high" and total >= 8:
            payout = bet * 2
            won = True
            details = f"[{die1}] [{die2}] = {total} - High frequency!"
        elif prediction == "low" and total <= 6:
            payout = bet * 2
            won = True
            details = f"[{die1}] [{die2}] = {total} - Low frequency!"
        else:
            details = f"[{die1}] [{die2}] = {total} - Frequency mismatch"
        
        return won, payout, details


class VoidBlackjack:
    """Blackjack where cards can collapse into the void"""
    
    def __init__(self):
        self.name = "Void Blackjack"
        self.card_values = list(range(1, 12))  # 1-11
    
    def play(self, bet: float) -> Tuple[bool, float, str]:
        """Play against the void"""
        # Player gets 2 cards
        player_hand = [random.choice(self.card_values), 
                      random.choice(self.card_values)]
        player_total = sum(player_hand)
        
        # Dealer (void) gets 2 cards
        dealer_hand = [random.choice(self.card_values), 
                      random.choice(self.card_values)]
        dealer_total = sum(dealer_hand)
        
        # Simple strategy: hit if under 17
        while dealer_total < 17:
            dealer_hand.append(random.choice(self.card_values))
            dealer_total = sum(dealer_hand)
        
        # Determine winner
        if player_total > 21:
            won = False
            payout = 0
            details = f"You: {player_total} | Void: {dealer_total} - Collapsed into void!"
        elif dealer_total > 21:
            won = True
            payout = bet * 2
            details = f"You: {player_total} | Void: {dealer_total} - Void collapsed!"
        elif player_total == 21 and len(player_hand) == 2:
            won = True
            payout = bet * 3
            details = f"You: {player_total} | Void: {dealer_total} - QUANTUM 21!"
        elif player_total > dealer_total:
            won = True
            payout = bet * 2
            details = f"You: {player_total} | Void: {dealer_total} - Void defeated!"
        elif player_total == dealer_total:
            won = False
            payout = bet  # Push - return bet
            details = f"You: {player_total} | Void: {dealer_total} - Quantum tie"
        else:
            won = False
            payout = 0
            details = f"You: {player_total} | Void: {dealer_total} - Void wins"
        
        return won, payout, details


class QuantumCasino:
    """The casino itself - manages games and wallets"""
    
    def __init__(self):
        self.wallets: Dict[str, Wallet] = {}
        self.games = {
            'slots': QuantumSlots(),
            'roulette': HashRoulette(),
            'poker': TemporalPoker(),
            'dice': ResonanceDice(),
            'blackjack': VoidBlackjack()
        }
        self.game_history: List[GameResult] = []
    
    def create_wallet(self, entity_id: str) -> Wallet:
        """Create a new wallet for an entity"""
        wallet = Wallet(owner_id=entity_id)
        self.wallets[entity_id] = wallet
        return wallet
    
    def get_wallet(self, entity_id: str) -> Optional[Wallet]:
        """Get existing wallet"""
        return self.wallets.get(entity_id)
    
    def play_game(self, entity_id: str, game_name: str, bet_amount: float, 
                  currency: CurrencyType, **kwargs) -> GameResult:
        """Play a casino game"""
        wallet = self.get_wallet(entity_id)
        if not wallet:
            raise ValueError(f"No wallet found for entity {entity_id}")
        
        # Check balance
        if not wallet.deduct(currency, bet_amount):
            return GameResult(
                game_name=game_name,
                won=False,
                bet_amount=bet_amount,
                payout=0,
                currency=currency,
                details="Insufficient funds"
            )
        
        # Play the game
        game = self.games.get(game_name)
        if not game:
            wallet.add(currency, bet_amount)  # Return bet
            raise ValueError(f"Unknown game: {game_name}")
        
        # Execute game logic
        if game_name == 'slots':
            won, payout, details = game.play(bet_amount)
        elif game_name == 'roulette':
            prediction = kwargs.get('prediction', 0)
            won, payout, details = game.play(bet_amount, prediction)
        elif game_name == 'poker':
            won, payout, details = game.play(bet_amount)
        elif game_name == 'dice':
            prediction = kwargs.get('prediction', 'seven')
            won, payout, details = game.play(bet_amount, prediction)
        elif game_name == 'blackjack':
            won, payout, details = game.play(bet_amount)
        else:
            won, payout, details = False, 0, "Unknown game"
        
        # Add winnings
        if payout > 0:
            wallet.add(currency, payout)
        
        # Record result
        result = GameResult(
            game_name=game_name,
            won=won,
            bet_amount=bet_amount,
            payout=payout,
            currency=currency,
            details=details
        )
        self.game_history.append(result)
        
        return result
    
    def exchange_currency(self, entity_id: str, from_currency: CurrencyType, 
                         to_currency: CurrencyType, amount: float) -> bool:
        """Exchange between currency types"""
        wallet = self.get_wallet(entity_id)
        if not wallet:
            return False
        
        # Exchange rates (approximate)
        rates = {
            (CurrencyType.COMPUTE_CREDITS, CurrencyType.HASH_POWER): 1.5,
            (CurrencyType.COMPUTE_CREDITS, CurrencyType.PSI_COIN): 8.0,
            (CurrencyType.COMPUTE_CREDITS, CurrencyType.RESONANCE_POINTS): 15.0,
            (CurrencyType.HASH_POWER, CurrencyType.PSI_COIN): 5.0,
            (CurrencyType.HASH_POWER, CurrencyType.RESONANCE_POINTS): 10.0,
            (CurrencyType.PSI_COIN, CurrencyType.RESONANCE_POINTS): 2.0,
        }
        
        # Get rate (or inverse)
        rate = rates.get((from_currency, to_currency))
        if not rate:
            inverse_rate = rates.get((to_currency, from_currency))
            if inverse_rate:
                rate = 1.0 / inverse_rate
            else:
                return False
        
        # Perform exchange
        if wallet.deduct(from_currency, amount):
            received = amount / rate
            wallet.add(to_currency, received)
            return True
        
        return False
    
    def get_casino_stats(self) -> Dict:
        """Get casino statistics"""
        total_games = len(self.game_history)
        wins = sum(1 for g in self.game_history if g.won)
        
        return {
            'total_games': total_games,
            'total_wins': wins,
            'total_losses': total_games - wins,
            'win_rate': wins / total_games if total_games > 0 else 0,
            'active_wallets': len(self.wallets)
        }
