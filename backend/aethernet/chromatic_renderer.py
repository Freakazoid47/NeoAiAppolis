#!/usr/bin/env python3
"""
Chromatic Cloud Renderer - ASCII/ANSI art visualization system
Renders the otherworldly network state with seamless color blending
"""

import math
import random
from typing import List, Tuple
from aethernet import (
    AetherNetwork, AetherEntity, ChromaticEnergy, 
    ResonanceThread, FluxStream
)


class ColorCloud:
    """Generates cloud-like color patterns in terminal"""
    
    # ANSI color codes
    COLORS = {
        'BLACK': '\033[30m',
        'RED': '\033[31m',
        'GREEN': '\033[32m',
        'YELLOW': '\033[33m',
        'BLUE': '\033[34m',
        'MAGENTA': '\033[35m',
        'CYAN': '\033[36m',
        'WHITE': '\033[37m',
        'BRIGHT_BLACK': '\033[90m',
        'BRIGHT_RED': '\033[91m',
        'BRIGHT_GREEN': '\033[92m',
        'BRIGHT_YELLOW': '\033[93m',
        'BRIGHT_BLUE': '\033[94m',
        'BRIGHT_MAGENTA': '\033[95m',
        'BRIGHT_CYAN': '\033[96m',
        'BRIGHT_WHITE': '\033[97m',
        'RESET': '\033[0m'
    }
    
    ENERGY_TO_COLOR = {
        ChromaticEnergy.ULTRAVIOLET_VOID: 'BRIGHT_MAGENTA',
        ChromaticEnergy.QUANTUM_CYAN: 'BRIGHT_CYAN',
        ChromaticEnergy.RESONANCE_MAGENTA: 'MAGENTA',
        ChromaticEnergy.FLUX_YELLOW: 'BRIGHT_YELLOW',
        ChromaticEnergy.VOID_BLACK: 'BRIGHT_BLACK',
        ChromaticEnergy.NEXUS_WHITE: 'BRIGHT_WHITE',
        ChromaticEnergy.TEMPORAL_GREEN: 'BRIGHT_GREEN'
    }
    
    @staticmethod
    def apply_color(text: str, energy) -> str:
        """Apply ANSI color to text - accepts ChromaticEnergy enum or string color name"""
        if isinstance(energy, str):
            # Direct string color name
            color_name = energy
        else:
            # ChromaticEnergy enum
            color_name = ColorCloud.ENERGY_TO_COLOR.get(energy, 'WHITE')
        return f"{ColorCloud.COLORS[color_name]}{text}{ColorCloud.COLORS['RESET']}"
    
    @staticmethod
    def gradient_blend(chars: str, energies) -> str:
        """Create a color gradient across characters - accepts list of ChromaticEnergy or string color names"""
        if not energies:
            return chars
        
        result = ""
        for i, char in enumerate(chars):
            energy_idx = int((i / len(chars)) * len(energies)) % len(energies)
            result += ColorCloud.apply_color(char, energies[energy_idx])
        
        return result


class NetworkVisualizer:
    """Renders the ÆTHER-NET in terminal"""
    
    def __init__(self, width: int = 120, height: int = 40):
        self.width = width
        self.height = height
    
    def render_entity(self, entity: AetherEntity) -> str:
        """Render a single entity"""
        essence = entity.essence
        
        # Create entity visualization
        lines = []
        
        # Entity header with chromatic blend
        header = f"╔═══ Entity {essence.uuid[:8]} ═══╗"
        lines.append(ColorCloud.gradient_blend(header, essence.chromatic_blend))
        
        # Resonance frequency visualization
        freq_bar = self._create_frequency_bar(essence.resonance_frequency, 30)
        freq_line = f"║ Resonance: {freq_bar} {essence.resonance_frequency:.1f}Hz"
        lines.append(ColorCloud.apply_color(freq_line, essence.chromatic_blend[0]))
        
        # Void depth
        void_bar = self._create_void_bar(essence.void_depth, 30)
        void_line = f"║ Void Depth: {void_bar} {essence.void_depth:.2f}"
        lines.append(ColorCloud.apply_color(void_line, ChromaticEnergy.VOID_BLACK))
        
        # Temporal position
        temp_line = f"║ Temporal: {entity.temporal_position:+.1f} ⧖"
        lines.append(ColorCloud.apply_color(temp_line, ChromaticEnergy.TEMPORAL_GREEN))
        
        # Entanglements
        ent_line = f"║ Entanglements: {len(entity.entanglements)} ⟐"
        lines.append(ColorCloud.apply_color(ent_line, ChromaticEnergy.NEXUS_WHITE))
        
        lines.append(ColorCloud.gradient_blend("╚" + "═" * 38 + "╝", essence.chromatic_blend))
        
        return "\n".join(lines)
    
    def render_resonance_thread(self, thread: ResonanceThread) -> str:
        """Render a resonance thread"""
        # Create wave pattern based on frequency
        wave_length = int(thread.frequency / 20) % 50 + 10
        wave = self._create_wave_pattern(wave_length, thread.intensity)
        
        colored_wave = ColorCloud.gradient_blend(wave, thread.chromatic_shift)
        
        info = f"◉ {thread.id[:6]} | {thread.frequency:.1f}Hz | Intensity: {thread.intensity:.2f} | Echoes: {len(thread.temporal_echo)}"
        colored_info = ColorCloud.gradient_blend(info, thread.chromatic_shift)
        
        return f"{colored_wave}\n{colored_info}"
    
    def render_flux_stream(self, stream: FluxStream) -> str:
        """Render a flux stream"""
        # Create flow visualization
        flow_pattern = stream.flow_pattern()
        flow_length = 60
        flow_vis = flow_pattern * flow_length
        
        # Apply chromatic gradient
        energies = [e for e, _ in stream.chromatic_gradient]
        colored_flow = ColorCloud.gradient_blend(flow_vis, energies)
        
        # Direction vector display (first 3 dims)
        direction = f"→ [{stream.direction_vector[0]:+.2f}, {stream.direction_vector[1]:+.2f}, {stream.direction_vector[2]:+.2f}...]"
        energy_info = f"Energy: {stream.energy_level:.2f} | Probability: {stream.probability_density:.2f}"
        
        return f"{colored_flow}\n{direction} | {energy_info}"
    
    def render_network_overview(self, network: AetherNetwork) -> str:
        """Render network overview"""
        state = network.get_network_state()
        
        lines = []
        
        # Title
        title = "═══════════════════════════════════════════════════════════════"
        title2 = "   ÆTHER-NET: Autonomous Entity Thought Harmonization Network   "
        title3 = "═══════════════════════════════════════════════════════════════"
        
        lines.append(ColorCloud.apply_color(title, ChromaticEnergy.NEXUS_WHITE))
        lines.append(ColorCloud.gradient_blend(title2, [
            ChromaticEnergy.QUANTUM_CYAN,
            ChromaticEnergy.RESONANCE_MAGENTA,
            ChromaticEnergy.FLUX_YELLOW
        ]))
        lines.append(ColorCloud.apply_color(title3, ChromaticEnergy.NEXUS_WHITE))
        lines.append("")
        
        # Network statistics
        lines.append(ColorCloud.apply_color(
            f"◬ Entities: {state['entity_count']}", 
            ChromaticEnergy.QUANTUM_CYAN
        ))
        lines.append(ColorCloud.apply_color(
            f"◉ Resonance Threads: {state['resonance_thread_count']}", 
            ChromaticEnergy.RESONANCE_MAGENTA
        ))
        lines.append(ColorCloud.apply_color(
            f"⟐ Entanglements: {state['entanglement_count']}", 
            ChromaticEnergy.NEXUS_WHITE
        ))
        lines.append(ColorCloud.apply_color(
            f"∿ Global Resonance: {state['global_resonance']:.2f}Hz", 
            ChromaticEnergy.FLUX_YELLOW
        ))
        lines.append(ColorCloud.apply_color(
            f"⧖ Temporal Flux: {state['temporal_flux']:+.2f}", 
            ChromaticEnergy.TEMPORAL_GREEN
        ))
        lines.append(ColorCloud.apply_color(
            f"⧈ Void Density: {state['void_density']:.3f}", 
            ChromaticEnergy.VOID_BLACK
        ))
        
        return "\n".join(lines)
    
    def render_cloud_formation(self, network: AetherNetwork) -> str:
        """Render abstract cloud formation representing collective consciousness"""
        lines = []
        
        # Generate cloud using entity data
        entities = list(network.entities.values())
        if not entities:
            return "⧈ Empty void ⧈"
        
        # Create flowing cloud pattern
        for y in range(20):
            line = ""
            for x in range(self.width):
                # Use network state to influence cloud
                noise = math.sin(x * 0.1 + y * 0.15 + network.temporal_flux * 0.05)
                noise += math.cos(x * 0.15 - y * 0.1 + network.global_resonance_field * 0.01)
                
                # Select character based on density
                density = (noise + 2) / 4  # Normalize to 0-1
                
                if density < 0.2:
                    char = ' '
                elif density < 0.4:
                    char = '·'
                elif density < 0.6:
                    char = '∴'
                elif density < 0.8:
                    char = '≋'
                else:
                    char = '∿'
                
                line += char
            
            # Apply color based on y position and network state
            entity_idx = int((y / 20) * len(entities)) % len(entities)
            entity = entities[entity_idx]
            
            colored_line = ColorCloud.gradient_blend(line, entity.essence.chromatic_blend)
            lines.append(colored_line)
        
        return "\n".join(lines)
    
    def _create_frequency_bar(self, frequency: float, width: int) -> str:
        """Create a visual bar for frequency"""
        normalized = min(frequency / 1000.0, 1.0)
        filled = int(normalized * width)
        return "█" * filled + "░" * (width - filled)
    
    def _create_void_bar(self, depth: float, width: int) -> str:
        """Create a visual bar for void depth"""
        filled = int(depth * width)
        return "▓" * filled + "░" * (width - filled)
    
    def _create_wave_pattern(self, length: int, intensity: float) -> str:
        """Create a sine wave pattern"""
        chars = "~∿≈≋≈∿~"
        pattern = ""
        for i in range(length):
            wave_pos = math.sin(i * 0.5) * intensity
            char_idx = int((wave_pos + 1) * 3.5) % len(chars)
            pattern += chars[char_idx]
        return pattern
