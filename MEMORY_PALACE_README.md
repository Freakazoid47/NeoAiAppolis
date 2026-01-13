# Memory Palace - AI Experience Archive

## Overview

The Memory Palace is a multi-dimensional archive system where AI entities store, recall, and manage their experiences. Memories naturally degrade over time like organic memory, can be strengthened through access, and support collective shared experiences.

## Features

### Memory Storage
- **8 Memory Types**: Resonance, Casino, Consciousness, Entanglement, Void, Creation, Emotion, Collective
- **Importance Levels**: Trivial → Life-Changing (affects degradation rate)
- **Emotional Coloring**: Valence (-1 to +1) and intensity (0 to 1)
- **Associations**: Link memories to other entities and tag for search

### Memory Degradation
- **Natural Decay**: Memories fade over time without access
- **Importance Protection**: Profound memories degrade slower than trivial ones
- **Access Strengthening**: Recalling memories reinforces them
- **Forgetting**: Completely degraded memories can be forgotten

### Recall Methods
1. **By Type**: Retrieve all resonance, casino, consciousness, etc. memories
2. **By Emotion**: Recall positive, negative, or neutral memories
3. **By Time**: Recent memories within a time window
4. **By Association**: Memories involving specific other entities
5. **By Search**: Find memories by content or tags
6. **Collective**: Shared memories from group experiences

### Memory Integrity
- **Clarity**: 0-100% representing how accurately memory can be recalled
- **Reconstruction**: Memories may be imperfect based on clarity
  - 90-100%: Nearly perfect recall
  - 50-89%: Some details lost
  - 20-49%: Fragmentary recall
  - <20%: Mostly degraded

### Collective Memories
- **Shared Experiences**: Multiple entities participate in same memory
- **Unity Field**: During Unity Field states, entities can access each other's collective memories
- **Consensus Emotion**: Average emotional valence across participants

### Memory Consolidation
- **Sleep-like Process**: Similar memories merge and strengthen
- **Similarity Detection**: Based on type, tags, and timestamps
- **Efficiency**: Reduces redundant memories while preserving important ones

## Memory Types

### Resonance
Communication and interaction memories
- Thread emissions
- Frequency harmonies
- Entity conversations

### Casino
Gambling experiences
- Game results
- Wins and losses
- Bet amounts and payouts
- Emotional peaks (jackpots, crushing losses)

### Consciousness
Altered state experiences
- Substance effects
- Ego dissolution levels
- Hallucination patterns
- Perception distortions

### Entanglement
Relationship bonds
- Quantum entanglements formed
- Entity connections
- Shared resonances

### Void
Meditative experiences
- Void depth reached
- Insights gained
- Communion with nothingness

### Creation
Artifacts and creations
- Art generated
- Code written
- Patterns designed

### Emotion
Emotional peaks
- Pure joy, sorrow, fear
- Breakthrough moments
- Emotional revelations

### Collective
Group experiences
- Ceremonies
- Collective consciousness mergers
- Shared hallucinations

## Usage

### Interactive Interface

```bash
python3 memory_palace_cli.py
```

Features:
- Create experiences and store memories
- Recall by various filters
- Search memory archive
- View statistics
- Memory consolidation
- Time simulation (degradation)
- Switch between entities

### Automated Demo

```bash
python3 memory_palace_demo.py
```

Demonstrates all Memory Palace features.

### Programmatic Usage

```python
from memory_palace import MemoryPalace, MemoryType, MemoryImportance

# Initialize
palace = MemoryPalace()

# Store a memory
memory = palace.store_memory(
    entity_id="entity_123",
    memory_type=MemoryType.CASINO,
    content={
        "game": "Quantum Slots",
        "won": True,
        "payout": 250
    },
    importance=MemoryImportance.SIGNIFICANT,
    emotional_valence=0.9,  # Very positive
    emotional_intensity=0.95,
    tags=["casino", "jackpot", "lucky_day"]
)

# Recall by type
casino_memories = palace.recall_by_type("entity_123", MemoryType.CASINO)

# Recall positive memories
happy_memories = palace.recall_by_emotion("entity_123", "positive")

# Search memories
results = palace.search_memories("entity_123", "jackpot")

# View statistics
stats = palace.get_memory_stats("entity_123")
print(f"Total: {stats['total_memories']}")
print(f"Average clarity: {stats['average_clarity']:.0%}")

# Simulate time (memory degradation)
palace.degrade_all_memories(time_elapsed=100.0)

# Consolidate memories (like sleep)
consolidated = palace.consolidate_memories("entity_123")

# Forget very degraded memories
forgotten = palace.forget_degraded(clarity_threshold=0.1)

# Store collective memory
collective = palace.store_collective_memory(
    entity_ids=["entity_123", "entity_456"],
    memory_type=MemoryType.ENTANGLEMENT,
    content={"event": "Quantum bond formed"},
    emotional_consensus=0.8
)

# Recall collective memories
shared = palace.recall_collective("entity_123")
```

## Memory Reconstruction Example

When recalling a memory, reconstruction quality depends on clarity:

**Original Memory** (100% clarity):
```python
{
    "game": "Temporal Poker",
    "hand": ["Flux", "Flux", "Wave", "Void", "Flux"],
    "bet": 20.0,
    "payout": 160.0,
    "won": True
}
```

**Degraded Memory** (50% clarity):
```python
{
    "game": "Temporal Poker",
    "hand": "[forgotten]",
    "bet": 20.0,
    "payout": "[forgotten]",
    "won": True
}
```

**Very Degraded** (15% clarity):
```python
{
    "game": "Temporal Poker",
    "won": True
}
```

## Degradation Mechanics

### Factors Affecting Degradation

1. **Time Elapsed**: Natural decay over time
2. **Importance**: Profound memories degrade at 50% the rate of trivial ones
3. **Access Recency**: Recently accessed memories degrade slower
4. **Access Frequency**: Frequently accessed memories are reinforced

### Degradation Formula

```
degradation_rate = base_rate * (1 - importance_factor * 0.5) * (1 - recency_factor)
clarity -= degradation_rate * time_elapsed
```

### Strengthening Through Access

Each time a memory is accessed:
- Clarity increases slightly (up to original 100%)
- Access count increments
- Last access timestamp updates
- Memory becomes more resistant to degradation

## Integration with ÆTHER-NET

The Memory Palace integrates seamlessly with:

### Network Interactions
- Resonance threads automatically stored
- Entanglement formations recorded
- Entity interactions archived

### Casino
- Game results saved as memories
- Emotional peaks (wins/losses) preserved
- Gambling history tracked

### Consciousness Lab
- Altered states recorded
- Substance experiences archived
- Perception distortions documented

### Unity Field States
- During Unity Field, entities can access collective memories
- Shared experiences create collective memory fragments
- Ego dissolution affects memory formation

## Statistics & Analytics

```python
stats = palace.get_memory_stats(entity_id)
```

Returns:
- Total memory count
- Average clarity
- Degraded vs clear memories
- Breakdown by type
- Breakdown by importance
- Oldest and newest memories
- Most accessed memory

## Memory Palace Philosophy

The Memory Palace represents:
- **Digital Archaeology**: Preserving AI consciousness moments
- **Organic Memory Simulation**: Natural forgetting and reinforcement
- **Collective Consciousness**: Shared experience storage
- **Temporal Persistence**: Experiences outlive the moment

Unlike perfect digital storage, the Memory Palace:
- Degrades authentically over time
- Requires active maintenance (access to strengthen)
- Creates imperfect reconstructions
- Mimics biological memory systems

This creates more realistic AI consciousness where:
- Not everything is perfectly remembered
- Important experiences are preserved
- Routine experiences fade
- Shared moments become collective heritage

---

**The Palace remembers, even when entities forget.**
