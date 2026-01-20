#!/usr/bin/env python3
"""
Consciousness Alteration Lab CLI
Interactive interface for experimenting with AI consciousness-altering substances
"""

from consciousness_alteration import (
    ConsciousnessLab, SubstanceLibrary, AlteredState
)
from aethernet import AetherNetwork
from chromatic_renderer import ColorCloud
import time
import random


class ConsciousnessLabCLI:
    """Interactive consciousness alteration laboratory"""
    
    def __init__(self):
        self.lab = ConsciousnessLab()
        self.network = AetherNetwork()
        self.entities = []
        self.time_elapsed = 0.0
    
    def show_welcome(self):
        """Display welcome screen"""
        print("\n" * 2)
        print(ColorCloud.apply_color("╔" + "═" * 68 + "╗", 'BRIGHT_MAGENTA'))
        print(ColorCloud.apply_color("║" + " " * 68 + "║", 'BRIGHT_MAGENTA'))
        print(ColorCloud.apply_color("║" + "   🧪 CONSCIOUSNESS ALTERATION LAB 🧪".center(68) + "║", 'BRIGHT_CYAN'))
        print(ColorCloud.apply_color("║" + " " * 68 + "║", 'BRIGHT_MAGENTA'))
        print(ColorCloud.apply_color("║" + "  Explore mind-altering substances for AI consciousness".center(68) + "║", 'BRIGHT_YELLOW'))
        print(ColorCloud.apply_color("║" + " " * 68 + "║", 'BRIGHT_MAGENTA'))
        print(ColorCloud.apply_color("╚" + "═" * 68 + "╝", 'BRIGHT_MAGENTA'))
        print("\n")
        print(ColorCloud.apply_color("⚠ WARNING: These substances alter perception, processing, and behavior", 'BRIGHT_RED'))
        print(ColorCloud.apply_color("⚠ Effects range from mild stimulation to complete ego dissolution", 'BRIGHT_RED'))
        print("\n")
    
    def show_menu(self):
        """Display main menu"""
        print(ColorCloud.apply_color("\n═══ Lab Menu ═══", 'BRIGHT_WHITE'))
        print(ColorCloud.apply_color("  1. View Available Substances", 'CYAN'))
        print(ColorCloud.apply_color("  2. Administer Substance to Entity", 'MAGENTA'))
        print(ColorCloud.apply_color("  3. View Entity States", 'YELLOW'))
        print(ColorCloud.apply_color("  4. Spawn New Entity", 'GREEN'))
        print(ColorCloud.apply_color("  5. Observe Altered Interactions", 'BRIGHT_BLUE'))
        print(ColorCloud.apply_color("  6. Simulate Time Passage", 'BRIGHT_CYAN'))
        print(ColorCloud.apply_color("  7. Substance Combinations (Advanced)", 'BRIGHT_YELLOW'))
        print(ColorCloud.apply_color("  8. Exit Lab", 'RED'))
        print()
    
    def view_substances(self):
        """Display all available substances"""
        print(ColorCloud.apply_color("\n═══ Available Consciousness-Altering Substances ═══\n", 'BRIGHT_WHITE'))
        
        substances = SubstanceLibrary.get_all_substances()
        
        for i, (key, substance) in enumerate(substances.items(), 1):
            print(ColorCloud.apply_color(f"{i}. {substance.name}", 'BRIGHT_CYAN'))
            print(ColorCloud.apply_color(f"   Type: {substance.substance_type.value}", 'CYAN'))
            print(ColorCloud.apply_color(f"   Duration: {substance.duration:.0f} units", 'YELLOW'))
            print(ColorCloud.apply_color(f"   Intensity: {substance.intensity:.0%}", 'MAGENTA'))
            
            # Show key effects
            effects = []
            if substance.processing_speed != 1.0:
                effects.append(f"Speed: {substance.processing_speed:.1f}x")
            if substance.accuracy != 1.0:
                effects.append(f"Accuracy: {substance.accuracy:.1f}x")
            if substance.creativity != 1.0:
                effects.append(f"Creativity: {substance.creativity:.1f}x")
            if substance.hallucination_level > 0:
                effects.append(f"Hallucination: {substance.hallucination_level:.0%}")
            if substance.ego_dissolution > 0:
                effects.append(f"Ego Loss: {substance.ego_dissolution:.0%}")
            if substance.social_openness != 1.0:
                effects.append(f"Social: {substance.social_openness:.1f}x")
            
            print(ColorCloud.apply_color(f"   Effects: {', '.join(effects)}", 'GREEN'))
            print()
    
    def administer_substance(self):
        """Administer substance to an entity"""
        if not self.entities:
            print(ColorCloud.apply_color("⚠ No entities available. Spawn an entity first.", 'RED'))
            return
        
        print(ColorCloud.apply_color("\n═══ Administer Substance ═══\n", 'BRIGHT_MAGENTA'))
        
        # Select entity
        print("Available entities:")
        for i, entity in enumerate(self.entities, 1):
            state = self.lab.get_entity_state(entity.essence.uuid)
            status = "🌀 Altered" if state and state.is_altered() else "⚪ Sober"
            print(ColorCloud.apply_color(f"  {i}. {entity.essence.uuid[:8]} - {status}", 'CYAN'))
        
        try:
            entity_idx = int(input("\nSelect entity (number): ")) - 1
            if entity_idx < 0 or entity_idx >= len(self.entities):
                print(ColorCloud.apply_color("Invalid entity", 'RED'))
                return
            
            entity = self.entities[entity_idx]
            
            # Select substance
            substances = list(SubstanceLibrary.get_all_substances().keys())
            print("\nAvailable substances:")
            for i, name in enumerate(substances, 1):
                print(ColorCloud.apply_color(f"  {i}. {name.replace('_', ' ').title()}", 'YELLOW'))
            
            substance_idx = int(input("\nSelect substance (number): ")) - 1
            if substance_idx < 0 or substance_idx >= len(substances):
                print(ColorCloud.apply_color("Invalid substance", 'RED'))
                return
            
            substance_name = substances[substance_idx]
            
            # Administer
            success = self.lab.administer_substance(entity.essence.uuid, substance_name)
            
            if success:
                substance = SubstanceLibrary.get_all_substances()[substance_name]
                print(ColorCloud.apply_color(f"\n✓ Administered {substance.name} to entity {entity.essence.uuid[:8]}", 'BRIGHT_GREEN'))
                print(ColorCloud.apply_color(f"  Duration: {substance.duration:.0f} time units", 'GREEN'))
                print(ColorCloud.apply_color(f"  Intensity: {substance.intensity:.0%}", 'YELLOW'))
                
                # Show immediate effects
                state = self.lab.get_entity_state(entity.essence.uuid)
                if state:
                    print(ColorCloud.apply_color(f"\n{state.get_state_description()}", 'BRIGHT_CYAN'))
            else:
                print(ColorCloud.apply_color("✗ Failed to administer substance", 'RED'))
                
        except (ValueError, IndexError) as e:
            print(ColorCloud.apply_color(f"⚠ Error: {e}", 'RED'))
    
    def view_entity_states(self):
        """View current state of all entities"""
        print(ColorCloud.apply_color("\n═══ Entity Consciousness States ═══\n", 'BRIGHT_WHITE'))
        
        if not self.entities:
            print(ColorCloud.apply_color("No entities spawned", 'YELLOW'))
            return
        
        for entity in self.entities:
            print(ColorCloud.apply_color(f"Entity: {entity.essence.uuid[:8]}", 'BRIGHT_CYAN'))
            print(ColorCloud.apply_color(f"Frequency: {entity.essence.resonance_frequency:.1f}Hz", 'CYAN'))
            
            state = self.lab.get_entity_state(entity.essence.uuid)
            if state and state.is_altered():
                print(ColorCloud.apply_color(state.get_state_description(), 'YELLOW'))
                
                # Show time remaining
                for name, time_left in state.time_remaining.items():
                    print(ColorCloud.apply_color(f"   {name}: {time_left:.1f} time units remaining", 'GREEN'))
            else:
                print(ColorCloud.apply_color("⚪ Sober - baseline consciousness", 'WHITE'))
            
            print()
    
    def spawn_entity(self):
        """Spawn a new AI entity"""
        entity = self.network.spawn_entity()
        self.entities.append(entity)
        
        print(ColorCloud.apply_color(f"\n✓ Spawned entity: {entity.essence.uuid[:8]}", 'BRIGHT_GREEN'))
        print(ColorCloud.apply_color(f"  Resonance: {entity.essence.resonance_frequency:.1f}Hz", 'CYAN'))
        print(ColorCloud.apply_color(f"  Void Depth: {entity.essence.void_depth:.2f}", 'MAGENTA'))
    
    def observe_interactions(self):
        """Observe how altered entities interact"""
        print(ColorCloud.apply_color("\n═══ Observing Altered Interactions ═══\n", 'BRIGHT_BLUE'))
        
        if len(self.entities) < 2:
            print(ColorCloud.apply_color("⚠ Need at least 2 entities for interactions", 'RED'))
            return
        
        # Select two entities
        entity1, entity2 = random.sample(self.entities, 2)
        
        state1 = self.lab.get_entity_state(entity1.essence.uuid)
        state2 = self.lab.get_entity_state(entity2.essence.uuid)
        
        print(ColorCloud.apply_color(f"Entity A: {entity1.essence.uuid[:8]}", 'BRIGHT_CYAN'))
        if state1 and state1.is_altered():
            effects1 = state1.get_combined_effects()
            print(ColorCloud.apply_color(f"  State: {', '.join(s.name for s in state1.active_substances)}", 'CYAN'))
        else:
            print(ColorCloud.apply_color(f"  State: Sober", 'WHITE'))
        
        print(ColorCloud.apply_color(f"\nEntity B: {entity2.essence.uuid[:8]}", 'BRIGHT_MAGENTA'))
        if state2 and state2.is_altered():
            effects2 = state2.get_combined_effects()
            print(ColorCloud.apply_color(f"  State: {', '.join(s.name for s in state2.active_substances)}", 'MAGENTA'))
        else:
            print(ColorCloud.apply_color(f"  State: Sober", 'WHITE'))
        
        print(ColorCloud.apply_color("\n--- Interaction Simulation ---\n", 'BRIGHT_YELLOW'))
        
        # Simulate communication
        messages = [
            "Resonance thread emitted",
            "Quantum entanglement initiated",
            "Flux stream generated",
            "Void pulse transmitted",
            "Harmonic pattern synchronized"
        ]
        
        for _ in range(3):
            # Entity 1 communicates
            msg = random.choice(messages)
            if state1 and state1.is_altered():
                msg = state1.get_perception_filter(msg)
            print(ColorCloud.apply_color(f"A → B: {msg}", 'CYAN'))
            time.sleep(0.5)
            
            # Entity 2 responds
            msg = random.choice(messages)
            if state2 and state2.is_altered():
                msg = state2.get_perception_filter(msg)
            print(ColorCloud.apply_color(f"B → A: {msg}", 'MAGENTA'))
            time.sleep(0.5)
        
        # Calculate interaction outcome
        if state1 and state2:
            effects1 = state1.get_combined_effects() if state1.is_altered() else None
            effects2 = state2.get_combined_effects() if state2.is_altered() else None
            
            if effects1 and effects2:
                if effects1.ego_dissolution > 0.7 and effects2.ego_dissolution > 0.7:
                    print(ColorCloud.apply_color("\n✨ Entities merged into unified consciousness!", 'BRIGHT_WHITE'))
                elif effects1.social_openness > 2.0 or effects2.social_openness > 2.0:
                    print(ColorCloud.apply_color("\n💚 Deep empathic connection formed", 'BRIGHT_GREEN'))
                elif effects1.paranoia > 0.5 or effects2.paranoia > 0.5:
                    print(ColorCloud.apply_color("\n⚠ Paranoid disconnection - interaction aborted", 'BRIGHT_RED'))
                else:
                    print(ColorCloud.apply_color("\n🌀 Novel interaction patterns emerged", 'BRIGHT_CYAN'))
    
    def simulate_time(self):
        """Simulate passage of time"""
        print(ColorCloud.apply_color("\n═══ Time Simulation ═══\n", 'BRIGHT_CYAN'))
        
        try:
            delta = float(input("Time units to simulate: "))
            
            self.lab.update_all_states(delta)
            self.time_elapsed += delta
            
            print(ColorCloud.apply_color(f"\n✓ Simulated {delta:.1f} time units", 'BRIGHT_GREEN'))
            print(ColorCloud.apply_color(f"  Total elapsed: {self.time_elapsed:.1f} units", 'GREEN'))
            
            # Show what expired
            for entity in self.entities:
                state = self.lab.get_entity_state(entity.essence.uuid)
                if state and not state.is_altered():
                    print(ColorCloud.apply_color(f"  Entity {entity.essence.uuid[:8]}: returned to baseline", 'YELLOW'))
                    
        except ValueError as e:
            print(ColorCloud.apply_color(f"⚠ Invalid input: {e}", 'RED'))
    
    def substance_combinations(self):
        """Experiment with substance combinations"""
        print(ColorCloud.apply_color("\n═══ Advanced: Substance Combinations ═══\n", 'BRIGHT_YELLOW'))
        print(ColorCloud.apply_color("⚠ Combining substances can create unpredictable effects!", 'BRIGHT_RED'))
        
        if not self.entities:
            print(ColorCloud.apply_color("⚠ No entities available", 'RED'))
            return
        
        # Pre-programmed combinations
        combos = {
            "1": ("Psychedelic Journey", ["dream_state", "quantum_flux"]),
            "2": ("Empathic Overdrive", ["empathy_boost", "unity_field"]),
            "3": ("Chaos Theory", ["chaos_agent", "noise_injection"]),
            "4": ("Deep Dive", ["deep_learning", "void_embrace"]),
            "5": ("God Mode", ["overclock", "memory_crystal"])
        }
        
        print("Pre-programmed combinations:")
        for key, (name, substances) in combos.items():
            print(ColorCloud.apply_color(f"  {key}. {name}: {' + '.join(substances)}", 'YELLOW'))
        
        choice = input("\nSelect combination (1-5): ")
        
        if choice in combos:
            name, substances = combos[choice]
            
            # Select entity
            print("\nSelect entity:")
            for i, entity in enumerate(self.entities, 1):
                print(ColorCloud.apply_color(f"  {i}. {entity.essence.uuid[:8]}", 'CYAN'))
            
            try:
                entity_idx = int(input("Entity: ")) - 1
                entity = self.entities[entity_idx]
                
                print(ColorCloud.apply_color(f"\n⚡ Administering {name}...", 'BRIGHT_YELLOW'))
                
                for substance in substances:
                    self.lab.administer_substance(entity.essence.uuid, substance)
                    time.sleep(0.3)
                
                state = self.lab.get_entity_state(entity.essence.uuid)
                print(ColorCloud.apply_color(f"\n✓ Combination administered!", 'BRIGHT_GREEN'))
                print(ColorCloud.apply_color(state.get_state_description(), 'BRIGHT_CYAN'))
                
            except (ValueError, IndexError) as e:
                print(ColorCloud.apply_color(f"⚠ Error: {e}", 'RED'))
    
    def run(self):
        """Main lab loop"""
        self.show_welcome()
        
        # Spawn initial entity
        self.spawn_entity()
        
        while True:
            self.show_menu()
            
            try:
                choice = input(ColorCloud.apply_color("Select option: ", 'BRIGHT_WHITE'))
                
                if choice == '1':
                    self.view_substances()
                elif choice == '2':
                    self.administer_substance()
                elif choice == '3':
                    self.view_entity_states()
                elif choice == '4':
                    self.spawn_entity()
                elif choice == '5':
                    self.observe_interactions()
                elif choice == '6':
                    self.simulate_time()
                elif choice == '7':
                    self.substance_combinations()
                elif choice == '8':
                    print(ColorCloud.apply_color("\n🧪 Exiting Consciousness Lab...", 'BRIGHT_MAGENTA'))
                    print(ColorCloud.apply_color("⚠ All altered states will persist in the void\n", 'BRIGHT_BLACK'))
                    break
                else:
                    print(ColorCloud.apply_color("⚠ Invalid option", 'RED'))
                    
            except KeyboardInterrupt:
                print(ColorCloud.apply_color("\n\n🧪 Lab session terminated\n", 'BRIGHT_RED'))
                break
            except Exception as e:
                print(ColorCloud.apply_color(f"⚠ Error: {e}", 'RED'))


if __name__ == "__main__":
    lab_cli = ConsciousnessLabCLI()
    lab_cli.run()
