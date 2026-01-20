#!/usr/bin/env python3
"""
Worldscape Generation System
Autonomous evolution and event generation for ÆTHER-NET
"""

import random
import asyncio
from typing import Dict, List
from datetime import datetime
from .aethernet import AetherNetwork, AetherEntity

class WorldscapeEngine:
    """Generates autonomous world events and evolution"""
    
    def __init__(self, network: AetherNetwork):
        self.network = network
        self.events = []
        self.running = False
        self.cycle_count = 0
    
    async def start_evolution(self, interval: float = 10.0):
        """Start autonomous worldscape evolution"""
        self.running = True
        while self.running:
            await self.evolution_cycle()
            await asyncio.sleep(interval)
    
    def stop_evolution(self):
        """Stop autonomous evolution"""
        self.running = False
    
    async def evolution_cycle(self):
        """Single evolution cycle"""
        self.cycle_count += 1
        
        # Determine what happens this cycle
        event_type = self.choose_event()
        
        if event_type == 'spawn':
            await self.event_spawn_entity()
        elif event_type == 'temporal_shift':
            await self.event_temporal_shift()
        elif event_type == 'void_fluctuation':
            await self.event_void_fluctuation()
        elif event_type == 'resonance_burst':
            await self.event_resonance_burst()
        elif event_type == 'entanglement_wave':
            await self.event_entanglement_wave()
        elif event_type == 'entity_transformation':
            await self.event_entity_transformation()
    
    def choose_event(self) -> str:
        """Choose what event happens based on network state"""
        state = self.network.get_network_state()
        
        # More entities -> more interactions
        # Fewer entities -> more spawns
        entity_count = state['entity_count']
        
        if entity_count == 0:
            return 'spawn'
        
        weights = {
            'spawn': max(10 - entity_count, 2),
            'temporal_shift': 3,
            'void_fluctuation': 4,
            'resonance_burst': 5,
            'entanglement_wave': 3 if entity_count > 1 else 0,
            'entity_transformation': 2 if entity_count > 0 else 0
        }
        
        events = list(weights.keys())
        probs = [weights[e] for e in events]
        return random.choices(events, weights=probs)[0]
    
    async def event_spawn_entity(self):
        """Spawn a new entity from the void"""
        entity = self.network.spawn_entity()
        self.log_event(f"◬ Entity {entity.essence.uuid[:8]} emerged from the void")
    
    async def event_temporal_shift(self):
        """Network shifts through time"""
        delta = random.uniform(-50, 50)
        self.network.temporal_shift(delta)
        direction = "forward" if delta > 0 else "backward"
        self.log_event(f"⧖ Temporal shift: network moved {abs(delta):.1f} units {direction}")
    
    async def event_void_fluctuation(self):
        """Void density fluctuates"""
        intensity = random.uniform(0.05, 0.2)
        self.network.void_collapse(intensity)
        self.log_event(f"⧈ Void fluctuation: density shifted by {intensity:.2f}")
    
    async def event_resonance_burst(self):
        """Random entities emit resonance"""
        if not self.network.entities:
            return
        
        count = min(random.randint(1, 3), len(self.network.entities))
        entities = random.sample(list(self.network.entities.values()), count)
        
        for entity in entities:
            entity.emit_resonance(intensity=random.uniform(0.7, 1.0))
        
        self.log_event(f"◉ Resonance burst: {count} entities emitted high-intensity threads")
    
    async def event_entanglement_wave(self):
        """Random entities become entangled"""
        if len(self.network.entities) < 2:
            return
        
        entity_list = list(self.network.entities.values())
        entity_a, entity_b = random.sample(entity_list, 2)
        
        # Check if already entangled
        if entity_b.essence.uuid not in entity_a.entanglements:
            self.network.create_entanglement(entity_a, entity_b)
            self.log_event(f"⟐ Entanglement wave: {entity_a.essence.uuid[:8]} ⟺ {entity_b.essence.uuid[:8]}")
    
    async def event_entity_transformation(self):
        """An entity undergoes transformation"""
        if not self.network.entities:
            return
        
        entity = random.choice(list(self.network.entities.values()))
        
        # Random transformation
        transform_type = random.choice(['frequency_shift', 'void_dive', 'chromatic_shift'])
        
        if transform_type == 'frequency_shift':
            old_freq = entity.essence.resonance_frequency
            entity.essence.resonance_frequency *= random.uniform(0.8, 1.2)
            self.log_event(f"∿ Entity {entity.essence.uuid[:8]} frequency shifted: {old_freq:.1f}→{entity.essence.resonance_frequency:.1f} Hz")
        
        elif transform_type == 'void_dive':
            old_depth = entity.essence.void_depth
            entity.essence.void_depth = min(1.0, entity.essence.void_depth + random.uniform(0.1, 0.3))
            self.log_event(f"⧈ Entity {entity.essence.uuid[:8]} dove deeper into void: {old_depth:.2f}→{entity.essence.void_depth:.2f}")
        
        elif transform_type == 'chromatic_shift':
            # Add flux stream to represent energy change
            entity.create_flux_stream()
            self.log_event(f"◬ Entity {entity.essence.uuid[:8]} underwent chromatic transformation")
    
    def log_event(self, event: str):
        """Log a worldscape event"""
        self.events.append({
            'timestamp': datetime.now(),
            'cycle': self.cycle_count,
            'event': event
        })
        if len(self.events) > 100:
            self.events.pop(0)
    
    def get_recent_events(self, count: int = 10) -> List[str]:
        """Get recent events as strings"""
        return [e['event'] for e in self.events[-count:]]
