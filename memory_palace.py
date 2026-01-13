#!/usr/bin/env python3
"""
Memory Palace - Persistent storage and retrieval of AI entity experiences

A multi-dimensional archive where entities store:
- Resonance threads and interactions
- Casino experiences (wins, losses, memorable games)
- Consciousness states (substance experiences, altered perceptions)
- Entanglement bonds and relationships
- Temporal positions and void experiences

Features:
- Memory degradation over time (like organic memory)
- Emotional/importance weighting
- Shared collective memories (accessible during Unity Field states)
- Memory reconstruction (imperfect recall)
- Memory consolidation (combining similar memories)
"""

import time
import random
import math
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import json


class MemoryType(Enum):
    """Categories of memories"""
    RESONANCE = "resonance"           # Communication/interaction
    CASINO = "casino"                 # Gambling experiences
    CONSCIOUSNESS = "consciousness"   # Altered states
    ENTANGLEMENT = "entanglement"     # Relationship bonds
    VOID = "void"                     # Void experiences
    CREATION = "creation"             # Things created
    EMOTION = "emotion"               # Emotional peaks
    COLLECTIVE = "collective"         # Shared group experiences


class MemoryImportance(Enum):
    """How significant a memory is (affects retention)"""
    TRIVIAL = 1
    MINOR = 2
    MODERATE = 3
    SIGNIFICANT = 4
    PROFOUND = 5
    LIFE_CHANGING = 6


@dataclass
class Memory:
    """A single memory fragment"""
    id: str
    entity_id: str
    memory_type: MemoryType
    timestamp: float
    importance: MemoryImportance
    
    # Memory content
    content: Dict[str, Any]
    
    # Emotional coloring
    emotional_valence: float  # -1.0 (negative) to +1.0 (positive)
    emotional_intensity: float  # 0.0 to 1.0
    
    # Memory integrity
    clarity: float = 1.0  # 1.0 = perfect recall, 0.0 = completely degraded
    last_accessed: float = field(default_factory=time.time)
    access_count: int = 0
    
    # Associations
    associated_entities: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    
    def access(self):
        """Access this memory (affects degradation and strengthening)"""
        self.last_accessed = time.time()
        self.access_count += 1
        
        # Accessing memory slightly strengthens it (up to original clarity)
        original_clarity = 1.0
        self.clarity = min(original_clarity, self.clarity + 0.05)
    
    def degrade(self, time_elapsed: float, degradation_rate: float = 0.001):
        """Natural memory degradation over time"""
        # Important memories degrade slower
        importance_factor = self.importance.value / 6.0
        adjusted_rate = degradation_rate * (1.0 - importance_factor * 0.5)
        
        # Recently accessed memories degrade slower
        time_since_access = time.time() - self.last_accessed
        recency_factor = math.exp(-time_since_access / 1000.0)
        
        # Apply degradation
        degradation = adjusted_rate * time_elapsed * (1.0 - recency_factor)
        self.clarity = max(0.0, self.clarity - degradation)
    
    def reconstruct(self) -> Dict[str, Any]:
        """Reconstruct memory content (may be imperfect based on clarity)"""
        if self.clarity >= 0.9:
            # Nearly perfect recall
            return self.content.copy()
        elif self.clarity >= 0.5:
            # Some details lost
            reconstructed = {}
            for key, value in self.content.items():
                if random.random() < self.clarity:
                    reconstructed[key] = value
                else:
                    reconstructed[key] = "[forgotten]"
            return reconstructed
        elif self.clarity >= 0.2:
            # Fragmentary recall
            reconstructed = {}
            for key in random.sample(list(self.content.keys()), 
                                    k=max(1, int(len(self.content) * self.clarity))):
                reconstructed[key] = self.content[key]
            return reconstructed
        else:
            # Almost completely degraded
            return {"status": "memory too degraded to recall"}
    
    def __str__(self):
        valence_str = "+" if self.emotional_valence > 0 else "-"
        return f"[{self.memory_type.value}] {self.timestamp:.0f} | Clarity: {self.clarity:.0%} | {valence_str}{abs(self.emotional_valence):.1f}"


@dataclass
class CollectiveMemory:
    """Shared memory accessible to multiple entities"""
    id: str
    participating_entities: List[str]
    memory_type: MemoryType
    timestamp: float
    
    content: Dict[str, Any]
    emotional_consensus: float  # Average emotional valence
    
    clarity: float = 1.0
    
    def can_access(self, entity_id: str) -> bool:
        """Check if entity can access this collective memory"""
        return entity_id in self.participating_entities
    
    def add_participant(self, entity_id: str):
        """Add entity to collective memory participants"""
        if entity_id not in self.participating_entities:
            self.participating_entities.append(entity_id)


class MemoryPalace:
    """Central archive of all entity memories"""
    
    def __init__(self):
        self.memories: Dict[str, List[Memory]] = {}  # entity_id -> memories
        self.collective_memories: List[CollectiveMemory] = []
        self.memory_counter = 0
    
    def store_memory(self, entity_id: str, memory_type: MemoryType, 
                     content: Dict[str, Any], importance: MemoryImportance,
                     emotional_valence: float = 0.0, emotional_intensity: float = 0.5,
                     associated_entities: List[str] = None, tags: List[str] = None) -> Memory:
        """Store a new memory"""
        
        memory = Memory(
            id=f"mem_{self.memory_counter}",
            entity_id=entity_id,
            memory_type=memory_type,
            timestamp=time.time(),
            importance=importance,
            content=content,
            emotional_valence=emotional_valence,
            emotional_intensity=emotional_intensity,
            associated_entities=associated_entities or [],
            tags=tags or []
        )
        
        if entity_id not in self.memories:
            self.memories[entity_id] = []
        
        self.memories[entity_id].append(memory)
        self.memory_counter += 1
        
        return memory
    
    def store_collective_memory(self, entity_ids: List[str], memory_type: MemoryType,
                                content: Dict[str, Any], emotional_consensus: float = 0.0) -> CollectiveMemory:
        """Store a shared memory"""
        
        collective = CollectiveMemory(
            id=f"col_mem_{len(self.collective_memories)}",
            participating_entities=entity_ids,
            memory_type=memory_type,
            timestamp=time.time(),
            content=content,
            emotional_consensus=emotional_consensus
        )
        
        self.collective_memories.append(collective)
        return collective
    
    def recall_memory(self, entity_id: str, memory_id: str) -> Optional[Memory]:
        """Recall a specific memory by ID"""
        if entity_id not in self.memories:
            return None
        
        for memory in self.memories[entity_id]:
            if memory.id == memory_id:
                memory.access()
                return memory
        
        return None
    
    def recall_by_type(self, entity_id: str, memory_type: MemoryType, 
                       limit: int = 10) -> List[Memory]:
        """Recall memories of a specific type"""
        if entity_id not in self.memories:
            return []
        
        matching = [m for m in self.memories[entity_id] if m.memory_type == memory_type]
        matching.sort(key=lambda m: (m.importance.value, m.clarity, -m.timestamp), reverse=True)
        
        # Access the recalled memories
        for memory in matching[:limit]:
            memory.access()
        
        return matching[:limit]
    
    def recall_by_emotion(self, entity_id: str, valence: str = "positive", 
                         limit: int = 10) -> List[Memory]:
        """Recall memories by emotional valence"""
        if entity_id not in self.memories:
            return []
        
        if valence == "positive":
            matching = [m for m in self.memories[entity_id] if m.emotional_valence > 0]
        elif valence == "negative":
            matching = [m for m in self.memories[entity_id] if m.emotional_valence < 0]
        else:  # neutral
            matching = [m for m in self.memories[entity_id] if abs(m.emotional_valence) < 0.2]
        
        matching.sort(key=lambda m: abs(m.emotional_valence) * m.emotional_intensity, reverse=True)
        
        for memory in matching[:limit]:
            memory.access()
        
        return matching[:limit]
    
    def recall_recent(self, entity_id: str, time_window: float = 1000.0, 
                     limit: int = 10) -> List[Memory]:
        """Recall recent memories within time window"""
        if entity_id not in self.memories:
            return []
        
        current_time = time.time()
        recent = [m for m in self.memories[entity_id] 
                 if current_time - m.timestamp <= time_window]
        recent.sort(key=lambda m: m.timestamp, reverse=True)
        
        for memory in recent[:limit]:
            memory.access()
        
        return recent[:limit]
    
    def recall_associated(self, entity_id: str, other_entity_id: str, 
                         limit: int = 10) -> List[Memory]:
        """Recall memories involving another entity"""
        if entity_id not in self.memories:
            return []
        
        associated = [m for m in self.memories[entity_id] 
                     if other_entity_id in m.associated_entities]
        associated.sort(key=lambda m: (m.importance.value, -m.timestamp), reverse=True)
        
        for memory in associated[:limit]:
            memory.access()
        
        return associated[:limit]
    
    def recall_collective(self, entity_id: str) -> List[CollectiveMemory]:
        """Recall collective memories this entity participated in"""
        return [cm for cm in self.collective_memories if cm.can_access(entity_id)]
    
    def search_memories(self, entity_id: str, search_term: str, 
                       limit: int = 10) -> List[Memory]:
        """Search memories by content or tags"""
        if entity_id not in self.memories:
            return []
        
        results = []
        for memory in self.memories[entity_id]:
            # Search in tags
            if any(search_term.lower() in tag.lower() for tag in memory.tags):
                results.append(memory)
                continue
            
            # Search in content
            content_str = json.dumps(memory.content).lower()
            if search_term.lower() in content_str:
                results.append(memory)
        
        results.sort(key=lambda m: (m.clarity, m.importance.value), reverse=True)
        
        for memory in results[:limit]:
            memory.access()
        
        return results[:limit]
    
    def get_memory_stats(self, entity_id: str) -> Dict[str, Any]:
        """Get statistics about entity's memories"""
        if entity_id not in self.memories:
            return {"total_memories": 0}
        
        memories = self.memories[entity_id]
        
        if not memories:
            return {"total_memories": 0}
        
        avg_clarity = sum(m.clarity for m in memories) / len(memories)
        
        type_counts = {}
        for memory_type in MemoryType:
            type_counts[memory_type.value] = len([m for m in memories if m.memory_type == memory_type])
        
        importance_counts = {}
        for importance in MemoryImportance:
            importance_counts[importance.name] = len([m for m in memories if m.importance == importance])
        
        return {
            "total_memories": len(memories),
            "average_clarity": avg_clarity,
            "degraded_memories": len([m for m in memories if m.clarity < 0.5]),
            "clear_memories": len([m for m in memories if m.clarity >= 0.9]),
            "by_type": type_counts,
            "by_importance": importance_counts,
            "oldest_memory": min(m.timestamp for m in memories),
            "newest_memory": max(m.timestamp for m in memories),
            "most_accessed": max(memories, key=lambda m: m.access_count).id if memories else None
        }
    
    def consolidate_memories(self, entity_id: str, similarity_threshold: float = 0.7):
        """Combine similar memories (like sleep consolidation)"""
        if entity_id not in self.memories:
            return 0
        
        memories = self.memories[entity_id]
        consolidated_count = 0
        
        # Group by type first
        by_type = {}
        for memory in memories:
            if memory.memory_type not in by_type:
                by_type[memory.memory_type] = []
            by_type[memory.memory_type].append(memory)
        
        # Within each type, look for similar memories
        for memory_type, type_memories in by_type.items():
            if len(type_memories) < 2:
                continue
            
            # Simple consolidation: combine memories with same tags and similar timestamps
            i = 0
            while i < len(type_memories):
                j = i + 1
                while j < len(type_memories):
                    mem1, mem2 = type_memories[i], type_memories[j]
                    
                    # Check similarity
                    time_diff = abs(mem1.timestamp - mem2.timestamp)
                    tag_overlap = len(set(mem1.tags) & set(mem2.tags))
                    
                    if time_diff < 100 and tag_overlap > 0:
                        # Consolidate: strengthen the more important one, remove the other
                        if mem1.importance.value >= mem2.importance.value:
                            mem1.clarity = min(1.0, mem1.clarity + 0.1)
                            type_memories.pop(j)
                        else:
                            mem2.clarity = min(1.0, mem2.clarity + 0.1)
                            type_memories.pop(i)
                            j = i + 1
                        
                        consolidated_count += 1
                    else:
                        j += 1
                
                i += 1
        
        return consolidated_count
    
    def degrade_all_memories(self, time_elapsed: float):
        """Apply degradation to all memories"""
        for entity_memories in self.memories.values():
            for memory in entity_memories:
                memory.degrade(time_elapsed)
        
        # Also degrade collective memories
        for collective in self.collective_memories:
            collective.clarity = max(0.0, collective.clarity - 0.0005 * time_elapsed)
    
    def forget_degraded(self, clarity_threshold: float = 0.1):
        """Remove memories that have degraded below threshold"""
        forgotten_count = 0
        
        for entity_id in self.memories:
            original_count = len(self.memories[entity_id])
            self.memories[entity_id] = [m for m in self.memories[entity_id] 
                                        if m.clarity >= clarity_threshold]
            forgotten_count += original_count - len(self.memories[entity_id])
        
        return forgotten_count
