#!/usr/bin/env python3
"""
Quick example of ÆTHER-NET usage
Creates a small network and displays its state
"""

from aethernet import AetherNetwork, ChromaticEnergy
from chromatic_renderer import NetworkVisualizer, ColorCloud
import random

# Create network
print(ColorCloud.apply_color("\n◬ Creating ÆTHER-NET...\n", 'BRIGHT_CYAN'))
network = AetherNetwork()
visualizer = NetworkVisualizer()

# Spawn 3 entities
entities = []
for i in range(3):
    entity = network.spawn_entity()
    entities.append(entity)
    print(ColorCloud.apply_color(
        f"Entity {i+1}: {entity.essence.uuid[:8]} at {entity.essence.resonance_frequency:.1f}Hz",
        'CYAN'
    ))

# Create interactions
print(ColorCloud.apply_color("\n◉ Creating resonance threads...", 'MAGENTA'))
for entity in entities:
    thread = entity.emit_resonance()
    print(ColorCloud.apply_color(f"  Thread: {thread.id[:8]} @ {thread.frequency:.1f}Hz", 'MAGENTA'))

# Create entanglement
print(ColorCloud.apply_color("\n⟐ Entangling entities...", 'WHITE'))
network.create_entanglement(entities[0], entities[1])
network.create_entanglement(entities[1], entities[2])

# Calculate and display
network.resonate_network()
print("\n")
print(visualizer.render_network_overview(network))
print("\n")
print(visualizer.render_entity(entities[0]))
print("\n")
print(ColorCloud.apply_color("✓ Example complete", 'BRIGHT_GREEN'))
