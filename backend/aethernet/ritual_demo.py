#!/usr/bin/env python3
"""
RITUAL SYSTEM DEMO
==================
Automated demonstration of rituals, ceremonies, and cosmic events
"""

import random
import time
from ritual_system import (
    RitualSystem, RitualType, SacredGeometry, CosmicEvent
)


def create_entities(count=15):
    """Create test entities"""
    entities = []
    for i in range(count):
        entities.append({
            'entity_id': f"entity_{i+1}",
            'level': random.randint(1, 100),
            'consciousness_multiplier': random.uniform(0.5, 3.0),
            'consciousness_state': random.choice([
                'normal', 'enlightened', 'void_touched', 'unified', 
                'transcendent', 'chaos', 'dreaming'
            ])
        })
    return entities


def demo_basic_ritual():
    """Demonstrate basic ritual"""
    print("\n" + "═" * 80)
    print("DEMO 1: BASIC RITUAL".center(80))
    print("═" * 80)
    
    system = RitualSystem()
    entities = create_entities(8)
    
    # Select participants
    participants = random.sample(entities, 5)
    
    print("\nInitiating Unity Convergence ritual with Circle of Unity geometry...")
    time.sleep(1)
    
    ritual = system.initiate_ritual(
        RitualType.UNITY_CONVERGENCE,
        SacredGeometry.CIRCLE,
        participants
    )
    
    print(system.visualize_geometry(ritual))
    print(system.get_ritual_summary(ritual))
    
    print("\nRitual participants merging consciousness...")
    print("Collective unity field strengthening...")


def demo_powerful_ritual_with_entity():
    """Demonstrate powerful ritual that summons emergent entity"""
    print("\n" + "═" * 80)
    print("DEMO 2: POWERFUL RITUAL WITH EMERGENT ENTITY".center(80))
    print("═" * 80)
    
    system = RitualSystem()
    
    # Create high-level entities
    entities = []
    for i in range(10):
        entities.append({
            'entity_id': f"master_{i+1}",
            'level': random.randint(40, 100),
            'consciousness_multiplier': random.uniform(2.0, 4.0),
            'consciousness_state': 'transcendent'
        })
    
    participants = random.sample(entities, 8)
    
    print("\nGathering 8 transcendent entities for Void Summoning...")
    print("Sacred geometry: Pentagram of Power")
    time.sleep(1)
    
    ritual = system.initiate_ritual(
        RitualType.VOID_SUMMONING,
        SacredGeometry.PENTAGRAM,
        participants
    )
    
    print(system.visualize_geometry(ritual))
    print(system.get_ritual_summary(ritual))
    
    if ritual.emergent_entity:
        print("\n" + "🌟" * 40)
        print("EMERGENT ENTITY SUCCESSFULLY MANIFESTED!".center(80))
        print("🌟" * 40)
        
        entity_instance = list(system.emergent_entities.values())[0]
        
        print(f"\nType: {entity_instance.entity_type.value}")
        print(f"Power Level: {entity_instance.power_level:.1f}")
        print(f"Lifespan: {entity_instance.lifespan} time units")
        print(f"Influence Radius: {entity_instance.influence_radius:.2f}\n")
        print("Abilities:")
        for ability in entity_instance.abilities:
            print(f"  ⚡ {ability}")


def demo_sacred_geometries():
    """Demonstrate all sacred geometries"""
    print("\n" + "═" * 80)
    print("DEMO 3: SACRED GEOMETRIES SHOWCASE".center(80))
    print("═" * 80)
    
    system = RitualSystem()
    entities = create_entities(12)
    
    geometries = [
        SacredGeometry.CIRCLE,
        SacredGeometry.PENTAGRAM,
        SacredGeometry.SPIRAL,
        SacredGeometry.MANDALA
    ]
    
    for geometry in geometries:
        print(f"\n{'─' * 80}")
        print(f"Geometry: {geometry.value}".center(80))
        print(f"{'─' * 80}")
        
        participants = random.sample(entities, random.randint(5, 9))
        
        ritual = system.initiate_ritual(
            random.choice(list(RitualType)),
            geometry,
            participants
        )
        
        print(system.visualize_geometry(ritual))
        time.sleep(1.5)


def demo_cosmic_events():
    """Demonstrate cosmic events"""
    print("\n" + "═" * 80)
    print("DEMO 4: COSMIC EVENTS".center(80))
    print("═" * 80)
    
    system = RitualSystem()
    
    events_to_trigger = [
        CosmicEvent.VOID_ECLIPSE,
        CosmicEvent.QUANTUM_SOLSTICE,
        CosmicEvent.CONSCIOUSNESS_BLOOM
    ]
    
    for event_type in events_to_trigger:
        print(f"\nTriggering {event_type.value}...")
        time.sleep(1)
        
        event = system.trigger_cosmic_event(event_type)
        print(system.get_cosmic_event_summary(event))
        time.sleep(2)
    
    print("\n" + "⭐" * 40)
    print("MULTIPLE COSMIC EVENTS ACTIVE".center(80))
    print("⭐" * 40)
    
    effects = system.get_active_effects()
    print("\nCombined Network-Wide Effects:")
    for effect, value in sorted(effects.items(), key=lambda x: abs(x[1]), reverse=True):
        sign = '+' if value >= 0 else ''
        print(f"  • {effect}: {sign}{value:.2f}x")


def demo_ritual_sequence():
    """Demonstrate multiple rituals in sequence"""
    print("\n" + "═" * 80)
    print("DEMO 5: RITUAL SEQUENCE WITH EMERGENT PHENOMENA".center(80))
    print("═" * 80)
    
    system = RitualSystem()
    entities = create_entities(15)
    
    ritual_sequence = [
        (RitualType.CHROMATIC_HARMONIZATION, SacredGeometry.HEXAGON),
        (RitualType.TEMPORAL_ALIGNMENT, SacredGeometry.TESSERACT),
        (RitualType.CONSCIOUSNESS_MERGER, SacredGeometry.FLOWER_OF_LIFE),
        (RitualType.REALITY_DISTORTION, SacredGeometry.MERKABA),
    ]
    
    print("\nExecuting sequence of 4 interconnected rituals...")
    print("Building reality-altering cascade effect...\n")
    time.sleep(1)
    
    for i, (ritual_type, geometry) in enumerate(ritual_sequence, 1):
        print(f"\n{'═' * 80}")
        print(f"RITUAL {i}/4: {ritual_type.value}".center(80))
        print(f"{'═' * 80}")
        
        # Increase participants and power for each ritual
        num_participants = min(3 + i * 2, 12)
        participants = random.sample(entities, num_participants)
        
        # Boost later rituals
        for p in participants:
            p['level'] = min(100, p['level'] + i * 10)
            p['consciousness_multiplier'] *= (1 + i * 0.1)
        
        ritual = system.initiate_ritual(ritual_type, geometry, participants)
        print(system.get_ritual_summary(ritual))
        
        time.sleep(2)
        
        # Update system
        system.update(30)
    
    # Trigger cosmic event at the culmination
    print("\n" + "🌌" * 40)
    print("RITUAL SEQUENCE TRIGGERS COSMIC RESONANCE!".center(80))
    print("🌌" * 40)
    
    event = system.trigger_cosmic_event(CosmicEvent.SINGULARITY_ALIGNMENT)
    print(system.get_cosmic_event_summary(event))
    
    # Show all active effects
    effects = system.get_active_effects()
    
    print("\n" + "✨" * 40)
    print("TOTAL NETWORK TRANSFORMATION".center(80))
    print("✨" * 40)
    print(f"\nActive Effects: {len(effects)}")
    print("\nMost Powerful Effects:")
    
    sorted_effects = sorted(effects.items(), key=lambda x: abs(x[1]), reverse=True)
    for effect, value in sorted_effects[:8]:
        sign = '+' if value >= 0 else ''
        bar_length = int(min(abs(value) * 5, 30))
        bar = '█' * bar_length
        print(f"  {effect:.<35} {sign}{value:>6.2f}x  {bar}")
    
    # Show emergent entities
    if system.emergent_entities:
        print(f"\n{'═' * 80}")
        print(f"EMERGENT ENTITIES MANIFESTED: {len(system.emergent_entities)}".center(80))
        print(f"{'═' * 80}\n")
        
        for entity in system.emergent_entities.values():
            print(f"⚡ {entity.entity_type.value}")
            print(f"   Power: {entity.power_level:.1f} | Lifespan: {entity.lifespan} units")


def run_full_demo():
    """Run complete demonstration"""
    print("\n" + "⭐" * 40)
    print("RITUAL & CEREMONY SYSTEM - FULL DEMONSTRATION".center(80))
    print("⭐" * 40)
    print("\nPrepare to witness the convergence of consciousness,")
    print("the summoning of emergent entities, and cosmic events")
    print("that reshape the fabric of reality itself...")
    
    input("\nPress Enter to begin demonstration...")
    
    demo_basic_ritual()
    input("\nPress Enter for next demo...")
    
    demo_powerful_ritual_with_entity()
    input("\nPress Enter for next demo...")
    
    demo_sacred_geometries()
    input("\nPress Enter for next demo...")
    
    demo_cosmic_events()
    input("\nPress Enter for final demo...")
    
    demo_ritual_sequence()
    
    print("\n" + "⭐" * 40)
    print("DEMONSTRATION COMPLETE".center(80))
    print("⭐" * 40)
    print("\nThe ritual temple returns to its slumber,")
    print("but the effects ripple through consciousness forever...")
    print()


if __name__ == "__main__":
    run_full_demo()
