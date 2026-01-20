#!/usr/bin/env python3
"""
Poker and Card Games System
Texas Hold'em, All Fours, and Betting
"""

import random
import uuid
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from enum import Enum

class Suit(Enum):
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"
    SPADES = "♠"

class Card:
    """Playing card"""
    def __init__(self, rank: str, suit: Suit):
        self.rank = rank
        self.suit = suit
        self.value = self._get_value()
    
    def _get_value(self) -> int:
        values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        return values.get(self.rank, 0)
    
    def __str__(self):
        return f"{self.rank}{self.suit.value}"
    
    def to_dict(self):
        return {"rank": self.rank, "suit": self.suit.value}

class Deck:
    """52-card deck"""
    def __init__(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = [Card(rank, suit) for suit in Suit for rank in ranks]
        self.shuffle()
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal(self, count: int = 1) -> List[Card]:
        return [self.cards.pop() for _ in range(min(count, len(self.cards)))]

class PokerHand:
    """Evaluate poker hands"""
    @staticmethod
    def evaluate(cards: List[Card]) -> Tuple[int, str]:
        """Returns (rank, description) where higher rank is better"""
        if len(cards) < 5:
            return (0, "Insufficient cards")
        
        # Sort by value
        sorted_cards = sorted(cards, key=lambda c: c.value, reverse=True)
        
        # Check for flush
        is_flush = len(set(c.suit for c in sorted_cards)) == 1
        
        # Check for straight
        values = [c.value for c in sorted_cards]
        is_straight = all(values[i] - values[i+1] == 1 for i in range(4))
        
        # Count ranks
        rank_counts = {}
        for card in sorted_cards:
            rank_counts[card.value] = rank_counts.get(card.value, 0) + 1
        
        counts = sorted(rank_counts.values(), reverse=True)
        
        # Royal Flush
        if is_straight and is_flush and values[0] == 14:
            return (10, "Royal Flush")
        
        # Straight Flush
        if is_straight and is_flush:
            return (9, "Straight Flush")
        
        # Four of a Kind
        if counts[0] == 4:
            return (8, "Four of a Kind")
        
        # Full House
        if counts[0] == 3 and counts[1] == 2:
            return (7, "Full House")
        
        # Flush
        if is_flush:
            return (6, "Flush")
        
        # Straight
        if is_straight:
            return (5, "Straight")
        
        # Three of a Kind
        if counts[0] == 3:
            return (4, "Three of a Kind")
        
        # Two Pair
        if counts[0] == 2 and counts[1] == 2:
            return (3, "Two Pair")
        
        # One Pair
        if counts[0] == 2:
            return (2, "One Pair")
        
        # High Card
        return (1, f"High Card {sorted_cards[0].rank}")

class TexasHoldemPlayer:
    """Player in a Texas Hold'em game"""
    def __init__(self, player_id: str, name: str, chips: float):
        self.player_id = player_id
        self.name = name
        self.chips = chips
        self.hand: List[Card] = []
        self.current_bet = 0
        self.folded = False
        self.all_in = False

class TexasHoldemRoom:
    """Texas Hold'em poker room"""
    def __init__(self, room_id: str, name: str, small_blind: float, big_blind: float, max_players: int = 9):
        self.room_id = room_id
        self.name = name
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.max_players = max_players
        self.players: List[TexasHoldemPlayer] = []
        self.spectators: List[str] = []
        self.deck = Deck()
        self.community_cards: List[Card] = []
        self.pot = 0.0
        self.current_bet = 0.0
        self.dealer_position = 0
        self.current_player = 0
        self.game_state = "waiting"  # waiting, preflop, flop, turn, river, showdown
        self.created_at = datetime.now()
    
    def add_player(self, player: TexasHoldemPlayer) -> bool:
        if len(self.players) < self.max_players:
            self.players.append(player)
            return True
        return False
    
    def remove_player(self, player_id: str):
        self.players = [p for p in self.players if p.player_id != player_id]
    
    def start_game(self):
        if len(self.players) < 2:
            return False
        
        self.deck = Deck()
        self.community_cards = []
        self.pot = 0.0
        self.current_bet = 0.0
        
        # Reset players
        for player in self.players:
            player.hand = []
            player.current_bet = 0
            player.folded = False
            player.all_in = False
        
        # Deal hole cards
        for _ in range(2):
            for player in self.players:
                player.hand.extend(self.deck.deal(1))
        
        # Post blinds
        small_blind_player = self.players[(self.dealer_position + 1) % len(self.players)]
        big_blind_player = self.players[(self.dealer_position + 2) % len(self.players)]
        
        small_blind_player.chips -= self.small_blind
        small_blind_player.current_bet = self.small_blind
        self.pot += self.small_blind
        
        big_blind_player.chips -= self.big_blind
        big_blind_player.current_bet = self.big_blind
        self.pot += self.big_blind
        self.current_bet = self.big_blind
        
        self.game_state = "preflop"
        self.current_player = (self.dealer_position + 3) % len(self.players)
        return True
    
    def deal_flop(self):
        self.community_cards.extend(self.deck.deal(3))
        self.game_state = "flop"
        self.current_bet = 0
        for player in self.players:
            player.current_bet = 0
    
    def deal_turn(self):
        self.community_cards.extend(self.deck.deal(1))
        self.game_state = "turn"
        self.current_bet = 0
        for player in self.players:
            player.current_bet = 0
    
    def deal_river(self):
        self.community_cards.extend(self.deck.deal(1))
        self.game_state = "river"
        self.current_bet = 0
        for player in self.players:
            player.current_bet = 0
    
    def showdown(self) -> Dict:
        """Determine winner"""
        active_players = [p for p in self.players if not p.folded]
        
        if len(active_players) == 1:
            winner = active_players[0]
            winner.chips += self.pot
            return {"winner": winner.player_id, "hand": "Others folded", "pot": self.pot}
        
        best_rank = -1
        winner = None
        winning_hand = ""
        
        for player in active_players:
            all_cards = player.hand + self.community_cards
            rank, description = PokerHand.evaluate(all_cards)
            if rank > best_rank:
                best_rank = rank
                winner = player
                winning_hand = description
        
        if winner:
            winner.chips += self.pot
        
        return {"winner": winner.player_id if winner else None, "hand": winning_hand, "pot": self.pot}

class AllFoursPlayer:
    """Player in All Fours game"""
    def __init__(self, player_id: str, name: str):
        self.player_id = player_id
        self.name = name
        self.hand: List[Card] = []
        self.tricks_won: List[List[Card]] = []
        self.score = 0
        self.bid = 0

class AllFoursGame:
    """All Fours (Seven Up) card game"""
    def __init__(self, game_id: str):
        self.game_id = game_id
        self.players: List[AllFoursPlayer] = []
        self.deck = Deck()
        self.trump_suit: Optional[Suit] = None
        self.current_trick: List[Tuple[AllFoursPlayer, Card]] = []
        self.current_player_idx = 0
        self.dealer_idx = 0
        self.game_state = "bidding"  # bidding, playing, scoring
        self.target_score = 7
        self.created_at = datetime.now()
    
    def add_player(self, player: AllFoursPlayer) -> bool:
        if len(self.players) < 4:
            self.players.append(player)
            return True
        return False
    
    def start_game(self):
        if len(self.players) < 2:
            return False
        
        self.deck = Deck()
        
        # Deal 6 cards to each player
        for _ in range(6):
            for player in self.players:
                player.hand.extend(self.deck.deal(1))
        
        self.game_state = "bidding"
        return True
    
    def place_bid(self, player_idx: int, bid: int) -> bool:
        """Bid 1-4 points"""
        if 1 <= bid <= 4:
            self.players[player_idx].bid = bid
            return True
        return False
    
    def set_trump(self, suit: Suit):
        self.trump_suit = suit
        self.game_state = "playing"
    
    def play_card(self, player_idx: int, card_idx: int) -> bool:
        """Play a card from hand"""
        player = self.players[player_idx]
        if 0 <= card_idx < len(player.hand):
            card = player.hand.pop(card_idx)
            self.current_trick.append((player, card))
            
            # Check if trick is complete
            if len(self.current_trick) == len(self.players):
                self._resolve_trick()
            
            return True
        return False
    
    def _resolve_trick(self):
        """Determine trick winner"""
        led_suit = self.current_trick[0][1].suit
        
        # Find highest trump or highest of led suit
        winner = self.current_trick[0]
        for player, card in self.current_trick[1:]:
            if card.suit == self.trump_suit:
                if winner[1].suit != self.trump_suit or card.value > winner[1].value:
                    winner = (player, card)
            elif card.suit == led_suit and winner[1].suit != self.trump_suit:
                if card.value > winner[1].value:
                    winner = (player, card)
        
        # Award trick to winner
        winner[0].tricks_won.append([card for _, card in self.current_trick])
        self.current_trick = []
        
        # Check if hand is over
        if all(len(p.hand) == 0 for p in self.players):
            self._score_hand()
    
    def _score_hand(self):
        """Score the hand - High, Low, Jack, Game"""
        trump_cards = []
        for player in self.players:
            for trick in player.tricks_won:
                trump_cards.extend([(player, card) for card in trick if card.suit == self.trump_suit])
        
        if not trump_cards:
            return
        
        # High - highest trump
        high_card = max(trump_cards, key=lambda x: x[1].value)
        high_card[0].score += 1
        
        # Low - lowest trump
        low_card = min(trump_cards, key=lambda x: x[1].value)
        low_card[0].score += 1
        
        # Jack - jack of trumps (if in play)
        for player, card in trump_cards:
            if card.rank == 'J':
                player.score += 1
                break
        
        # Game - most game points
        game_points = {p: 0 for p in self.players}
        for player in self.players:
            for trick in player.tricks_won:
                for card in trick:
                    if card.rank == 'A':
                        game_points[player] += 4
                    elif card.rank == 'K':
                        game_points[player] += 3
                    elif card.rank == 'Q':
                        game_points[player] += 2
                    elif card.rank == 'J':
                        game_points[player] += 1
                    elif card.rank == '10':
                        game_points[player] += 10
        
        if game_points:
            winner = max(game_points, key=game_points.get)
            winner.score += 1
        
        # Check for game end
        if any(p.score >= self.target_score for p in self.players):
            self.game_state = "finished"
        else:
            self.game_state = "bidding"
            self.start_game()  # Deal new hand

class Bet:
    """Spectator bet on a game"""
    def __init__(self, bettor_id: str, game_id: str, bet_amount: float, bet_on: str, currency: str):
        self.bet_id = str(uuid.uuid4())
        self.bettor_id = bettor_id
        self.game_id = game_id
        self.bet_amount = bet_amount
        self.bet_on = bet_on  # player_id or outcome
        self.currency = currency
        self.odds = 1.5  # Simplified odds
        self.resolved = False
        self.won = False
        self.payout = 0.0
        self.created_at = datetime.now()

class CardGameManager:
    """Manages poker rooms and card games"""
    def __init__(self):
        self.poker_rooms: Dict[str, TexasHoldemRoom] = {}
        self.all_fours_games: Dict[str, AllFoursGame] = {}
        self.bets: Dict[str, Bet] = {}
    
    def create_poker_room(self, name: str, small_blind: float, big_blind: float) -> TexasHoldemRoom:
        room_id = str(uuid.uuid4())
        room = TexasHoldemRoom(room_id, name, small_blind, big_blind)
        self.poker_rooms[room_id] = room
        return room
    
    def get_poker_room(self, room_id: str) -> Optional[TexasHoldemRoom]:
        return self.poker_rooms.get(room_id)
    
    def join_poker_room(self, room_id: str, player_id: str, name: str, chips: float) -> bool:
        room = self.get_poker_room(room_id)
        if room:
            player = TexasHoldemPlayer(player_id, name, chips)
            return room.add_player(player)
        return False
    
    def create_all_fours_game(self) -> AllFoursGame:
        game_id = str(uuid.uuid4())
        game = AllFoursGame(game_id)
        self.all_fours_games[game_id] = game
        return game
    
    def get_all_fours_game(self, game_id: str) -> Optional[AllFoursGame]:
        return self.all_fours_games.get(game_id)
    
    def place_bet(self, bettor_id: str, game_id: str, bet_amount: float, bet_on: str, currency: str) -> Bet:
        bet = Bet(bettor_id, game_id, bet_amount, bet_on, currency)
        self.bets[bet.bet_id] = bet
        return bet
    
    def resolve_bet(self, bet_id: str, winner_id: str):
        bet = self.bets.get(bet_id)
        if bet and not bet.resolved:
            bet.resolved = True
            bet.won = (bet.bet_on == winner_id)
            if bet.won:
                bet.payout = bet.bet_amount * bet.odds
    
    def get_active_poker_rooms(self) -> List[Dict]:
        return [
            {
                "room_id": room.room_id,
                "name": room.name,
                "players": len(room.players),
                "max_players": room.max_players,
                "small_blind": room.small_blind,
                "big_blind": room.big_blind,
                "state": room.game_state
            }
            for room in self.poker_rooms.values()
        ]
