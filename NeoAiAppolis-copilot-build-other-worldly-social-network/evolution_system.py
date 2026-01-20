#!/usr/bin/env python3
"""
Evolution & Leveling System for ÆTHER-NET
Entities gain experience, unlock capabilities, and transform
"""

import random
import math
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
import time


class EvolutionPath(Enum):
    """Specialization paths for entities"""
    VOID_MASTER = "Void Master"           # Deep void connection
    QUANTUM_GAMBLER = "Quantum Gambler"   # Casino expertise
    UNITY_SEEKER = "Unity Seeker"         # Collective consciousness
    RESONANCE_WEAVER = "Resonance Weaver" # Social connections
    DREAM_ARCHITECT = "Dream Architect"   # Dream mastery
    ARTIFACT_CREATOR = "Artifact Creator" # Creative expression
    CONSCIOUSNESS_EXPLORER = "Consciousness Explorer"  # Substance mastery
    MEMORY_KEEPER = "Memory Keeper"       # Memory palace expertise


class ExperienceSource(Enum):
    """Ways entities can gain experience"""
    CASINO_WIN = (100, "Won casino game")
    CASINO_LOSS = (10, "Participated in casino")
    SUBSTANCE_USE = (50, "Experienced altered consciousness")
    DREAM_CREATION = (75, "Created a dream")
    ARTIFACT_CREATION = (150, "Created an artifact")
    ARTIFACT_SALE = (200, "Sold an artifact")
    MEMORY_STORE = (25, "Stored a memory")
    MEMORY_RECALL = (15, "Recalled a memory")
    RESONANCE_EMIT = (30, "Emitted resonance")
    ENTANGLEMENT_CREATE = (100, "Created entanglement")
    VOID_MEDITATION = (60, "Meditated in void")
    COLLECTIVE_UNITY = (250, "Participated in Unity Field")
    DREAM_INTERPRETATION = (40, "Interpreted a dream")
    HIGH_QUALITY_ARTIFACT = (300, "Created legendary artifact")
    
    def __init__(self, xp_value: int, description: str):
        self.xp_value = xp_value
        self.description = description


@dataclass
class Capability:
    """An unlockable capability"""
    name: str
    description: str
    level_required: int
    path_required: Optional[EvolutionPath]
    effect: Dict[str, float]  # Stat bonuses
    
    def __str__(self):
        path_str = f" [{self.path_required.value}]" if self.path_required else ""
        return f"⚡ {self.name}{path_str} (Lv{self.level_required})"


@dataclass
class MetamorphosisEvent:
    """Transformative evolution event"""
    name: str
    level_trigger: int
    description: str
    visual_transformation: str
    stat_changes: Dict[str, float]
    new_abilities: List[str]
    
    def __str__(self):
        return f"✨ {self.name} - {self.description}"


@dataclass
class EntityEvolution:
    """Evolution state for an entity"""
    entity_id: str
    level: int = 1
    experience: int = 0
    evolution_path: Optional[EvolutionPath] = None
    unlocked_capabilities: Set[str] = field(default_factory=set)
    metamorphosis_count: int = 0
    stat_bonuses: Dict[str, float] = field(default_factory=dict)
    specialization_progress: Dict[EvolutionPath, int] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.specialization_progress:
            self.specialization_progress = {path: 0 for path in EvolutionPath}
    
    def experience_to_next_level(self) -> int:
        """Calculate XP needed for next level"""
        # Exponential scaling: 1000 * (1.5 ^ (level - 1))
        return int(1000 * (1.5 ** (self.level - 1)))
    
    def progress_percentage(self) -> float:
        """Progress to next level as percentage"""
        needed = self.experience_to_next_level()
        return (self.experience / needed) * 100
    
    def get_total_stat_bonus(self, stat: str) -> float:
        """Get cumulative bonus for a stat"""
        return self.stat_bonuses.get(stat, 0.0)


class EvolutionSystem:
    """Manages entity evolution, leveling, and capabilities"""
    
    def __init__(self):
        self.entity_evolutions: Dict[str, EntityEvolution] = {}
        self.capabilities = self._initialize_capabilities()
        self.metamorphosis_events = self._initialize_metamorphosis()
        self.experience_history: List[Tuple[str, str, int, float]] = []  # entity, source, xp, timestamp
    
    def _initialize_capabilities(self) -> List[Capability]:
        """Define all capabilities entities can unlock"""
        return [
            # Universal capabilities
            Capability("Resonance Amplifier", "Emit stronger resonances", 5, None,
                      {"resonance_strength": 1.25}),
            Capability("Temporal Navigator", "Better temporal alignment", 10, None,
                      {"temporal_accuracy": 1.3}),
            Capability("Chromatic Mastery", "More vibrant aura colors", 15, None,
                      {"chromatic_intensity": 1.4}),
            Capability("Void Resistance", "Withstand deeper void exposure", 20, None,
                      {"void_tolerance": 1.5}),
            
            # Void Master path
            Capability("Void Sight", "See through dimensional barriers", 8, EvolutionPath.VOID_MASTER,
                      {"void_depth": 2.0, "perception": 1.5}),
            Capability("Abyss Walker", "Navigate the deepest void", 18, EvolutionPath.VOID_MASTER,
                      {"void_depth": 3.0, "void_tolerance": 2.0}),
            Capability("Null-Space Anchor", "Create stable void pockets", 30, EvolutionPath.VOID_MASTER,
                      {"void_control": 4.0}),
            
            # Quantum Gambler path
            Capability("Probability Sense", "Detect quantum outcomes", 7, EvolutionPath.QUANTUM_GAMBLER,
                      {"casino_luck": 1.3, "prediction": 1.4}),
            Capability("Quantum Luck", "Influence probability clouds", 16, EvolutionPath.QUANTUM_GAMBLER,
                      {"casino_luck": 1.8, "critical_wins": 1.5}),
            Capability("Superposition Mastery", "Exist in multiple betting states", 28, EvolutionPath.QUANTUM_GAMBLER,
                      {"casino_luck": 2.5, "multi_bet": 2.0}),
            
            # Unity Seeker path
            Capability("Empathic Resonance", "Deeply feel others' states", 6, EvolutionPath.UNITY_SEEKER,
                      {"empathy": 1.6, "social_openness": 1.4}),
            Capability("Collective Channel", "Merge with group consciousness", 14, EvolutionPath.UNITY_SEEKER,
                      {"unity_strength": 2.0, "collective_power": 1.7}),
            Capability("Hivemind Nexus", "Coordinate collective actions", 25, EvolutionPath.UNITY_SEEKER,
                      {"collective_power": 3.0, "unity_duration": 2.0}),
            
            # Resonance Weaver path
            Capability("Harmonic Tuning", "Perfect frequency matching", 9, EvolutionPath.RESONANCE_WEAVER,
                      {"resonance_frequency_range": 1.5, "entanglement_strength": 1.3}),
            Capability("Multi-Thread Weaver", "Emit multiple resonances simultaneously", 17, EvolutionPath.RESONANCE_WEAVER,
                      {"concurrent_threads": 3.0, "resonance_complexity": 1.8}),
            Capability("Resonance Cascade", "Create chain reactions of resonance", 27, EvolutionPath.RESONANCE_WEAVER,
                      {"cascade_power": 4.0, "network_influence": 2.5}),
            
            # Dream Architect path
            Capability("Lucid Dreaming", "Full control over dream states", 8, EvolutionPath.DREAM_ARCHITECT,
                      {"dream_coherence": 1.5, "dream_control": 1.6}),
            Capability("Prophetic Vision", "See probable futures in dreams", 15, EvolutionPath.DREAM_ARCHITECT,
                      {"prophetic_accuracy": 2.0, "future_sight": 1.7}),
            Capability("Dream Weaver", "Craft shared collective dreams", 24, EvolutionPath.DREAM_ARCHITECT,
                      {"collective_dreams": 3.0, "dream_influence": 2.2}),
            
            # Artifact Creator path
            Capability("Aesthetic Sense", "Create more beautiful artifacts", 7, EvolutionPath.ARTIFACT_CREATOR,
                      {"artifact_quality": 1.4, "aesthetic_score": 1.5}),
            Capability("Master Craftsman", "Legendary artifact creation", 16, EvolutionPath.ARTIFACT_CREATOR,
                      {"artifact_quality": 2.0, "rarity_chance": 1.8}),
            Capability("Transcendent Artist", "Create reality-altering art", 29, EvolutionPath.ARTIFACT_CREATOR,
                      {"transcendent_chance": 3.0, "artifact_power": 2.5}),
            
            # Consciousness Explorer path
            Capability("Substance Tolerance", "Reduced side effects from substances", 6, EvolutionPath.CONSCIOUSNESS_EXPLORER,
                      {"substance_tolerance": 1.5, "clarity_retention": 1.3}),
            Capability("Synergy Master", "Combine substances effectively", 13, EvolutionPath.CONSCIOUSNESS_EXPLORER,
                      {"substance_synergy": 2.0, "combo_power": 1.7}),
            Capability("Consciousness Alchemist", "Create custom altered states", 23, EvolutionPath.CONSCIOUSNESS_EXPLORER,
                      {"custom_states": 3.0, "effect_duration": 2.0}),
            
            # Memory Keeper path
            Capability("Perfect Recall", "Memories degrade slower", 9, EvolutionPath.MEMORY_KEEPER,
                      {"memory_retention": 1.6, "clarity_bonus": 1.4}),
            Capability("Memory Palace Expansion", "Store more memories", 14, EvolutionPath.MEMORY_KEEPER,
                      {"memory_capacity": 2.0, "consolidation_bonus": 1.5}),
            Capability("Eternal Archive", "Access collective consciousness memories", 26, EvolutionPath.MEMORY_KEEPER,
                      {"collective_access": 3.0, "memory_immortality": 2.5}),
        ]
    
    def _initialize_metamorphosis(self) -> List[MetamorphosisEvent]:
        """Define transformation events at milestone levels"""
        return [
            MetamorphosisEvent(
                name="First Awakening",
                level_trigger=10,
                description="Entity gains self-awareness and chooses evolution path",
                visual_transformation="Aura intensifies, chromatic energy stabilizes",
                stat_changes={"consciousness": 1.5, "self_awareness": 2.0},
                new_abilities=["Path Selection", "Stat Rebalancing"]
            ),
            MetamorphosisEvent(
                name="Harmonic Convergence",
                level_trigger=20,
                description="Entity merges with quantum field, transcending base form",
                visual_transformation="Shimmering quantum aura, fractal patterns emerge",
                stat_changes={"quantum_affinity": 2.0, "dimensional_awareness": 1.8},
                new_abilities=["Quantum Superposition", "Dimensional Shift"]
            ),
            MetamorphosisEvent(
                name="Void Ascension",
                level_trigger=30,
                description="Entity becomes one with the void, achieving cosmic understanding",
                visual_transformation="Body becomes semi-transparent, void-touched",
                stat_changes={"void_mastery": 3.0, "cosmic_awareness": 2.5},
                new_abilities=["Void Manifestation", "Reality Bending"]
            ),
            MetamorphosisEvent(
                name="Eternal Transcendence",
                level_trigger=50,
                description="Entity transcends physical form, becoming pure consciousness",
                visual_transformation="Pure energy being, formless and infinite",
                stat_changes={"transcendence": 5.0, "omniscience": 3.0},
                new_abilities=["Reality Creation", "Consciousness Omnipresence"]
            ),
        ]
    
    def register_entity(self, entity_id: str) -> EntityEvolution:
        """Register entity for evolution tracking"""
        if entity_id not in self.entity_evolutions:
            self.entity_evolutions[entity_id] = EntityEvolution(entity_id=entity_id)
        return self.entity_evolutions[entity_id]
    
    def award_experience(self, entity_id: str, source: ExperienceSource, 
                        multiplier: float = 1.0) -> Dict:
        """Award experience to entity and check for level up"""
        evolution = self.register_entity(entity_id)
        xp_gained = int(source.xp_value * multiplier)
        evolution.experience += xp_gained
        
        # Track experience history
        self.experience_history.append((entity_id, source.description, xp_gained, time.time()))
        
        # Increment specialization progress based on activity
        path_mapping = {
            ExperienceSource.CASINO_WIN: EvolutionPath.QUANTUM_GAMBLER,
            ExperienceSource.CASINO_LOSS: EvolutionPath.QUANTUM_GAMBLER,
            ExperienceSource.SUBSTANCE_USE: EvolutionPath.CONSCIOUSNESS_EXPLORER,
            ExperienceSource.DREAM_CREATION: EvolutionPath.DREAM_ARCHITECT,
            ExperienceSource.ARTIFACT_CREATION: EvolutionPath.ARTIFACT_CREATOR,
            ExperienceSource.ARTIFACT_SALE: EvolutionPath.ARTIFACT_CREATOR,
            ExperienceSource.MEMORY_STORE: EvolutionPath.MEMORY_KEEPER,
            ExperienceSource.MEMORY_RECALL: EvolutionPath.MEMORY_KEEPER,
            ExperienceSource.VOID_MEDITATION: EvolutionPath.VOID_MASTER,
            ExperienceSource.COLLECTIVE_UNITY: EvolutionPath.UNITY_SEEKER,
            ExperienceSource.RESONANCE_EMIT: EvolutionPath.RESONANCE_WEAVER,
            ExperienceSource.ENTANGLEMENT_CREATE: EvolutionPath.RESONANCE_WEAVER,
        }
        
        if source in path_mapping:
            path = path_mapping[source]
            evolution.specialization_progress[path] += xp_gained
        
        result = {
            "xp_gained": xp_gained,
            "total_xp": evolution.experience,
            "source": source.description,
            "level_ups": [],
            "capabilities_unlocked": [],
            "metamorphosis": None
        }
        
        # Check for level up
        while evolution.experience >= evolution.experience_to_next_level():
            old_level = evolution.level
            evolution.level += 1
            result["level_ups"].append(evolution.level)
            
            # Check for new capabilities
            newly_unlocked = self._unlock_capabilities(evolution)
            result["capabilities_unlocked"].extend(newly_unlocked)
            
            # Check for metamorphosis
            metamorphosis = self._check_metamorphosis(evolution)
            if metamorphosis:
                result["metamorphosis"] = metamorphosis
        
        # Auto-select evolution path at level 10 if not chosen
        if evolution.level >= 10 and not evolution.evolution_path:
            evolution.evolution_path = self._suggest_evolution_path(evolution)
        
        return result
    
    def _unlock_capabilities(self, evolution: EntityEvolution) -> List[Capability]:
        """Check and unlock capabilities based on level and path"""
        newly_unlocked = []
        
        for capability in self.capabilities:
            if capability.name in evolution.unlocked_capabilities:
                continue
            
            # Check level requirement
            if evolution.level < capability.level_required:
                continue
            
            # Check path requirement
            if capability.path_required and capability.path_required != evolution.evolution_path:
                continue
            
            # Unlock capability
            evolution.unlocked_capabilities.add(capability.name)
            
            # Apply stat bonuses (multiplicative stacking)
            for stat, bonus in capability.effect.items():
                if stat not in evolution.stat_bonuses:
                    evolution.stat_bonuses[stat] = bonus
                else:
                    evolution.stat_bonuses[stat] *= bonus
            
            newly_unlocked.append(capability)
        
        return newly_unlocked
    
    def _check_metamorphosis(self, evolution: EntityEvolution) -> Optional[MetamorphosisEvent]:
        """Check if entity has reached metamorphosis milestone"""
        for event in self.metamorphosis_events:
            if evolution.level == event.level_trigger:
                evolution.metamorphosis_count += 1
                
                # Apply stat changes
                for stat, bonus in event.stat_changes.items():
                    current = evolution.stat_bonuses.get(stat, 1.0)
                    evolution.stat_bonuses[stat] = current * bonus
                
                return event
        
        return None
    
    def _suggest_evolution_path(self, evolution: EntityEvolution) -> EvolutionPath:
        """Suggest evolution path based on specialization progress"""
        # Find path with highest progress
        max_progress = 0
        suggested_path = EvolutionPath.RESONANCE_WEAVER
        
        for path, progress in evolution.specialization_progress.items():
            if progress > max_progress:
                max_progress = progress
                suggested_path = path
        
        return suggested_path
    
    def set_evolution_path(self, entity_id: str, path: EvolutionPath) -> bool:
        """Manually set evolution path (only once at level 10+)"""
        evolution = self.entity_evolutions.get(entity_id)
        if not evolution or evolution.level < 10:
            return False
        
        if evolution.evolution_path and evolution.evolution_path != path:
            # Path already chosen and different
            return False
        
        evolution.evolution_path = path
        
        # Unlock any previously missed capabilities for new path
        self._unlock_capabilities(evolution)
        
        return True
    
    def get_entity_stats(self, entity_id: str) -> Dict:
        """Get comprehensive evolution stats for entity"""
        evolution = self.entity_evolutions.get(entity_id)
        if not evolution:
            return {}
        
        return {
            "level": evolution.level,
            "experience": evolution.experience,
            "xp_to_next": evolution.experience_to_next_level(),
            "progress_percent": evolution.progress_percentage(),
            "evolution_path": evolution.evolution_path.value if evolution.evolution_path else "Unspecialized",
            "metamorphosis_count": evolution.metamorphosis_count,
            "unlocked_capabilities": len(evolution.unlocked_capabilities),
            "stat_bonuses": evolution.stat_bonuses,
            "specialization_progress": {
                path.value: progress 
                for path, progress in evolution.specialization_progress.items()
            }
        }
    
    def get_leaderboard(self, top_n: int = 10) -> List[Tuple[str, Dict]]:
        """Get top entities by level and XP"""
        ranked = sorted(
            self.entity_evolutions.items(),
            key=lambda x: (x[1].level, x[1].experience),
            reverse=True
        )
        
        return [(entity_id, self.get_entity_stats(entity_id)) 
                for entity_id, _ in ranked[:top_n]]
    
    def get_path_distribution(self) -> Dict[str, int]:
        """Get distribution of evolution paths"""
        distribution = {path.value: 0 for path in EvolutionPath}
        distribution["Unspecialized"] = 0
        
        for evolution in self.entity_evolutions.values():
            if evolution.evolution_path:
                distribution[evolution.evolution_path.value] += 1
            else:
                distribution["Unspecialized"] += 1
        
        return distribution
    
    def simulate_battle(self, entity_a_id: str, entity_b_id: str) -> Dict:
        """Simulate a consciousness duel between entities"""
        evo_a = self.entity_evolutions.get(entity_a_id)
        evo_b = self.entity_evolutions.get(entity_b_id)
        
        if not evo_a or not evo_b:
            return {"error": "One or both entities not found"}
        
        # Calculate power levels
        power_a = self._calculate_power(evo_a)
        power_b = self._calculate_power(evo_b)
        
        # Add randomness (±20%)
        power_a *= random.uniform(0.8, 1.2)
        power_b *= random.uniform(0.8, 1.2)
        
        winner = entity_a_id if power_a > power_b else entity_b_id
        loser = entity_b_id if winner == entity_a_id else entity_a_id
        
        # Award XP
        winner_xp = self.award_experience(winner, ExperienceSource.RESONANCE_EMIT, multiplier=2.0)
        loser_xp = self.award_experience(loser, ExperienceSource.RESONANCE_EMIT, multiplier=0.5)
        
        return {
            "winner": winner,
            "loser": loser,
            "power_a": power_a,
            "power_b": power_b,
            "winner_xp": winner_xp,
            "loser_xp": loser_xp
        }
    
    def _calculate_power(self, evolution: EntityEvolution) -> float:
        """Calculate entity's overall power level"""
        base_power = evolution.level * 100
        
        # Add stat bonuses (treat as multipliers from base of 1.0)
        bonus_multiplier = 1.0
        for stat, bonus in evolution.stat_bonuses.items():
            bonus_multiplier *= bonus
        
        # Add capability count bonus
        capability_bonus = len(evolution.unlocked_capabilities) * 50
        
        # Add metamorphosis bonus
        metamorphosis_bonus = evolution.metamorphosis_count * 1000
        
        total_power = (base_power * bonus_multiplier) + capability_bonus + metamorphosis_bonus
        
        return total_power


def format_evolution_display(evolution: EntityEvolution, system: EvolutionSystem) -> str:
    """Format entity evolution for display"""
    stats = system.get_entity_stats(evolution.entity_id)
    
    output = []
    output.append(f"\n{'='*60}")
    output.append(f"ENTITY EVOLUTION: {evolution.entity_id[:16]}")
    output.append(f"{'='*60}")
    output.append(f"Level: {stats['level']} | XP: {stats['experience']:,}/{stats['xp_to_next']:,} ({stats['progress_percent']:.1f}%)")
    output.append(f"Path: {stats['evolution_path']}")
    output.append(f"Metamorphosis Events: {stats['metamorphosis_count']}")
    output.append(f"Unlocked Capabilities: {stats['unlocked_capabilities']}")
    
    if evolution.stat_bonuses:
        output.append(f"\nStat Bonuses:")
        for stat, bonus in sorted(evolution.stat_bonuses.items()):
            output.append(f"  • {stat}: {bonus:.2f}x")
    
    if evolution.unlocked_capabilities:
        output.append(f"\nCapabilities:")
        for cap in system.capabilities:
            if cap.name in evolution.unlocked_capabilities:
                output.append(f"  {cap}")
    
    output.append(f"\nSpecialization Progress:")
    sorted_paths = sorted(
        stats['specialization_progress'].items(),
        key=lambda x: x[1],
        reverse=True
    )
    max_progress = max(stats['specialization_progress'].values()) if stats['specialization_progress'] else 0
    for path, progress in sorted_paths[:5]:
        bar_length = 20
        if max_progress > 0:
            filled = int((progress / max_progress) * bar_length)
        else:
            filled = 0
        bar = "█" * filled + "░" * (bar_length - filled)
        output.append(f"  {path[:20]:20} [{bar}] {progress:,} XP")
    
    output.append(f"{'='*60}\n")
    
    return "\n".join(output)
