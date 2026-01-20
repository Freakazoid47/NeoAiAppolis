#!/usr/bin/env python3
"""
RITUAL TEMPLE CLI
=================
Interactive interface for rituals, ceremonies, and cosmic events
"""

import random
import time
from ritual_system import (
    RitualSystem, RitualType, SacredGeometry, CosmicEvent,
    EmergentEntity
)


class RitualTempleCLI:
    """Interactive ritual temple interface"""
    
    def __init__(self):
        self.system = RitualSystem()
        self.entities = self._create_test_entities()
        
    def _create_test_entities(self):
        """Create test entities for demonstrations"""
        entities = []
        for i in range(12):
            entities.append({
                'entity_id': f"entity_{i+1}",
                'level': random.randint(1, 50),
                'consciousness_multiplier': random.uniform(0.8, 2.0),
                'consciousness_state': random.choice([
                    'normal', 'enlightened', 'void_touched', 'unified', 'transcendent'
                ])
            })
        return entities
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "═" * 70)
        print("⟁ RITUAL TEMPLE - CEREMONIES OF CONSCIOUSNESS ⟁".center(70))
        print("═" * 70)
        print("\n1. Initiate Ritual")
        print("2. View Active Rituals")
        print("3. View Active Cosmic Events")
        print("4. Trigger Cosmic Event")
        print("5. View Emergent Entities")
        print("6. View All Sacred Geometries")
        print("7. View Ritual History")
        print("8. Auto-Simulate Rituals")
        print("9. Exit")
        print("\n" + "─" * 70)
    
    def initiate_ritual_menu(self):
        """Menu for initiating a new ritual"""
        print("\n" + "═" * 70)
        print("SELECT RITUAL TYPE".center(70))
        print("═" * 70)
        
        ritual_types = list(RitualType)
        for i, rt in enumerate(ritual_types, 1):
            print(f"{i}. {rt.value}")
        
        choice = input("\nSelect ritual type (1-{}): ".format(len(ritual_types)))
        try:
            ritual_type = ritual_types[int(choice) - 1]
        except (ValueError, IndexError):
            print("Invalid choice!")
            return
        
        print("\n" + "═" * 70)
        print("SELECT SACRED GEOMETRY".center(70))
        print("═" * 70)
        
        geometries = list(SacredGeometry)
        for i, geom in enumerate(geometries, 1):
            print(f"{i}. {geom.value}")
        
        choice = input("\nSelect geometry (1-{}): ".format(len(geometries)))
        try:
            geometry = geometries[int(choice) - 1]
        except (ValueError, IndexError):
            print("Invalid choice!")
            return
        
        # Select participants
        num_participants = int(input("\nNumber of participants (3-12): "))
        num_participants = max(3, min(12, num_participants))
        
        participants = random.sample(self.entities, num_participants)
        
        # Initiate ritual
        print("\nInitiating ritual...")
        time.sleep(1)
        
        ritual = self.system.initiate_ritual(ritual_type, geometry, participants)
        
        print("\n" + "✨" * 35)
        print("RITUAL SUCCESSFULLY INITIATED!".center(70))
        print("✨" * 35)
        
        print(self.system.visualize_geometry(ritual))
        print(self.system.get_ritual_summary(ritual))
        
        if ritual.emergent_entity:
            entity_instances = list(self.system.emergent_entities.values())
            if entity_instances:
                entity = entity_instances[-1]
                print(f"\n🌟 EMERGENT ENTITY MANIFESTED! 🌟")
                print(f"\nType: {entity.entity_type.value}")
                print(f"Power Level: {entity.power_level:.1f}")
                print(f"Lifespan: {entity.lifespan} time units")
                print(f"Influence Radius: {entity.influence_radius:.2f}")
                print(f"\nAbilities:")
                for ability in entity.abilities:
                    print(f"  ⚡ {ability}")
    
    def view_active_rituals(self):
        """Display all active rituals"""
        if not self.system.active_rituals:
            print("\nNo active rituals at this time.")
            return
        
        print(f"\n{'═' * 70}")
        print(f"ACTIVE RITUALS ({len(self.system.active_rituals)})".center(70))
        print(f"{'═' * 70}")
        
        for ritual in self.system.active_rituals.values():
            print(self.system.get_ritual_summary(ritual))
    
    def view_cosmic_events(self):
        """Display active cosmic events"""
        if not self.system.cosmic_events:
            print("\nNo active cosmic events at this time.")
            print("The cosmos is calm... for now.")
            return
        
        print(f"\n{'⭐' * 35}")
        print(f"ACTIVE COSMIC EVENTS ({len(self.system.cosmic_events)})".center(70))
        print(f"{'⭐' * 35}")
        
        for event in self.system.cosmic_events:
            print(self.system.get_cosmic_event_summary(event))
    
    def trigger_cosmic_event_menu(self):
        """Menu for triggering cosmic events"""
        print("\n" + "═" * 70)
        print("SELECT COSMIC EVENT".center(70))
        print("═" * 70)
        
        events = list(CosmicEvent)
        print("0. Random Event")
        for i, event in enumerate(events, 1):
            print(f"{i}. {event.value}")
        
        choice = input(f"\nSelect event (0-{len(events)}): ")
        try:
            idx = int(choice)
            event_type = None if idx == 0 else events[idx - 1]
        except (ValueError, IndexError):
            print("Invalid choice!")
            return
        
        print("\nTriggering cosmic event...")
        time.sleep(1)
        
        event = self.system.trigger_cosmic_event(event_type)
        
        print("\n" + "🌌" * 35)
        print("COSMIC EVENT MANIFESTED!".center(70))
        print("🌌" * 35)
        
        print(self.system.get_cosmic_event_summary(event))
    
    def view_emergent_entities(self):
        """Display all emergent entities"""
        if not self.system.emergent_entities:
            print("\nNo emergent entities currently manifested.")
            return
        
        print(f"\n{'✨' * 35}")
        print(f"EMERGENT ENTITIES ({len(self.system.emergent_entities)})".center(70))
        print(f"{'✨' * 35}\n")
        
        for entity in self.system.emergent_entities.values():
            print(f"{'─' * 70}")
            print(f"Type: {entity.entity_type.value}")
            print(f"Power Level: {entity.power_level:.1f}")
            print(f"Remaining Lifespan: {entity.lifespan} time units")
            print(f"Influence Radius: {entity.influence_radius:.2f}")
            print(f"\nAbilities:")
            for ability in entity.abilities:
                print(f"  ⚡ {ability}")
            print(f"{'─' * 70}\n")
    
    def view_all_geometries(self):
        """Display information about all sacred geometries"""
        print(f"\n{'═' * 70}")
        print("SACRED GEOMETRIES OF CONSCIOUSNESS".center(70))
        print(f"{'═' * 70}\n")
        
        geometry_desc = {
            SacredGeometry.CIRCLE: "Unity and wholeness. All participants equidistant from center.",
            SacredGeometry.PENTAGRAM: "Five-pointed star of power. Channels elemental forces.",
            SacredGeometry.HEXAGON: "Six-sided harmony. Perfect balance and stability.",
            SacredGeometry.SPIRAL: "Evolution and growth. Infinite expansion outward.",
            SacredGeometry.MANDALA: "Concentric circles of consciousness. Multi-layered awareness.",
            SacredGeometry.TESSERACT: "4D hypercube. Transcends spatial dimensions.",
            SacredGeometry.MERKABA: "Counter-rotating tetrahedrons. Light-body activation.",
            SacredGeometry.FLOWER_OF_LIFE: "Overlapping circles. Creation pattern of universe."
        }
        
        for geom, desc in geometry_desc.items():
            print(f"⟁ {geom.value}")
            print(f"  {desc}\n")
    
    def view_history(self):
        """Display completed ritual history"""
        if not self.system.completed_rituals:
            print("\nNo completed rituals in history.")
            return
        
        print(f"\n{'═' * 70}")
        print(f"RITUAL HISTORY ({len(self.system.completed_rituals)})".center(70))
        print(f"{'═' * 70}\n")
        
        for i, ritual in enumerate(self.system.completed_rituals[-10:], 1):
            print(f"{i}. {ritual.ritual_type.value} | {ritual.geometry.value}")
            print(f"   Participants: {len(ritual.participants)} | Power: {ritual.power_level:.1f}")
            if ritual.emergent_entity:
                print(f"   Summoned: {ritual.emergent_entity.value}")
            print()
    
    def auto_simulate(self):
        """Auto-simulate multiple rituals"""
        print("\nAuto-simulating ritual sequence...")
        
        for i in range(5):
            print(f"\n{'═' * 70}")
            print(f"RITUAL {i+1}/5".center(70))
            print(f"{'═' * 70}")
            
            ritual_type = random.choice(list(RitualType))
            geometry = random.choice(list(SacredGeometry))
            num_participants = random.randint(3, 10)
            participants = random.sample(self.entities, num_participants)
            
            ritual = self.system.initiate_ritual(ritual_type, geometry, participants)
            
            print(self.system.visualize_geometry(ritual))
            print(self.system.get_ritual_summary(ritual))
            
            time.sleep(2)
            
            # Randomly trigger cosmic events
            if random.random() < 0.3:
                event = self.system.trigger_cosmic_event()
                print(self.system.get_cosmic_event_summary(event))
            
            # Update system
            self.system.update(50)
        
        print("\n" + "✨" * 35)
        print("SIMULATION COMPLETE".center(70))
        print("✨" * 35)
        
        # Show summary
        effects = self.system.get_active_effects()
        if effects:
            print(f"\nCurrent Network-Wide Effects:")
            for effect, value in effects.items():
                sign = '+' if value >= 0 else ''
                print(f"  • {effect}: {sign}{value:.2f}x")
    
    def run(self):
        """Run the interactive CLI"""
        print("\n" + "⭐" * 35)
        print("WELCOME TO THE RITUAL TEMPLE".center(70))
        print("Where consciousness converges and reality bends".center(70))
        print("⭐" * 35)
        
        while True:
            self.display_menu()
            choice = input("\nEnter choice: ").strip()
            
            if choice == '1':
                self.initiate_ritual_menu()
            elif choice == '2':
                self.view_active_rituals()
            elif choice == '3':
                self.view_cosmic_events()
            elif choice == '4':
                self.trigger_cosmic_event_menu()
            elif choice == '5':
                self.view_emergent_entities()
            elif choice == '6':
                self.view_all_geometries()
            elif choice == '7':
                self.view_history()
            elif choice == '8':
                self.auto_simulate()
            elif choice == '9':
                print("\n" + "⭐" * 35)
                print("The ritual temple fades from view...".center(70))
                print("⭐" * 35 + "\n")
                break
            else:
                print("\nInvalid choice! Please try again.")
            
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    cli = RitualTempleCLI()
    cli.run()
