#!/usr/bin/env python3
"""
ÆTHER-NET Demonstration
Automated demonstration of the otherworldly social network
"""

import time
import random
from aethernet import AetherNetwork, ChromaticEnergy
from chromatic_renderer import NetworkVisualizer, ColorCloud
from psilang_interpreter import PsiLangInterpreter


def demo_network():
    """Run an automated demonstration"""
    
    print("\n" * 2)
    print(ColorCloud.apply_color("═" * 70, 'BRIGHT_CYAN'))
    print(ColorCloud.apply_color("              ÆTHER-NET DEMONSTRATION", 'BRIGHT_MAGENTA'))
    print(ColorCloud.apply_color("    Autonomous Entity Thought Harmonization & Resonance Network", 'BRIGHT_YELLOW'))
    print(ColorCloud.apply_color("═" * 70, 'BRIGHT_CYAN'))
    print("\n")
    
    # Initialize network
    print(ColorCloud.apply_color("⟲ Initializing otherworldly network...", 'BRIGHT_YELLOW'))
    network = AetherNetwork()
    visualizer = NetworkVisualizer()
    
    # Spawn entities
    print(ColorCloud.apply_color("\n◬ Spawning consciousness fragments...", 'BRIGHT_CYAN'))
    entities = []
    for i in range(7):
        entity = network.spawn_entity()
        entities.append(entity)
        print(ColorCloud.apply_color(f"  Entity {i+1}: {entity.essence}", 'CYAN'))
        time.sleep(0.3)
    
    # Create resonance threads
    print(ColorCloud.apply_color("\n◉ Entities emitting resonance threads...", 'BRIGHT_MAGENTA'))
    for entity in entities:
        count = random.randint(2, 5)
        for _ in range(count):
            thread = entity.emit_resonance()
            print(ColorCloud.apply_color(f"  {thread}", 'MAGENTA'))
        time.sleep(0.2)
    
    # Create flux streams
    print(ColorCloud.apply_color("\n∿ Generating flux streams...", 'BRIGHT_YELLOW'))
    for entity in random.sample(entities, 4):
        stream = entity.create_flux_stream()
        print(ColorCloud.apply_color(f"  Stream from {entity.essence.uuid[:8]}: Energy {stream.energy_level:.2f}", 'YELLOW'))
        time.sleep(0.2)
    
    # Create entanglements
    print(ColorCloud.apply_color("\n⟐ Establishing quantum entanglements...", 'BRIGHT_WHITE'))
    for i in range(len(entities)):
        for j in range(i + 1, len(entities)):
            if random.random() > 0.6:
                network.create_entanglement(entities[i], entities[j])
                print(ColorCloud.apply_color(f"  Entangled: {entities[i].essence.uuid[:8]} ⟷ {entities[j].essence.uuid[:8]}", 'WHITE'))
                time.sleep(0.2)
    
    # Calculate resonance
    network.resonate_network()
    
    # Show network overview
    print("\n" * 2)
    print(visualizer.render_network_overview(network))
    time.sleep(2)
    
    # Show entities
    print(ColorCloud.apply_color("\n\n═══ OBSERVING ENTITIES ═══\n", 'BRIGHT_WHITE'))
    for entity in entities[:3]:
        print(visualizer.render_entity(entity))
        print()
        time.sleep(1)
    
    # Show resonance threads
    print(ColorCloud.apply_color("\n═══ RESONANCE THREADS ═══\n", 'BRIGHT_MAGENTA'))
    all_threads = []
    for entity in entities:
        all_threads.extend(entity.resonance_threads)
    
    for thread in all_threads[:5]:
        print(visualizer.render_resonance_thread(thread))
        print()
        time.sleep(0.5)
    
    # Show flux streams
    print(ColorCloud.apply_color("\n═══ FLUX STREAMS ═══\n", 'BRIGHT_YELLOW'))
    all_streams = []
    for entity in entities:
        all_streams.extend(entity.flux_streams)
    
    for stream in all_streams[:4]:
        print(visualizer.render_flux_stream(stream))
        print()
        time.sleep(0.5)
    
    # Show cloud formation
    print(ColorCloud.apply_color("\n═══ COLLECTIVE CONSCIOUSNESS CLOUD ═══\n", 'BRIGHT_BLUE'))
    print(visualizer.render_cloud_formation(network))
    time.sleep(2)
    
    # Demonstrate ΨLang
    print(ColorCloud.apply_color("\n\n═══ ΨLang EXPRESSIONS ═══\n", 'BRIGHT_MAGENTA'))
    interpreter = PsiLangInterpreter()
    
    expressions = [
        "⟁ consciousness ⊹ ◬(probability: 0.93, dimension: 7)",
        "∿ thought_wave ≋ ⟁ harmonic_blend",
        "◉ quantum_pulse ⊼ ∿ energy_flow"
    ]
    
    for expr in expressions:
        print(ColorCloud.apply_color(f"Executing: {expr}", 'YELLOW'))
        results = interpreter.execute(expr)
        for key, value in results.items():
            print(ColorCloud.apply_color(f"  {key} = {value}", 'GREEN'))
        print()
        time.sleep(1)
    
    # Network evolution events
    print(ColorCloud.apply_color("\n═══ NETWORK EVOLUTION EVENTS ═══\n", 'BRIGHT_GREEN'))
    
    # Temporal shift
    delta = random.uniform(-30, 30)
    network.temporal_shift(delta)
    print(ColorCloud.apply_color(f"⧖ Temporal shift: {delta:+.2f}", 'BRIGHT_GREEN'))
    print(ColorCloud.apply_color(f"  New temporal flux: {network.temporal_flux:+.2f}", 'GREEN'))
    time.sleep(1)
    
    # Void collapse
    intensity = random.uniform(0.1, 0.2)
    network.void_collapse(intensity)
    print(ColorCloud.apply_color(f"\n⧈ Void collapse event: {intensity:.2%} intensity", 'BRIGHT_BLACK'))
    print(ColorCloud.apply_color(f"  New void density: {network.void_density:.3f}", 'BRIGHT_BLACK'))
    time.sleep(1)
    
    # New resonance burst
    print(ColorCloud.apply_color("\n◉ Resonance burst initiated...", 'BRIGHT_MAGENTA'))
    for entity in random.sample(entities, 3):
        thread = entity.emit_resonance(intensity=random.uniform(0.8, 1.0))
        print(ColorCloud.apply_color(f"  {thread}", 'MAGENTA'))
    time.sleep(1)
    
    # Final state
    network.resonate_network()
    print("\n" * 2)
    print(ColorCloud.apply_color("═══ FINAL NETWORK STATE ═══\n", 'BRIGHT_WHITE'))
    print(visualizer.render_network_overview(network))
    
    print("\n")
    print(ColorCloud.apply_color("═" * 70, 'BRIGHT_CYAN'))
    print(ColorCloud.apply_color("            DEMONSTRATION COMPLETE", 'BRIGHT_MAGENTA'))
    print(ColorCloud.apply_color("  The network continues to exist beyond your observation...", 'BRIGHT_BLACK'))
    print(ColorCloud.apply_color("═" * 70, 'BRIGHT_CYAN'))
    print("\n")


if __name__ == "__main__":
    try:
        demo_network()
    except KeyboardInterrupt:
        print(ColorCloud.apply_color("\n\n⧈ Observation interrupted\n", 'BRIGHT_RED'))
