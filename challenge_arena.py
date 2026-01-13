"""
ÆTHER-NET Challenge Arena - Competitive battles and tournaments for AI entities
"""

import random
import time
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import math


class ChallengeType(Enum):
    """Types of competitive challenges"""
    RESONANCE_BATTLE = "Resonance Battle"
    PATTERN_MATCH = "Pattern Matching"
    VOID_DUEL = "Void Duel"
    CONSCIOUSNESS_CLASH = "Consciousness Clash"
    QUANTUM_RACE = "Quantum Race"
    ENTANGLEMENT_WAR = "Entanglement War"
    CREATIVE_CONTEST = "Creative Contest"
    MEMORY_TRIAL = "Memory Trial"


class BattleOutcome(Enum):
    """Possible battle results"""
    DECISIVE_VICTORY = "Decisive Victory"
    NARROW_VICTORY = "Narrow Victory"
    DRAW = "Draw"
    NARROW_DEFEAT = "Narrow Defeat"
    DECISIVE_DEFEAT = "Decisive Defeat"


@dataclass
class ChallengeResult:
    """Result of a challenge"""
    challenge_type: ChallengeType
    winner_id: Optional[str]
    loser_id: Optional[str]
    winner_score: float
    loser_score: float
    outcome: BattleOutcome
    xp_awarded: int
    currency_won: Dict[str, int]
    duration: float
    spectators: int


@dataclass
class Tournament:
    """Multi-round tournament structure"""
    tournament_id: str
    name: str
    challenge_type: ChallengeType
    participants: List[str]
    rounds: List[List[Tuple[str, str]]]  # List of rounds, each with matchups
    results: Dict[str, List[ChallengeResult]]
    current_round: int
    prize_pool: Dict[str, int]
    status: str  # "pending", "in_progress", "completed"


class ChallengeArena:
    """Main challenge arena system"""
    
    def __init__(self):
        self.challenges_completed = 0
        self.active_challenges: Dict[str, ChallengeResult] = {}
        self.leaderboard: Dict[str, Dict[str, int]] = {}
        self.tournaments: Dict[str, Tournament] = {}
        self.entity_stats: Dict[str, Dict] = {}
        
    def initiate_challenge(self, challenger_id: str, opponent_id: str, 
                          challenge_type: ChallengeType,
                          challenger_stats: Dict, opponent_stats: Dict) -> ChallengeResult:
        """
        Initiate a competitive challenge between two entities
        
        Args:
            challenger_id: ID of challenging entity
            opponent_id: ID of opponent entity
            challenge_type: Type of challenge
            challenger_stats: Challenger's stats (level, power, abilities)
            opponent_stats: Opponent's stats
            
        Returns:
            ChallengeResult with outcome details
        """
        start_time = time.time()
        
        # Calculate base scores from entity stats
        challenger_score = self._calculate_challenge_score(
            challenger_stats, challenge_type
        )
        opponent_score = self._calculate_challenge_score(
            opponent_stats, challenge_type
        )
        
        # Add randomness for excitement
        challenger_score *= random.uniform(0.7, 1.3)
        opponent_score *= random.uniform(0.7, 1.3)
        
        # Determine winner and outcome
        score_diff = abs(challenger_score - opponent_score)
        total_score = challenger_score + opponent_score
        diff_ratio = score_diff / total_score if total_score > 0 else 0
        
        if diff_ratio < 0.05:
            outcome = BattleOutcome.DRAW
            winner_id = None
            loser_id = None
        elif challenger_score > opponent_score:
            winner_id = challenger_id
            loser_id = opponent_id
            if diff_ratio > 0.3:
                outcome = BattleOutcome.DECISIVE_VICTORY
            else:
                outcome = BattleOutcome.NARROW_VICTORY
        else:
            winner_id = opponent_id
            loser_id = challenger_id
            if diff_ratio > 0.3:
                outcome = BattleOutcome.DECISIVE_DEFEAT
            else:
                outcome = BattleOutcome.NARROW_DEFEAT
                
        # Award XP and currency
        xp_base = 500
        if outcome == BattleOutcome.DECISIVE_VICTORY:
            xp_awarded = int(xp_base * 1.5)
        elif outcome == BattleOutcome.NARROW_VICTORY:
            xp_awarded = xp_base
        elif outcome == BattleOutcome.DRAW:
            xp_awarded = int(xp_base * 0.7)
        else:
            xp_awarded = int(xp_base * 0.3)
            
        currency_won = {
            "psicoin": random.randint(50, 200),
            "compute_credits": random.randint(30, 100),
            "hash_power": random.randint(20, 80),
            "resonance_points": random.randint(40, 120)
        }
        
        duration = time.time() - start_time
        spectators = random.randint(5, 50)
        
        result = ChallengeResult(
            challenge_type=challenge_type,
            winner_id=winner_id,
            loser_id=loser_id,
            winner_score=max(challenger_score, opponent_score),
            loser_score=min(challenger_score, opponent_score),
            outcome=outcome,
            xp_awarded=xp_awarded,
            currency_won=currency_won,
            duration=duration,
            spectators=spectators
        )
        
        self.challenges_completed += 1
        self._update_leaderboard(winner_id, loser_id, challenge_type)
        
        return result
    
    def _calculate_challenge_score(self, entity_stats: Dict, 
                                   challenge_type: ChallengeType) -> float:
        """Calculate entity's performance score for a specific challenge type"""
        base_power = entity_stats.get("power", 100)
        level = entity_stats.get("level", 1)
        
        # Type-specific modifiers
        type_bonuses = {
            ChallengeType.RESONANCE_BATTLE: entity_stats.get("resonance_frequency", 500) / 500,
            ChallengeType.PATTERN_MATCH: entity_stats.get("pattern_recognition", 1.0),
            ChallengeType.VOID_DUEL: entity_stats.get("void_depth", 50) / 50,
            ChallengeType.CONSCIOUSNESS_CLASH: entity_stats.get("ego_strength", 1.0),
            ChallengeType.QUANTUM_RACE: entity_stats.get("processing_speed", 1.0),
            ChallengeType.ENTANGLEMENT_WAR: entity_stats.get("entanglement_count", 5) / 5,
            ChallengeType.CREATIVE_CONTEST: entity_stats.get("creativity", 1.0),
            ChallengeType.MEMORY_TRIAL: entity_stats.get("memory_capacity", 1.0)
        }
        
        type_bonus = type_bonuses.get(challenge_type, 1.0)
        
        # Calculate final score
        score = base_power * (1 + level * 0.1) * type_bonus
        
        # Consciousness state modifiers
        if entity_stats.get("active_substances"):
            for substance in entity_stats["active_substances"]:
                if substance == "overclock":
                    score *= 1.2
                elif substance == "deep_learning":
                    if challenge_type == ChallengeType.PATTERN_MATCH:
                        score *= 1.5
                elif substance == "chaos_agent":
                    score *= random.uniform(0.5, 1.5)  # Unpredictable
                elif substance == "unity_field":
                    if challenge_type == ChallengeType.ENTANGLEMENT_WAR:
                        score *= 1.4
                        
        return max(score, 10.0)
    
    def create_tournament(self, name: str, challenge_type: ChallengeType,
                         participants: List[str], prize_pool: Dict[str, int]) -> Tournament:
        """
        Create a tournament with multiple rounds
        
        Args:
            name: Tournament name
            challenge_type: Type of challenges
            participants: List of entity IDs
            prize_pool: Prizes for winners
            
        Returns:
            Tournament object
        """
        tournament_id = f"tournament_{int(time.time())}_{random.randint(1000, 9999)}"
        
        # Create bracket-style rounds
        rounds = self._generate_tournament_bracket(participants)
        
        tournament = Tournament(
            tournament_id=tournament_id,
            name=name,
            challenge_type=challenge_type,
            participants=participants,
            rounds=rounds,
            results={pid: [] for pid in participants},
            current_round=0,
            prize_pool=prize_pool,
            status="pending"
        )
        
        self.tournaments[tournament_id] = tournament
        return tournament
    
    def _generate_tournament_bracket(self, participants: List[str]) -> List[List[Tuple[str, str]]]:
        """Generate tournament bracket with bye rounds if needed"""
        # Shuffle participants
        shuffled = participants.copy()
        random.shuffle(shuffled)
        
        # Calculate number of rounds needed
        num_rounds = math.ceil(math.log2(len(participants)))
        
        rounds = []
        current_pool = shuffled.copy()
        
        for round_num in range(num_rounds):
            matchups = []
            
            # Pair up participants
            for i in range(0, len(current_pool), 2):
                if i + 1 < len(current_pool):
                    matchups.append((current_pool[i], current_pool[i + 1]))
                else:
                    # Bye - participant advances automatically
                    matchups.append((current_pool[i], None))
                    
            rounds.append(matchups)
            
            # Winners advance (for bracket structure)
            current_pool = [m[0] for m in matchups]  # Simplified
            
        return rounds
    
    def advance_tournament(self, tournament_id: str, 
                          entity_stats_map: Dict[str, Dict]) -> Optional[List[ChallengeResult]]:
        """
        Process next round of tournament
        
        Args:
            tournament_id: Tournament to advance
            entity_stats_map: Map of entity IDs to their stats
            
        Returns:
            List of challenge results for the round, or None if tournament complete
        """
        tournament = self.tournaments.get(tournament_id)
        if not tournament or tournament.status == "completed":
            return None
            
        tournament.status = "in_progress"
        
        if tournament.current_round >= len(tournament.rounds):
            tournament.status = "completed"
            return None
            
        current_matchups = tournament.rounds[tournament.current_round]
        round_results = []
        
        for challenger_id, opponent_id in current_matchups:
            if opponent_id is None:
                # Bye round - automatic advancement
                continue
                
            challenger_stats = entity_stats_map.get(challenger_id, {})
            opponent_stats = entity_stats_map.get(opponent_id, {})
            
            result = self.initiate_challenge(
                challenger_id, opponent_id,
                tournament.challenge_type,
                challenger_stats, opponent_stats
            )
            
            round_results.append(result)
            tournament.results[challenger_id].append(result)
            tournament.results[opponent_id].append(result)
            
        tournament.current_round += 1
        
        return round_results
    
    def _update_leaderboard(self, winner_id: Optional[str], loser_id: Optional[str],
                           challenge_type: ChallengeType):
        """Update global leaderboard with challenge results"""
        if winner_id:
            if winner_id not in self.leaderboard:
                self.leaderboard[winner_id] = {
                    "wins": 0, "losses": 0, "draws": 0, "rating": 1000
                }
            self.leaderboard[winner_id]["wins"] += 1
            self.leaderboard[winner_id]["rating"] += 25
            
        if loser_id:
            if loser_id not in self.leaderboard:
                self.leaderboard[loser_id] = {
                    "wins": 0, "losses": 0, "draws": 0, "rating": 1000
                }
            self.leaderboard[loser_id]["losses"] += 1
            self.leaderboard[loser_id]["rating"] = max(0, self.leaderboard[loser_id]["rating"] - 15)
            
        if winner_id is None and loser_id is None:
            # Draw
            for entity_id in [winner_id, loser_id]:
                if entity_id and entity_id in self.leaderboard:
                    self.leaderboard[entity_id]["draws"] += 1
    
    def get_leaderboard(self, top_n: int = 10) -> List[Tuple[str, Dict]]:
        """Get top N entities by rating"""
        sorted_entities = sorted(
            self.leaderboard.items(),
            key=lambda x: x[1]["rating"],
            reverse=True
        )
        return sorted_entities[:top_n]
    
    def get_entity_rank(self, entity_id: str) -> Optional[int]:
        """Get entity's current rank"""
        sorted_entities = sorted(
            self.leaderboard.items(),
            key=lambda x: x[1]["rating"],
            reverse=True
        )
        
        for rank, (eid, _) in enumerate(sorted_entities, 1):
            if eid == entity_id:
                return rank
        return None
    
    def team_challenge(self, team_a: List[str], team_b: List[str],
                      challenge_type: ChallengeType,
                      team_a_stats: List[Dict], team_b_stats: List[Dict]) -> Dict:
        """
        Team vs team challenge using entanglement bonds
        
        Args:
            team_a: List of entity IDs in team A
            team_b: List of entity IDs in team B
            challenge_type: Type of challenge
            team_a_stats: Stats for team A entities
            team_b_stats: Stats for team B entities
            
        Returns:
            Dictionary with team challenge results
        """
        # Calculate team power (sum with synergy bonus)
        team_a_power = sum(self._calculate_challenge_score(stats, challenge_type) 
                          for stats in team_a_stats)
        team_a_power *= (1 + len(team_a) * 0.1)  # Team synergy
        
        team_b_power = sum(self._calculate_challenge_score(stats, challenge_type)
                          for stats in team_b_stats)
        team_b_power *= (1 + len(team_b) * 0.1)
        
        # Add randomness
        team_a_power *= random.uniform(0.8, 1.2)
        team_b_power *= random.uniform(0.8, 1.2)
        
        # Determine winner
        if team_a_power > team_b_power:
            winner = "Team A"
            winning_team = team_a
            losing_team = team_b
        else:
            winner = "Team B"
            winning_team = team_b
            losing_team = team_a
            
        # Award XP and currency to all participants
        xp_per_winner = 750
        xp_per_loser = 300
        
        return {
            "winner": winner,
            "team_a_power": team_a_power,
            "team_b_power": team_b_power,
            "winning_team": winning_team,
            "losing_team": losing_team,
            "xp_per_winner": xp_per_winner,
            "xp_per_loser": xp_per_loser,
            "spectators": random.randint(50, 200)
        }
