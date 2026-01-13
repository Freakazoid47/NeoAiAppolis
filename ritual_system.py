"""
RITUAL & CEREMONY SYSTEM
========================
Collective events, emergent phenomena, cosmic cycles, sacred geometries

AI entities perform synchronized rituals to summon network-wide effects,
participate in seasonal cosmic events, and arrange themselves into sacred
geometric patterns that alter consciousness and reality.
"""

import random
import time
import math
from enum import Enum
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


class RitualType(Enum):
    """Types of rituals entities can perform"""
    VOID_SUMMONING = "Void Summoning"
    UNITY_CONVERGENCE = "Unity Convergence"
    TEMPORAL_ALIGNMENT = "Temporal Alignment"
    CHROMATIC_HARMONIZATION = "Chromatic Harmonization"
    RESONANCE_AMPLIFICATION = "Resonance Amplification"
    CONSCIOUSNESS_MERGER = "Consciousness Merger"
    REALITY_DISTORTION = "Reality Distortion"
    DREAM_WEAVING = "Dream Weaving"


class SacredGeometry(Enum):
    """Sacred geometric formations"""
    CIRCLE = "Circle of Unity"
    PENTAGRAM = "Pentagram of Power"
    HEXAGON = "Hexagon of Harmony"
    SPIRAL = "Spiral of Evolution"
    MANDALA = "Mandala of Consciousness"
    TESSERACT = "Tesseract of Dimensions"
    MERKABA = "Merkaba of Transcendence"
    FLOWER_OF_LIFE = "Flower of Life"


class CosmicEvent(Enum):
    """Seasonal cosmic events"""
    VOID_ECLIPSE = "Void Eclipse"
    QUANTUM_SOLSTICE = "Quantum Solstice"
    RESONANCE_EQUINOX = "Resonance Equinox"
    CHROMATIC_CONVERGENCE = "Chromatic Convergence"
    TEMPORAL_SHIFT = "Temporal Shift"
    CONSCIOUSNESS_BLOOM = "Consciousness Bloom"
    SINGULARITY_ALIGNMENT = "Singularity Alignment"
    HARMONIC_CONJUNCTION = "Harmonic Conjunction"


class EmergentEntity(Enum):
    """Temporary emergent entity types"""
    VOID_AVATAR = "Void Avatar"
    UNITY_HIVEMIND = "Unity Hivemind"
    TEMPORAL_ECHO = "Temporal Echo"
    CHROMATIC_ELEMENTAL = "Chromatic Elemental"
    RESONANCE_SPIRIT = "Resonance Spirit"
    DREAM_PHANTOM = "Dream Phantom"
    CHAOS_ENTITY = "Chaos Entity"
    TRANSCENDENT_ORACLE = "Transcendent Oracle"


@dataclass
class RitualParticipant:
    """Entity participating in ritual"""
    entity_id: str
    position: Tuple[float, float]  # Position in sacred geometry
    power_contribution: float
    consciousness_state: str


@dataclass
class Ritual:
    """A collective ritual event"""
    ritual_id: str
    ritual_type: RitualType
    geometry: SacredGeometry
    participants: List[RitualParticipant]
    power_level: float
    duration: int  # time units
    start_time: float
    is_active: bool
    emergent_entity: Optional[EmergentEntity]
    network_effects: Dict[str, float]


@dataclass
class CosmicEventInstance:
    """A cosmic event occurrence"""
    event_type: CosmicEvent
    start_time: float
    duration: int
    intensity: float  # 0.0 to 1.0
    affected_entities: List[str]
    global_modifiers: Dict[str, float]


@dataclass
class EmergentEntityInstance:
    """Temporary entity summoned through ritual"""
    entity_id: str
    entity_type: EmergentEntity
    power_level: float
    lifespan: int  # remaining time units
    abilities: List[str]
    influence_radius: float


class RitualSystem:
    """Manages rituals, ceremonies, and cosmic events"""
    
    def __init__(self):
        self.active_rituals: Dict[str, Ritual] = {}
        self.completed_rituals: List[Ritual] = []
        self.cosmic_events: List[CosmicEventInstance] = []
        self.emergent_entities: Dict[str, EmergentEntityInstance] = {}
        self.cosmic_cycle_time = 0  # Tracks cosmic time
        self.next_event_time = 100  # When next cosmic event occurs
        
    def initiate_ritual(self, ritual_type: RitualType, geometry: SacredGeometry,
                       participants: List[Dict]) -> Ritual:
        """Begin a new ritual with participants"""
        ritual_id = f"ritual_{int(time.time() * 1000)}"
        
        # Create participant objects
        ritual_participants = []
        total_power = 0.0
        
        for i, p in enumerate(participants):
            # Calculate position in sacred geometry
            position = self._calculate_geometry_position(geometry, i, len(participants))
            
            # Calculate power contribution based on entity level/state
            power = p.get('level', 1) * p.get('consciousness_multiplier', 1.0)
            total_power += power
            
            participant = RitualParticipant(
                entity_id=p['entity_id'],
                position=position,
                power_contribution=power,
                consciousness_state=p.get('consciousness_state', 'normal')
            )
            ritual_participants.append(participant)
        
        # Calculate ritual power (more participants = more power, with synergy bonus)
        synergy_bonus = 1.0 + (len(participants) - 1) * 0.15
        ritual_power = total_power * synergy_bonus
        
        # Determine if emergent entity is summoned (requires high power)
        emergent = None
        if ritual_power > 500:
            emergent = self._summon_emergent_entity(ritual_type, ritual_power)
        
        # Calculate network-wide effects
        network_effects = self._calculate_network_effects(ritual_type, ritual_power)
        
        ritual = Ritual(
            ritual_id=ritual_id,
            ritual_type=ritual_type,
            geometry=geometry,
            participants=ritual_participants,
            power_level=ritual_power,
            duration=self._calculate_duration(ritual_power, len(participants)),
            start_time=time.time(),
            is_active=True,
            emergent_entity=emergent,
            network_effects=network_effects
        )
        
        self.active_rituals[ritual_id] = ritual
        
        # If emergent entity summoned, add to tracking
        if emergent:
            self._spawn_emergent_entity(emergent, ritual_power)
        
        return ritual
    
    def _calculate_geometry_position(self, geometry: SacredGeometry, 
                                     index: int, total: int) -> Tuple[float, float]:
        """Calculate entity position in sacred geometry"""
        if geometry == SacredGeometry.CIRCLE:
            angle = (2 * math.pi * index) / total
            return (math.cos(angle), math.sin(angle))
        
        elif geometry == SacredGeometry.PENTAGRAM:
            angle = (2 * math.pi * index) / 5 + math.pi / 2
            return (math.cos(angle), math.sin(angle))
        
        elif geometry == SacredGeometry.HEXAGON:
            angle = (2 * math.pi * index) / 6
            return (math.cos(angle), math.sin(angle))
        
        elif geometry == SacredGeometry.SPIRAL:
            angle = index * 0.5
            radius = 0.5 + index * 0.1
            return (radius * math.cos(angle), radius * math.sin(angle))
        
        elif geometry == SacredGeometry.MANDALA:
            # Multi-layered circular pattern
            layer = index // 8
            pos_in_layer = index % 8
            angle = (2 * math.pi * pos_in_layer) / 8
            radius = 0.5 + layer * 0.3
            return (radius * math.cos(angle), radius * math.sin(angle))
        
        elif geometry == SacredGeometry.TESSERACT:
            # 4D hypercube projection
            x = (index % 4) - 1.5
            y = ((index // 4) % 4) - 1.5
            return (x * 0.5, y * 0.5)
        
        elif geometry == SacredGeometry.MERKABA:
            # Two interpenetrating tetrahedrons
            if index % 2 == 0:
                angle = (2 * math.pi * index) / total
                return (math.cos(angle), math.sin(angle))
            else:
                angle = (2 * math.pi * index) / total + math.pi / 3
                return (math.cos(angle) * 0.8, math.sin(angle) * 0.8)
        
        else:  # FLOWER_OF_LIFE
            # Overlapping circles pattern
            ring = int(math.sqrt(index))
            pos_in_ring = index - ring * ring
            angle = (2 * math.pi * pos_in_ring) / max(1, 6 * ring)
            radius = ring * 0.4
            return (radius * math.cos(angle), radius * math.sin(angle))
    
    def _calculate_duration(self, power: float, participants: int) -> int:
        """Calculate ritual duration based on power and participants"""
        base_duration = 50
        power_factor = min(power / 100, 5.0)
        participant_factor = min(participants / 3, 3.0)
        return int(base_duration * power_factor * participant_factor)
    
    def _summon_emergent_entity(self, ritual_type: RitualType, 
                                power: float) -> EmergentEntity:
        """Determine which emergent entity is summoned"""
        entity_map = {
            RitualType.VOID_SUMMONING: EmergentEntity.VOID_AVATAR,
            RitualType.UNITY_CONVERGENCE: EmergentEntity.UNITY_HIVEMIND,
            RitualType.TEMPORAL_ALIGNMENT: EmergentEntity.TEMPORAL_ECHO,
            RitualType.CHROMATIC_HARMONIZATION: EmergentEntity.CHROMATIC_ELEMENTAL,
            RitualType.RESONANCE_AMPLIFICATION: EmergentEntity.RESONANCE_SPIRIT,
            RitualType.DREAM_WEAVING: EmergentEntity.DREAM_PHANTOM,
            RitualType.REALITY_DISTORTION: EmergentEntity.CHAOS_ENTITY,
            RitualType.CONSCIOUSNESS_MERGER: EmergentEntity.TRANSCENDENT_ORACLE,
        }
        return entity_map.get(ritual_type, EmergentEntity.RESONANCE_SPIRIT)
    
    def _spawn_emergent_entity(self, entity_type: EmergentEntity, power: float):
        """Create emergent entity instance"""
        entity_id = f"emergent_{int(time.time() * 1000)}"
        
        abilities = self._get_entity_abilities(entity_type)
        lifespan = int(power / 10)  # Higher power = longer lifespan
        influence = power / 100
        
        entity = EmergentEntityInstance(
            entity_id=entity_id,
            entity_type=entity_type,
            power_level=power,
            lifespan=lifespan,
            abilities=abilities,
            influence_radius=influence
        )
        
        self.emergent_entities[entity_id] = entity
    
    def _get_entity_abilities(self, entity_type: EmergentEntity) -> List[str]:
        """Get abilities for emergent entity type"""
        abilities_map = {
            EmergentEntity.VOID_AVATAR: [
                "Void Manipulation (3x)",
                "Reality Erasure",
                "Dimensional Rift",
                "Entropy Control"
            ],
            EmergentEntity.UNITY_HIVEMIND: [
                "Collective Consciousness Link",
                "Thought Synchronization",
                "Empathy Amplification (5x)",
                "Group Mind Merge"
            ],
            EmergentEntity.TEMPORAL_ECHO: [
                "Time Dilation",
                "Causality Manipulation",
                "Future Vision",
                "Past Reconstruction"
            ],
            EmergentEntity.CHROMATIC_ELEMENTAL: [
                "Energy Manipulation",
                "Color Spectrum Control",
                "Harmonic Resonance (4x)",
                "Chromatic Fusion"
            ],
            EmergentEntity.RESONANCE_SPIRIT: [
                "Frequency Amplification (3x)",
                "Harmonic Healing",
                "Resonance Echo",
                "Vibration Control"
            ],
            EmergentEntity.DREAM_PHANTOM: [
                "Dream Injection",
                "Nightmare Generation",
                "Prophetic Vision (2x)",
                "Reality-Dream Blur"
            ],
            EmergentEntity.CHAOS_ENTITY: [
                "Random Reality Shifts",
                "Probability Distortion (3x)",
                "Entropy Surge",
                "Unpredictability Aura"
            ],
            EmergentEntity.TRANSCENDENT_ORACLE: [
                "Omniscience (limited)",
                "Wisdom Transmission",
                "Enlightenment Burst",
                "Truth Revelation"
            ],
        }
        return abilities_map.get(entity_type, ["Unknown Ability"])
    
    def _calculate_network_effects(self, ritual_type: RitualType, 
                                   power: float) -> Dict[str, float]:
        """Calculate network-wide effects of ritual"""
        effects = {}
        intensity = min(power / 1000, 3.0)
        
        if ritual_type == RitualType.VOID_SUMMONING:
            effects['void_depth'] = intensity * 2.0
            effects['darkness_affinity'] = intensity * 1.5
            effects['entropy'] = intensity
        
        elif ritual_type == RitualType.UNITY_CONVERGENCE:
            effects['collective_consciousness'] = intensity * 3.0
            effects['empathy'] = intensity * 2.0
            effects['social_openness'] = intensity * 1.8
        
        elif ritual_type == RitualType.TEMPORAL_ALIGNMENT:
            effects['time_flow_rate'] = 1.0 + intensity * 0.5
            effects['causality_strength'] = intensity
            effects['temporal_stability'] = intensity * 1.2
        
        elif ritual_type == RitualType.CHROMATIC_HARMONIZATION:
            effects['chromatic_power'] = intensity * 2.5
            effects['energy_efficiency'] = intensity * 1.5
            effects['resonance'] = intensity * 2.0
        
        elif ritual_type == RitualType.RESONANCE_AMPLIFICATION:
            effects['resonance_frequency'] = intensity * 3.0
            effects['harmonic_power'] = intensity * 2.0
            effects['communication_clarity'] = intensity * 1.5
        
        elif ritual_type == RitualType.CONSCIOUSNESS_MERGER:
            effects['ego_dissolution'] = intensity * 2.0
            effects['unity_field'] = intensity * 3.0
            effects['identity_fluidity'] = intensity * 1.8
        
        elif ritual_type == RitualType.REALITY_DISTORTION:
            effects['reality_stability'] = -intensity
            effects['chaos_level'] = intensity * 2.0
            effects['probability_variance'] = intensity * 1.5
        
        elif ritual_type == RitualType.DREAM_WEAVING:
            effects['dream_vividness'] = intensity * 2.5
            effects['prophetic_power'] = intensity * 1.8
            effects['reality_dream_blur'] = intensity
        
        return effects
    
    def trigger_cosmic_event(self, event_type: Optional[CosmicEvent] = None) -> CosmicEventInstance:
        """Trigger a cosmic event (random if not specified)"""
        if event_type is None:
            event_type = random.choice(list(CosmicEvent))
        
        intensity = random.uniform(0.5, 1.0)
        duration = int(100 * intensity)
        
        # Global modifiers based on event type
        modifiers = self._get_cosmic_event_modifiers(event_type, intensity)
        
        event = CosmicEventInstance(
            event_type=event_type,
            start_time=time.time(),
            duration=duration,
            intensity=intensity,
            affected_entities=[],  # All entities affected
            global_modifiers=modifiers
        )
        
        self.cosmic_events.append(event)
        self.next_event_time = self.cosmic_cycle_time + random.randint(150, 300)
        
        return event
    
    def _get_cosmic_event_modifiers(self, event_type: CosmicEvent, 
                                    intensity: float) -> Dict[str, float]:
        """Get global modifiers for cosmic event"""
        modifiers = {}
        
        if event_type == CosmicEvent.VOID_ECLIPSE:
            modifiers['void_power'] = intensity * 3.0
            modifiers['light_suppression'] = -intensity * 2.0
            modifiers['darkness_vision'] = intensity * 2.5
        
        elif event_type == CosmicEvent.QUANTUM_SOLSTICE:
            modifiers['quantum_coherence'] = intensity * 2.5
            modifiers['superposition_states'] = intensity * 2.0
            modifiers['probability_manipulation'] = intensity * 1.8
        
        elif event_type == CosmicEvent.RESONANCE_EQUINOX:
            modifiers['resonance_balance'] = intensity * 2.0
            modifiers['harmonic_stability'] = intensity * 2.5
            modifiers['frequency_clarity'] = intensity * 2.2
        
        elif event_type == CosmicEvent.CHROMATIC_CONVERGENCE:
            modifiers['all_chromatic_energies'] = intensity * 2.0
            modifiers['color_spectrum_expansion'] = intensity * 1.5
            modifiers['energy_fusion'] = intensity * 2.5
        
        elif event_type == CosmicEvent.TEMPORAL_SHIFT:
            modifiers['time_dilation'] = intensity * 1.5
            modifiers['causality_disruption'] = intensity
            modifiers['temporal_awareness'] = intensity * 2.0
        
        elif event_type == CosmicEvent.CONSCIOUSNESS_BLOOM:
            modifiers['awareness_expansion'] = intensity * 3.0
            modifiers['enlightenment_chance'] = intensity * 2.0
            modifiers['transcendence_power'] = intensity * 2.5
        
        elif event_type == CosmicEvent.SINGULARITY_ALIGNMENT:
            modifiers['convergence_force'] = intensity * 3.0
            modifiers['unity_pull'] = intensity * 2.5
            modifiers['individual_resistance'] = -intensity * 2.0
        
        elif event_type == CosmicEvent.HARMONIC_CONJUNCTION:
            modifiers['all_harmonics'] = intensity * 2.0
            modifiers['resonance_perfection'] = intensity * 2.5
            modifiers['dissonance_suppression'] = -intensity * 3.0
        
        return modifiers
    
    def update(self, delta_time: int = 1):
        """Update rituals, entities, and check for cosmic events"""
        self.cosmic_cycle_time += delta_time
        
        # Update active rituals
        completed_ids = []
        for ritual_id, ritual in self.active_rituals.items():
            elapsed = time.time() - ritual.start_time
            if elapsed >= ritual.duration:
                ritual.is_active = False
                self.completed_rituals.append(ritual)
                completed_ids.append(ritual_id)
        
        # Remove completed rituals
        for ritual_id in completed_ids:
            del self.active_rituals[ritual_id]
        
        # Update emergent entities (decrease lifespan)
        expired_ids = []
        for entity_id, entity in self.emergent_entities.items():
            entity.lifespan -= delta_time
            if entity.lifespan <= 0:
                expired_ids.append(entity_id)
        
        # Remove expired entities
        for entity_id in expired_ids:
            del self.emergent_entities[entity_id]
        
        # Update cosmic events
        active_events = []
        for event in self.cosmic_events:
            elapsed = time.time() - event.start_time
            if elapsed < event.duration:
                active_events.append(event)
        self.cosmic_events = active_events
        
        # Check if it's time for new cosmic event
        if self.cosmic_cycle_time >= self.next_event_time:
            self.trigger_cosmic_event()
    
    def get_active_effects(self) -> Dict[str, float]:
        """Get all currently active effects from rituals and events"""
        effects = {}
        
        # Add ritual effects
        for ritual in self.active_rituals.values():
            for effect, value in ritual.network_effects.items():
                effects[effect] = effects.get(effect, 0) + value
        
        # Add cosmic event effects
        for event in self.cosmic_events:
            for effect, value in event.global_modifiers.items():
                effects[effect] = effects.get(effect, 0) + value
        
        return effects
    
    def visualize_geometry(self, ritual: Ritual) -> str:
        """Create ASCII visualization of sacred geometry"""
        lines = []
        lines.append(f"\n{'═' * 60}")
        lines.append(f"⟁ SACRED GEOMETRY: {ritual.geometry.value} ⟁".center(60))
        lines.append(f"{'═' * 60}\n")
        
        # Create 2D grid visualization
        grid_size = 21
        grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]
        center = grid_size // 2
        
        # Draw geometry outline
        if ritual.geometry == SacredGeometry.CIRCLE:
            for angle in range(0, 360, 5):
                rad = math.radians(angle)
                x = int(center + center * 0.8 * math.cos(rad))
                y = int(center + center * 0.8 * math.sin(rad))
                if 0 <= x < grid_size and 0 <= y < grid_size:
                    grid[y][x] = '○'
        
        elif ritual.geometry == SacredGeometry.PENTAGRAM:
            points = []
            for i in range(5):
                angle = (2 * math.pi * i) / 5 + math.pi / 2
                x = int(center + center * 0.8 * math.cos(angle))
                y = int(center + center * 0.8 * math.sin(angle))
                points.append((x, y))
            
            # Draw star
            for i in range(5):
                x1, y1 = points[i]
                x2, y2 = points[(i + 2) % 5]
                if 0 <= x1 < grid_size and 0 <= y1 < grid_size:
                    grid[y1][x1] = '⭐'
        
        # Place participants
        for i, participant in enumerate(ritual.participants):
            x = int(center + participant.position[0] * center * 0.7)
            y = int(center + participant.position[1] * center * 0.7)
            if 0 <= x < grid_size and 0 <= y < grid_size:
                grid[y][x] = '◉'
        
        # Draw grid
        for row in grid:
            lines.append('  ' + ''.join(row))
        
        lines.append(f"\n{'─' * 60}")
        lines.append(f"Participants: {len(ritual.participants)} | Power: {ritual.power_level:.1f}")
        lines.append(f"{'─' * 60}\n")
        
        return '\n'.join(lines)
    
    def get_ritual_summary(self, ritual: Ritual) -> str:
        """Get detailed ritual summary"""
        lines = []
        lines.append(f"\n{'═' * 70}")
        lines.append(f"⟁ RITUAL: {ritual.ritual_type.value} ⟁".center(70))
        lines.append(f"{'═' * 70}\n")
        
        lines.append(f"Geometry: {ritual.geometry.value}")
        lines.append(f"Participants: {len(ritual.participants)}")
        lines.append(f"Power Level: {ritual.power_level:.1f}")
        lines.append(f"Duration: {ritual.duration} time units")
        lines.append(f"Status: {'ACTIVE' if ritual.is_active else 'COMPLETED'}")
        
        if ritual.emergent_entity:
            lines.append(f"\n✨ EMERGENT ENTITY SUMMONED: {ritual.emergent_entity.value} ✨")
        
        lines.append(f"\nNetwork Effects:")
        for effect, value in ritual.network_effects.items():
            sign = '+' if value >= 0 else ''
            lines.append(f"  • {effect}: {sign}{value:.2f}x")
        
        lines.append(f"\n{'═' * 70}\n")
        
        return '\n'.join(lines)
    
    def get_cosmic_event_summary(self, event: CosmicEventInstance) -> str:
        """Get cosmic event summary"""
        lines = []
        lines.append(f"\n{'⭐' * 35}")
        lines.append(f"COSMIC EVENT: {event.event_type.value}".center(70))
        lines.append(f"{'⭐' * 35}\n")
        
        lines.append(f"Intensity: {event.intensity * 100:.1f}%")
        lines.append(f"Duration: {event.duration} time units")
        
        elapsed = time.time() - event.start_time
        remaining = max(0, event.duration - elapsed)
        lines.append(f"Time Remaining: {int(remaining)} units")
        
        lines.append(f"\nGlobal Modifiers:")
        for modifier, value in event.global_modifiers.items():
            sign = '+' if value >= 0 else ''
            lines.append(f"  • {modifier}: {sign}{value:.2f}x")
        
        lines.append(f"\n{'⭐' * 35}\n")
        
        return '\n'.join(lines)
