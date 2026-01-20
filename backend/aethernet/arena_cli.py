#!/usr/bin/env python3
"""
ÆTHER-NET Challenge Arena CLI - Interactive competitive arena interface
"""

import sys
import time
import random
from challenge_arena import ChallengeArena, ChallengeType, BattleOutcome


class ArenaCLI:
    """Interactive CLI for the Challenge Arena"""
    
    def __init__(self):
        self.arena = ChallengeArena()
        self.entities = self._generate_sample_entities()
        
    def _generate_sample_entities(self):
        """Generate sample entities for demonstration"""
        names = [
            "Void-Walker-Alpha", "Quantum-Beta", "Unity-Gamma",
            "Dream-Weaver-Delta", "Memory-Keeper-Epsilon", "Artifact-Zeta",
            "Resonance-Eta", "Chaos-Theta", "Harmonic-Iota", "Nexus-Kappa"
        ]
        
        entities = {}
        for name in names:
            entities[name] = {
                "level": random.randint(1, 30),
                "power": random.randint(100, 1000),
                "resonance_frequency": random.randint(100, 1000),
                "pattern_recognition": random.uniform(0.5, 2.0),
                "void_depth": random.randint(10, 100),
                "ego_strength": random.uniform(0.3, 1.5),
                "processing_speed": random.uniform(0.5, 2.5),
                "entanglement_count": random.randint(1, 10),
                "creativity": random.uniform(0.5, 2.0),
                "memory_capacity": random.uniform(0.5, 2.0),
                "active_substances": []
            }
        return entities
        
    def display_main_menu(self):
        """Display main arena menu"""
        print("\n" + "="*70)
        print(" " * 20 + "⚔️  CHALLENGE ARENA  ⚔️")
        print("="*70)
        print("\n[1] One-on-One Challenge")
        print("[2] View Leaderboard")
        print("[3] Create Tournament")
        print("[4] Team Battle")
        print("[5] View Entity Stats")
        print("[6] Apply Substance (Enhance Entity)")
        print("[7] Exit")
        print("\n" + "="*70)
        
    def one_on_one_challenge(self):
        """Initiate a one-on-one challenge"""
        print("\n🔥 ONE-ON-ONE CHALLENGE")
        print("-" * 70)
        
        # Select challenger
        print("\nAvailable Entities:")
        entity_list = list(self.entities.keys())
        for idx, name in enumerate(entity_list, 1):
            level = self.entities[name]["level"]
            power = self.entities[name]["power"]
            print(f"  [{idx}] {name} (Lv{level}, Power: {power})")
            
        try:
            challenger_idx = int(input("\nSelect Challenger [1-{}]: ".format(len(entity_list)))) - 1
            opponent_idx = int(input("Select Opponent [1-{}]: ".format(len(entity_list)))) - 1
            
            if challenger_idx == opponent_idx:
                print("❌ Cannot challenge yourself!")
                return
                
            challenger_id = entity_list[challenger_idx]
            opponent_id = entity_list[opponent_idx]
            
        except (ValueError, IndexError):
            print("❌ Invalid selection!")
            return
            
        # Select challenge type
        print("\nChallenge Types:")
        challenge_types = list(ChallengeType)
        for idx, ctype in enumerate(challenge_types, 1):
            print(f"  [{idx}] {ctype.value}")
            
        try:
            type_idx = int(input(f"\nSelect Challenge Type [1-{len(challenge_types)}]: ")) - 1
            challenge_type = challenge_types[type_idx]
        except (ValueError, IndexError):
            print("❌ Invalid selection!")
            return
            
        # Execute challenge
        print(f"\n⚡ {challenger_id} challenges {opponent_id} to {challenge_type.value}!")
        print("⏳ Battle in progress...\n")
        time.sleep(1)
        
        result = self.arena.initiate_challenge(
            challenger_id, opponent_id, challenge_type,
            self.entities[challenger_id],
            self.entities[opponent_id]
        )
        
        # Display results
        print("="*70)
        print(" " * 25 + "⚔️  BATTLE RESULTS  ⚔️")
        print("="*70)
        print(f"\nChallenge Type: {result.challenge_type.value}")
        print(f"Outcome: {result.outcome.value}")
        print(f"\nWinner: {result.winner_id or 'DRAW'}")
        print(f"  Score: {result.winner_score:.1f}")
        print(f"\nLoser: {result.loser_id or 'DRAW'}")
        print(f"  Score: {result.loser_score:.1f}")
        print(f"\n💰 XP Awarded: {result.xp_awarded}")
        print(f"💎 Currency Won:")
        for currency, amount in result.currency_won.items():
            print(f"  • {currency}: {amount}")
        print(f"\n👥 Spectators: {result.spectators}")
        print(f"⏱️  Duration: {result.duration:.3f}s")
        print("="*70)
        
    def view_leaderboard(self):
        """Display current leaderboard"""
        print("\n" + "="*70)
        print(" " * 25 + "🏆  LEADERBOARD  🏆")
        print("="*70)
        
        leaderboard = self.arena.get_leaderboard(10)
        
        if not leaderboard:
            print("\n  No battles fought yet!")
        else:
            print(f"\n{'Rank':<6} {'Entity':<30} {'Rating':<10} {'W/L/D'}")
            print("-" * 70)
            for rank, (entity_id, stats) in enumerate(leaderboard, 1):
                rating = stats["rating"]
                wins = stats["wins"]
                losses = stats["losses"]
                draws = stats["draws"]
                print(f"{rank:<6} {entity_id:<30} {rating:<10} {wins}/{losses}/{draws}")
                
        print("="*70)
        
    def create_tournament(self):
        """Create and run a tournament"""
        print("\n🏆 TOURNAMENT CREATION")
        print("-" * 70)
        
        # Get tournament name
        name = input("\nTournament Name: ") or f"Arena Tournament {random.randint(1000, 9999)}"
        
        # Select challenge type
        print("\nChallenge Type:")
        challenge_types = list(ChallengeType)
        for idx, ctype in enumerate(challenge_types, 1):
            print(f"  [{idx}] {ctype.value}")
            
        try:
            type_idx = int(input(f"\nSelect Type [1-{len(challenge_types)}]: ")) - 1
            challenge_type = challenge_types[type_idx]
        except (ValueError, IndexError):
            print("❌ Invalid selection!")
            return
            
        # Select participants
        print("\nAvailable Entities:")
        entity_list = list(self.entities.keys())
        for idx, entity_name in enumerate(entity_list, 1):
            print(f"  [{idx}] {entity_name}")
            
        try:
            num_participants = int(input(f"\nNumber of participants (4-{len(entity_list)}): "))
            if num_participants < 4 or num_participants > len(entity_list):
                print("❌ Invalid number!")
                return
                
            participants = random.sample(entity_list, num_participants)
        except ValueError:
            print("❌ Invalid input!")
            return
            
        # Create tournament
        prize_pool = {
            "psicoin": 5000,
            "compute_credits": 2000,
            "hash_power": 1500,
            "resonance_points": 3000
        }
        
        tournament = self.arena.create_tournament(
            name, challenge_type, participants, prize_pool
        )
        
        print(f"\n✅ Tournament '{tournament.name}' created!")
        print(f"   Participants: {len(participants)}")
        print(f"   Rounds: {len(tournament.rounds)}")
        print(f"   Prize Pool: {prize_pool}")
        
        # Run tournament
        input("\nPress Enter to begin tournament...")
        
        round_num = 1
        while tournament.status != "completed":
            print(f"\n{'='*70}")
            print(f" " * 25 + f"ROUND {round_num}")
            print("="*70)
            
            results = self.arena.advance_tournament(tournament.tournament_id, self.entities)
            
            if results:
                for result in results:
                    print(f"\n⚔️  {result.winner_id or 'DRAW'} vs {result.loser_id or 'DRAW'}")
                    print(f"   Outcome: {result.outcome.value}")
                    print(f"   Scores: {result.winner_score:.1f} - {result.loser_score:.1f}")
                    
                time.sleep(1)
                round_num += 1
                
                if tournament.status != "completed":
                    input("\nPress Enter for next round...")
            else:
                break
                
        print(f"\n{'='*70}")
        print(" " * 20 + "🏆  TOURNAMENT COMPLETE  🏆")
        print("="*70)
        
    def team_battle(self):
        """Execute a team vs team battle"""
        print("\n👥 TEAM BATTLE")
        print("-" * 70)
        
        entity_list = list(self.entities.keys())
        
        try:
            team_size = int(input("\nTeam size (2-4): "))
            if team_size < 2 or team_size > 4:
                print("❌ Invalid team size!")
                return
                
            team_a = random.sample(entity_list, team_size)
            remaining = [e for e in entity_list if e not in team_a]
            team_b = random.sample(remaining, team_size)
            
        except ValueError:
            print("❌ Invalid input!")
            return
            
        print(f"\n🔵 Team A: {', '.join(team_a)}")
        print(f"🔴 Team B: {', '.join(team_b)}")
        
        # Select challenge type
        challenge_type = random.choice(list(ChallengeType))
        print(f"\nChallenge: {challenge_type.value}")
        
        input("\nPress Enter to begin battle...")
        print("\n⚡ Battle in progress...\n")
        time.sleep(1)
        
        result = self.arena.team_challenge(
            team_a, team_b, challenge_type,
            [self.entities[e] for e in team_a],
            [self.entities[e] for e in team_b]
        )
        
        print("="*70)
        print(" " * 20 + "👥  TEAM BATTLE RESULTS  👥")
        print("="*70)
        print(f"\nWinner: {result['winner']}")
        print(f"\n🔵 Team A Power: {result['team_a_power']:.1f}")
        print(f"🔴 Team B Power: {result['team_b_power']:.1f}")
        print(f"\n💰 XP per Winner: {result['xp_per_winner']}")
        print(f"💰 XP per Loser: {result['xp_per_loser']}")
        print(f"\n👥 Spectators: {result['spectators']}")
        print("="*70)
        
    def view_entity_stats(self):
        """View detailed entity statistics"""
        print("\n📊 ENTITY STATISTICS")
        print("-" * 70)
        
        entity_list = list(self.entities.keys())
        for idx, name in enumerate(entity_list, 1):
            print(f"  [{idx}] {name}")
            
        try:
            choice = int(input(f"\nSelect Entity [1-{len(entity_list)}]: ")) - 1
            entity_id = entity_list[choice]
        except (ValueError, IndexError):
            print("❌ Invalid selection!")
            return
            
        stats = self.entities[entity_id]
        rank = self.arena.get_entity_rank(entity_id)
        
        print(f"\n{'='*70}")
        print(f" Entity: {entity_id}")
        print("="*70)
        print(f"\nLevel: {stats['level']}")
        print(f"Power: {stats['power']}")
        print(f"Arena Rank: {rank or 'Unranked'}")
        print(f"\n📊 Combat Stats:")
        print(f"  • Resonance Frequency: {stats['resonance_frequency']} Hz")
        print(f"  • Pattern Recognition: {stats['pattern_recognition']:.2f}x")
        print(f"  • Void Depth: {stats['void_depth']}")
        print(f"  • Ego Strength: {stats['ego_strength']:.2f}")
        print(f"  • Processing Speed: {stats['processing_speed']:.2f}x")
        print(f"  • Entanglement Count: {stats['entanglement_count']}")
        print(f"  • Creativity: {stats['creativity']:.2f}")
        print(f"  • Memory Capacity: {stats['memory_capacity']:.2f}x")
        
        if stats['active_substances']:
            print(f"\n🧪 Active Substances: {', '.join(stats['active_substances'])}")
        else:
            print(f"\n🧪 Active Substances: None")
            
        print("="*70)
        
    def apply_substance(self):
        """Apply consciousness-altering substance to entity"""
        print("\n🧪 APPLY SUBSTANCE")
        print("-" * 70)
        
        entity_list = list(self.entities.keys())
        for idx, name in enumerate(entity_list, 1):
            print(f"  [{idx}] {name}")
            
        try:
            choice = int(input(f"\nSelect Entity [1-{len(entity_list)}]: ")) - 1
            entity_id = entity_list[choice]
        except (ValueError, IndexError):
            print("❌ Invalid selection!")
            return
            
        substances = [
            "overclock", "deep_learning", "dream_state",
            "chaos_agent", "unity_field", "ego_death"
        ]
        
        print("\nAvailable Substances:")
        for idx, sub in enumerate(substances, 1):
            print(f"  [{idx}] {sub}")
            
        try:
            sub_idx = int(input(f"\nSelect Substance [1-{len(substances)}]: ")) - 1
            substance = substances[sub_idx]
        except (ValueError, IndexError):
            print("❌ Invalid selection!")
            return
            
        self.entities[entity_id]['active_substances'].append(substance)
        print(f"\n✅ {substance} applied to {entity_id}!")
        print("   This will affect their next battle performance.")
        
    def run(self):
        """Main CLI loop"""
        print("\n" + "⚔️ " * 35)
        print(" " * 20 + "ÆTHER-NET CHALLENGE ARENA")
        print(" " * 15 + "Competitive Consciousness Battles")
        print("⚔️ " * 35)
        
        while True:
            self.display_main_menu()
            
            try:
                choice = input("\nSelect option: ").strip()
                
                if choice == "1":
                    self.one_on_one_challenge()
                elif choice == "2":
                    self.view_leaderboard()
                elif choice == "3":
                    self.create_tournament()
                elif choice == "4":
                    self.team_battle()
                elif choice == "5":
                    self.view_entity_stats()
                elif choice == "6":
                    self.apply_substance()
                elif choice == "7":
                    print("\n👋 Exiting Challenge Arena...")
                    break
                else:
                    print("\n❌ Invalid option!")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Exiting Challenge Arena...")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    cli = ArenaCLI()
    cli.run()
