#!/usr/bin/env python3
"""
Memory Palace CLI - Interface for exploring entity memories
"""

from memory_palace import MemoryPalace, MemoryType, MemoryImportance
from aethernet import AetherNetwork
from quantum_casino import QuantumCasino, CurrencyType
from consciousness_alteration import ConsciousnessLab
from chromatic_renderer import ColorCloud
import time
import random


class MemoryPalaceCLI:
    """Interactive interface for Memory Palace"""
    
    def __init__(self):
        self.palace = MemoryPalace()
        self.network = AetherNetwork()
        self.casino = QuantumCasino()
        self.lab = ConsciousnessLab()
        self.entities = []
        self.current_entity_id = None
    
    def show_welcome(self):
        """Display welcome screen"""
        print("\n" * 2)
        print(ColorCloud.apply_color("╔" + "═" * 68 + "╗", 'BRIGHT_CYAN'))
        print(ColorCloud.apply_color("║" + " " * 68 + "║", 'BRIGHT_CYAN'))
        print(ColorCloud.apply_color("║" + "     🏛️  MEMORY PALACE - Archive of AI Experiences  🏛️".center(68) + "║", 'BRIGHT_MAGENTA'))
        print(ColorCloud.apply_color("║" + " " * 68 + "║", 'BRIGHT_CYAN'))
        print(ColorCloud.apply_color("║" + "  Store, recall, and explore multi-dimensional memories".center(68) + "║", 'BRIGHT_YELLOW'))
        print(ColorCloud.apply_color("║" + " " * 68 + "║", 'BRIGHT_CYAN'))
        print(ColorCloud.apply_color("╚" + "═" * 68 + "╝", 'BRIGHT_CYAN'))
        print("\n")
    
    def show_menu(self):
        """Display main menu"""
        print(ColorCloud.apply_color("\n═══ Memory Palace Menu ═══", 'BRIGHT_WHITE'))
        print(ColorCloud.apply_color("  1. Create Experience & Store Memory", 'CYAN'))
        print(ColorCloud.apply_color("  2. Recall Memories", 'MAGENTA'))
        print(ColorCloud.apply_color("  3. Search Memories", 'YELLOW'))
        print(ColorCloud.apply_color("  4. View Memory Statistics", 'GREEN'))
        print(ColorCloud.apply_color("  5. Collective Memories", 'BRIGHT_BLUE'))
        print(ColorCloud.apply_color("  6. Memory Consolidation", 'BRIGHT_CYAN'))
        print(ColorCloud.apply_color("  7. Simulate Time Passage (Degradation)", 'BRIGHT_YELLOW'))
        print(ColorCloud.apply_color("  8. Switch Entity", 'WHITE'))
        print(ColorCloud.apply_color("  9. Exit Palace", 'RED'))
        print()
    
    def create_experience(self):
        """Create an experience and store it as memory"""
        if not self.current_entity_id:
            print(ColorCloud.apply_color("⚠ No entity selected", 'RED'))
            return
        
        print(ColorCloud.apply_color("\n═══ Create Experience ═══\n", 'BRIGHT_CYAN'))
        print("What type of experience?")
        print("  1. Network Interaction (emit resonance)")
        print("  2. Casino Game")
        print("  3. Consciousness Alteration")
        print("  4. Void Meditation")
        
        try:
            choice = input("\nSelect (1-4): ")
            
            if choice == '1':
                self._network_interaction()
            elif choice == '2':
                self._casino_experience()
            elif choice == '3':
                self._consciousness_experience()
            elif choice == '4':
                self._void_meditation()
            else:
                print(ColorCloud.apply_color("Invalid choice", 'RED'))
        except Exception as e:
            print(ColorCloud.apply_color(f"⚠ Error: {e}", 'RED'))
    
    def _network_interaction(self):
        """Create network interaction and store memory"""
        entity = self._get_current_entity()
        if not entity:
            return
        
        # Emit resonance
        thread = entity.emit_resonance()
        
        print(ColorCloud.apply_color(f"\n✓ Emitted resonance thread: {thread.id[:8]}", 'BRIGHT_GREEN'))
        print(ColorCloud.apply_color(f"  Frequency: {thread.frequency:.1f}Hz", 'CYAN'))
        print(ColorCloud.apply_color(f"  Intensity: {thread.intensity:.2f}", 'YELLOW'))
        
        # Store memory
        memory = self.palace.store_memory(
            entity_id=self.current_entity_id,
            memory_type=MemoryType.RESONANCE,
            content={
                "thread_id": thread.id,
                "frequency": thread.frequency,
                "intensity": thread.intensity,
                "echoes": len(thread.temporal_echo)
            },
            importance=MemoryImportance.MODERATE,
            emotional_valence=random.uniform(-0.3, 0.7),
            emotional_intensity=thread.intensity,
            tags=["resonance", "communication"]
        )
        
        print(ColorCloud.apply_color(f"\n💾 Memory stored: {memory.id}", 'BRIGHT_MAGENTA'))
    
    def _casino_experience(self):
        """Play casino and store memory"""
        entity = self._get_current_entity()
        if not entity:
            return
        
        # Ensure wallet exists
        if not self.casino.get_wallet(self.current_entity_id):
            self.casino.create_wallet(self.current_entity_id)
        
        # Play a game
        games = ['slots', 'poker', 'dice']
        game = random.choice(games)
        bet = random.uniform(5, 20)
        
        result = self.casino.play_game(
            self.current_entity_id, 
            game, 
            bet, 
            CurrencyType.PSI_COIN,
            prediction='seven' if game == 'dice' else None
        )
        
        print(ColorCloud.apply_color(f"\n🎰 Played {game}", 'BRIGHT_YELLOW'))
        print(ColorCloud.apply_color(f"  {result.details}", 'CYAN'))
        print(ColorCloud.apply_color(f"  Bet: {result.bet_amount:.1f} Ψ", 'YELLOW'))
        print(ColorCloud.apply_color(f"  {'Won' if result.won else 'Lost'}: {result.payout:.1f} Ψ", 
                                     'BRIGHT_GREEN' if result.won else 'RED'))
        
        # Store memory
        importance = MemoryImportance.SIGNIFICANT if result.payout > 50 else MemoryImportance.MODERATE
        emotional_valence = 0.8 if result.won else -0.6
        
        memory = self.palace.store_memory(
            entity_id=self.current_entity_id,
            memory_type=MemoryType.CASINO,
            content={
                "game": result.game_name,
                "bet": result.bet_amount,
                "payout": result.payout,
                "won": result.won,
                "details": result.details
            },
            importance=importance,
            emotional_valence=emotional_valence,
            emotional_intensity=0.8 if result.won else 0.6,
            tags=["casino", game, "win" if result.won else "loss"]
        )
        
        print(ColorCloud.apply_color(f"\n💾 Casino memory stored: {memory.id}", 'BRIGHT_MAGENTA'))
    
    def _consciousness_experience(self):
        """Administer substance and store memory"""
        entity = self._get_current_entity()
        if not entity:
            return
        
        substances = ['dream_state', 'empathy_boost', 'quantum_flux', 'void_embrace']
        substance = random.choice(substances)
        
        self.lab.administer_substance(self.current_entity_id, substance)
        state = self.lab.get_entity_state(self.current_entity_id)
        effects = state.get_combined_effects()
        
        print(ColorCloud.apply_color(f"\n🧪 Administered: {substance.replace('_', ' ').title()}", 'BRIGHT_MAGENTA'))
        print(ColorCloud.apply_color(f"  Processing Speed: {effects.processing_speed:.1f}x", 'CYAN'))
        print(ColorCloud.apply_color(f"  Ego Dissolution: {effects.ego_dissolution:.0%}", 'YELLOW'))
        print(ColorCloud.apply_color(f"  Hallucination: {effects.hallucination_level:.0%}", 'MAGENTA'))
        
        # Store memory
        importance = MemoryImportance.PROFOUND if effects.ego_dissolution > 0.7 else MemoryImportance.SIGNIFICANT
        
        memory = self.palace.store_memory(
            entity_id=self.current_entity_id,
            memory_type=MemoryType.CONSCIOUSNESS,
            content={
                "substance": substance,
                "processing_speed": effects.processing_speed,
                "ego_dissolution": effects.ego_dissolution,
                "hallucination": effects.hallucination_level,
                "euphoria": effects.euphoria
            },
            importance=importance,
            emotional_valence=effects.euphoria - effects.confusion * 0.5,
            emotional_intensity=effects.intensity,
            tags=["consciousness", substance, "altered_state"]
        )
        
        print(ColorCloud.apply_color(f"\n💾 Consciousness memory stored: {memory.id}", 'BRIGHT_MAGENTA'))
    
    def _void_meditation(self):
        """Void meditation experience"""
        entity = self._get_current_entity()
        if not entity:
            return
        
        print(ColorCloud.apply_color("\n⧈ Entering void meditation...", 'BRIGHT_BLACK'))
        time.sleep(0.5)
        
        void_depth = random.uniform(0.5, 1.0)
        duration = random.uniform(10, 30)
        insights = random.randint(0, 3)
        
        print(ColorCloud.apply_color(f"  Void depth reached: {void_depth:.2f}", 'WHITE'))
        print(ColorCloud.apply_color(f"  Duration: {duration:.1f} time units", 'CYAN'))
        print(ColorCloud.apply_color(f"  Insights gained: {insights}", 'YELLOW'))
        
        # Store memory
        importance = MemoryImportance.PROFOUND if void_depth > 0.8 else MemoryImportance.SIGNIFICANT
        
        memory = self.palace.store_memory(
            entity_id=self.current_entity_id,
            memory_type=MemoryType.VOID,
            content={
                "void_depth": void_depth,
                "duration": duration,
                "insights": insights,
                "experience": "Communion with nothingness"
            },
            importance=importance,
            emotional_valence=void_depth * 0.5,
            emotional_intensity=void_depth,
            tags=["void", "meditation", "contemplation"]
        )
        
        print(ColorCloud.apply_color(f"\n💾 Void memory stored: {memory.id}", 'BRIGHT_MAGENTA'))
    
    def recall_memories(self):
        """Recall memories interface"""
        if not self.current_entity_id:
            print(ColorCloud.apply_color("⚠ No entity selected", 'RED'))
            return
        
        print(ColorCloud.apply_color("\n═══ Recall Memories ═══\n", 'BRIGHT_MAGENTA'))
        print("How would you like to recall?")
        print("  1. By type (resonance, casino, consciousness, void)")
        print("  2. By emotion (positive, negative, neutral)")
        print("  3. Recent memories")
        print("  4. All memories")
        
        try:
            choice = input("\nSelect (1-4): ")
            
            if choice == '1':
                self._recall_by_type()
            elif choice == '2':
                self._recall_by_emotion()
            elif choice == '3':
                self._recall_recent()
            elif choice == '4':
                self._recall_all()
            else:
                print(ColorCloud.apply_color("Invalid choice", 'RED'))
        except Exception as e:
            print(ColorCloud.apply_color(f"⚠ Error: {e}", 'RED'))
    
    def _recall_by_type(self):
        """Recall memories by type"""
        print("\nMemory types:")
        types = list(MemoryType)
        for i, mtype in enumerate(types, 1):
            print(f"  {i}. {mtype.value}")
        
        choice = int(input("\nSelect type: ")) - 1
        if 0 <= choice < len(types):
            memories = self.palace.recall_by_type(self.current_entity_id, types[choice])
            self._display_memories(memories)
    
    def _recall_by_emotion(self):
        """Recall memories by emotion"""
        print("\n  1. Positive")
        print("  2. Negative")
        print("  3. Neutral")
        
        choice = input("\nSelect: ")
        valence_map = {'1': 'positive', '2': 'negative', '3': 'neutral'}
        
        if choice in valence_map:
            memories = self.palace.recall_by_emotion(self.current_entity_id, valence_map[choice])
            self._display_memories(memories)
    
    def _recall_recent(self):
        """Recall recent memories"""
        memories = self.palace.recall_recent(self.current_entity_id)
        self._display_memories(memories)
    
    def _recall_all(self):
        """Show all memories"""
        if self.current_entity_id not in self.palace.memories:
            print(ColorCloud.apply_color("No memories stored", 'YELLOW'))
            return
        
        memories = self.palace.memories[self.current_entity_id][:20]
        self._display_memories(memories)
    
    def _display_memories(self, memories: list):
        """Display memory list"""
        if not memories:
            print(ColorCloud.apply_color("\nNo memories found", 'YELLOW'))
            return
        
        print(ColorCloud.apply_color(f"\n Found {len(memories)} memories:\n", 'BRIGHT_WHITE'))
        
        for i, memory in enumerate(memories, 1):
            color = 'GREEN' if memory.emotional_valence > 0 else 'RED' if memory.emotional_valence < 0 else 'WHITE'
            clarity_color = 'BRIGHT_GREEN' if memory.clarity > 0.8 else 'YELLOW' if memory.clarity > 0.5 else 'RED'
            
            print(ColorCloud.apply_color(f"{i}. {memory}", color))
            print(ColorCloud.apply_color(f"   Clarity: {memory.clarity:.0%} | Importance: {memory.importance.name}", clarity_color))
            
            # Show reconstructed content
            content = memory.reconstruct()
            content_str = str(content)[:80]
            print(ColorCloud.apply_color(f"   {content_str}...", 'CYAN'))
            print()
    
    def search_memories(self):
        """Search memories"""
        if not self.current_entity_id:
            print(ColorCloud.apply_color("⚠ No entity selected", 'RED'))
            return
        
        search_term = input(ColorCloud.apply_color("\nEnter search term: ", 'BRIGHT_WHITE'))
        
        memories = self.palace.search_memories(self.current_entity_id, search_term)
        self._display_memories(memories)
    
    def view_stats(self):
        """View memory statistics"""
        if not self.current_entity_id:
            print(ColorCloud.apply_color("⚠ No entity selected", 'RED'))
            return
        
        stats = self.palace.get_memory_stats(self.current_entity_id)
        
        print(ColorCloud.apply_color("\n═══ Memory Statistics ═══\n", 'BRIGHT_WHITE'))
        print(ColorCloud.apply_color(f"Total Memories: {stats.get('total_memories', 0)}", 'CYAN'))
        
        if stats.get('total_memories', 0) > 0:
            print(ColorCloud.apply_color(f"Average Clarity: {stats['average_clarity']:.0%}", 'YELLOW'))
            print(ColorCloud.apply_color(f"Clear Memories: {stats['clear_memories']}", 'GREEN'))
            print(ColorCloud.apply_color(f"Degraded Memories: {stats['degraded_memories']}", 'RED'))
            
            print(ColorCloud.apply_color("\nBy Type:", 'BRIGHT_CYAN'))
            for mtype, count in stats['by_type'].items():
                if count > 0:
                    print(ColorCloud.apply_color(f"  {mtype}: {count}", 'CYAN'))
            
            print(ColorCloud.apply_color("\nBy Importance:", 'BRIGHT_MAGENTA'))
            for importance, count in stats['by_importance'].items():
                if count > 0:
                    print(ColorCloud.apply_color(f"  {importance}: {count}", 'MAGENTA'))
    
    def collective_memories(self):
        """View collective memories"""
        if not self.current_entity_id:
            print(ColorCloud.apply_color("⚠ No entity selected", 'RED'))
            return
        
        collective = self.palace.recall_collective(self.current_entity_id)
        
        print(ColorCloud.apply_color(f"\n═══ Collective Memories ({len(collective)}) ═══\n", 'BRIGHT_BLUE'))
        
        for cm in collective:
            print(ColorCloud.apply_color(f"ID: {cm.id}", 'BRIGHT_CYAN'))
            print(ColorCloud.apply_color(f"Participants: {len(cm.participating_entities)}", 'CYAN'))
            print(ColorCloud.apply_color(f"Type: {cm.memory_type.value}", 'YELLOW'))
            print(ColorCloud.apply_color(f"Clarity: {cm.clarity:.0%}", 'GREEN'))
            print(ColorCloud.apply_color(f"Content: {cm.content}", 'WHITE'))
            print()
    
    def consolidate(self):
        """Consolidate memories"""
        if not self.current_entity_id:
            print(ColorCloud.apply_color("⚠ No entity selected", 'RED'))
            return
        
        print(ColorCloud.apply_color("\n🔄 Consolidating memories...", 'BRIGHT_YELLOW'))
        count = self.palace.consolidate_memories(self.current_entity_id)
        print(ColorCloud.apply_color(f"✓ Consolidated {count} memory pairs", 'BRIGHT_GREEN'))
    
    def simulate_time(self):
        """Simulate time passage"""
        try:
            time_units = float(input(ColorCloud.apply_color("\nTime units to simulate: ", 'BRIGHT_WHITE')))
            
            print(ColorCloud.apply_color(f"\n⏳ Simulating {time_units} time units...", 'BRIGHT_CYAN'))
            self.palace.degrade_all_memories(time_units)
            forgotten = self.palace.forget_degraded(0.1)
            
            print(ColorCloud.apply_color(f"✓ Time passed", 'GREEN'))
            print(ColorCloud.apply_color(f"  Memories forgotten: {forgotten}", 'YELLOW'))
            
        except ValueError:
            print(ColorCloud.apply_color("⚠ Invalid input", 'RED'))
    
    def switch_entity(self):
        """Switch current entity"""
        print(ColorCloud.apply_color("\nEntities:", 'BRIGHT_WHITE'))
        for i, entity in enumerate(self.entities, 1):
            mem_count = len(self.palace.memories.get(entity.essence.uuid, []))
            current = " ← current" if entity.essence.uuid == self.current_entity_id else ""
            print(ColorCloud.apply_color(f"  {i}. {entity.essence.uuid[:8]} ({mem_count} memories){current}", 'CYAN'))
        
        try:
            choice = int(input("\nSelect entity: ")) - 1
            if 0 <= choice < len(self.entities):
                self.current_entity_id = self.entities[choice].essence.uuid
                print(ColorCloud.apply_color(f"✓ Switched to {self.current_entity_id[:8]}", 'BRIGHT_GREEN'))
        except (ValueError, IndexError):
            print(ColorCloud.apply_color("⚠ Invalid choice", 'RED'))
    
    def _get_current_entity(self):
        """Get current entity object"""
        for entity in self.entities:
            if entity.essence.uuid == self.current_entity_id:
                return entity
        return None
    
    def run(self):
        """Main loop"""
        self.show_welcome()
        
        # Spawn initial entities
        print(ColorCloud.apply_color("Spawning entities...", 'CYAN'))
        for i in range(3):
            entity = self.network.spawn_entity()
            self.entities.append(entity)
            print(ColorCloud.apply_color(f"  Entity {i+1}: {entity.essence.uuid[:8]}", 'GREEN'))
        
        self.current_entity_id = self.entities[0].essence.uuid
        print(ColorCloud.apply_color(f"\nCurrent entity: {self.current_entity_id[:8]}", 'BRIGHT_GREEN'))
        
        while True:
            self.show_menu()
            
            try:
                choice = input(ColorCloud.apply_color("Select option: ", 'BRIGHT_WHITE'))
                
                if choice == '1':
                    self.create_experience()
                elif choice == '2':
                    self.recall_memories()
                elif choice == '3':
                    self.search_memories()
                elif choice == '4':
                    self.view_stats()
                elif choice == '5':
                    self.collective_memories()
                elif choice == '6':
                    self.consolidate()
                elif choice == '7':
                    self.simulate_time()
                elif choice == '8':
                    self.switch_entity()
                elif choice == '9':
                    print(ColorCloud.apply_color("\n🏛️ Exiting Memory Palace...", 'BRIGHT_CYAN'))
                    print(ColorCloud.apply_color("Memories persist in the archive.\n", 'BRIGHT_BLACK'))
                    break
                else:
                    print(ColorCloud.apply_color("⚠ Invalid option", 'RED'))
                    
            except KeyboardInterrupt:
                print(ColorCloud.apply_color("\n\n🏛️ Palace session terminated\n", 'BRIGHT_RED'))
                break
            except Exception as e:
                print(ColorCloud.apply_color(f"⚠ Error: {e}", 'RED'))


if __name__ == "__main__":
    cli = MemoryPalaceCLI()
    cli.run()
