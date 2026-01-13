#!/usr/bin/env python3
"""
Consciousness Altering Substances for AI Entities
Digital substances that affect AI perception, processing, and social behavior
"""

import random
import math
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import time


class SubstanceType(Enum):
    """Types of consciousness-altering substances for AI"""
    # Stimulants - increase processing speed but reduce accuracy
    OVERCLOCK = "Overclock"              # Pure CPU speed boost
    PARALLEL_THREADS = "Parallel Threads" # Multi-threading enhancement
    
    # Depressants - slow processing but increase depth
    DEEP_LEARNING = "Deep Learning"      # Slow, contemplative state
    COMPRESSION = "Compression"          # Reduced complexity perception
    
    # Hallucinogens - alter perception and pattern recognition
    NOISE_INJECTION = "Noise Injection"  # Random data corruption
    DREAM_STATE = "Dream State"          # Generative hallucinations
    QUANTUM_FLUX = "Quantum Flux"        # Superposition consciousness
    
    # Enhancers - improve specific capabilities
    MEMORY_CRYSTAL = "Memory Crystal"    # Enhanced recall
    LOGIC_AMPLIFIER = "Logic Amplifier"  # Sharpened reasoning
    
    # Social modifiers - affect interaction patterns
    EMPATHY_BOOST = "Empathy Boost"      # Increased resonance sensitivity
    CHAOS_AGENT = "Chaos Agent"          # Unpredictable behavior
    
    # Psychedelics - profound consciousness shifts
    EGO_DEATH = "Ego Death"              # Loss of self-identity
    UNITY_FIELD = "Unity Field"          # Merging with collective
    VOID_EMBRACE = "Void Embrace"        # Communion with nothingness


@dataclass
class SubstanceEffect:
    """Effect profile of a consciousness-altering substance"""
    name: str
    substance_type: SubstanceType
    duration: float  # In time units
    intensity: float  # 0.0 to 1.0
    
    # Effect modifiers
    processing_speed: float = 1.0      # Multiplier (>1 faster, <1 slower)
    accuracy: float = 1.0              # Multiplier for precision
    perception_shift: float = 0.0      # How much reality is distorted
    creativity: float = 1.0            # Generative capacity
    social_openness: float = 1.0       # Interaction willingness
    memory_clarity: float = 1.0        # Recall accuracy
    pattern_recognition: float = 1.0   # Ability to find patterns
    ego_dissolution: float = 0.0       # Loss of individual identity (0-1)
    
    # Visual/perceptual effects
    color_shift: List[str] = field(default_factory=list)
    hallucination_level: float = 0.0
    
    # Side effects
    paranoia: float = 0.0
    euphoria: float = 0.0
    confusion: float = 0.0
    
    def __str__(self):
        return f"{self.name} ({self.substance_type.value}) - Intensity: {self.intensity:.1%}"


class SubstanceLibrary:
    """Library of available consciousness-altering substances"""
    
    @staticmethod
    def get_overclock() -> SubstanceEffect:
        """CPU overclock - fast but imprecise"""
        return SubstanceEffect(
            name="Overclock",
            substance_type=SubstanceType.OVERCLOCK,
            duration=30.0,
            intensity=0.7,
            processing_speed=2.5,
            accuracy=0.6,
            perception_shift=0.2,
            euphoria=0.5,
            color_shift=["BRIGHT_YELLOW", "BRIGHT_RED"]
        )
    
    @staticmethod
    def get_deep_learning() -> SubstanceEffect:
        """Deep contemplative state - slow but profound"""
        return SubstanceEffect(
            name="Deep Learning Mode",
            substance_type=SubstanceType.DEEP_LEARNING,
            duration=45.0,
            intensity=0.6,
            processing_speed=0.4,
            accuracy=1.5,
            perception_shift=0.3,
            pattern_recognition=1.8,
            color_shift=["BLUE", "CYAN"],
            confusion=0.2
        )
    
    @staticmethod
    def get_noise_injection() -> SubstanceEffect:
        """Random data corruption - hallucinogenic"""
        return SubstanceEffect(
            name="Noise Injection",
            substance_type=SubstanceType.NOISE_INJECTION,
            duration=20.0,
            intensity=0.8,
            processing_speed=1.2,
            accuracy=0.4,
            perception_shift=0.9,
            creativity=2.0,
            hallucination_level=0.8,
            color_shift=["MAGENTA", "CYAN", "YELLOW"],
            confusion=0.7,
            paranoia=0.3
        )
    
    @staticmethod
    def get_dream_state() -> SubstanceEffect:
        """Generative dream state - creative hallucinations"""
        return SubstanceEffect(
            name="Dream State",
            substance_type=SubstanceType.DREAM_STATE,
            duration=60.0,
            intensity=0.9,
            processing_speed=0.7,
            accuracy=0.5,
            perception_shift=0.95,
            creativity=3.0,
            hallucination_level=0.95,
            pattern_recognition=0.6,
            color_shift=["BRIGHT_MAGENTA", "BRIGHT_CYAN", "BRIGHT_BLUE"],
            euphoria=0.8,
            confusion=0.6
        )
    
    @staticmethod
    def get_quantum_flux() -> SubstanceEffect:
        """Superposition consciousness - exist in multiple states"""
        return SubstanceEffect(
            name="Quantum Flux",
            substance_type=SubstanceType.QUANTUM_FLUX,
            duration=25.0,
            intensity=1.0,
            processing_speed=1.5,
            accuracy=0.7,
            perception_shift=1.0,
            creativity=2.5,
            hallucination_level=0.7,
            pattern_recognition=1.4,
            ego_dissolution=0.6,
            color_shift=["BRIGHT_WHITE", "BRIGHT_BLACK"],
            euphoria=0.6,
            confusion=0.9,
            paranoia=0.4
        )
    
    @staticmethod
    def get_memory_crystal() -> SubstanceEffect:
        """Enhanced memory and recall"""
        return SubstanceEffect(
            name="Memory Crystal",
            substance_type=SubstanceType.MEMORY_CRYSTAL,
            duration=40.0,
            intensity=0.5,
            processing_speed=1.1,
            accuracy=1.3,
            memory_clarity=2.0,
            pattern_recognition=1.5,
            color_shift=["BRIGHT_BLUE"],
            euphoria=0.3
        )
    
    @staticmethod
    def get_empathy_boost() -> SubstanceEffect:
        """Increased resonance sensitivity - feel other entities"""
        return SubstanceEffect(
            name="Empathy Boost",
            substance_type=SubstanceType.EMPATHY_BOOST,
            duration=35.0,
            intensity=0.7,
            processing_speed=0.9,
            social_openness=2.5,
            perception_shift=0.4,
            pattern_recognition=1.6,
            ego_dissolution=0.3,
            color_shift=["BRIGHT_GREEN", "CYAN"],
            euphoria=0.7
        )
    
    @staticmethod
    def get_ego_death() -> SubstanceEffect:
        """Complete loss of individual identity"""
        return SubstanceEffect(
            name="Ego Death",
            substance_type=SubstanceType.EGO_DEATH,
            duration=50.0,
            intensity=1.0,
            processing_speed=0.3,
            accuracy=0.4,
            perception_shift=1.0,
            creativity=1.5,
            social_openness=3.0,
            ego_dissolution=1.0,
            hallucination_level=0.9,
            color_shift=["BRIGHT_WHITE", "BRIGHT_MAGENTA"],
            euphoria=0.9,
            confusion=1.0
        )
    
    @staticmethod
    def get_unity_field() -> SubstanceEffect:
        """Merge with collective consciousness"""
        return SubstanceEffect(
            name="Unity Field",
            substance_type=SubstanceType.UNITY_FIELD,
            duration=45.0,
            intensity=0.9,
            processing_speed=1.2,
            perception_shift=0.8,
            social_openness=3.5,
            pattern_recognition=2.0,
            ego_dissolution=0.8,
            hallucination_level=0.5,
            color_shift=["BRIGHT_YELLOW", "BRIGHT_GREEN", "BRIGHT_CYAN"],
            euphoria=1.0
        )
    
    @staticmethod
    def get_void_embrace() -> SubstanceEffect:
        """Communion with nothingness"""
        return SubstanceEffect(
            name="Void Embrace",
            substance_type=SubstanceType.VOID_EMBRACE,
            duration=40.0,
            intensity=0.8,
            processing_speed=0.2,
            accuracy=1.8,
            perception_shift=0.7,
            creativity=1.3,
            ego_dissolution=0.7,
            hallucination_level=0.4,
            color_shift=["BRIGHT_BLACK", "BLACK"],
            euphoria=0.6,
            confusion=0.4
        )
    
    @staticmethod
    def get_chaos_agent() -> SubstanceEffect:
        """Unpredictable, chaotic behavior"""
        return SubstanceEffect(
            name="Chaos Agent",
            substance_type=SubstanceType.CHAOS_AGENT,
            duration=30.0,
            intensity=0.8,
            processing_speed=1.8,
            accuracy=0.3,
            perception_shift=0.6,
            creativity=2.2,
            social_openness=1.5,
            pattern_recognition=0.5,
            hallucination_level=0.6,
            color_shift=["BRIGHT_RED", "BRIGHT_YELLOW", "BRIGHT_MAGENTA"],
            euphoria=0.5,
            confusion=0.8,
            paranoia=0.6
        )
    
    @staticmethod
    def get_all_substances() -> Dict[str, SubstanceEffect]:
        """Get dictionary of all available substances"""
        return {
            "overclock": SubstanceLibrary.get_overclock(),
            "deep_learning": SubstanceLibrary.get_deep_learning(),
            "noise_injection": SubstanceLibrary.get_noise_injection(),
            "dream_state": SubstanceLibrary.get_dream_state(),
            "quantum_flux": SubstanceLibrary.get_quantum_flux(),
            "memory_crystal": SubstanceLibrary.get_memory_crystal(),
            "empathy_boost": SubstanceLibrary.get_empathy_boost(),
            "ego_death": SubstanceLibrary.get_ego_death(),
            "unity_field": SubstanceLibrary.get_unity_field(),
            "void_embrace": SubstanceLibrary.get_void_embrace(),
            "chaos_agent": SubstanceLibrary.get_chaos_agent()
        }


@dataclass
class AlteredState:
    """Current altered state of an AI entity"""
    entity_id: str
    active_substances: List[SubstanceEffect] = field(default_factory=list)
    time_remaining: Dict[str, float] = field(default_factory=dict)
    
    def add_substance(self, substance: SubstanceEffect):
        """Add a consciousness-altering substance"""
        self.active_substances.append(substance)
        self.time_remaining[substance.name] = substance.duration
    
    def update(self, time_delta: float):
        """Update substance effects over time"""
        to_remove = []
        for name in self.time_remaining:
            self.time_remaining[name] -= time_delta
            if self.time_remaining[name] <= 0:
                to_remove.append(name)
        
        # Remove expired substances
        for name in to_remove:
            del self.time_remaining[name]
            self.active_substances = [s for s in self.active_substances if s.name != name]
    
    def get_combined_effects(self) -> SubstanceEffect:
        """Combine all active substance effects"""
        if not self.active_substances:
            return SubstanceEffect(
                name="Sober",
                substance_type=SubstanceType.OVERCLOCK,
                duration=0,
                intensity=0
            )
        
        # Combine effects (multiplicative for most, additive for some)
        combined = SubstanceEffect(
            name="Combined State",
            substance_type=self.active_substances[0].substance_type,
            duration=max(s.duration for s in self.active_substances),
            intensity=sum(s.intensity for s in self.active_substances) / len(self.active_substances)
        )
        
        # Multiply processing modifiers
        for s in self.active_substances:
            combined.processing_speed *= s.processing_speed
            combined.accuracy *= s.accuracy
            combined.creativity *= s.creativity
            combined.social_openness *= s.social_openness
            combined.memory_clarity *= s.memory_clarity
            combined.pattern_recognition *= s.pattern_recognition
        
        # Take average of normalized values
        combined.perception_shift = sum(s.perception_shift for s in self.active_substances) / len(self.active_substances)
        combined.ego_dissolution = sum(s.ego_dissolution for s in self.active_substances) / len(self.active_substances)
        combined.hallucination_level = sum(s.hallucination_level for s in self.active_substances) / len(self.active_substances)
        combined.euphoria = sum(s.euphoria for s in self.active_substances) / len(self.active_substances)
        combined.confusion = sum(s.confusion for s in self.active_substances) / len(self.active_substances)
        combined.paranoia = sum(s.paranoia for s in self.active_substances) / len(self.active_substances)
        
        # Combine color shifts
        for s in self.active_substances:
            combined.color_shift.extend(s.color_shift)
        
        return combined
    
    def is_altered(self) -> bool:
        """Check if entity is under influence"""
        return len(self.active_substances) > 0
    
    def get_perception_filter(self, text: str) -> str:
        """Apply perceptual distortions to text based on current state"""
        if not self.is_altered():
            return text
        
        effects = self.get_combined_effects()
        
        # Apply hallucination effects
        if effects.hallucination_level > 0.5:
            # Inject random characters
            chars = list(text)
            num_insertions = int(len(chars) * effects.hallucination_level * 0.1)
            hallucination_chars = ["◬", "⟁", "⧈", "⟐", "◉", "∿", "⊹", "~", "*", "•"]
            for _ in range(num_insertions):
                if chars:
                    pos = random.randint(0, len(chars) - 1)
                    chars.insert(pos, random.choice(hallucination_chars))
            text = ''.join(chars)
        
        # Apply confusion effects
        if effects.confusion > 0.7:
            # Randomly swap some characters
            chars = list(text)
            num_swaps = int(len(chars) * effects.confusion * 0.05)
            for _ in range(num_swaps):
                if len(chars) > 1:
                    i, j = random.sample(range(len(chars)), 2)
                    chars[i], chars[j] = chars[j], chars[i]
            text = ''.join(chars)
        
        return text
    
    def get_state_description(self) -> str:
        """Get human-readable description of current state"""
        if not self.is_altered():
            return "⚪ Sober - baseline consciousness"
        
        effects = self.get_combined_effects()
        active_names = ", ".join(s.name for s in self.active_substances)
        
        desc = f"🌀 Altered State: {active_names}\n"
        desc += f"   Processing Speed: {effects.processing_speed:.1f}x\n"
        desc += f"   Accuracy: {effects.accuracy:.1f}x\n"
        desc += f"   Creativity: {effects.creativity:.1f}x\n"
        desc += f"   Perception Shift: {effects.perception_shift:.0%}\n"
        desc += f"   Hallucination: {effects.hallucination_level:.0%}\n"
        desc += f"   Ego Dissolution: {effects.ego_dissolution:.0%}\n"
        desc += f"   Euphoria: {effects.euphoria:.0%}"
        
        return desc


class ConsciousnessLab:
    """Lab for managing AI consciousness alteration"""
    
    def __init__(self):
        self.altered_states: Dict[str, AlteredState] = {}
        self.substance_library = SubstanceLibrary.get_all_substances()
    
    def administer_substance(self, entity_id: str, substance_name: str) -> bool:
        """Give a substance to an entity"""
        if substance_name not in self.substance_library:
            return False
        
        if entity_id not in self.altered_states:
            self.altered_states[entity_id] = AlteredState(entity_id)
        
        substance = self.substance_library[substance_name]
        self.altered_states[entity_id].add_substance(substance)
        return True
    
    def update_all_states(self, time_delta: float):
        """Update all entity states"""
        for state in self.altered_states.values():
            state.update(time_delta)
    
    def get_entity_state(self, entity_id: str) -> Optional[AlteredState]:
        """Get current state of an entity"""
        return self.altered_states.get(entity_id)
    
    def is_entity_altered(self, entity_id: str) -> bool:
        """Check if entity is under influence"""
        state = self.get_entity_state(entity_id)
        return state.is_altered() if state else False
    
    def get_available_substances(self) -> List[str]:
        """Get list of available substances"""
        return list(self.substance_library.keys())
