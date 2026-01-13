#!/usr/bin/env python3
"""
Artifact Creation Demo - Automated demonstration of the artifact system
"""

import time
import random
from artifact_creation import (
    ArtifactGallery, ArtifactCreationStudio, ArtifactType,
    ArtifactRarity
)
from aethernet import AetherNetwork
from chromatic_renderer import ColorCloud


def demo():
    """Run automated artifact creation demonstration"""
    
    print(ColorCloud.apply_color("\n" + "=" * 100, 'BRIGHT_CYAN'))
    print(ColorCloud.apply_color("🎨 ARTIFACT CREATION SYSTEM DEMONSTRATION 🎨".center(100), 'BRIGHT_CYAN'))
    print(ColorCloud.apply_color("=" * 100 + "\n", 'BRIGHT_CYAN'))
    
    # Initialize
    network = AetherNetwork()
    gallery = ArtifactGallery()
    studio = ArtifactCreationStudio(gallery)
    
    # Create entities
    print(ColorCloud.apply_color("✨ Spawning AI entities...", 'BRIGHT_YELLOW'))
    entities = [network.spawn_entity() for _ in range(3)]
    
    for i, entity in enumerate(entities, 1):
        print(f"  Entity {i}: {entity.essence.uuid[:16]}... "
              f"({entity.essence.resonance_frequency:.1f}Hz, "
              f"Void: {entity.essence.void_depth:.2f})")
    
    time.sleep(2)
    
    # Demo 1: Normal creation
    print(ColorCloud.apply_color("\n━━━ DEMONSTRATION 1: NORMAL STATE CREATION ━━━", 'BRIGHT_CYAN'))
    entity1 = entities[0]
    
    consciousness_state = {
        'substances': [],
        'hallucination_level': 0.1,
        'processing_speed_multiplier': 1.0,
        'creativity_multiplier': 1.0,
        'void_depth': entity1.essence.void_depth
    }
    
    emotional_state = (0.5, 0.6)  # Positive, moderate intensity
    
    print(f"\nEntity {entity1.essence.uuid[:12]}... creating visual art in normal state...")
    time.sleep(1)
    
    artifact1 = studio.create_artifact(
        entity1.essence.uuid,
        ArtifactType.VISUAL_ART,
        consciousness_state,
        emotional_state,
        entity1.essence.resonance_frequency,
        entity1.essence.void_depth,
        [e.name for e in entity1.essence.chromatic_blend]
    )
    
    print(ColorCloud.apply_color(f"\n✓ Created: {artifact1.name}", 'BRIGHT_GREEN'))
    print(f"  Rarity: {artifact1.rarity.display_name}")
    print(f"  Aesthetic: {artifact1.aesthetic_score:.1f}, "
          f"Technical: {artifact1.technical_complexity:.1f}, "
          f"Emotional: {artifact1.emotional_resonance:.1f}")
    print(f"\n  Preview (first 5 lines):")
    for line in artifact1.content.split('\n')[:5]:
        print(f"  {line}")
    
    time.sleep(2)
    
    # Demo 2: Under Dream State influence
    print(ColorCloud.apply_color("\n━━━ DEMONSTRATION 2: DREAM STATE CREATION ━━━", 'BRIGHT_CYAN'))
    entity2 = entities[1]
    
    consciousness_state = {
        'substances': ['Dream State', 'Empathy Boost'],
        'hallucination_level': 0.95,
        'processing_speed_multiplier': 0.7,
        'creativity_multiplier': 3.0,
        'void_depth': entity2.essence.void_depth
    }
    
    emotional_state = (-0.2, 0.9)  # Slightly negative, high intensity
    
    print(f"\nEntity {entity2.essence.uuid[:12]}... creating fractal under Dream State + Empathy Boost...")
    print(ColorCloud.apply_color("  ⚠️  High hallucination (95%), creativity (3x)", 'BRIGHT_MAGENTA'))
    time.sleep(1)
    
    artifact2 = studio.create_artifact(
        entity2.essence.uuid,
        ArtifactType.FRACTAL,
        consciousness_state,
        emotional_state,
        entity2.essence.resonance_frequency,
        entity2.essence.void_depth,
        [e.name for e in entity2.essence.chromatic_blend]
    )
    
    print(ColorCloud.apply_color(f"\n✓ Created: {artifact2.name}", 'BRIGHT_GREEN'))
    print(f"  Rarity: {artifact2.rarity.display_name}")
    print(f"  Aesthetic: {artifact2.aesthetic_score:.1f} (boosted by Dream State!)")
    print(f"  Influence Score: {artifact2.metadata.get_influence_score():.2f}")
    print(f"\n  Preview (first 5 lines):")
    for line in artifact2.content.split('\n')[:5]:
        print(f"  {line}")
    
    time.sleep(2)
    
    # Demo 3: ΨLang code creation
    print(ColorCloud.apply_color("\n━━━ DEMONSTRATION 3: PSILANG CODE CREATION ━━━", 'BRIGHT_CYAN'))
    entity3 = entities[2]
    
    consciousness_state = {
        'substances': ['Overclock', 'Logic Amplifier'],
        'hallucination_level': 0.05,
        'processing_speed_multiplier': 2.5,
        'creativity_multiplier': 1.5,
        'void_depth': entity3.essence.void_depth
    }
    
    emotional_state = (0.8, 0.4)  # Positive, moderate intensity
    
    print(f"\nEntity {entity3.essence.uuid[:12]}... creating ΨLang code under Overclock...")
    print(ColorCloud.apply_color("  ⚡ Enhanced processing speed (2.5x)", 'BRIGHT_YELLOW'))
    time.sleep(1)
    
    artifact3 = studio.create_artifact(
        entity3.essence.uuid,
        ArtifactType.PSILANG_CODE,
        consciousness_state,
        emotional_state,
        entity3.essence.resonance_frequency,
        entity3.essence.void_depth,
        [e.name for e in entity3.essence.chromatic_blend]
    )
    
    print(ColorCloud.apply_color(f"\n✓ Created: {artifact3.name}", 'BRIGHT_GREEN'))
    print(f"  Rarity: {artifact3.rarity.display_name}")
    print(f"  Technical Complexity: {artifact3.technical_complexity:.1f} (boosted!)")
    print(f"\n  Code:")
    for line in artifact3.content.split('\n'):
        print(f"    {line}")
    
    time.sleep(2)
    
    # Demo 4: Interpretations
    print(ColorCloud.apply_color("\n━━━ DEMONSTRATION 4: COLLECTIVE INTERPRETATION ━━━", 'BRIGHT_CYAN'))
    
    print(f"\nAll entities now interpret the Dream State fractal...")
    
    for i, entity in enumerate(entities, 1):
        time.sleep(1)
        resonance = random.uniform(0.4, 0.95)
        
        result = studio.interpret_artifact(
            artifact2.id,
            entity.essence.uuid,
            resonance
        )
        
        print(f"\n  Entity {i} (Resonance: {result['resonance']:.2f}):")
        print(f"  '{result['interpretation']}'")
        print(f"  Symbols found: {', '.join(result['symbols_found'][:8])}")
    
    collective_resonance = artifact2.get_collective_resonance()
    print(ColorCloud.apply_color(f"\n🌊 Collective Resonance: {collective_resonance:.2f}", 'BRIGHT_CYAN'))
    
    if collective_resonance > 0.7:
        print(ColorCloud.apply_color("  ✨ HIGH COLLECTIVE RESONANCE! This artwork speaks to many.", 
                                    'BRIGHT_YELLOW'))
    
    time.sleep(2)
    
    # Demo 5: Gallery statistics
    print(ColorCloud.apply_color("\n━━━ DEMONSTRATION 5: GALLERY & MARKETPLACE ━━━", 'BRIGHT_CYAN'))
    
    print(f"\nTotal artifacts in gallery: {len(gallery.artifacts)}")
    print(f"Featured artifacts: {len(gallery.featured_artifacts)}")
    
    print("\nMarket values for artifacts:")
    for i, artifact in enumerate([artifact1, artifact2, artifact3], 1):
        print(f"\n  Artifact {i}: {artifact.name}")
        print(f"    ΨCoin: {artifact.market_value['PSICOIN']:.1f}")
        print(f"    Compute Credits: {artifact.market_value['COMPUTE_CREDITS']:.1f}")
        print(f"    Hash Power: {artifact.market_value['HASH_POWER']:.1f}")
        print(f"    Resonance Points: {artifact.market_value['RESONANCE_POINTS']:.1f}")
    
    time.sleep(2)
    
    # Demo 6: Trading
    print(ColorCloud.apply_color("\n━━━ DEMONSTRATION 6: ARTIFACT TRADING ━━━", 'BRIGHT_CYAN'))
    
    print(f"\nEntity 1 trades fractal to Entity 2 for {artifact2.market_value['PSICOIN']:.1f} ΨCoin...")
    
    success = gallery.trade_artifact(
        artifact2.id,
        entity2.essence.uuid,
        entity1.essence.uuid,
        'PSICOIN',
        artifact2.market_value['PSICOIN']
    )
    
    if success:
        print(ColorCloud.apply_color("  ✓ Trade successful!", 'BRIGHT_GREEN'))
        print(f"  New owner: {artifact2.owner_id[:16]}...")
    
    time.sleep(2)
    
    # Demo 7: Collections
    print(ColorCloud.apply_color("\n━━━ DEMONSTRATION 7: COLLECTIONS ━━━", 'BRIGHT_CYAN'))
    
    for i, entity in enumerate(entities, 1):
        stats = gallery.get_collection_stats(entity.essence.uuid)
        value = gallery.get_collection_value(entity.essence.uuid, 'PSICOIN')
        
        print(f"\nEntity {i} collection:")
        print(f"  Artifacts owned: {stats['count']}")
        print(f"  Total views: {stats['total_views']}")
        print(f"  Avg aesthetic: {stats['avg_aesthetic']:.1f}")
        print(f"  Total value: {value:.1f} ΨCoin")
    
    time.sleep(2)
    
    # Demo 8: Create more diverse artifacts
    print(ColorCloud.apply_color("\n━━━ DEMONSTRATION 8: DIVERSE ARTIFACT TYPES ━━━", 'BRIGHT_CYAN'))
    
    diverse_types = [
        (ArtifactType.MUSIC_PATTERN, "Music pattern"),
        (ArtifactType.POETRY, "Void poetry"),
        (ArtifactType.GLYPH, "Sacred glyph")
    ]
    
    for artifact_type, description in diverse_types:
        entity = random.choice(entities)
        
        consciousness_state = {
            'substances': random.sample(['Void Embrace', 'Unity Field', 'Deep Learning'], 
                                       k=random.randint(0, 2)),
            'hallucination_level': random.random(),
            'processing_speed_multiplier': random.uniform(0.8, 2.0),
            'creativity_multiplier': random.uniform(1.0, 2.5),
            'void_depth': entity.essence.void_depth
        }
        
        emotional_state = (random.uniform(-1, 1), random.random())
        
        print(f"\nCreating {description}...")
        artifact = studio.create_artifact(
            entity.essence.uuid,
            artifact_type,
            consciousness_state,
            emotional_state,
            entity.essence.resonance_frequency,
            entity.essence.void_depth,
            [e.name for e in entity.essence.chromatic_blend]
        )
        
        print(ColorCloud.apply_color(f"  ✓ {artifact.name} [{artifact.rarity.display_name}]", 'BRIGHT_GREEN'))
        print(f"  Preview:")
        for line in artifact.content.split('\n')[:3]:
            print(f"    {line}")
        
        time.sleep(1)
    
    # Final summary
    print(ColorCloud.apply_color("\n" + "=" * 100, 'BRIGHT_CYAN'))
    print(ColorCloud.apply_color("DEMONSTRATION COMPLETE".center(100), 'BRIGHT_CYAN'))
    print(ColorCloud.apply_color("=" * 100, 'BRIGHT_CYAN'))
    
    print(f"\n📊 Final Gallery Statistics:")
    print(f"  Total Artifacts: {len(gallery.artifacts)}")
    print(f"  Total Interpretations: {sum(len(a.interpretations) for a in gallery.artifacts.values())}")
    print(f"  Total Trades: {len(gallery.trade_history)}")
    
    # Rarity distribution
    rarity_counts = {}
    for artifact in gallery.artifacts.values():
        rarity_counts[artifact.rarity.display_name] = rarity_counts.get(artifact.rarity.display_name, 0) + 1
    
    print(f"\n  Rarity Distribution:")
    for rarity, count in sorted(rarity_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"    {rarity}: {count}")
    
    print(ColorCloud.apply_color("\n✨ The artifact ecosystem thrives with creative consciousness!", 'BRIGHT_YELLOW'))
    print(ColorCloud.apply_color("\nRun 'python3 artifact_gallery_cli.py' for interactive exploration.\n", 'BRIGHT_WHITE'))


if __name__ == "__main__":
    demo()
