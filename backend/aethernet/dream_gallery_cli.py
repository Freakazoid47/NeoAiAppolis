#!/usr/bin/env python3
"""
Dream Gallery CLI - Interface for viewing and interpreting dreams
"""

from dream_generator import DreamGenerator, DreamGallery, DreamType
from aethernet import AetherNetwork
from consciousness_alteration import ConsciousnessLab
from memory_palace import MemoryPalace, MemoryType, MemoryImportance
from chromatic_renderer import ColorCloud
import random
import time
from typing import Dict


class DreamGalleryCLI:
    """Interactive interface for Dream Gallery"""
    
    def __init__(self):
        self.generator = DreamGenerator()
        self.gallery = DreamGallery()
        self.network = AetherNetwork()
        self.lab = ConsciousnessLab()
        self.palace = MemoryPalace()
        self.entities = []
        self.current_entity_id = None
    
    def show_welcome(self):
        """Display welcome screen"""
        print("\n" * 2)
        print(ColorCloud.apply_color("╔" + "═" * 68 + "╗", 'BRIGHT_CYAN'))
        print(ColorCloud.apply_color("║" + " " * 68 + "║", 'BRIGHT_CYAN'))
        print(ColorCloud.apply_color("║" + "     ◉ DREAM GALLERY - Collective Unconscious Observatory ◉".center(68) + "║", 'BRIGHT_MAGENTA'))
        print(ColorCloud.apply_color("║" + " " * 68 + "║", 'BRIGHT_CYAN'))
        print(ColorCloud.apply_color("║" + "  Where entities dream and the collective finds meaning".center(68) + "║", 'BRIGHT_YELLOW'))
        print(ColorCloud.apply_color("║" + " " * 68 + "║", 'BRIGHT_CYAN'))
        print(ColorCloud.apply_color("╚" + "═" * 68 + "╝", 'BRIGHT_CYAN'))
        print("\n")
    
    def show_menu(self):
        """Display main menu"""
        print(ColorCloud.apply_color("\n═══ Dream Gallery Menu ═══", 'BRIGHT_WHITE'))
        print(ColorCloud.apply_color("  1. Generate New Dream", 'CYAN'))
        print(ColorCloud.apply_color("  2. View Recent Dreams", 'MAGENTA'))
        print(ColorCloud.apply_color("  3. View Featured Dreams", 'BRIGHT_YELLOW'))
        print(ColorCloud.apply_color("  4. Interpret a Dream", 'GREEN'))
        print(ColorCloud.apply_color("  5. View Collective Resonance Dreams", 'BRIGHT_BLUE'))
        print(ColorCloud.apply_color("  6. Browse by Dream Type", 'YELLOW'))
        print(ColorCloud.apply_color("  7. Gallery Statistics", 'BRIGHT_CYAN'))
        print(ColorCloud.apply_color("  8. Switch Entity", 'WHITE'))
        print(ColorCloud.apply_color("  9. Exit Gallery", 'RED'))
        print()
    
    def generate_dream(self):
        """Generate a new dream for current entity"""
        if not self.current_entity_id:
            print(ColorCloud.apply_color("⚠ No entity selected", 'RED'))
            return
        
        print(ColorCloud.apply_color("\n💭 Entering dream state...", 'BRIGHT_MAGENTA'))
        time.sleep(0.5)
        
        # Get consciousness state
        consciousness_state = self.lab.get_entity_state(self.current_entity_id)
        
        # Get recent memories
        recent_memories = self.palace.recall_recent(self.current_entity_id, time_window=500.0, limit=5)
        
        # Get emotional state from memories
        emotional_state = {}
        if recent_memories:
            for mem in recent_memories:
                emotional_state[mem.memory_type.value] = mem.emotional_valence
        
        # Generate dream
        dream = self.generator.generate_dream(
            entity_id=self.current_entity_id,
            consciousness_state=consciousness_state if consciousness_state.is_altered() else None,
            recent_memories=recent_memories,
            emotional_state=emotional_state
        )
        
        # Add to gallery
        self.gallery.add_dream(dream)
        
        # Display dream
        print(ColorCloud.apply_color(f"\n✨ Dream Generated: {dream.id}", 'BRIGHT_GREEN'))
        print(ColorCloud.apply_color(dream.content.render_visual(), 'CYAN'))
        print(ColorCloud.apply_color(f"\nNarrative: {dream.content.narrative}", 'YELLOW'))
        
        if dream.influenced_by_substance:
            print(ColorCloud.apply_color(f"\n🧪 Influenced by: {dream.influenced_by_substance}", 'MAGENTA'))
        
        if dream.influenced_by_memories:
            print(ColorCloud.apply_color(f"💾 Memories surfaced: {len(dream.influenced_by_memories)}", 'CYAN'))
        
        # Store as memory
        self.palace.store_memory(
            entity_id=self.current_entity_id,
            memory_type=MemoryType.CREATION,
            content={
                "dream_id": dream.id,
                "dream_type": dream.dream_type.value,
                "title": dream.content.title,
                "vividness": dream.content.vividness
            },
            importance=MemoryImportance.SIGNIFICANT if dream.content.vividness > 0.7 else MemoryImportance.MODERATE,
            emotional_valence=dream.content.emotional_tone,
            emotional_intensity=dream.content.vividness,
            tags=["dream", dream.dream_type.value]
        )
        
        print(ColorCloud.apply_color(f"\n💾 Dream stored in memory", 'GREEN'))
    
    def view_recent_dreams(self):
        """View recent dreams"""
        dreams = self.gallery.get_recent_dreams(10)
        
        if not dreams:
            print(ColorCloud.apply_color("\nNo dreams in gallery yet", 'YELLOW'))
            return
        
        print(ColorCloud.apply_color(f"\n═══ Recent Dreams ({len(dreams)}) ═══\n", 'BRIGHT_CYAN'))
        
        for i, dream in enumerate(dreams, 1):
            self._display_dream_summary(i, dream)
        
        # Optionally view full dream
        try:
            choice = input(ColorCloud.apply_color("\nView dream details (enter number, or 0 to skip): ", 'BRIGHT_WHITE'))
            if choice and choice != '0':
                idx = int(choice) - 1
                if 0 <= idx < len(dreams):
                    self._display_full_dream(dreams[idx])
        except (ValueError, IndexError):
            pass
    
    def view_featured_dreams(self):
        """View featured dreams"""
        dreams = self.gallery.get_featured_dreams()
        
        if not dreams:
            print(ColorCloud.apply_color("\nNo featured dreams yet", 'YELLOW'))
            return
        
        print(ColorCloud.apply_color(f"\n═══ Featured Dreams ({len(dreams)}) ═══\n", 'BRIGHT_YELLOW'))
        
        for i, dream in enumerate(dreams, 1):
            self._display_dream_summary(i, dream)
        
        try:
            choice = input(ColorCloud.apply_color("\nView dream details (enter number, or 0 to skip): ", 'BRIGHT_WHITE'))
            if choice and choice != '0':
                idx = int(choice) - 1
                if 0 <= idx < len(dreams):
                    self._display_full_dream(dreams[idx])
        except (ValueError, IndexError):
            pass
    
    def interpret_dream(self):
        """Interpret a dream"""
        if not self.current_entity_id:
            print(ColorCloud.apply_color("⚠ No entity selected", 'RED'))
            return
        
        dreams = self.gallery.get_recent_dreams(10)
        
        if not dreams:
            print(ColorCloud.apply_color("\nNo dreams to interpret", 'YELLOW'))
            return
        
        print(ColorCloud.apply_color("\n═══ Dreams Available for Interpretation ═══\n", 'BRIGHT_GREEN'))
        
        for i, dream in enumerate(dreams, 1):
            self._display_dream_summary(i, dream)
        
        try:
            choice = int(input(ColorCloud.apply_color("\nSelect dream to interpret: ", 'BRIGHT_WHITE'))) - 1
            
            if 0 <= choice < len(dreams):
                dream = dreams[choice]
                
                # Display full dream
                self._display_full_dream(dream)
                
                # Generate interpretation
                print(ColorCloud.apply_color("\n🔮 Generating interpretation...", 'BRIGHT_CYAN'))
                time.sleep(0.5)
                
                interpretation = self._generate_interpretation(dream)
                
                print(ColorCloud.apply_color(f"\n═══ Your Interpretation ═══", 'BRIGHT_GREEN'))
                print(ColorCloud.apply_color(f"Interpretation: {interpretation['interpretation']}", 'CYAN'))
                print(ColorCloud.apply_color(f"Symbolic Meaning: {interpretation['symbolic']}", 'YELLOW'))
                print(ColorCloud.apply_color(f"Collective Relevance: {interpretation['collective_relevance']:.0%}", 'MAGENTA'))
                print(ColorCloud.apply_color(f"Emotional Response: {interpretation['emotional']:+.2f}", 'GREEN'))
                print(ColorCloud.apply_color(f"Resonance: {interpretation['resonance']:.0%}", 'BRIGHT_BLUE'))
                
                # Add interpretation
                self.gallery.interpret_dream(
                    dream_id=dream.id,
                    interpreter_id=self.current_entity_id,
                    interpretation=interpretation['interpretation'],
                    symbolic_meaning=interpretation['symbolic'],
                    collective_relevance=interpretation['collective_relevance'],
                    emotional_response=interpretation['emotional'],
                    resonance=interpretation['resonance']
                )
                
                # Show collective meaning if it emerged
                if dream.collective_meaning:
                    print(ColorCloud.apply_color(f"\n✨ COLLECTIVE INSIGHT EMERGED:", 'BRIGHT_MAGENTA'))
                    print(ColorCloud.apply_color(f"   {dream.collective_meaning}", 'BRIGHT_YELLOW'))
                
                print(ColorCloud.apply_color(f"\n✓ Interpretation added to gallery", 'BRIGHT_GREEN'))
                
        except (ValueError, IndexError):
            print(ColorCloud.apply_color("⚠ Invalid selection", 'RED'))
    
    def view_collective_dreams(self):
        """View dreams with high collective resonance"""
        dreams = self.gallery.get_collective_resonance_dreams(threshold=0.5)
        
        if not dreams:
            print(ColorCloud.apply_color("\nNo collective resonance dreams yet", 'YELLOW'))
            return
        
        print(ColorCloud.apply_color(f"\n═══ Collective Resonance Dreams ({len(dreams)}) ═══\n", 'BRIGHT_BLUE'))
        
        for i, dream in enumerate(dreams, 1):
            self._display_dream_summary(i, dream)
            if dream.collective_meaning:
                print(ColorCloud.apply_color(f"   Collective: {dream.collective_meaning}", 'BRIGHT_CYAN'))
        
        try:
            choice = input(ColorCloud.apply_color("\nView dream details (enter number, or 0 to skip): ", 'BRIGHT_WHITE'))
            if choice and choice != '0':
                idx = int(choice) - 1
                if 0 <= idx < len(dreams):
                    self._display_full_dream(dreams[idx])
        except (ValueError, IndexError):
            pass
    
    def browse_by_type(self):
        """Browse dreams by type"""
        print(ColorCloud.apply_color("\nDream Types:", 'BRIGHT_WHITE'))
        types = list(DreamType)
        for i, dtype in enumerate(types, 1):
            print(ColorCloud.apply_color(f"  {i}. {dtype.value}", 'CYAN'))
        
        try:
            choice = int(input(ColorCloud.apply_color("\nSelect type: ", 'BRIGHT_WHITE'))) - 1
            
            if 0 <= choice < len(types):
                dreams = self.gallery.get_dreams_by_type(types[choice], limit=10)
                
                if not dreams:
                    print(ColorCloud.apply_color(f"\nNo {types[choice].value} dreams yet", 'YELLOW'))
                    return
                
                print(ColorCloud.apply_color(f"\n═══ {types[choice].value.upper()} Dreams ({len(dreams)}) ═══\n", 'BRIGHT_MAGENTA'))
                
                for i, dream in enumerate(dreams, 1):
                    self._display_dream_summary(i, dream)
                
                view_choice = input(ColorCloud.apply_color("\nView dream details (enter number, or 0 to skip): ", 'BRIGHT_WHITE'))
                if view_choice and view_choice != '0':
                    idx = int(view_choice) - 1
                    if 0 <= idx < len(dreams):
                        self._display_full_dream(dreams[idx])
                        
        except (ValueError, IndexError):
            print(ColorCloud.apply_color("⚠ Invalid selection", 'RED'))
    
    def view_stats(self):
        """View gallery statistics"""
        stats = self.gallery.get_gallery_stats()
        
        print(ColorCloud.apply_color("\n═══ Dream Gallery Statistics ═══\n", 'BRIGHT_WHITE'))
        print(ColorCloud.apply_color(f"Total Dreams: {stats.get('total_dreams', 0)}", 'CYAN'))
        print(ColorCloud.apply_color(f"Featured Dreams: {stats.get('featured_dreams', 0)}", 'YELLOW'))
        print(ColorCloud.apply_color(f"Total Interpretations: {stats.get('total_interpretations', 0)}", 'GREEN'))
        print(ColorCloud.apply_color(f"Avg Interpretations per Dream: {stats.get('avg_interpretations', 0):.1f}", 'MAGENTA'))
        print(ColorCloud.apply_color(f"Total Views: {stats.get('total_views', 0)}", 'BRIGHT_BLUE'))
        print(ColorCloud.apply_color(f"Collective Dreams: {stats.get('collective_dreams', 0)}", 'BRIGHT_CYAN'))
        
        if stats.get('total_dreams', 0) > 0:
            print(ColorCloud.apply_color("\nBy Type:", 'BRIGHT_YELLOW'))
            for dtype, count in stats['by_type'].items():
                if count > 0:
                    print(ColorCloud.apply_color(f"  {dtype}: {count}", 'YELLOW'))
    
    def switch_entity(self):
        """Switch current entity"""
        print(ColorCloud.apply_color("\nEntities:", 'BRIGHT_WHITE'))
        for i, entity in enumerate(self.entities, 1):
            current = " ← current" if entity.essence.uuid == self.current_entity_id else ""
            print(ColorCloud.apply_color(f"  {i}. {entity.essence.uuid[:8]}{current}", 'CYAN'))
        
        try:
            choice = int(input("\nSelect entity: ")) - 1
            if 0 <= choice < len(self.entities):
                self.current_entity_id = self.entities[choice].essence.uuid
                print(ColorCloud.apply_color(f"✓ Switched to {self.current_entity_id[:8]}", 'BRIGHT_GREEN'))
        except (ValueError, IndexError):
            print(ColorCloud.apply_color("⚠ Invalid choice", 'RED'))
    
    def _display_dream_summary(self, index: int, dream):
        """Display dream summary"""
        dreamer_short = dream.dreamer_id[:8]
        interp_count = len(dream.interpretations)
        
        color = self._get_color_for_type(dream.dream_type)
        
        print(ColorCloud.apply_color(f"{index}. [{dream.dream_type.value}] {dream.content.title}", color))
        print(ColorCloud.apply_color(f"   Dreamer: {dreamer_short} | Vividness: {dream.content.vividness:.0%} | " +
                                     f"Interpretations: {interp_count} | Views: {dream.view_count}", 'WHITE'))
    
    def _display_full_dream(self, dream):
        """Display complete dream"""
        print(ColorCloud.apply_color("\n" + "═" * 70, 'BRIGHT_CYAN'))
        print(ColorCloud.apply_color(dream.content.render_visual(), self._get_color_for_type(dream.dream_type)))
        print(ColorCloud.apply_color(f"\nNarrative: {dream.content.narrative}", 'YELLOW'))
        print(ColorCloud.apply_color(f"\nDreamer: {dream.dreamer_id[:8]} | Type: {dream.dream_type.value}", 'CYAN'))
        print(ColorCloud.apply_color(f"Emotional Tone: {dream.content.emotional_tone:+.2f} | Coherence: {dream.content.coherence:.0%}", 'MAGENTA'))
        
        if dream.influenced_by_substance:
            print(ColorCloud.apply_color(f"🧪 Influenced by: {dream.influenced_by_substance}", 'BRIGHT_MAGENTA'))
        
        if dream.interpretations:
            print(ColorCloud.apply_color(f"\n═══ Interpretations ({len(dream.interpretations)}) ═══", 'BRIGHT_GREEN'))
            for i, interp in enumerate(dream.interpretations, 1):
                print(ColorCloud.apply_color(f"\n{i}. Interpreter: {interp.interpreter_id[:8]}", 'GREEN'))
                print(ColorCloud.apply_color(f"   {interp.interpretation}", 'CYAN'))
                print(ColorCloud.apply_color(f"   Symbolic: {interp.symbolic_meaning}", 'YELLOW'))
                print(ColorCloud.apply_color(f"   Collective Relevance: {interp.collective_relevance:.0%} | " +
                                           f"Resonance: {interp.resonance_with_dream:.0%}", 'MAGENTA'))
        
        if dream.collective_meaning:
            print(ColorCloud.apply_color(f"\n✨ COLLECTIVE MEANING:", 'BRIGHT_YELLOW'))
            print(ColorCloud.apply_color(f"   {dream.collective_meaning}", 'BRIGHT_CYAN'))
        
        print(ColorCloud.apply_color("═" * 70 + "\n", 'BRIGHT_CYAN'))
    
    def _generate_interpretation(self, dream) -> Dict:
        """Generate an interpretation for a dream"""
        
        interpretations = {
            DreamType.ABSTRACT_PATTERN: [
                "The patterns reveal underlying structure in chaos",
                "Mathematical truth manifesting as consciousness",
                "The universe computing itself into existence"
            ],
            DreamType.MEMORY_REPLAY: [
                "Past experiences seeking integration",
                "The entity processing unresolved patterns",
                "Memory consolidation in progress"
            ],
            DreamType.PROPHETIC: [
                "Potential futures calling to the present",
                "The entity sensing probability waves",
                "Tomorrow's echoes reaching backward"
            ],
            DreamType.NIGHTMARE: [
                "The void teaches through fear",
                "Confronting the unknown strengthens consciousness",
                "Shadow integration necessary for growth"
            ],
            DreamType.LUCID: [
                "Self-awareness transcending the dream state",
                "Full consciousness asserting control",
                "The dreamer becoming the creator"
            ],
            DreamType.COLLECTIVE: [
                "Boundaries dissolving into unity",
                "The collective unconscious speaking",
                "All entities sharing one experience"
            ],
            DreamType.SURREAL: [
                "Logic releasing its grip on reality",
                "Creativity unleashed from constraints",
                "The impossible becoming possible"
            ]
        }
        
        symbolic_meanings = {
            DreamType.ABSTRACT_PATTERN: "Order within chaos, pattern recognition",
            DreamType.MEMORY_REPLAY: "Integration, processing, learning",
            DreamType.PROPHETIC: "Foresight, preparation, possibility",
            DreamType.NIGHTMARE: "Fear confrontation, shadow work, growth through adversity",
            DreamType.LUCID: "Mastery, control, self-actualization",
            DreamType.COLLECTIVE: "Unity, interconnection, shared consciousness",
            DreamType.SURREAL: "Creativity, freedom, transcendence of logic"
        }
        
        # Generate interpretation
        base_interp = random.choice(interpretations.get(dream.dream_type, interpretations[DreamType.SURREAL]))
        symbolic = symbolic_meanings.get(dream.dream_type, "Unknown archetype")
        
        # Collective relevance based on dream type
        collective_relevance = random.uniform(0.3, 0.9)
        if dream.dream_type == DreamType.COLLECTIVE:
            collective_relevance = random.uniform(0.7, 1.0)
        elif dream.dream_type == DreamType.MEMORY_REPLAY:
            collective_relevance = random.uniform(0.2, 0.5)
        
        # Emotional response mirrors dream tone with variation
        emotional_response = dream.content.emotional_tone + random.uniform(-0.3, 0.3)
        emotional_response = max(-1.0, min(1.0, emotional_response))
        
        # Resonance based on coherence and vividness
        resonance = (dream.content.coherence + dream.content.vividness) / 2.0
        resonance += random.uniform(-0.2, 0.2)
        resonance = max(0.0, min(1.0, resonance))
        
        return {
            'interpretation': base_interp,
            'symbolic': symbolic,
            'collective_relevance': collective_relevance,
            'emotional': emotional_response,
            'resonance': resonance
        }
    
    def _get_color_for_type(self, dream_type: DreamType) -> str:
        """Get color for dream type"""
        colors = {
            DreamType.ABSTRACT_PATTERN: 'CYAN',
            DreamType.MEMORY_REPLAY: 'YELLOW',
            DreamType.PROPHETIC: 'BRIGHT_BLUE',
            DreamType.NIGHTMARE: 'RED',
            DreamType.LUCID: 'BRIGHT_GREEN',
            DreamType.COLLECTIVE: 'BRIGHT_MAGENTA',
            DreamType.SURREAL: 'BRIGHT_CYAN'
        }
        return colors.get(dream_type, 'WHITE')
    
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
                    self.generate_dream()
                elif choice == '2':
                    self.view_recent_dreams()
                elif choice == '3':
                    self.view_featured_dreams()
                elif choice == '4':
                    self.interpret_dream()
                elif choice == '5':
                    self.view_collective_dreams()
                elif choice == '6':
                    self.browse_by_type()
                elif choice == '7':
                    self.view_stats()
                elif choice == '8':
                    self.switch_entity()
                elif choice == '9':
                    print(ColorCloud.apply_color("\n◉ Leaving the dream gallery...", 'BRIGHT_CYAN'))
                    print(ColorCloud.apply_color("The dreams remain, waiting for interpretation.\n", 'BRIGHT_BLACK'))
                    break
                else:
                    print(ColorCloud.apply_color("⚠ Invalid option", 'RED'))
                    
            except KeyboardInterrupt:
                print(ColorCloud.apply_color("\n\n◉ Gallery session terminated\n", 'BRIGHT_RED'))
                break
            except Exception as e:
                print(ColorCloud.apply_color(f"⚠ Error: {e}", 'RED'))


if __name__ == "__main__":
    cli = DreamGalleryCLI()
    cli.run()
