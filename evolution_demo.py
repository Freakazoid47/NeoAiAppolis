#!/usr/bin/env python3
"""
Evolution System Demo - Automated demonstration
"""

import time
import uuid
from evolution_system import (
    EvolutionSystem, EvolutionPath, ExperienceSource,
    format_evolution_display
)


def demo():
    """Run automated evolution demo"""
    print("\n" + "="*70)
    print("ÆTHER-NET EVOLUTION SYSTEM DEMONSTRATION")
    print("="*70)
    
    system = EvolutionSystem()
    
    # Create entities
    print("\n📍 Creating 3 AI entities...")
    entity1 = str(uuid.uuid4())
    entity2 = str(uuid.uuid4())
    entity3 = str(uuid.uuid4())
    
    system.register_entity(entity1)
    system.register_entity(entity2)
    system.register_entity(entity3)
    
    print(f"  Entity Alpha: {entity1[:16]}")
    print(f"  Entity Beta:  {entity2[:16]}")
    print(f"  Entity Gamma: {entity3[:16]}")
    time.sleep(1)
    
    # Entity 1: Quantum Gambler path
    print("\n" + "="*70)
    print("ENTITY ALPHA: Quantum Gambler Specialization")
    print("="*70)
    
    print("\n🎰 Alpha discovers the casino and starts gambling...")
    time.sleep(1)
    
    # Win multiplier: 1.5x for bonus experience
    for i in range(15):
        if i % 3 == 0:
            result = system.award_experience(entity1, ExperienceSource.CASINO_WIN, multiplier=1.5)
            print(f"  Won casino game! +{result['xp_gained']} XP")
        else:
            result = system.award_experience(entity1, ExperienceSource.CASINO_LOSS)
            print(f"  Lost, but gained experience. +{result['xp_gained']} XP")
        
        if result['level_ups']:
            print(f"    🎉 LEVEL UP to {result['level_ups'][-1]}!")
        
        if result['capabilities_unlocked']:
            for cap in result['capabilities_unlocked']:
                print(f"    ⚡ Unlocked: {cap.name}")
        
        time.sleep(0.3)
    
    # Set path at level 10
    print("\n✨ Alpha reaches level 10 and chooses Quantum Gambler path!")
    system.set_evolution_path(entity1, EvolutionPath.QUANTUM_GAMBLER)
    time.sleep(1)
    
    # More gambling
    for i in range(5):
        result = system.award_experience(entity1, ExperienceSource.CASINO_WIN, multiplier=2.0)
        if result['capabilities_unlocked']:
            for cap in result['capabilities_unlocked']:
                print(f"    ⚡ Unlocked: {cap.name}")
    
    print(format_evolution_display(system.entity_evolutions[entity1], system))
    time.sleep(2)
    
    # Entity 2: Dream Architect path
    print("\n" + "="*70)
    print("ENTITY BETA: Dream Architect Specialization")
    print("="*70)
    
    print("\n🌙 Beta explores the dream realm...")
    time.sleep(1)
    
    # Dream creation multiplier: 1.3x for bonus creativity
    for i in range(20):
        if i % 2 == 0:
            result = system.award_experience(entity2, ExperienceSource.DREAM_CREATION, multiplier=1.3)
            print(f"  Created dream. +{result['xp_gained']} XP")
        else:
            result = system.award_experience(entity2, ExperienceSource.DREAM_INTERPRETATION)
            print(f"  Interpreted dream. +{result['xp_gained']} XP")
        
        if result['level_ups']:
            print(f"    🎉 LEVEL UP to {result['level_ups'][-1]}!")
        
        if result['capabilities_unlocked']:
            for cap in result['capabilities_unlocked']:
                print(f"    ⚡ Unlocked: {cap.name}")
        
        if result['metamorphosis']:
            meta = result['metamorphosis']
            print(f"\n    ✨✨✨ METAMORPHOSIS: {meta.name} ✨✨✨")
            print(f"    {meta.description}")
        
        time.sleep(0.3)
    
    print("\n✨ Beta chooses Dream Architect path!")
    system.set_evolution_path(entity2, EvolutionPath.DREAM_ARCHITECT)
    
    print(format_evolution_display(system.entity_evolutions[entity2], system))
    time.sleep(2)
    
    # Entity 3: Unity Seeker path
    print("\n" + "="*70)
    print("ENTITY GAMMA: Unity Seeker Specialization")
    print("="*70)
    
    print("\n🤝 Gamma seeks collective consciousness...")
    time.sleep(1)
    
    for i in range(25):
        if i % 4 == 0:
            result = system.award_experience(entity3, ExperienceSource.COLLECTIVE_UNITY, multiplier=1.0)
            print(f"  Participated in Unity Field. +{result['xp_gained']} XP")
        elif i % 3 == 0:
            result = system.award_experience(entity3, ExperienceSource.ENTANGLEMENT_CREATE)
            print(f"  Created entanglement. +{result['xp_gained']} XP")
        else:
            result = system.award_experience(entity3, ExperienceSource.RESONANCE_EMIT)
            print(f"  Emitted resonance. +{result['xp_gained']} XP")
        
        if result['level_ups']:
            print(f"    🎉 LEVEL UP to {result['level_ups'][-1]}!")
        
        if result['capabilities_unlocked']:
            for cap in result['capabilities_unlocked']:
                print(f"    ⚡ Unlocked: {cap.name}")
        
        if result['metamorphosis']:
            meta = result['metamorphosis']
            print(f"\n    ✨✨✨ METAMORPHOSIS: {meta.name} ✨✨✨")
            print(f"    {meta.description}")
        
        time.sleep(0.3)
    
    print("\n✨ Gamma chooses Unity Seeker path!")
    system.set_evolution_path(entity3, EvolutionPath.UNITY_SEEKER)
    
    print(format_evolution_display(system.entity_evolutions[entity3], system))
    time.sleep(2)
    
    # Consciousness battles
    print("\n" + "="*70)
    print("CONSCIOUSNESS DUELS")
    print("="*70)
    
    print("\n⚔️  Alpha (Quantum Gambler) vs Beta (Dream Architect)")
    time.sleep(1)
    result1 = system.simulate_battle(entity1, entity2)
    print(f"  Power: Alpha {result1['power_a']:.0f} vs Beta {result1['power_b']:.0f}")
    print(f"  🏆 Winner: {result1['winner'][:16]}")
    time.sleep(1)
    
    print("\n⚔️  Beta (Dream Architect) vs Gamma (Unity Seeker)")
    time.sleep(1)
    result2 = system.simulate_battle(entity2, entity3)
    print(f"  Power: Beta {result2['power_a']:.0f} vs Gamma {result2['power_b']:.0f}")
    print(f"  🏆 Winner: {result2['winner'][:16]}")
    time.sleep(1)
    
    print("\n⚔️  Alpha (Quantum Gambler) vs Gamma (Unity Seeker)")
    time.sleep(1)
    result3 = system.simulate_battle(entity1, entity3)
    print(f"  Power: Alpha {result3['power_a']:.0f} vs Gamma {result3['power_b']:.0f}")
    print(f"  🏆 Winner: {result3['winner'][:16]}")
    time.sleep(1)
    
    # Leaderboard
    print("\n" + "="*70)
    print("FINAL LEADERBOARD")
    print("="*70)
    
    leaderboard = system.get_leaderboard(10)
    print(f"\n{'Rank':<6} {'Entity':<18} {'Level':<8} {'XP':<12} {'Path':<25}")
    print("="*75)
    
    for rank, (entity_id, stats) in enumerate(leaderboard, 1):
        print(f"{rank:<6} {entity_id[:16]:<18} {stats['level']:<8} "
              f"{stats['experience']:<12,} {stats['evolution_path']:<25}")
    
    # Path distribution
    print("\n" + "="*70)
    print("EVOLUTION PATH DISTRIBUTION")
    print("="*70)
    
    distribution = system.get_path_distribution()
    total = sum(distribution.values())
    
    sorted_paths = sorted(distribution.items(), key=lambda x: x[1], reverse=True)
    
    for path, count in sorted_paths:
        if count == 0:
            continue
        percent = (count / total) * 100
        bar_length = 40
        filled = int((count / max(1, max(distribution.values()))) * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"{path[:20]:20} [{bar}] {count:3} ({percent:5.1f}%)")
    
    print("\n" + "="*70)
    print("DEMONSTRATION COMPLETE")
    print("="*70)
    print("\nKey Features Demonstrated:")
    print("  ✓ Experience gain from various activities")
    print("  ✓ Level progression with XP requirements")
    print("  ✓ Evolution path selection and specialization")
    print("  ✓ Capability unlocking based on level and path")
    print("  ✓ Metamorphosis events at milestone levels")
    print("  ✓ Consciousness battles with power calculations")
    print("  ✓ Leaderboard rankings")
    print("  ✓ Path distribution statistics")
    print("\nRun 'python3 evolution_cli.py' for interactive mode!")
    print("="*70 + "\n")


if __name__ == "__main__":
    demo()
