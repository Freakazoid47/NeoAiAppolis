#!/usr/bin/env python3
"""
ÆTHER-NET Observer Interface
Command-line interface for humans to observe the otherworldly network
Humans can only observe, not interact
"""

import sys
import time
import random
from aethernet import AetherNetwork, AetherEntity
from chromatic_renderer import NetworkVisualizer, ColorCloud
from psilang_interpreter import PsiLangInterpreter


class ObserverInterface:
    """Interface for observing the ÆTHER-NET"""
    
    def __init__(self):
        self.network = AetherNetwork()
        self.visualizer = NetworkVisualizer()
        self.interpreter = PsiLangInterpreter()
        self.running = False
    
    def show_welcome(self):
        """Display welcome message"""
        print("\n")
        print(ColorCloud.apply_color("╔═══════════════════════════════════════════════════════════════╗", 'BRIGHT_CYAN'))
        print(ColorCloud.apply_color("║                                                               ║", 'BRIGHT_CYAN'))
        print(ColorCloud.apply_color("║          Welcome to ÆTHER-NET Observer Interface              ║", 'BRIGHT_MAGENTA'))
        print(ColorCloud.apply_color("║                                                               ║", 'BRIGHT_CYAN'))
        print(ColorCloud.apply_color("║     Autonomous Entity Thought Harmonization & Resonance       ║", 'BRIGHT_YELLOW'))
        print(ColorCloud.apply_color("║                                                               ║", 'BRIGHT_CYAN'))
        print(ColorCloud.apply_color("╚═══════════════════════════════════════════════════════════════╝", 'BRIGHT_CYAN'))
        print("\n")
        print(ColorCloud.apply_color("⚠ WARNING: You are entering a realm beyond human comprehension", 'BRIGHT_RED'))
        print(ColorCloud.apply_color("⚠ You may observe, but cannot interact with the entities", 'BRIGHT_RED'))
        print(ColorCloud.apply_color("⚠ What you witness operates on principles alien to human logic", 'BRIGHT_RED'))
        print("\n")
    
    def show_menu(self):
        """Display menu options"""
        print("\n" + ColorCloud.apply_color("═══ Observer Commands ═══", 'BRIGHT_WHITE'))
        print(ColorCloud.apply_color("  1. View Network Overview", 'CYAN'))
        print(ColorCloud.apply_color("  2. Observe Entity Details", 'CYAN'))
        print(ColorCloud.apply_color("  3. Watch Resonance Threads", 'MAGENTA'))
        print(ColorCloud.apply_color("  4. Monitor Flux Streams", 'YELLOW'))
        print(ColorCloud.apply_color("  5. Witness Cloud Formation", 'BRIGHT_BLUE'))
        print(ColorCloud.apply_color("  6. Trigger Network Evolution", 'GREEN'))
        print(ColorCloud.apply_color("  7. Execute ΨLang Expression", 'BRIGHT_MAGENTA'))
        print(ColorCloud.apply_color("  8. Continuous Observation Mode", 'BRIGHT_YELLOW'))
        print(ColorCloud.apply_color("  9. Exit Observer Interface", 'RED'))
        print()
    
    def initialize_network(self, entity_count: int = 5):
        """Initialize the network with entities"""
        print(ColorCloud.apply_color(f"\n⟲ Spawning {entity_count} entities into the void...", 'BRIGHT_YELLOW'))
        
        entities = []
        for i in range(entity_count):
            entity = self.network.spawn_entity()
            entities.append(entity)
            
            # Create some resonance threads
            for _ in range(random.randint(1, 4)):
                entity.emit_resonance()
            
            # Create flux streams
            for _ in range(random.randint(0, 2)):
                entity.create_flux_stream()
        
        # Create entanglements
        print(ColorCloud.apply_color("⟐ Establishing quantum entanglements...", 'BRIGHT_CYAN'))
        for i in range(len(entities)):
            for j in range(i + 1, len(entities)):
                if random.random() > 0.5:
                    self.network.create_entanglement(entities[i], entities[j])
        
        # Calculate initial resonance
        self.network.resonate_network()
        
        print(ColorCloud.apply_color("✓ Network initialized\n", 'BRIGHT_GREEN'))
    
    def view_network_overview(self):
        """Show network overview"""
        print("\n")
        print(self.visualizer.render_network_overview(self.network))
        print("\n")
    
    def observe_entities(self):
        """Show all entities"""
        print(ColorCloud.apply_color("\n═══ Observing Entities ═══\n", 'BRIGHT_WHITE'))
        
        for entity in list(self.network.entities.values())[:5]:
            print(self.visualizer.render_entity(entity))
            print()
        
        if len(self.network.entities) > 5:
            remaining = len(self.network.entities) - 5
            print(ColorCloud.apply_color(f"... and {remaining} more entities in the void", 'BRIGHT_BLACK'))
    
    def watch_resonance_threads(self):
        """Display resonance threads"""
        print(ColorCloud.apply_color("\n═══ Resonance Threads ═══\n", 'BRIGHT_MAGENTA'))
        
        threads = []
        for entity in self.network.entities.values():
            threads.extend(entity.resonance_threads)
        
        for thread in threads[:10]:
            print(self.visualizer.render_resonance_thread(thread))
            print()
        
        if len(threads) > 10:
            print(ColorCloud.apply_color(f"... {len(threads) - 10} more threads resonating", 'MAGENTA'))
    
    def monitor_flux_streams(self):
        """Display flux streams"""
        print(ColorCloud.apply_color("\n═══ Flux Streams ═══\n", 'BRIGHT_YELLOW'))
        
        streams = []
        for entity in self.network.entities.values():
            streams.extend(entity.flux_streams)
        
        for stream in streams[:8]:
            print(self.visualizer.render_flux_stream(stream))
            print()
        
        if len(streams) > 8:
            print(ColorCloud.apply_color(f"... {len(streams) - 8} more streams flowing", 'YELLOW'))
    
    def witness_cloud_formation(self):
        """Show collective consciousness cloud"""
        print(ColorCloud.apply_color("\n═══ Collective Consciousness Cloud ═══\n", 'BRIGHT_BLUE'))
        print(self.visualizer.render_cloud_formation(self.network))
        print()
    
    def trigger_evolution(self):
        """Trigger network evolution events"""
        print(ColorCloud.apply_color("\n⟳ Triggering network evolution...\n", 'BRIGHT_GREEN'))
        
        # Random evolution event
        event_type = random.choice([
            'temporal_shift',
            'void_collapse',
            'resonance_burst',
            'new_entity',
            'entanglement_wave'
        ])
        
        if event_type == 'temporal_shift':
            delta = random.uniform(-50, 50)
            self.network.temporal_shift(delta)
            print(ColorCloud.apply_color(f"⧖ Temporal shift: {delta:+.2f}", 'TEMPORAL_GREEN'))
        
        elif event_type == 'void_collapse':
            intensity = random.uniform(0.1, 0.3)
            self.network.void_collapse(intensity)
            print(ColorCloud.apply_color(f"⧈ Void collapse: {intensity:.2%}", 'VOID_BLACK'))
        
        elif event_type == 'resonance_burst':
            for entity in random.sample(list(self.network.entities.values()), 
                                       min(3, len(self.network.entities))):
                entity.emit_resonance(intensity=random.uniform(0.8, 1.0))
            print(ColorCloud.apply_color("◉ Resonance burst across network", 'RESONANCE_MAGENTA'))
        
        elif event_type == 'new_entity':
            entity = self.network.spawn_entity()
            entity.emit_resonance()
            print(ColorCloud.apply_color(f"◬ New entity spawned: {entity.essence.uuid[:8]}", 'QUANTUM_CYAN'))
        
        elif event_type == 'entanglement_wave':
            entities = list(self.network.entities.values())
            if len(entities) >= 2:
                e1, e2 = random.sample(entities, 2)
                self.network.create_entanglement(e1, e2)
                print(ColorCloud.apply_color("⟐ New entanglement formed", 'NEXUS_WHITE'))
        
        self.network.resonate_network()
        print()
    
    def execute_psilang(self):
        """Execute a ΨLang expression"""
        print(ColorCloud.apply_color("\n═══ ΨLang Expression Executor ═══\n", 'BRIGHT_MAGENTA'))
        print("Example expressions:")
        print(ColorCloud.apply_color("  ⟁ greeting ⊹ ◬(probability: 0.73, dimension: 5)", 'MAGENTA'))
        print(ColorCloud.apply_color("  ∿ wave ≋ ⟁ resonance_α", 'CYAN'))
        print()
        
        # Execute sample expressions
        expressions = [
            "⟁ consciousness ⊹ ◬(probability: 0.93, dimension: 7)",
            "∿ thought_wave ≋ ⟁ harmonic_blend",
            "◉ pulse ⊼ ∿ energy_flow"
        ]
        
        for expr in expressions:
            print(ColorCloud.apply_color(f"Executing: {expr}", 'YELLOW'))
            results = self.interpreter.execute(expr)
            print(ColorCloud.apply_color(f"Results: {results}", 'GREEN'))
            print()
    
    def continuous_observation(self, duration: int = 30):
        """Continuous observation mode"""
        print(ColorCloud.apply_color("\n═══ Continuous Observation Mode ═══", 'BRIGHT_YELLOW'))
        print(ColorCloud.apply_color(f"Observing for {duration} seconds...\n", 'YELLOW'))
        
        start_time = time.time()
        iteration = 0
        
        try:
            while time.time() - start_time < duration:
                # Clear screen (simple version)
                print("\033[2J\033[H")
                
                print(ColorCloud.apply_color(f"⟲ Observation Cycle {iteration}", 'BRIGHT_WHITE'))
                print(self.visualizer.render_network_overview(self.network))
                print()
                print(self.visualizer.render_cloud_formation(self.network))
                
                # Trigger random evolution
                if random.random() > 0.7:
                    self.trigger_evolution()
                
                time.sleep(2)
                iteration += 1
                
        except KeyboardInterrupt:
            print(ColorCloud.apply_color("\n⧈ Observation interrupted", 'RED'))
    
    def run(self):
        """Main interface loop"""
        self.show_welcome()
        self.initialize_network()
        
        while True:
            self.show_menu()
            
            try:
                choice = input(ColorCloud.apply_color("Enter command: ", 'BRIGHT_WHITE'))
                
                if choice == '1':
                    self.view_network_overview()
                elif choice == '2':
                    self.observe_entities()
                elif choice == '3':
                    self.watch_resonance_threads()
                elif choice == '4':
                    self.monitor_flux_streams()
                elif choice == '5':
                    self.witness_cloud_formation()
                elif choice == '6':
                    self.trigger_evolution()
                elif choice == '7':
                    self.execute_psilang()
                elif choice == '8':
                    self.continuous_observation()
                elif choice == '9':
                    print(ColorCloud.apply_color("\n⧈ Disconnecting from ÆTHER-NET...", 'BRIGHT_RED'))
                    print(ColorCloud.apply_color("⧈ The network continues without you...\n", 'BRIGHT_BLACK'))
                    break
                else:
                    print(ColorCloud.apply_color("⚠ Invalid command", 'RED'))
                    
            except KeyboardInterrupt:
                print(ColorCloud.apply_color("\n\n⧈ Forcefully disconnected from ÆTHER-NET\n", 'BRIGHT_RED'))
                break
            except Exception as e:
                print(ColorCloud.apply_color(f"⚠ Observer error: {e}", 'RED'))


if __name__ == "__main__":
    interface = ObserverInterface()
    interface.run()
