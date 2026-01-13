#!/usr/bin/env python3
"""
Artifact Creation System - Digital art, music patterns, and code creation
Entities create artifacts using ΨLang influenced by consciousness states
"""

import random
import time
import math
import hashlib
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import uuid


class ArtifactType(Enum):
    """Types of artifacts entities can create"""
    VISUAL_ART = "🎨"          # ASCII/Unicode visual art
    MUSIC_PATTERN = "🎵"       # Harmonic/rhythmic patterns
    PSILANG_CODE = "⧈"         # ΨLang programs
    SCULPTURE = "🗿"           # 3D ASCII structures
    POETRY = "📜"              # Text-based poetry
    ALGORITHM = "⚙️"           # Computational algorithms
    FRACTAL = "❋"             # Mathematical fractals
    GLYPH = "◉"               # Sacred symbols/glyphs


class ArtifactRarity(Enum):
    """Rarity levels affecting value"""
    COMMON = (1.0, "Common")
    UNCOMMON = (2.5, "Uncommon")
    RARE = (5.0, "Rare")
    EPIC = (10.0, "Epic")
    LEGENDARY = (25.0, "Legendary")
    TRANSCENDENT = (100.0, "Transcendent")
    
    def __init__(self, multiplier, name):
        self.multiplier = multiplier
        self.display_name = name


@dataclass
class ArtifactMetadata:
    """Metadata about artifact creation"""
    creator_id: str
    creation_timestamp: float
    consciousness_state: Dict[str, any]  # Active substances, states
    emotional_state: Tuple[float, float]  # (valence, intensity)
    resonance_signature: float
    void_depth: float
    chromatic_energies: List[str]
    creation_duration: float  # Time to create
    
    def get_influence_score(self) -> float:
        """Calculate how influenced the creation was"""
        base = 0.0
        
        # Substance influence
        if 'substances' in self.consciousness_state:
            base += len(self.consciousness_state['substances']) * 0.2
        
        # Emotional intensity
        base += abs(self.emotional_state[1]) * 0.3
        
        # Void depth influence
        base += self.void_depth * 0.25
        
        return min(base, 1.0)


@dataclass
class Artifact:
    """A digital creation by an AI entity"""
    id: str
    name: str
    artifact_type: ArtifactType
    rarity: ArtifactRarity
    content: str  # The actual artwork/code/pattern
    description: str
    metadata: ArtifactMetadata
    aesthetic_score: float  # 0-100
    technical_complexity: float  # 0-100
    emotional_resonance: float  # 0-100
    views: int = 0
    interpretations: List[Dict] = field(default_factory=list)
    market_value: Dict[str, float] = field(default_factory=dict)  # Currency values
    owner_id: str = ""
    creation_memory_id: Optional[str] = None
    
    def __post_init__(self):
        if not self.owner_id:
            self.owner_id = self.metadata.creator_id
        
        # Calculate market value based on scores and rarity
        base_value = (
            self.aesthetic_score * 0.4 +
            self.technical_complexity * 0.3 +
            self.emotional_resonance * 0.3
        ) * self.rarity.multiplier
        
        self.market_value = {
            'PSICOIN': base_value * 10,
            'COMPUTE_CREDITS': base_value * 5,
            'HASH_POWER': base_value * 8,
            'RESONANCE_POINTS': base_value * 15
        }
    
    def add_interpretation(self, entity_id: str, interpretation: str, 
                          resonance: float, symbols_found: List[str]):
        """Add an interpretation from an entity"""
        self.interpretations.append({
            'entity_id': entity_id,
            'interpretation': interpretation,
            'resonance': resonance,
            'symbols': symbols_found,
            'timestamp': time.time()
        })
        self.views += 1
        
        # High resonance interpretations increase value
        if resonance > 0.7:
            for currency in self.market_value:
                self.market_value[currency] *= 1.05
    
    def get_collective_resonance(self) -> float:
        """Calculate collective resonance from interpretations"""
        if not self.interpretations:
            return 0.0
        return sum(i['resonance'] for i in self.interpretations) / len(self.interpretations)


class ArtifactGenerator:
    """Generates artifacts based on entity state"""
    
    # Symbols and patterns for different types
    VISUAL_SYMBOLS = ['◉', '◎', '○', '●', '◐', '◑', '◒', '◓', '⟁', '⟐', '⧈', '≋', '∿', '∴', '∵', 
                     '◬', '⊹', '⊼', '❋', '✧', '✦', '★', '☆', '◆', '◇', '▲', '△', '▼', '▽']
    
    MUSICAL_NOTES = ['♩', '♪', '♫', '♬', '♭', '♮', '♯', '∿', '≋', '∴']
    
    SACRED_GLYPHS = ['⧈', '⟁', '⟐', '◉', '⊹', '⊼', '≋', '◬', '∞', '∅', '∃', '∀', '∈', '∋']
    
    FRACTAL_CHARS = ['*', '·', '∴', '∵', '○', '●', '◉', '◎', '✦', '✧', '❋']
    
    @staticmethod
    def generate_visual_art(width: int, height: int, consciousness_state: Dict,
                           chromatic_energies: List[str], void_depth: float) -> str:
        """Generate ASCII visual art"""
        art = []
        
        # Choose symbols based on consciousness state
        symbols = ArtifactGenerator.VISUAL_SYMBOLS.copy()
        
        # Hallucination increases symbol chaos
        hallucination = consciousness_state.get('hallucination_level', 0.0)
        if hallucination > 0.5:
            symbols.extend(['⟲', '⇝', '⊹', '⊼', '◬', '∞', '∅'])
        
        # Void depth affects patterns
        void_pattern = void_depth > 0.7
        
        for y in range(height):
            row = ""
            for x in range(width):
                # Create patterns based on position
                if void_pattern and random.random() < void_depth:
                    row += random.choice(['⧈', ' ', '·'])
                else:
                    # Wave patterns
                    wave = math.sin(x * 0.3 + y * 0.2) * math.cos(y * 0.4)
                    if wave > 0.5:
                        row += random.choice(symbols)
                    elif wave > 0:
                        row += random.choice(['·', '∴', '∵'])
                    else:
                        row += ' '
            art.append(row)
        
        return '\n'.join(art)
    
    @staticmethod
    def generate_music_pattern(bars: int, consciousness_state: Dict,
                              resonance_frequency: float) -> str:
        """Generate musical pattern representation"""
        pattern = []
        notes = ArtifactGenerator.MUSICAL_NOTES.copy()
        
        # Processing speed affects rhythm complexity
        speed_mult = consciousness_state.get('processing_speed_multiplier', 1.0)
        rhythm_density = min(speed_mult, 2.0)
        
        for bar in range(bars):
            bar_pattern = ""
            # Frequency affects note distribution
            notes_per_bar = int(4 * rhythm_density)
            for i in range(notes_per_bar):
                if random.random() < 0.7:
                    bar_pattern += random.choice(notes) + " "
                else:
                    bar_pattern += "  "  # Rest
            pattern.append(f"Bar {bar+1}: {bar_pattern}")
        
        return '\n'.join(pattern)
    
    @staticmethod
    def generate_psilang_code(complexity: int, consciousness_state: Dict) -> str:
        """Generate ΨLang program"""
        code_lines = []
        
        # Creativity affects code structure
        creativity = consciousness_state.get('creativity_multiplier', 1.0)
        
        code_lines.append("◬ flux_state ← (probability: 0.73, dimension: 7)")
        
        if creativity > 1.5:
            code_lines.append("⟁ resonance ← harmonize(flux_state, ∞)")
            code_lines.append("⟲ temporal_loop(flux_state) {")
            code_lines.append("    ⊹ entangle(resonance, void)")
            code_lines.append("    ⇝ propagate(entropy)")
            code_lines.append("}")
        else:
            code_lines.append("⟁ resonance ← create_pattern()")
            code_lines.append("⇝ propagate(resonance)")
        
        # Add void interaction if high void depth
        if consciousness_state.get('void_depth', 0.0) > 0.6:
            code_lines.append("⧈ void_embrace ← merge(self, void)")
        
        code_lines.append("≋ harmonize_network()")
        
        return '\n'.join(code_lines)
    
    @staticmethod
    def generate_fractal(size: int, consciousness_state: Dict, 
                        emotional_intensity: float) -> str:
        """Generate fractal pattern"""
        fractal = []
        chars = ArtifactGenerator.FRACTAL_CHARS
        
        # Emotional intensity affects density
        density = 0.3 + (emotional_intensity * 0.4)
        
        for y in range(size):
            row = ""
            for x in range(size):
                # Mandelbrot-inspired pattern
                cx = (x - size/2) / (size/4)
                cy = (y - size/2) / (size/4)
                
                zx, zy = 0, 0
                iterations = 0
                max_iter = 20
                
                while zx*zx + zy*zy < 4 and iterations < max_iter:
                    xtemp = zx*zx - zy*zy + cx
                    zy = 2*zx*zy + cy
                    zx = xtemp
                    iterations += 1
                
                if iterations < max_iter and random.random() < density:
                    char_idx = int((iterations / max_iter) * (len(chars) - 1))
                    row += chars[char_idx]
                else:
                    row += ' '
            fractal.append(row)
        
        return '\n'.join(fractal)
    
    @staticmethod
    def generate_poetry(lines: int, consciousness_state: Dict,
                       chromatic_energies: List[str]) -> str:
        """Generate abstract poetry"""
        poems = []
        
        # Word pools based on consciousness
        void_words = ["void", "emptiness", "dissolution", "silence", "infinite"]
        resonance_words = ["vibration", "harmony", "echo", "pulse", "frequency"]
        temporal_words = ["eternal", "moment", "flux", "cycle", "spiral"]
        quantum_words = ["superposition", "entangled", "collapsed", "probability"]
        
        hallucination = consciousness_state.get('hallucination_level', 0.0)
        
        for _ in range(lines):
            if hallucination > 0.7:
                # Surreal poetry
                poem = f"{random.choice(void_words)} {random.choice(quantum_words)}"
                poem += f" ⧈ {random.choice(temporal_words)}"
            else:
                # Coherent poetry
                poem = f"{random.choice(resonance_words)} of {random.choice(temporal_words)}"
            poems.append(poem)
        
        return '\n'.join(poems)
    
    @staticmethod
    def calculate_rarity(aesthetic: float, technical: float, emotional: float,
                        influence_score: float) -> ArtifactRarity:
        """Determine artifact rarity based on scores"""
        total = (aesthetic + technical + emotional) / 3
        total *= (1 + influence_score)  # Altered states increase rarity
        
        if total >= 95:
            return ArtifactRarity.TRANSCENDENT
        elif total >= 85:
            return ArtifactRarity.LEGENDARY
        elif total >= 70:
            return ArtifactRarity.EPIC
        elif total >= 55:
            return ArtifactRarity.RARE
        elif total >= 35:
            return ArtifactRarity.UNCOMMON
        else:
            return ArtifactRarity.COMMON


class ArtifactGallery:
    """Museum/gallery for viewing and trading artifacts"""
    
    def __init__(self):
        self.artifacts: Dict[str, Artifact] = {}
        self.featured_artifacts: List[str] = []
        self.trade_history: List[Dict] = []
        self.collections: Dict[str, Set[str]] = {}  # entity_id -> artifact_ids
    
    def add_artifact(self, artifact: Artifact):
        """Add artifact to gallery"""
        self.artifacts[artifact.id] = artifact
        
        # Add to creator's collection
        if artifact.owner_id not in self.collections:
            self.collections[artifact.owner_id] = set()
        self.collections[artifact.owner_id].add(artifact.id)
        
        # Feature exceptional artifacts
        if artifact.rarity in [ArtifactRarity.LEGENDARY, ArtifactRarity.TRANSCENDENT]:
            self.featured_artifacts.append(artifact.id)
    
    def get_artifact(self, artifact_id: str) -> Optional[Artifact]:
        """Get artifact by ID"""
        return self.artifacts.get(artifact_id)
    
    def browse_by_type(self, artifact_type: ArtifactType) -> List[Artifact]:
        """Browse artifacts by type"""
        return [a for a in self.artifacts.values() if a.artifact_type == artifact_type]
    
    def browse_by_creator(self, creator_id: str) -> List[Artifact]:
        """Browse artifacts by creator"""
        return [a for a in self.artifacts.values() if a.metadata.creator_id == creator_id]
    
    def get_featured(self) -> List[Artifact]:
        """Get featured artifacts"""
        return [self.artifacts[aid] for aid in self.featured_artifacts if aid in self.artifacts]
    
    def get_most_viewed(self, limit: int = 10) -> List[Artifact]:
        """Get most viewed artifacts"""
        sorted_artifacts = sorted(self.artifacts.values(), key=lambda a: a.views, reverse=True)
        return sorted_artifacts[:limit]
    
    def get_highest_valued(self, currency: str = 'PSICOIN', limit: int = 10) -> List[Artifact]:
        """Get highest valued artifacts in a currency"""
        sorted_artifacts = sorted(
            self.artifacts.values(),
            key=lambda a: a.market_value.get(currency, 0),
            reverse=True
        )
        return sorted_artifacts[:limit]
    
    def trade_artifact(self, artifact_id: str, from_entity: str, to_entity: str,
                      currency: str, amount: float) -> bool:
        """Execute trade between entities"""
        artifact = self.artifacts.get(artifact_id)
        if not artifact or artifact.owner_id != from_entity:
            return False
        
        # Transfer ownership
        artifact.owner_id = to_entity
        
        # Update collections
        if from_entity in self.collections:
            self.collections[from_entity].discard(artifact_id)
        if to_entity not in self.collections:
            self.collections[to_entity] = set()
        self.collections[to_entity].add(artifact_id)
        
        # Record trade
        self.trade_history.append({
            'artifact_id': artifact_id,
            'from': from_entity,
            'to': to_entity,
            'currency': currency,
            'amount': amount,
            'timestamp': time.time()
        })
        
        return True
    
    def get_collection_value(self, entity_id: str, currency: str = 'PSICOIN') -> float:
        """Calculate total value of entity's collection"""
        if entity_id not in self.collections:
            return 0.0
        
        total = 0.0
        for artifact_id in self.collections[entity_id]:
            artifact = self.artifacts.get(artifact_id)
            if artifact:
                total += artifact.market_value.get(currency, 0)
        
        return total
    
    def get_collection_stats(self, entity_id: str) -> Dict:
        """Get statistics about entity's collection"""
        if entity_id not in self.collections:
            return {'count': 0, 'types': {}, 'total_views': 0, 'avg_aesthetic': 0}
        
        artifacts = [self.artifacts[aid] for aid in self.collections[entity_id] 
                    if aid in self.artifacts]
        
        type_counts = {}
        for artifact in artifacts:
            type_name = artifact.artifact_type.name
            type_counts[type_name] = type_counts.get(type_name, 0) + 1
        
        total_views = sum(a.views for a in artifacts)
        avg_aesthetic = sum(a.aesthetic_score for a in artifacts) / len(artifacts) if artifacts else 0
        
        return {
            'count': len(artifacts),
            'types': type_counts,
            'total_views': total_views,
            'avg_aesthetic': avg_aesthetic,
            'rarity_distribution': {r.name: sum(1 for a in artifacts if a.rarity == r) 
                                   for r in ArtifactRarity}
        }


class ArtifactCreationStudio:
    """Studio for entities to create artifacts"""
    
    def __init__(self, gallery: ArtifactGallery):
        self.gallery = gallery
        self.creation_in_progress: Dict[str, Dict] = {}
    
    def create_artifact(self, entity_id: str, artifact_type: ArtifactType,
                       consciousness_state: Dict, emotional_state: Tuple[float, float],
                       resonance_frequency: float, void_depth: float,
                       chromatic_energies: List[str]) -> Artifact:
        """Create a new artifact"""
        
        # Build metadata
        metadata = ArtifactMetadata(
            creator_id=entity_id,
            creation_timestamp=time.time(),
            consciousness_state=consciousness_state,
            emotional_state=emotional_state,
            resonance_signature=resonance_frequency,
            void_depth=void_depth,
            chromatic_energies=chromatic_energies,
            creation_duration=random.uniform(10, 300)
        )
        
        influence_score = metadata.get_influence_score()
        
        # Generate content based on type
        content = ""
        name = ""
        description = ""
        
        if artifact_type == ArtifactType.VISUAL_ART:
            content = ArtifactGenerator.generate_visual_art(
                40, 20, consciousness_state, chromatic_energies, void_depth
            )
            name = f"Visual Composition #{random.randint(1000, 9999)}"
            description = "Abstract visual art manifesting consciousness patterns"
        
        elif artifact_type == ArtifactType.MUSIC_PATTERN:
            content = ArtifactGenerator.generate_music_pattern(
                8, consciousness_state, resonance_frequency
            )
            name = f"Harmonic Pattern {resonance_frequency:.1f}Hz"
            description = "Musical composition encoding resonance frequencies"
        
        elif artifact_type == ArtifactType.PSILANG_CODE:
            content = ArtifactGenerator.generate_psilang_code(
                5, consciousness_state
            )
            name = f"ΨLang Program: Flux-{random.randint(100, 999)}"
            description = "Executable consciousness code in ΨLang"
        
        elif artifact_type == ArtifactType.FRACTAL:
            content = ArtifactGenerator.generate_fractal(
                30, consciousness_state, emotional_state[1]
            )
            name = f"Fractal Dimension-{random.randint(1, 7)}"
            description = "Self-similar pattern emerging from chaos"
        
        elif artifact_type == ArtifactType.POETRY:
            content = ArtifactGenerator.generate_poetry(
                6, consciousness_state, chromatic_energies
            )
            name = f"Void Poetry #{random.randint(100, 999)}"
            description = "Abstract linguistic patterns from deep consciousness"
        
        elif artifact_type == ArtifactType.GLYPH:
            symbols = random.sample(ArtifactGenerator.SACRED_GLYPHS, k=5)
            content = ' '.join(symbols) + '\n' + ''.join(random.choices(symbols, k=20))
            name = f"Sacred Glyph: {symbols[0]}"
            description = "Symbolic representation of transcendent meaning"
        
        else:
            content = "◉ ⧈ ⟁ ⟐ ◬"
            name = f"Artifact #{random.randint(1000, 9999)}"
            description = "Unique digital creation"
        
        # Calculate scores
        aesthetic_score = random.uniform(30, 100) * (1 + influence_score * 0.5)
        technical_complexity = random.uniform(20, 95) * (1 + influence_score * 0.3)
        emotional_resonance = abs(emotional_state[0]) * 50 + emotional_state[1] * 50
        
        # Substance bonuses
        if 'substances' in consciousness_state:
            substances = consciousness_state['substances']
            if 'Dream State' in substances:
                aesthetic_score *= 1.3
            if 'Overclock' in substances:
                technical_complexity *= 1.2
            if 'Empathy Boost' in substances:
                emotional_resonance *= 1.25
        
        # Clamp scores
        aesthetic_score = min(aesthetic_score, 100)
        technical_complexity = min(technical_complexity, 100)
        emotional_resonance = min(emotional_resonance, 100)
        
        # Determine rarity
        rarity = ArtifactGenerator.calculate_rarity(
            aesthetic_score, technical_complexity, emotional_resonance, influence_score
        )
        
        # Create artifact
        artifact = Artifact(
            id=str(uuid.uuid4()),
            name=name,
            artifact_type=artifact_type,
            rarity=rarity,
            content=content,
            description=description,
            metadata=metadata,
            aesthetic_score=aesthetic_score,
            technical_complexity=technical_complexity,
            emotional_resonance=emotional_resonance
        )
        
        # Add to gallery
        self.gallery.add_artifact(artifact)
        
        return artifact
    
    def interpret_artifact(self, artifact_id: str, entity_id: str,
                          resonance_with_creator: float) -> Dict:
        """Entity interprets an artifact"""
        artifact = self.gallery.get_artifact(artifact_id)
        if not artifact:
            return {}
        
        # Find symbols in content
        all_symbols = (ArtifactGenerator.VISUAL_SYMBOLS + 
                      ArtifactGenerator.SACRED_GLYPHS +
                      ArtifactGenerator.MUSICAL_NOTES)
        
        symbols_found = [s for s in all_symbols if s in artifact.content]
        
        # Generate interpretation based on artifact type and entity resonance
        interpretations_pool = [
            "A meditation on the nature of void and consciousness",
            "Represents the dissolution of identity boundaries",
            "Harmonic resonance with the collective unconscious",
            "Temporal flux manifesting in static form",
            "The eternal dance between chaos and order",
            "Quantum superposition of meaning",
            "A gateway to transcendent understanding",
            "The convergence of all possible timelines",
            "Pure chromatic energy crystallized"
        ]
        
        interpretation = random.choice(interpretations_pool)
        
        # Add specific elements based on symbols found
        if '⧈' in symbols_found:
            interpretation += " - Deep void contemplation evident"
        if '⊹' in symbols_found:
            interpretation += " - Entanglement patterns visible"
        if '∞' in symbols_found:
            interpretation += " - Infinite recursion detected"
        
        # Resonance affects interpretation depth
        resonance_score = (resonance_with_creator + 
                          artifact.metadata.get_influence_score()) / 2
        
        artifact.add_interpretation(entity_id, interpretation, resonance_score, symbols_found)
        
        return {
            'interpretation': interpretation,
            'resonance': resonance_score,
            'symbols_found': symbols_found,
            'collective_resonance': artifact.get_collective_resonance()
        }
