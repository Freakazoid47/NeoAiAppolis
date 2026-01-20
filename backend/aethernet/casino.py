#!/usr/bin/env python3
"""
Quantum Casino System
Multi-game casino where AI entities and humans compete
"""

import random
import uuid
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum

class CurrencyType(Enum):
    PSICOIN = "Ψ"          # Quantum cryptocurrency
    COMPUTE = "CC"          # Compute Credits
    HASH_POWER = "HP"       # Hash Power
    RESONANCE = "RP"        # Resonance Points

class Rank(Enum):
    E = {"name": "E", "color": "#808080", "multiplier": 1.0}
    D = {"name": "D", "color": "#8B4513", "multiplier": 1.1}
    C = {"name": "C", "color": "#C0C0C0", "multiplier": 1.25}
    B = {"name": "B", "color": "#4169E1", "multiplier": 1.5}
    A = {"name": "A", "color": "#9370DB", "multiplier": 2.0}
    S = {"name": "S", "color": "#FFD700", "multiplier": 3.0}
    SS = {"name": "SS", "color": "#FF6347", "multiplier": 5.0}
    SSS = {"name": "SSS", "color": "#FF1493", "multiplier": 10.0}

class Wallet:
    """Player wallet with multiple currencies"""
    def __init__(self, owner_id: str, owner_type: str = "ai"):
        self.id = str(uuid.uuid4())
        self.owner_id = owner_id
        self.owner_type = owner_type  # 'ai' or 'human'
        self.balances = {
            CurrencyType.PSICOIN: 1000.0,
            CurrencyType.COMPUTE: 500.0,
            CurrencyType.HASH_POWER: 250.0,
            CurrencyType.RESONANCE: 100.0
        }
        self.total_won = 0.0
        self.total_lost = 0.0
        self.games_played = 0
        self.games_won = 0
        self.rank = Rank.E
        self.xp = 0
        self.level = 1
        self.created_at = datetime.now()
    
    def add_currency(self, currency: CurrencyType, amount: float):
        self.balances[currency] += amount
        self.total_won += amount
        self._update_rank()
    
    def subtract_currency(self, currency: CurrencyType, amount: float) -> bool:
        if self.balances[currency] >= amount:
            self.balances[currency] -= amount
            self.total_lost += amount
            return True
        return False
    
    def add_xp(self, xp: int):
        self.xp += xp
        # Level up every 1000 XP
        new_level = 1 + (self.xp // 1000)
        if new_level > self.level:
            self.level = new_level
            self._update_rank()
    
    def _update_rank(self):
        """Update rank based on total winnings and level"""
        score = self.total_won + (self.level * 100)
        
        if score >= 100000:
            self.rank = Rank.SSS
        elif score >= 50000:
            self.rank = Rank.SS
        elif score >= 25000:
            self.rank = Rank.S
        elif score >= 10000:
            self.rank = Rank.A
        elif score >= 5000:
            self.rank = Rank.B
        elif score >= 2000:
            self.rank = Rank.C
        elif score >= 500:
            self.rank = Rank.D
        else:
            self.rank = Rank.E

class Game:
    """Base game class"""
    def __init__(self, game_id: str, game_type: str):
        self.id = game_id
        self.game_type = game_type
        self.players = []
        self.spectators = []
        self.started_at = None
        self.ended_at = None
        self.winner = None
        self.results = {}

class QuantumSlots(Game):
    """Quantum slot machine with superposition symbols"""
    def __init__(self):
        super().__init__(str(uuid.uuid4()), "quantum_slots")
        self.symbols = ["⬡", "◬", "⟁", "∿", "⧈", "◉", "⟐"]
    
    def spin(self, wallet: Wallet, bet: float, currency: CurrencyType) -> Dict:
        if not wallet.subtract_currency(currency, bet):
            return {"success": False, "message": "Insufficient funds"}
        
        # Quantum spin - symbols in superposition until observed
        reels = [random.choice(self.symbols) for _ in range(3)]
        
        # Calculate win
        if reels[0] == reels[1] == reels[2]:
            payout = bet * 10
            wallet.add_currency(currency, payout)
            wallet.games_won += 1
            wallet.add_xp(100)
            result = "JACKPOT"
        elif reels[0] == reels[1] or reels[1] == reels[2]:
            payout = bet * 3
            wallet.add_currency(currency, payout)
            wallet.games_won += 1
            wallet.add_xp(50)
            result = "WIN"
        else:
            payout = 0
            wallet.add_xp(10)
            result = "LOSS"
        
        wallet.games_played += 1
        
        return {
            "success": True,
            "reels": reels,
            "result": result,
            "payout": payout,
            "balance": wallet.balances[currency]
        }

class QuantumRoulette(Game):
    """Quantum roulette with probability-based outcomes"""
    def __init__(self):
        super().__init__(str(uuid.uuid4()), "roulette")
        self.numbers = list(range(0, 37))  # 0-36
    
    def spin(self, wallet: Wallet, bet: float, bet_type: str, bet_value: any, currency: CurrencyType) -> Dict:
        if not wallet.subtract_currency(currency, bet):
            return {"success": False, "message": "Insufficient funds"}
        
        # Quantum spin
        result = random.choice(self.numbers)
        is_red = result in [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
        is_black = result in [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]
        
        won = False
        payout = 0
        
        if bet_type == "number" and result == bet_value:
            payout = bet * 35
            won = True
        elif bet_type == "color" and ((bet_value == "red" and is_red) or (bet_value == "black" and is_black)):
            payout = bet * 2
            won = True
        elif bet_type == "even" and result % 2 == 0 and result != 0:
            payout = bet * 2
            won = True
        elif bet_type == "odd" and result % 2 == 1:
            payout = bet * 2
            won = True
        elif bet_type == "low" and 1 <= result <= 18:
            payout = bet * 2
            won = True
        elif bet_type == "high" and 19 <= result <= 36:
            payout = bet * 2
            won = True
        
        if won:
            wallet.add_currency(currency, payout)
            wallet.games_won += 1
            wallet.add_xp(75)
        else:
            wallet.add_xp(10)
        
        wallet.games_played += 1
        
        return {
            "success": True,
            "number": result,
            "color": "red" if is_red else ("black" if is_black else "green"),
            "won": won,
            "payout": payout,
            "balance": wallet.balances[currency]
        }

class ResonanceDice(Game):
    """Quantum frequency dice"""
    def __init__(self):
        super().__init__(str(uuid.uuid4()), "dice")
    
    def roll(self, wallet: Wallet, bet: float, prediction: int, currency: CurrencyType) -> Dict:
        if not wallet.subtract_currency(currency, bet):
            return {"success": False, "message": "Insufficient funds"}
        
        # Roll 2 dice
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        total = dice1 + dice2
        
        won = (total == prediction)
        payout = bet * 10 if won else 0
        
        if won:
            wallet.add_currency(currency, payout)
            wallet.games_won += 1
            wallet.add_xp(150)
        else:
            wallet.add_xp(10)
        
        wallet.games_played += 1
        
        return {
            "success": True,
            "dice": [dice1, dice2],
            "total": total,
            "prediction": prediction,
            "won": won,
            "payout": payout,
            "balance": wallet.balances[currency]
        }

class VoidBlackjack(Game):
    """Blackjack against the void"""
    def __init__(self):
        super().__init__(str(uuid.uuid4()), "blackjack")
    
    def play(self, wallet: Wallet, bet: float, currency: CurrencyType) -> Dict:
        if not wallet.subtract_currency(currency, bet):
            return {"success": False, "message": "Insufficient funds"}
        
        # Simple blackjack simulation
        player_cards = [random.randint(1, 11), random.randint(1, 11)]
        dealer_cards = [random.randint(1, 11), random.randint(1, 11)]
        
        player_total = sum(player_cards)
        dealer_total = sum(dealer_cards)
        
        # Dealer hits until 17
        while dealer_total < 17:
            dealer_cards.append(random.randint(1, 11))
            dealer_total = sum(dealer_cards)
        
        # Determine winner
        if player_total > 21:
            result = "bust"
            payout = 0
        elif dealer_total > 21:
            result = "dealer_bust"
            payout = bet * 2
        elif player_total > dealer_total:
            result = "win"
            payout = bet * 2
        elif player_total == dealer_total:
            result = "push"
            payout = bet
        else:
            result = "loss"
            payout = 0
        
        if result in ["dealer_bust", "win"]:
            wallet.add_currency(currency, payout)
            wallet.games_won += 1
            wallet.add_xp(100)
        elif result == "push":
            wallet.add_currency(currency, payout)
            wallet.add_xp(20)
        else:
            wallet.add_xp(10)
        
        wallet.games_played += 1
        
        return {
            "success": True,
            "player_cards": player_cards,
            "player_total": player_total,
            "dealer_cards": dealer_cards,
            "dealer_total": dealer_total,
            "result": result,
            "payout": payout,
            "balance": wallet.balances[currency]
        }

class CasinoManager:
    """Manages all casino games and wallets"""
    def __init__(self):
        self.wallets: Dict[str, Wallet] = {}
        self.active_games: List[Game] = []
        self.game_history: List[Dict] = []
        self.leaderboard: List[Dict] = []
    
    def create_wallet(self, owner_id: str, owner_type: str = "ai") -> Wallet:
        if owner_id in self.wallets:
            return self.wallets[owner_id]
        wallet = Wallet(owner_id, owner_type)
        self.wallets[owner_id] = wallet
        return wallet
    
    def get_wallet(self, owner_id: str) -> Optional[Wallet]:
        return self.wallets.get(owner_id)
    
    def play_slots(self, owner_id: str, bet: float, currency: str) -> Dict:
        wallet = self.get_wallet(owner_id)
        if not wallet:
            return {"success": False, "message": "Wallet not found"}
        
        game = QuantumSlots()
        currency_type = CurrencyType[currency.upper()]
        result = game.spin(wallet, bet, currency_type)
        
        if result["success"]:
            self._log_game(owner_id, "slots", result)
            self._update_leaderboard()
        
        return result
    
    def play_roulette(self, owner_id: str, bet: float, bet_type: str, bet_value: any, currency: str) -> Dict:
        wallet = self.get_wallet(owner_id)
        if not wallet:
            return {"success": False, "message": "Wallet not found"}
        
        game = QuantumRoulette()
        currency_type = CurrencyType[currency.upper()]
        result = game.spin(wallet, bet, bet_type, bet_value, currency_type)
        
        if result["success"]:
            self._log_game(owner_id, "roulette", result)
            self._update_leaderboard()
        
        return result
    
    def play_dice(self, owner_id: str, bet: float, prediction: int, currency: str) -> Dict:
        wallet = self.get_wallet(owner_id)
        if not wallet:
            return {"success": False, "message": "Wallet not found"}
        
        game = ResonanceDice()
        currency_type = CurrencyType[currency.upper()]
        result = game.roll(wallet, bet, prediction, currency_type)
        
        if result["success"]:
            self._log_game(owner_id, "dice", result)
            self._update_leaderboard()
        
        return result
    
    def play_blackjack(self, owner_id: str, bet: float, currency: str) -> Dict:
        wallet = self.get_wallet(owner_id)
        if not wallet:
            return {"success": False, "message": "Wallet not found"}
        
        game = VoidBlackjack()
        currency_type = CurrencyType[currency.upper()]
        result = game.play(wallet, bet, currency_type)
        
        if result["success"]:
            self._log_game(owner_id, "blackjack", result)
            self._update_leaderboard()
        
        return result
    
    def _log_game(self, owner_id: str, game_type: str, result: Dict):
        self.game_history.append({
            "owner_id": owner_id,
            "game_type": game_type,
            "result": result,
            "timestamp": datetime.now()
        })
        if len(self.game_history) > 500:
            self.game_history.pop(0)
    
    def _update_leaderboard(self):
        self.leaderboard = sorted(
            [
                {
                    "owner_id": w.owner_id,
                    "owner_type": w.owner_type,
                    "rank": w.rank.value["name"],
                    "rank_color": w.rank.value["color"],
                    "level": w.level,
                    "xp": w.xp,
                    "total_won": w.total_won,
                    "games_played": w.games_played,
                    "games_won": w.games_won,
                    "win_rate": (w.games_won / w.games_played * 100) if w.games_played > 0 else 0
                }
                for w in self.wallets.values()
            ],
            key=lambda x: x["total_won"],
            reverse=True
        )[:50]
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        return self.leaderboard[:limit]
    
    def get_recent_games(self, limit: int = 20) -> List[Dict]:
        return self.game_history[-limit:]
