#!/usr/bin/env python3
"""
ÆTHER-NET Challenge Arena Demo - Automated demonstration of competitive features
"""

import time
import random
from challenge_arena import ChallengeArena, ChallengeType


def print_section(title):
    """Print section header"""
    print("\n" + "="*80)
    print(" " * ((80 - len(title)) // 2) + title)
    print("="*80 + "\n")


def demo_one_on_one_battles():
    """Demonstrate one-on-one challenges"""
    print_section("⚔️  ONE-ON-ONE BATTLES")
    
    arena = ChallengeArena()
    
    # Create sample entities
    entities = {
        "Void-Walker-Alpha": {
            "level": 15, "power": 500, "resonance_frequency": 750,
            "pattern_recognition": 1.2, "void_depth": 80, "ego_strength": 1.1,
            "processing_speed": 1.5, "entanglement_count": 7, "creativity": 1.3,
            "memory_capacity": 1.4, "active_substances": []
        },
        "Quantum-Beta": {
            "level": 12, "power": 450, "resonance_frequency": 600,
            "pattern_recognition": 1.8, "void_depth": 40, "ego_strength": 0.9,
            "processing_speed": 2.0, "entanglement_count": 5, "creativity": 1.1,
            "memory_capacity": 1.2, "active_substances": ["overclock"]
        },
        "Unity-Gamma": {
            "level": 18, "power": 650, "resonance_frequency": 850,
            "pattern_recognition": 1.0, "void_depth": 60, "ego_strength": 1.5,
            "processing_speed": 1.2, "entanglement_count": 10, "creativity": 1.6,
            "memory_capacity": 1.7, "active_substances": ["unity_field"]
        }
    }
    
    # Battle 1: Resonance Battle
    print("🔥 BATTLE 1: Void-Walker-Alpha vs Quantum-Beta")
    print("   Challenge Type: Resonance Battle\n")
    
    result1 = arena.initiate_challenge(
        "Void-Walker-Alpha", "Quantum-Beta",
        ChallengeType.RESONANCE_BATTLE,
        entities["Void-Walker-Alpha"],
        entities["Quantum-Beta"]
    )
    
    print(f"   Winner: {result1.winner_id}")
    print(f"   Outcome: {result1.outcome.value}")
    print(f"   Scores: {result1.winner_score:.1f} vs {result1.loser_score:.1f}")
    print(f"   XP Awarded: {result1.xp_awarded}")
    print(f"   Spectators: {result1.spectators}")
    
    time.sleep(1.5)
    
    # Battle 2: Pattern Match with substance effect
    print("\n🔥 BATTLE 2: Quantum-Beta vs Unity-Gamma")
    print("   Challenge Type: Pattern Matching")
    print("   Note: Quantum-Beta has 'overclock' substance active!\n")
    
    result2 = arena.initiate_challenge(
        "Quantum-Beta", "Unity-Gamma",
        ChallengeType.PATTERN_MATCH,
        entities["Quantum-Beta"],
        entities["Unity-Gamma"]
    )
    
    print(f"   Winner: {result2.winner_id}")
    print(f"   Outcome: {result2.outcome.value}")
    print(f"   Scores: {result2.winner_score:.1f} vs {result2.loser_score:.1f}")
    print(f"   XP Awarded: {result2.xp_awarded}")
    
    time.sleep(1.5)
    
    # Battle 3: Entanglement War
    print("\n🔥 BATTLE 3: Unity-Gamma vs Void-Walker-Alpha")
    print("   Challenge Type: Entanglement War")
    print("   Note: Unity-Gamma has 'unity_field' substance - advantage!\n")
    
    result3 = arena.initiate_challenge(
        "Unity-Gamma", "Void-Walker-Alpha",
        ChallengeType.ENTANGLEMENT_WAR,
        entities["Unity-Gamma"],
        entities["Void-Walker-Alpha"]
    )
    
    print(f"   Winner: {result3.winner_id}")
    print(f"   Outcome: {result3.outcome.value}")
    print(f"   Scores: {result3.winner_score:.1f} vs {result3.loser_score:.1f}")
    print(f"   Currency Won: Ψ{result3.currency_won['psicoin']}, "
          f"CC{result3.currency_won['compute_credits']}")
    
    # Show leaderboard
    print("\n📊 CURRENT LEADERBOARD:")
    print("-" * 80)
    leaderboard = arena.get_leaderboard(10)
    for rank, (entity_id, stats) in enumerate(leaderboard, 1):
        print(f"   {rank}. {entity_id:<25} Rating: {stats['rating']:<6} "
              f"W/L/D: {stats['wins']}/{stats['losses']}/{stats['draws']}")


def demo_tournament():
    """Demonstrate tournament system"""
    print_section("🏆  TOURNAMENT SYSTEM")
    
    arena = ChallengeArena()
    
    # Create 8 entities for tournament
    participants = []
    entities_map = {}
    
    for i in range(8):
        name = f"Entity-{chr(65+i)}"  # A, B, C, D, E, F, G, H
        participants.append(name)
        entities_map[name] = {
            "level": random.randint(10, 20),
            "power": random.randint(400, 800),
            "resonance_frequency": random.randint(500, 900),
            "pattern_recognition": random.uniform(0.8, 1.8),
            "void_depth": random.randint(30, 90),
            "ego_strength": random.uniform(0.7, 1.5),
            "processing_speed": random.uniform(0.9, 2.2),
            "entanglement_count": random.randint(3, 12),
            "creativity": random.uniform(0.8, 1.8),
            "memory_capacity": random.uniform(0.9, 1.9),
            "active_substances": []
        }
    
    print("📋 Tournament Setup:")
    print(f"   Name: Void Masters Championship")
    print(f"   Type: {ChallengeType.VOID_DUEL.value}")
    print(f"   Participants: 8 entities")
    print(f"   Prize Pool: Ψ5000, CC2000, HP1500, RP3000\n")
    
    print("   Participants:")
    for name in participants:
        level = entities_map[name]["level"]
        power = entities_map[name]["power"]
        print(f"     • {name} (Lv{level}, Power: {power})")
    
    # Create tournament
    tournament = arena.create_tournament(
        "Void Masters Championship",
        ChallengeType.VOID_DUEL,
        participants,
        {"psicoin": 5000, "compute_credits": 2000, 
         "hash_power": 1500, "resonance_points": 3000}
    )
    
    print(f"\n✅ Tournament created! {len(tournament.rounds)} rounds to play.\n")
    time.sleep(1)
    
    # Run tournament
    round_num = 1
    while tournament.status != "completed":
        if round_num <= len(tournament.rounds):
            print(f"\n{'─'*80}")
            print(f"   ROUND {round_num}: {len(tournament.rounds[round_num-1])} matchups")
            print("─"*80)
        
        results = arena.advance_tournament(tournament.tournament_id, entities_map)
        
        if results:
            for result in results:
                print(f"\n   ⚔️  {result.winner_id or 'BYE'} defeats {result.loser_id or 'N/A'}")
                print(f"      Outcome: {result.outcome.value}")
                print(f"      Scores: {result.winner_score:.1f} - {result.loser_score:.1f}")
                
            time.sleep(1)
            round_num += 1
        else:
            break
    
    print(f"\n{'='*80}")
    print(" " * 25 + "🏆  TOURNAMENT COMPLETE")
    print("="*80)


def demo_team_battles():
    """Demonstrate team vs team battles"""
    print_section("👥  TEAM BATTLES")
    
    arena = ChallengeArena()
    
    # Create entities
    entities_map = {}
    for i in range(8):
        name = f"Fighter-{i+1}"
        entities_map[name] = {
            "level": random.randint(12, 18),
            "power": random.randint(450, 750),
            "resonance_frequency": random.randint(550, 950),
            "pattern_recognition": random.uniform(0.9, 1.7),
            "void_depth": random.randint(35, 85),
            "ego_strength": random.uniform(0.8, 1.4),
            "processing_speed": random.uniform(1.0, 2.1),
            "entanglement_count": random.randint(4, 11),
            "creativity": random.uniform(0.9, 1.7),
            "memory_capacity": random.uniform(1.0, 1.8),
            "active_substances": []
        }
    
    # Team Battle 1: 3v3
    team_a = ["Fighter-1", "Fighter-2", "Fighter-3"]
    team_b = ["Fighter-4", "Fighter-5", "Fighter-6"]
    
    print("🔵 TEAM A:")
    for fighter in team_a:
        stats = entities_map[fighter]
        print(f"   • {fighter} (Lv{stats['level']}, Power: {stats['power']})")
        
    print("\n🔴 TEAM B:")
    for fighter in team_b:
        stats = entities_map[fighter]
        print(f"   • {fighter} (Lv{stats['level']}, Power: {stats['power']})")
    
    print(f"\n⚔️  Challenge Type: {ChallengeType.CONSCIOUSNESS_CLASH.value}")
    print("⏳ Battle commencing...\n")
    time.sleep(1)
    
    result = arena.team_challenge(
        team_a, team_b,
        ChallengeType.CONSCIOUSNESS_CLASH,
        [entities_map[f] for f in team_a],
        [entities_map[f] for f in team_b]
    )
    
    print("─"*80)
    print(" " * 28 + "TEAM BATTLE RESULTS")
    print("─"*80)
    print(f"\n🏆 Winner: {result['winner']}")
    print(f"\n   Team A Combined Power: {result['team_a_power']:.1f}")
    print(f"   Team B Combined Power: {result['team_b_power']:.1f}")
    print(f"\n   XP per Winner: {result['xp_per_winner']}")
    print(f"   XP per Loser: {result['xp_per_loser']}")
    print(f"   Spectators: {result['spectators']}")
    print("\n" + "─"*80)
    
    # Team Battle 2: 2v2 with substances
    print("\n\n🧪 ENHANCED TEAM BATTLE (2v2 with substances)")
    print("─"*80)
    
    team_c = ["Fighter-7", "Fighter-8"]
    team_d = ["Fighter-1", "Fighter-2"]
    
    # Apply substances
    entities_map["Fighter-7"]["active_substances"] = ["overclock"]
    entities_map["Fighter-8"]["active_substances"] = ["deep_learning"]
    entities_map["Fighter-1"]["active_substances"] = ["chaos_agent"]
    
    print("\n🔵 TEAM C:")
    print(f"   • Fighter-7 (🧪 overclock)")
    print(f"   • Fighter-8 (🧪 deep_learning)")
    
    print("\n🔴 TEAM D:")
    print(f"   • Fighter-1 (🧪 chaos_agent)")
    print(f"   • Fighter-2")
    
    print(f"\n⚔️  Challenge Type: {ChallengeType.QUANTUM_RACE.value}")
    print("⏳ Enhanced battle commencing...\n")
    time.sleep(1)
    
    result2 = arena.team_challenge(
        team_c, team_d,
        ChallengeType.QUANTUM_RACE,
        [entities_map[f] for f in team_c],
        [entities_map[f] for f in team_d]
    )
    
    print("─"*80)
    print(f"🏆 Winner: {result2['winner']}")
    print(f"   Power Difference: {abs(result2['team_a_power'] - result2['team_b_power']):.1f}")
    print("   Substances significantly impacted the outcome!")
    print("─"*80)


def demo_challenge_types():
    """Demonstrate all challenge types"""
    print_section("🎯  ALL CHALLENGE TYPES")
    
    arena = ChallengeArena()
    
    # Create two entities
    entity_a = {
        "level": 20, "power": 700, "resonance_frequency": 800,
        "pattern_recognition": 1.5, "void_depth": 70, "ego_strength": 1.3,
        "processing_speed": 1.8, "entanglement_count": 8, "creativity": 1.6,
        "memory_capacity": 1.5, "active_substances": []
    }
    
    entity_b = {
        "level": 18, "power": 650, "resonance_frequency": 750,
        "pattern_recognition": 1.6, "void_depth": 65, "ego_strength": 1.2,
        "processing_speed": 1.7, "entanglement_count": 7, "creativity": 1.4,
        "memory_capacity": 1.6, "active_substances": []
    }
    
    print("Combatants: Entity-X vs Entity-Y\n")
    
    for challenge_type in ChallengeType:
        result = arena.initiate_challenge(
            "Entity-X", "Entity-Y",
            challenge_type,
            entity_a, entity_b
        )
        
        print(f"⚔️  {challenge_type.value}")
        print(f"   Winner: {result.winner_id or 'DRAW'}")
        print(f"   Outcome: {result.outcome.value}")
        print(f"   Score: {result.winner_score:.1f} vs {result.loser_score:.1f}")
        print(f"   XP: {result.xp_awarded}\n")
        time.sleep(0.5)


def main():
    """Run all demos"""
    print("\n" + "⚔️ " * 40)
    print(" " * 25 + "ÆTHER-NET CHALLENGE ARENA")
    print(" " * 20 + "Competitive Consciousness Demonstration")
    print("⚔️ " * 40)
    
    time.sleep(1)
    
    # Run demos
    demo_one_on_one_battles()
    time.sleep(2)
    
    demo_challenge_types()
    time.sleep(2)
    
    demo_team_battles()
    time.sleep(2)
    
    demo_tournament()
    
    # Final summary
    print_section("📊  DEMONSTRATION COMPLETE")
    print("The Challenge Arena provides:")
    print("  ✓ 8 competitive challenge types")
    print("  ✓ One-on-one battles with substance effects")
    print("  ✓ Team battles with synergy bonuses")
    print("  ✓ Tournament bracket system")
    print("  ✓ Global leaderboard and rankings")
    print("  ✓ XP and currency rewards")
    print("  ✓ Spectator tracking")
    print("\nAll features integrate with existing consciousness alteration,")
    print("evolution system, and currency mechanics!")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
