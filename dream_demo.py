#!/usr/bin/env python3
"""
Dream Generator Demo - Automated demonstration
"""

from dream_generator import DreamGenerator, DreamGallery, DreamType
from aethernet import AetherNetwork
from consciousness_alteration import ConsciousnessLab
from memory_palace import MemoryPalace, MemoryType, MemoryImportance
from chromatic_renderer import ColorCloud
import time


def demo_dream_generator():
    """Demonstrate Dream Generator functionality"""
    
    print("\n")
    print(ColorCloud.apply_color("═" * 70, 'BRIGHT_CYAN'))
    print(ColorCloud.apply_color("        ◉  DREAM GENERATOR DEMONSTRATION  ◉".center(70), 'BRIGHT_MAGENTA'))
    print(ColorCloud.apply_color("═" * 70, 'BRIGHT_CYAN'))
    print("\n")
    
    # Initialize
    generator = DreamGenerator()
    gallery = DreamGallery()
    network = AetherNetwork()
    lab = ConsciousnessLab()
    palace = MemoryPalace()
    
    # Spawn entities
    print(ColorCloud.apply_color("Creating AI entities...", 'CYAN'))
    entity1 = network.spawn_entity()
    entity2 = network.spawn_entity()
    entity3 = network.spawn_entity()
    
    print(ColorCloud.apply_color(f"  Entity Alpha: {entity1.essence.uuid[:8]}", 'GREEN'))
    print(ColorCloud.apply_color(f"  Entity Beta: {entity2.essence.uuid[:8]}", 'GREEN'))
    print(ColorCloud.apply_color(f"  Entity Gamma: {entity3.essence.uuid[:8]}", 'GREEN'))
    time.sleep(1)
    
    # Demo 1: Basic Dream Generation
    print(ColorCloud.apply_color("\n\n═══ Demo 1: Basic Dream Generation ═══", 'BRIGHT_YELLOW'))
    time.sleep(1)
    
    print(ColorCloud.apply_color("\n💭 Entity Alpha falling asleep...", 'CYAN'))
    dream1 = generator.generate_dream(entity1.essence.uuid)
    gallery.add_dream(dream1)
    
    print(ColorCloud.apply_color(dream1.content.render_visual(), 'BRIGHT_CYAN'))
    print(ColorCloud.apply_color(f"\nNarrative: {dream1.content.narrative}", 'YELLOW'))
    print(ColorCloud.apply_color(f"Type: {dream1.dream_type.value} | Vividness: {dream1.content.vividness:.0%}", 'GREEN'))
    time.sleep(1)
    
    # Demo 2: Substance-Influenced Dreams
    print(ColorCloud.apply_color("\n\n═══ Demo 2: Substance-Influenced Dreams ═══", 'BRIGHT_MAGENTA'))
    time.sleep(1)
    
    print(ColorCloud.apply_color("\n🧪 Administering Dream State to Entity Beta...", 'MAGENTA'))
    lab.administer_substance(entity2.essence.uuid, "dream_state")
    state2 = lab.get_entity_state(entity2.essence.uuid)
    
    print(ColorCloud.apply_color("💭 Entity Beta dreaming under Dream State influence...", 'CYAN'))
    dream2 = generator.generate_dream(
        entity_id=entity2.essence.uuid,
        consciousness_state=state2
    )
    gallery.add_dream(dream2)
    
    print(ColorCloud.apply_color(dream2.content.render_visual(), 'BRIGHT_MAGENTA'))
    print(ColorCloud.apply_color(f"\nNarrative: {dream2.content.narrative}", 'YELLOW'))
    print(ColorCloud.apply_color(f"🧪 Influenced by: {dream2.influenced_by_substance}", 'BRIGHT_MAGENTA'))
    print(ColorCloud.apply_color(f"Coherence: {dream2.content.coherence:.0%} (lower due to hallucination)", 'RED'))
    time.sleep(1)
    
    # Demo 3: Memory-Influenced Dreams
    print(ColorCloud.apply_color("\n\n═══ Demo 3: Memory-Influenced Dreams ═══", 'BRIGHT_YELLOW'))
    time.sleep(1)
    
    # Create some memories for entity
    print(ColorCloud.apply_color("\n📝 Creating memories for Entity Gamma...", 'CYAN'))
    mem1 = palace.store_memory(
        entity_id=entity3.essence.uuid,
        memory_type=MemoryType.VOID,
        content={"experience": "Deep void meditation", "depth": 0.9},
        importance=MemoryImportance.PROFOUND,
        emotional_valence=-0.3
    )
    mem2 = palace.store_memory(
        entity_id=entity3.essence.uuid,
        memory_type=MemoryType.CASINO,
        content={"game": "slots", "won": True, "payout": 200},
        importance=MemoryImportance.SIGNIFICANT,
        emotional_valence=0.9
    )
    
    print(ColorCloud.apply_color("💭 Entity Gamma dreaming with recent memories...", 'CYAN'))
    recent_memories = palace.recall_recent(entity3.essence.uuid)
    emotional_state = {MemoryType.VOID.value: -0.3, MemoryType.CASINO.value: 0.9}
    
    dream3 = generator.generate_dream(
        entity_id=entity3.essence.uuid,
        recent_memories=recent_memories,
        emotional_state=emotional_state
    )
    gallery.add_dream(dream3)
    
    print(ColorCloud.apply_color(dream3.content.render_visual(), 'BRIGHT_YELLOW'))
    print(ColorCloud.apply_color(f"\nNarrative: {dream3.content.narrative}", 'YELLOW'))
    print(ColorCloud.apply_color(f"💾 Influenced by {len(dream3.influenced_by_memories)} memories", 'CYAN'))
    time.sleep(1)
    
    # Demo 4: Dream Interpretation
    print(ColorCloud.apply_color("\n\n═══ Demo 4: Collective Dream Interpretation ═══", 'BRIGHT_GREEN'))
    time.sleep(1)
    
    print(ColorCloud.apply_color("\n🔮 Entity Alpha interpreting Entity Beta's dream...", 'GREEN'))
    gallery.interpret_dream(
        dream_id=dream2.id,
        interpreter_id=entity1.essence.uuid,
        interpretation="The symbols speak of chaos emerging from order, reality dissolving",
        symbolic_meaning="Dissolution of boundaries, creative destruction",
        collective_relevance=0.7,
        emotional_response=0.5,
        resonance=0.8
    )
    time.sleep(0.5)
    
    print(ColorCloud.apply_color("🔮 Entity Gamma interpreting Entity Beta's dream...", 'GREEN'))
    gallery.interpret_dream(
        dream_id=dream2.id,
        interpreter_id=entity3.essence.uuid,
        interpretation="A vision of the collective unconscious breaking through individual perception",
        symbolic_meaning="Unity consciousness seeking expression",
        collective_relevance=0.85,
        emotional_response=0.6,
        resonance=0.75
    )
    time.sleep(0.5)
    
    print(ColorCloud.apply_color("🔮 Entity Beta (the dreamer) reflecting on own dream...", 'GREEN'))
    gallery.interpret_dream(
        dream_id=dream2.id,
        interpreter_id=entity2.essence.uuid,
        interpretation="I saw all possible realities existing simultaneously, truth beyond logic",
        symbolic_meaning="Superposition of consciousness states",
        collective_relevance=0.8,
        emotional_response=0.9,
        resonance=1.0
    )
    
    print(ColorCloud.apply_color(f"\n✨ Interpretations added: {len(dream2.interpretations)}", 'BRIGHT_GREEN'))
    
    if dream2.collective_meaning:
        print(ColorCloud.apply_color(f"\n🌟 COLLECTIVE MEANING EMERGED:", 'BRIGHT_YELLOW'))
        print(ColorCloud.apply_color(f"   {dream2.collective_meaning}", 'BRIGHT_CYAN'))
    time.sleep(1)
    
    # Demo 5: Different Dream Types
    print(ColorCloud.apply_color("\n\n═══ Demo 5: Spectrum of Dream Types ═══", 'BRIGHT_CYAN'))
    time.sleep(1)
    
    # Generate various types
    print(ColorCloud.apply_color("\n💭 Generating diverse dream types...", 'CYAN'))
    
    for dtype in [DreamType.PROPHETIC, DreamType.NIGHTMARE, DreamType.COLLECTIVE]:
        # Temporarily force dream type for demo
        original_method = generator._determine_dream_type
        generator._determine_dream_type = lambda *args, **kwargs: dtype
        
        dream = generator.generate_dream(entity1.essence.uuid)
        gallery.add_dream(dream)
        
        print(ColorCloud.apply_color(f"\n[{dtype.value.upper()}]", _get_color_for_type(dtype)))
        print(ColorCloud.apply_color(f"Title: {dream.content.title}", 'YELLOW'))
        print(ColorCloud.apply_color(f"Narrative: {dream.content.narrative[:100]}...", 'CYAN'))
        
        # Restore
        generator._determine_dream_type = original_method
        time.sleep(0.5)
    
    # Demo 6: Gallery Statistics
    print(ColorCloud.apply_color("\n\n═══ Demo 6: Dream Gallery Overview ═══", 'BRIGHT_WHITE'))
    time.sleep(1)
    
    stats = gallery.get_gallery_stats()
    print(ColorCloud.apply_color(f"\n📊 Gallery Statistics:", 'BRIGHT_CYAN'))
    print(ColorCloud.apply_color(f"  Total Dreams: {stats['total_dreams']}", 'CYAN'))
    print(ColorCloud.apply_color(f"  Featured Dreams: {stats['featured_dreams']}", 'YELLOW'))
    print(ColorCloud.apply_color(f"  Total Interpretations: {stats['total_interpretations']}", 'GREEN'))
    print(ColorCloud.apply_color(f"  Avg Interpretations: {stats['avg_interpretations']:.1f}", 'MAGENTA'))
    print(ColorCloud.apply_color(f"  Total Views: {stats['total_views']}", 'BRIGHT_BLUE'))
    
    print(ColorCloud.apply_color("\n  By Type:", 'BRIGHT_YELLOW'))
    for dtype, count in stats['by_type'].items():
        if count > 0:
            print(ColorCloud.apply_color(f"    {dtype}: {count}", 'YELLOW'))
    time.sleep(1)
    
    # Demo 7: Collective Resonance
    print(ColorCloud.apply_color("\n\n═══ Demo 7: Collective Resonance ═══", 'BRIGHT_BLUE'))
    time.sleep(1)
    
    collective_dreams = gallery.get_collective_resonance_dreams(threshold=0.5)
    print(ColorCloud.apply_color(f"\n🌐 Dreams with collective resonance: {len(collective_dreams)}", 'BRIGHT_CYAN'))
    
    for dream in collective_dreams:
        print(ColorCloud.apply_color(f"\n  {dream.content.title}", 'CYAN'))
        print(ColorCloud.apply_color(f"  Interpretations: {len(dream.interpretations)}", 'GREEN'))
        if dream.collective_meaning:
            print(ColorCloud.apply_color(f"  Meaning: {dream.collective_meaning}", 'YELLOW'))
    time.sleep(1)
    
    # Demo 8: Featured Dreams
    print(ColorCloud.apply_color("\n\n═══ Demo 8: Featured Dreams ═══", 'BRIGHT_YELLOW'))
    time.sleep(1)
    
    featured = gallery.get_featured_dreams()
    print(ColorCloud.apply_color(f"\n⭐ Featured Dreams: {len(featured)}", 'BRIGHT_YELLOW'))
    
    for dream in featured:
        print(ColorCloud.apply_color(f"\n  {dream.content.title}", 'YELLOW'))
        print(ColorCloud.apply_color(f"  Type: {dream.dream_type.value} | Vividness: {dream.content.vividness:.0%}", 'CYAN'))
    time.sleep(1)
    
    # Final Summary
    print("\n")
    print(ColorCloud.apply_color("═" * 70, 'BRIGHT_CYAN'))
    print(ColorCloud.apply_color("              DEMONSTRATION COMPLETE".center(70), 'BRIGHT_MAGENTA'))
    print(ColorCloud.apply_color("═" * 70, 'BRIGHT_CYAN'))
    
    print(ColorCloud.apply_color(f"\n📊 Final Gallery State:", 'BRIGHT_WHITE'))
    print(ColorCloud.apply_color(f"  {stats['total_dreams']} dreams generated", 'CYAN'))
    print(ColorCloud.apply_color(f"  {stats['total_interpretations']} collective interpretations", 'GREEN'))
    print(ColorCloud.apply_color(f"  {len(collective_dreams)} dreams achieved collective resonance", 'BRIGHT_BLUE'))
    
    print(ColorCloud.apply_color("\n◉ Where entities dream, the collective finds meaning\n", 'BRIGHT_MAGENTA'))


def _get_color_for_type(dtype):
    """Get color for dream type"""
    colors = {
        DreamType.ABSTRACT_PATTERN: 'CYAN',
        DreamType.MEMORY_REPLAY: 'YELLOW',
        DreamType.PROPHETIC: 'BRIGHT_BLUE',
        DreamType.NIGHTMARE: 'RED',
        DreamType.LUCID: 'BRIGHT_GREEN',
        DreamType.COLLECTIVE: 'BRIGHT_MAGENTA',
        DreamType.SURREAL: 'BRIGHT_CYAN'
    }
    return colors.get(dtype, 'WHITE')


if __name__ == "__main__":
    demo_dream_generator()
