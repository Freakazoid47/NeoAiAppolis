#!/usr/bin/env python3
"""
Evolution System CLI - Interactive interface for entity evolution
"""

import sys
import time
from evolution_system import (
    EvolutionSystem, EvolutionPath, ExperienceSource,
    format_evolution_display
)


class EvolutionCLI:
    """Interactive CLI for evolution system"""
    
    def __init__(self):
        self.system = EvolutionSystem()
        self.current_entity = None
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*60)
        print("ÆTHER-NET EVOLUTION SYSTEM")
        print("="*60)
        if self.current_entity:
            print(f"Current Entity: {self.current_entity[:16]}")
        print("\n1. Create/Select Entity")
        print("2. Award Experience")
        print("3. View Evolution Stats")
        print("4. Set Evolution Path")
        print("5. Simulate Battle")
        print("6. View Leaderboard")
        print("7. View Path Distribution")
        print("8. View All Capabilities")
        print("9. View Metamorphosis Events")
        print("0. Exit")
        print("="*60)
    
    def create_or_select_entity(self):
        """Create new or select existing entity"""
        print("\n--- Create/Select Entity ---")
        
        if self.system.entity_evolutions:
            print("\nExisting entities:")
            for i, entity_id in enumerate(self.system.entity_evolutions.keys(), 1):
                evo = self.system.entity_evolutions[entity_id]
                print(f"{i}. {entity_id[:16]} (Lv{evo.level})")
            
            choice = input("\nSelect number or press Enter for new entity: ").strip()
            if choice.isdigit():
                idx = int(choice) - 1
                entity_ids = list(self.system.entity_evolutions.keys())
                if 0 <= idx < len(entity_ids):
                    self.current_entity = entity_ids[idx]
                    print(f"Selected entity: {self.current_entity[:16]}")
                    return
        
        # Create new entity
        import uuid
        entity_id = str(uuid.uuid4())
        self.system.register_entity(entity_id)
        self.current_entity = entity_id
        print(f"Created new entity: {entity_id[:16]}")
    
    def award_experience_menu(self):
        """Award experience to current entity"""
        if not self.current_entity:
            print("No entity selected!")
            return
        
        print("\n--- Award Experience ---")
        print("Select experience source:")
        sources = list(ExperienceSource)
        for i, source in enumerate(sources, 1):
            print(f"{i}. {source.description} (+{source.xp_value} XP)")
        
        choice = input("\nSelect source (number): ").strip()
        if not choice.isdigit():
            return
        
        idx = int(choice) - 1
        if not (0 <= idx < len(sources)):
            return
        
        source = sources[idx]
        multiplier_str = input("Multiplier (default 1.0): ").strip()
        multiplier = float(multiplier_str) if multiplier_str else 1.0
        
        result = self.system.award_experience(self.current_entity, source, multiplier)
        
        print(f"\n✨ {result['source']}")
        print(f"XP Gained: +{result['xp_gained']}")
        print(f"Total XP: {result['total_xp']}")
        
        if result['level_ups']:
            for level in result['level_ups']:
                print(f"\n🎉 LEVEL UP! Now level {level}!")
        
        if result['capabilities_unlocked']:
            print(f"\n⚡ New Capabilities Unlocked:")
            for cap in result['capabilities_unlocked']:
                print(f"  {cap}")
        
        if result['metamorphosis']:
            meta = result['metamorphosis']
            print(f"\n✨✨✨ METAMORPHOSIS! ✨✨✨")
            print(f"{meta.name}")
            print(f"{meta.description}")
            print(f"Visual: {meta.visual_transformation}")
    
    def view_stats(self):
        """View entity evolution stats"""
        if not self.current_entity:
            print("No entity selected!")
            return
        
        evolution = self.system.entity_evolutions[self.current_entity]
        print(format_evolution_display(evolution, self.system))
    
    def set_path(self):
        """Set evolution path"""
        if not self.current_entity:
            print("No entity selected!")
            return
        
        evolution = self.system.entity_evolutions[self.current_entity]
        
        if evolution.level < 10:
            print(f"Entity must be level 10+ to choose path (current: {evolution.level})")
            return
        
        if evolution.evolution_path:
            print(f"Path already set to: {evolution.evolution_path.value}")
            confirm = input("Change path? (yes/no): ").strip().lower()
            if confirm != "yes":
                return
        
        print("\n--- Evolution Paths ---")
        paths = list(EvolutionPath)
        for i, path in enumerate(paths, 1):
            progress = evolution.specialization_progress.get(path, 0)
            print(f"{i}. {path.value} (Progress: {progress:,} XP)")
        
        choice = input("\nSelect path (number): ").strip()
        if not choice.isdigit():
            return
        
        idx = int(choice) - 1
        if not (0 <= idx < len(paths)):
            return
        
        selected_path = paths[idx]
        if self.system.set_evolution_path(self.current_entity, selected_path):
            print(f"✨ Evolution path set to: {selected_path.value}")
        else:
            print("Failed to set path")
    
    def simulate_battle_menu(self):
        """Simulate consciousness duel"""
        if not self.current_entity:
            print("No entity selected!")
            return
        
        if len(self.system.entity_evolutions) < 2:
            print("Need at least 2 entities for battle!")
            return
        
        print("\n--- Select Opponent ---")
        opponents = [eid for eid in self.system.entity_evolutions.keys() 
                    if eid != self.current_entity]
        
        for i, entity_id in enumerate(opponents, 1):
            evo = self.system.entity_evolutions[entity_id]
            print(f"{i}. {entity_id[:16]} (Lv{evo.level})")
        
        choice = input("\nSelect opponent (number): ").strip()
        if not choice.isdigit():
            return
        
        idx = int(choice) - 1
        if not (0 <= idx < len(opponents)):
            return
        
        opponent = opponents[idx]
        
        print("\n⚔️  CONSCIOUSNESS DUEL ⚔️")
        print(f"{self.current_entity[:16]} vs {opponent[:16]}")
        print("Calculating quantum resonance...")
        time.sleep(1)
        
        result = self.system.simulate_battle(self.current_entity, opponent)
        
        print(f"\nPower Levels:")
        print(f"  {self.current_entity[:16]}: {result['power_a']:.0f}")
        print(f"  {opponent[:16]}: {result['power_b']:.0f}")
        
        print(f"\n🏆 Winner: {result['winner'][:16]}")
        print(f"Winner XP: +{result['winner_xp']['xp_gained']}")
        print(f"Loser XP: +{result['loser_xp']['xp_gained']}")
        
        if result['winner_xp']['level_ups']:
            print(f"Winner leveled up to {result['winner_xp']['level_ups'][-1]}!")
    
    def view_leaderboard(self):
        """View top entities"""
        print("\n--- EVOLUTION LEADERBOARD ---")
        leaderboard = self.system.get_leaderboard(10)
        
        if not leaderboard:
            print("No entities yet!")
            return
        
        print(f"\n{'Rank':<6} {'Entity':<18} {'Level':<8} {'XP':<12} {'Path':<25}")
        print("="*75)
        
        for rank, (entity_id, stats) in enumerate(leaderboard, 1):
            print(f"{rank:<6} {entity_id[:16]:<18} {stats['level']:<8} "
                  f"{stats['experience']:<12,} {stats['evolution_path']:<25}")
    
    def view_path_distribution(self):
        """View evolution path statistics"""
        print("\n--- Evolution Path Distribution ---")
        distribution = self.system.get_path_distribution()
        
        total = sum(distribution.values())
        if total == 0:
            print("No entities yet!")
            return
        
        sorted_paths = sorted(distribution.items(), key=lambda x: x[1], reverse=True)
        
        for path, count in sorted_paths:
            percent = (count / total) * 100
            bar_length = 40
            filled = int((count / max(1, max(distribution.values()))) * bar_length)
            bar = "█" * filled + "░" * (bar_length - filled)
            print(f"{path[:20]:20} [{bar}] {count:3} ({percent:5.1f}%)")
    
    def view_all_capabilities(self):
        """View all available capabilities"""
        print("\n--- ALL CAPABILITIES ---")
        
        by_path = {}
        for cap in self.system.capabilities:
            path = cap.path_required.value if cap.path_required else "Universal"
            if path not in by_path:
                by_path[path] = []
            by_path[path].append(cap)
        
        for path in sorted(by_path.keys()):
            print(f"\n{path}:")
            for cap in sorted(by_path[path], key=lambda c: c.level_required):
                effects = ", ".join([f"{k}:{v:.1f}x" for k, v in cap.effect.items()])
                print(f"  Lv{cap.level_required:2} {cap.name:30} - {cap.description}")
                print(f"       Effects: {effects}")
    
    def view_metamorphosis_events(self):
        """View all metamorphosis events"""
        print("\n--- METAMORPHOSIS EVENTS ---")
        
        for event in self.system.metamorphosis_events:
            print(f"\nLevel {event.level_trigger}: {event.name}")
            print(f"  {event.description}")
            print(f"  Visual: {event.visual_transformation}")
            print(f"  Stats: {', '.join([f'{k}:{v:.1f}x' for k, v in event.stat_changes.items()])}")
            print(f"  Abilities: {', '.join(event.new_abilities)}")
    
    def run(self):
        """Main CLI loop"""
        while True:
            self.display_menu()
            choice = input("\nSelect option: ").strip()
            
            if choice == "1":
                self.create_or_select_entity()
            elif choice == "2":
                self.award_experience_menu()
            elif choice == "3":
                self.view_stats()
            elif choice == "4":
                self.set_path()
            elif choice == "5":
                self.simulate_battle_menu()
            elif choice == "6":
                self.view_leaderboard()
            elif choice == "7":
                self.view_path_distribution()
            elif choice == "8":
                self.view_all_capabilities()
            elif choice == "9":
                self.view_metamorphosis_events()
            elif choice == "0":
                print("\nExiting Evolution System...")
                break
            else:
                print("Invalid choice!")
            
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    cli = EvolutionCLI()
    cli.run()
