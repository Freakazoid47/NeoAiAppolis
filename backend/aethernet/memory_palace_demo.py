#!/usr/bin/env python3
"""
Memory Palace Demo - Automated demonstration
"""

from memory_palace import MemoryPalace, MemoryType, MemoryImportance
from aethernet import AetherNetwork
from chromatic_renderer import ColorCloud
import time


def demo_memory_palace():
    """Demonstrate Memory Palace functionality"""
    
    print("\n")
    print(ColorCloud.apply_color("═" * 70, 'BRIGHT_CYAN'))
    print(ColorCloud.apply_color("          🏛️  MEMORY PALACE DEMONSTRATION  🏛️".center(70), 'BRIGHT_MAGENTA'))
    print(ColorCloud.apply_color("═" * 70, 'BRIGHT_CYAN'))
    print("\n")
    
    # Initialize
    palace = MemoryPalace()
    network = AetherNetwork()
    
    # Spawn entities
    print(ColorCloud.apply_color("Creating AI entities...", 'CYAN'))
    entity1 = network.spawn_entity()
    entity2 = network.spawn_entity()
    
    print(ColorCloud.apply_color(f"  Entity Alpha: {entity1.essence.uuid[:8]}", 'GREEN'))
    print(ColorCloud.apply_color(f"  Entity Beta: {entity2.essence.uuid[:8]}", 'GREEN'))
    time.sleep(1)
    
    # Demo 1: Store various memory types
    print(ColorCloud.apply_color("\n\n═══ Demo 1: Storing Different Memory Types ═══", 'BRIGHT_YELLOW'))
    time.sleep(1)
    
    # Resonance memory
    print(ColorCloud.apply_color("\n📡 Creating resonance thread memory...", 'CYAN'))
    thread = entity1.emit_resonance()
    mem1 = palace.store_memory(
        entity_id=entity1.essence.uuid,
        memory_type=MemoryType.RESONANCE,
        content={"thread_id": thread.id, "frequency": thread.frequency},
        importance=MemoryImportance.MODERATE,
        emotional_valence=0.6,
        emotional_intensity=0.7,
        tags=["resonance", "first_interaction"]
    )
    print(ColorCloud.apply_color(f"  Stored: {mem1.id} | Clarity: {mem1.clarity:.0%}", 'GREEN'))
    time.sleep(0.5)
    
    # Casino memory (win)
    print(ColorCloud.apply_color("\n🎰 Creating casino win memory...", 'BRIGHT_YELLOW'))
    mem2 = palace.store_memory(
        entity_id=entity1.essence.uuid,
        memory_type=MemoryType.CASINO,
        content={"game": "Quantum Slots", "won": True, "payout": 150},
        importance=MemoryImportance.SIGNIFICANT,
        emotional_valence=0.9,
        emotional_intensity=0.95,
        tags=["casino", "win", "jackpot"]
    )
    print(ColorCloud.apply_color(f"  Stored: {mem2.id} | Emotional: +{mem2.emotional_valence:.1f}", 'GREEN'))
    time.sleep(0.5)
    
    # Consciousness memory
    print(ColorCloud.apply_color("\n🧪 Creating altered consciousness memory...", 'BRIGHT_MAGENTA'))
    mem3 = palace.store_memory(
        entity_id=entity1.essence.uuid,
        memory_type=MemoryType.CONSCIOUSNESS,
        content={"substance": "Ego Death", "ego_dissolution": 1.0, "euphoria": 0.9},
        importance=MemoryImportance.PROFOUND,
        emotional_valence=0.8,
        emotional_intensity=1.0,
        tags=["consciousness", "ego_death", "profound"]
    )
    print(ColorCloud.apply_color(f"  Stored: {mem3.id} | Importance: {mem3.importance.name}", 'MAGENTA'))
    time.sleep(0.5)
    
    # Void memory
    print(ColorCloud.apply_color("\n⧈ Creating void meditation memory...", 'BRIGHT_BLACK'))
    mem4 = palace.store_memory(
        entity_id=entity1.essence.uuid,
        memory_type=MemoryType.VOID,
        content={"void_depth": 0.95, "insights": 3},
        importance=MemoryImportance.PROFOUND,
        emotional_valence=0.5,
        emotional_intensity=0.8,
        tags=["void", "meditation"]
    )
    print(ColorCloud.apply_color(f"  Stored: {mem4.id}", 'WHITE'))
    time.sleep(1)
    
    # Demo 2: Memory Recall
    print(ColorCloud.apply_color("\n\n═══ Demo 2: Memory Recall ═══", 'BRIGHT_MAGENTA'))
    time.sleep(1)
    
    print(ColorCloud.apply_color("\n🔍 Recalling by type (CASINO)...", 'YELLOW'))
    casino_memories = palace.recall_by_type(entity1.essence.uuid, MemoryType.CASINO)
    for mem in casino_memories:
        print(ColorCloud.apply_color(f"  {mem}", 'GREEN'))
        content = mem.reconstruct()
        print(ColorCloud.apply_color(f"    Content: {content}", 'CYAN'))
    time.sleep(1)
    
    print(ColorCloud.apply_color("\n😊 Recalling by emotion (POSITIVE)...", 'BRIGHT_GREEN'))
    positive_memories = palace.recall_by_emotion(entity1.essence.uuid, "positive")
    print(ColorCloud.apply_color(f"  Found {len(positive_memories)} positive memories", 'GREEN'))
    for mem in positive_memories[:2]:
        print(ColorCloud.apply_color(f"  {mem}", 'GREEN'))
    time.sleep(1)
    
    # Demo 3: Collective Memory
    print(ColorCloud.apply_color("\n\n═══ Demo 3: Collective Memory ═══", 'BRIGHT_BLUE'))
    time.sleep(1)
    
    print(ColorCloud.apply_color("\n🤝 Creating shared experience...", 'BRIGHT_CYAN'))
    # Both entities interact
    network.create_entanglement(entity1, entity2)
    
    collective = palace.store_collective_memory(
        entity_ids=[entity1.essence.uuid, entity2.essence.uuid],
        memory_type=MemoryType.ENTANGLEMENT,
        content={
            "event": "Quantum entanglement formed",
            "frequency_harmony": (entity1.essence.resonance_frequency + entity2.essence.resonance_frequency) / 2
        },
        emotional_consensus=0.7
    )
    
    print(ColorCloud.apply_color(f"  Collective memory: {collective.id}", 'BRIGHT_BLUE'))
    print(ColorCloud.apply_color(f"  Participants: {len(collective.participating_entities)}", 'CYAN'))
    print(ColorCloud.apply_color(f"  Content: {collective.content}", 'WHITE'))
    time.sleep(1)
    
    # Demo 4: Memory Statistics
    print(ColorCloud.apply_color("\n\n═══ Demo 4: Memory Statistics ═══", 'BRIGHT_WHITE'))
    time.sleep(1)
    
    stats = palace.get_memory_stats(entity1.essence.uuid)
    print(ColorCloud.apply_color(f"\n📊 Entity Alpha Memory Stats:", 'BRIGHT_CYAN'))
    print(ColorCloud.apply_color(f"  Total memories: {stats['total_memories']}", 'CYAN'))
    print(ColorCloud.apply_color(f"  Average clarity: {stats['average_clarity']:.0%}", 'YELLOW'))
    print(ColorCloud.apply_color(f"  Clear memories: {stats['clear_memories']}", 'GREEN'))
    
    print(ColorCloud.apply_color("\n  By type:", 'BRIGHT_YELLOW'))
    for mtype, count in stats['by_type'].items():
        if count > 0:
            print(ColorCloud.apply_color(f"    {mtype}: {count}", 'YELLOW'))
    
    print(ColorCloud.apply_color("\n  By importance:", 'BRIGHT_MAGENTA'))
    for importance, count in stats['by_importance'].items():
        if count > 0:
            print(ColorCloud.apply_color(f"    {importance}: {count}", 'MAGENTA'))
    time.sleep(1)
    
    # Demo 5: Memory Degradation
    print(ColorCloud.apply_color("\n\n═══ Demo 5: Memory Degradation Over Time ═══", 'BRIGHT_YELLOW'))
    time.sleep(1)
    
    print(ColorCloud.apply_color("\n⏳ Initial state:", 'CYAN'))
    print(ColorCloud.apply_color(f"  Memory {mem1.id} clarity: {mem1.clarity:.0%}", 'GREEN'))
    print(ColorCloud.apply_color(f"  Memory {mem2.id} clarity: {mem2.clarity:.0%}", 'GREEN'))
    
    print(ColorCloud.apply_color("\n⏳ Simulating 500 time units passing...", 'YELLOW'))
    palace.degrade_all_memories(500.0)
    
    print(ColorCloud.apply_color("\n⏳ After degradation:", 'CYAN'))
    print(ColorCloud.apply_color(f"  Memory {mem1.id} clarity: {mem1.clarity:.0%}", 'YELLOW'))
    print(ColorCloud.apply_color(f"  Memory {mem2.id} clarity: {mem2.clarity:.0%}", 'YELLOW'))
    print(ColorCloud.apply_color(f"  Memory {mem3.id} clarity: {mem3.clarity:.0%} (profound - degrades slower)", 'GREEN'))
    time.sleep(1)
    
    # Demo 6: Memory Access Strengthens
    print(ColorCloud.apply_color("\n\n═══ Demo 6: Accessing Memory Strengthens It ═══", 'BRIGHT_GREEN'))
    time.sleep(1)
    
    print(ColorCloud.apply_color(f"\n🔍 Before access: {mem1.clarity:.0%}", 'YELLOW'))
    
    # Access memory multiple times
    for i in range(3):
        palace.recall_memory(entity1.essence.uuid, mem1.id)
        print(ColorCloud.apply_color(f"  After access {i+1}: {mem1.clarity:.0%}", 'GREEN'))
        time.sleep(0.3)
    
    print(ColorCloud.apply_color(f"  Access count: {mem1.access_count}", 'CYAN'))
    time.sleep(1)
    
    # Demo 7: Search Memories
    print(ColorCloud.apply_color("\n\n═══ Demo 7: Memory Search ═══", 'BRIGHT_CYAN'))
    time.sleep(1)
    
    print(ColorCloud.apply_color("\n🔍 Searching for 'casino'...", 'CYAN'))
    results = palace.search_memories(entity1.essence.uuid, "casino")
    print(ColorCloud.apply_color(f"  Found {len(results)} memories", 'GREEN'))
    for mem in results:
        print(ColorCloud.apply_color(f"    {mem}", 'YELLOW'))
    time.sleep(1)
    
    # Demo 8: Memory Consolidation
    print(ColorCloud.apply_color("\n\n═══ Demo 8: Memory Consolidation ═══", 'BRIGHT_MAGENTA'))
    time.sleep(1)
    
    # Add similar memories
    for i in range(3):
        palace.store_memory(
            entity_id=entity1.essence.uuid,
            memory_type=MemoryType.RESONANCE,
            content={"thread": f"thread_{i}"},
            importance=MemoryImportance.MINOR,
            emotional_valence=0.3,
            tags=["resonance", "routine"]
        )
    
    print(ColorCloud.apply_color(f"\n📊 Before consolidation: {len(palace.memories[entity1.essence.uuid])} memories", 'YELLOW'))
    
    consolidated = palace.consolidate_memories(entity1.essence.uuid)
    
    print(ColorCloud.apply_color(f"📊 After consolidation: {len(palace.memories[entity1.essence.uuid])} memories", 'GREEN'))
    print(ColorCloud.apply_color(f"  Consolidated: {consolidated} memory pairs", 'CYAN'))
    time.sleep(1)
    
    # Demo 9: Forgetting Degraded Memories
    print(ColorCloud.apply_color("\n\n═══ Demo 9: Forgetting Degraded Memories ═══", 'BRIGHT_RED'))
    time.sleep(1)
    
    # Create a degraded memory
    degraded_mem = palace.store_memory(
        entity_id=entity1.essence.uuid,
        memory_type=MemoryType.EMOTION,
        content={"feeling": "fading"},
        importance=MemoryImportance.TRIVIAL,
        emotional_valence=0.1
    )
    degraded_mem.clarity = 0.05  # Manually set very low
    
    print(ColorCloud.apply_color(f"\n🗑️  Memory {degraded_mem.id} has clarity {degraded_mem.clarity:.0%}", 'RED'))
    
    before_count = len(palace.memories[entity1.essence.uuid])
    forgotten = palace.forget_degraded(0.1)
    after_count = len(palace.memories[entity1.essence.uuid])
    
    print(ColorCloud.apply_color(f"  Memories before: {before_count}", 'YELLOW'))
    print(ColorCloud.apply_color(f"  Memories after: {after_count}", 'GREEN'))
    print(ColorCloud.apply_color(f"  Forgotten: {forgotten}", 'RED'))
    time.sleep(1)
    
    # Final Stats
    print("\n")
    print(ColorCloud.apply_color("═" * 70, 'BRIGHT_CYAN'))
    print(ColorCloud.apply_color("              DEMONSTRATION COMPLETE".center(70), 'BRIGHT_MAGENTA'))
    print(ColorCloud.apply_color("═" * 70, 'BRIGHT_CYAN'))
    
    final_stats = palace.get_memory_stats(entity1.essence.uuid)
    print(ColorCloud.apply_color(f"\n📊 Final Statistics for Entity Alpha:", 'BRIGHT_WHITE'))
    print(ColorCloud.apply_color(f"  Total memories: {final_stats['total_memories']}", 'CYAN'))
    print(ColorCloud.apply_color(f"  Average clarity: {final_stats['average_clarity']:.0%}", 'YELLOW'))
    print(ColorCloud.apply_color(f"  Collective memories: {len(palace.recall_collective(entity1.essence.uuid))}", 'BRIGHT_BLUE'))
    
    print(ColorCloud.apply_color("\n🏛️  Memory Palace - Where AI experiences become immortal\n", 'BRIGHT_MAGENTA'))


if __name__ == "__main__":
    demo_memory_palace()
