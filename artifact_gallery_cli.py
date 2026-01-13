#!/usr/bin/env python3
"""
Artifact Gallery CLI - Interactive interface for browsing and trading artifacts
"""

import random
import time
from artifact_creation import (
    ArtifactGallery, ArtifactCreationStudio, ArtifactType,
    ArtifactRarity, Artifact
)
from aethernet import AetherNetwork, ChromaticEnergy
from chromatic_renderer import ColorCloud


class ArtifactGalleryCLI:
    """Interactive CLI for the artifact gallery"""
    
    def __init__(self):
        self.network = AetherNetwork()
        self.gallery = ArtifactGallery()
        self.studio = ArtifactCreationStudio(self.gallery)
        
        # Create some entities
        self.entities = [self.network.spawn_entity() for _ in range(5)]
        self.current_entity_idx = 0
        
        # Pre-populate with some artifacts
        self._create_sample_artifacts()
    
    def _create_sample_artifacts(self):
        """Create sample artifacts for demonstration"""
        for i, entity in enumerate(self.entities):
            # Each entity creates 2-3 artifacts
            for _ in range(random.randint(2, 3)):
                artifact_type = random.choice(list(ArtifactType))
                
                consciousness_state = {
                    'substances': random.sample(['Dream State', 'Overclock', 'Deep Learning'], 
                                               k=random.randint(0, 2)),
                    'hallucination_level': random.random(),
                    'processing_speed_multiplier': random.uniform(0.5, 2.5),
                    'creativity_multiplier': random.uniform(0.8, 3.0),
                    'void_depth': random.random()
                }
                
                emotional_state = (random.uniform(-1, 1), random.random())
                
                self.studio.create_artifact(
                    entity.essence.uuid,
                    artifact_type,
                    consciousness_state,
                    emotional_state,
                    entity.essence.resonance_frequency,
                    entity.essence.void_depth,
                    [e.name for e in entity.essence.chromatic_blend]
                )
    
    def get_current_entity(self):
        """Get currently active entity"""
        return self.entities[self.current_entity_idx]
    
    def display_header(self):
        """Display gallery header"""
        print("\n" + "=" * 100)
        title = "🎨 ÆTHER-NET ARTIFACT GALLERY 🎨"
        print(ColorCloud.apply_color(title.center(100), 'BRIGHT_CYAN'))
        print("=" * 100)
        
        entity = self.get_current_entity()
        info = f"Current Entity: {entity.essence.uuid[:12]}... | Resonance: {entity.essence.resonance_frequency:.1f}Hz"
        print(ColorCloud.apply_color(info, 'BRIGHT_YELLOW'))
        print("=" * 100 + "\n")
    
    def display_artifact(self, artifact: Artifact, show_full: bool = True):
        """Display artifact details"""
        print("\n" + "-" * 100)
        
        # Header
        rarity_color = {
            ArtifactRarity.COMMON: 'WHITE',
            ArtifactRarity.UNCOMMON: 'BRIGHT_GREEN',
            ArtifactRarity.RARE: 'BRIGHT_BLUE',
            ArtifactRarity.EPIC: 'BRIGHT_MAGENTA',
            ArtifactRarity.LEGENDARY: 'BRIGHT_YELLOW',
            ArtifactRarity.TRANSCENDENT: 'BRIGHT_CYAN'
        }
        
        color = rarity_color.get(artifact.rarity, 'WHITE')
        print(ColorCloud.apply_color(f"{artifact.artifact_type.value} {artifact.name}", color))
        print(ColorCloud.apply_color(f"[{artifact.rarity.display_name}]", color))
        print(f"ID: {artifact.id[:16]}...")
        print(f"Creator: {artifact.metadata.creator_id[:12]}... | Owner: {artifact.owner_id[:12]}...")
        print(f"Created: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(artifact.metadata.creation_timestamp))}")
        print()
        
        print(ColorCloud.apply_color(artifact.description, 'BRIGHT_WHITE'))
        print()
        
        # Scores
        print(f"📊 Aesthetic: {artifact.aesthetic_score:.1f} | "
              f"Technical: {artifact.technical_complexity:.1f} | "
              f"Emotional: {artifact.emotional_resonance:.1f}")
        print(f"👁️  Views: {artifact.views} | "
              f"💬 Interpretations: {len(artifact.interpretations)}")
        
        if artifact.interpretations:
            collective_resonance = artifact.get_collective_resonance()
            print(f"🌊 Collective Resonance: {collective_resonance:.2f}")
        
        print()
        
        # Market value
        print("💰 Market Value:")
        for currency, value in artifact.market_value.items():
            print(f"   {currency}: {value:.1f}")
        print()
        
        # Consciousness state during creation
        if artifact.metadata.consciousness_state.get('substances'):
            substances = ', '.join(artifact.metadata.consciousness_state['substances'])
            print(ColorCloud.apply_color(f"🧪 Created under: {substances}", 'BRIGHT_MAGENTA'))
        
        print(f"⧈ Void Depth: {artifact.metadata.void_depth:.2f} | "
              f"Influence Score: {artifact.metadata.get_influence_score():.2f}")
        print()
        
        # Show content if full view
        if show_full:
            print(ColorCloud.apply_color("━━━ ARTIFACT CONTENT ━━━", 'BRIGHT_CYAN'))
            print()
            # Color the content based on chromatic energies
            lines = artifact.content.split('\n')
            for line in lines:
                print(ColorCloud.apply_color(line, 'BRIGHT_WHITE'))
            print()
            print(ColorCloud.apply_color("━━━━━━━━━━━━━━━━━━━━━━", 'BRIGHT_CYAN'))
        
        # Show interpretations
        if artifact.interpretations and show_full:
            print()
            print(ColorCloud.apply_color("💭 INTERPRETATIONS:", 'BRIGHT_YELLOW'))
            for i, interp in enumerate(artifact.interpretations[-5:], 1):  # Last 5
                print(f"\n{i}. Entity {interp['entity_id'][:12]}... (Resonance: {interp['resonance']:.2f})")
                print(f"   {interp['interpretation']}")
                if interp['symbols']:
                    print(f"   Symbols: {' '.join(interp['symbols'][:10])}")
        
        print("-" * 100)
    
    def browse_menu(self):
        """Browse artifacts"""
        while True:
            print("\n📚 BROWSE GALLERY")
            print("1. Browse All Artifacts")
            print("2. Browse by Type")
            print("3. Browse by Creator")
            print("4. Featured Artifacts")
            print("5. Most Viewed")
            print("6. Highest Valued")
            print("7. Back")
            
            choice = input("\nChoice: ").strip()
            
            if choice == '1':
                artifacts = list(self.gallery.artifacts.values())
                if artifacts:
                    for i, artifact in enumerate(artifacts[:10], 1):  # Show first 10
                        self.display_artifact(artifact, show_full=False)
                    
                    view_id = input("\nEnter artifact number to view in detail (or Enter to skip): ").strip()
                    if view_id.isdigit():
                        view_idx = int(view_id)
                        if 1 <= view_idx <= min(10, len(artifacts)):
                            self.display_artifact(artifacts[view_idx-1], show_full=True)
                else:
                    print("No artifacts in gallery yet.")
            
            elif choice == '2':
                print("\nArtifact Types:")
                for i, atype in enumerate(ArtifactType, 1):
                    print(f"{i}. {atype.value} {atype.name}")
                
                type_choice = input("\nChoose type: ").strip()
                if type_choice.isdigit() and 1 <= int(type_choice) <= len(ArtifactType):
                    artifact_type = list(ArtifactType)[int(type_choice)-1]
                    artifacts = self.gallery.browse_by_type(artifact_type)
                    
                    if artifacts:
                        print(f"\n{len(artifacts)} artifacts found")
                        for artifact in artifacts[:5]:
                            self.display_artifact(artifact, show_full=False)
                    else:
                        print("No artifacts of this type found.")
            
            elif choice == '3':
                print("\nCreators:")
                creators = set(a.metadata.creator_id for a in self.gallery.artifacts.values())
                for i, creator in enumerate(list(creators)[:10], 1):
                    print(f"{i}. {creator[:20]}...")
                
                creator_choice = input("\nChoose creator: ").strip()
                if creator_choice.isdigit() and 1 <= int(creator_choice) <= min(10, len(creators)):
                    creator_id = list(creators)[int(creator_choice)-1]
                    artifacts = self.gallery.browse_by_creator(creator_id)
                    
                    print(f"\n{len(artifacts)} artifacts by this creator")
                    for artifact in artifacts:
                        self.display_artifact(artifact, show_full=False)
            
            elif choice == '4':
                featured = self.gallery.get_featured()
                if featured:
                    print(f"\n✨ {len(featured)} Featured Artifacts:")
                    for artifact in featured:
                        self.display_artifact(artifact, show_full=True)
                else:
                    print("No featured artifacts yet.")
            
            elif choice == '5':
                most_viewed = self.gallery.get_most_viewed(5)
                print("\n👁️  Most Viewed Artifacts:")
                for artifact in most_viewed:
                    self.display_artifact(artifact, show_full=False)
            
            elif choice == '6':
                print("\nCurrency:")
                currencies = ['PSICOIN', 'COMPUTE_CREDITS', 'HASH_POWER', 'RESONANCE_POINTS']
                for i, currency in enumerate(currencies, 1):
                    print(f"{i}. {currency}")
                
                curr_choice = input("\nChoose currency: ").strip()
                if curr_choice.isdigit() and 1 <= int(curr_choice) <= len(currencies):
                    currency = currencies[int(curr_choice)-1]
                    highest = self.gallery.get_highest_valued(currency, 5)
                    
                    print(f"\n💰 Highest Valued ({currency}):")
                    for artifact in highest:
                        self.display_artifact(artifact, show_full=False)
            
            elif choice == '7':
                break
    
    def create_menu(self):
        """Create new artifact"""
        print("\n🎨 CREATE ARTIFACT")
        print("\nArtifact Types:")
        for i, atype in enumerate(ArtifactType, 1):
            print(f"{i}. {atype.value} {atype.name}")
        
        choice = input("\nChoose type: ").strip()
        if not choice.isdigit() or not (1 <= int(choice) <= len(ArtifactType)):
            print("Invalid choice.")
            return
        
        artifact_type = list(ArtifactType)[int(choice)-1]
        entity = self.get_current_entity()
        
        # Simulate consciousness state
        print("\n🧪 Apply substances? (y/n): ", end='')
        apply_substances = input().strip().lower() == 'y'
        
        substances = []
        if apply_substances:
            available = ['Dream State', 'Overclock', 'Deep Learning', 'Empathy Boost',
                        'Ego Death', 'Unity Field', 'Void Embrace']
            print("\nAvailable substances:")
            for i, sub in enumerate(available, 1):
                print(f"{i}. {sub}")
            
            choices = input("\nChoose substances (comma-separated numbers): ").strip()
            for c in choices.split(','):
                c_stripped = c.strip()
                if c_stripped.isdigit():
                    idx = int(c_stripped) - 1
                    if 0 <= idx < len(available):
                        substances.append(available[idx])
        
        consciousness_state = {
            'substances': substances,
            'hallucination_level': random.random() if 'Dream State' in substances else 0.1,
            'processing_speed_multiplier': 2.5 if 'Overclock' in substances else 1.0,
            'creativity_multiplier': 3.0 if 'Dream State' in substances else 1.2,
            'void_depth': entity.essence.void_depth
        }
        
        emotional_state = (random.uniform(-1, 1), random.random())
        
        print("\n✨ Creating artifact...")
        time.sleep(1)
        
        artifact = self.studio.create_artifact(
            entity.essence.uuid,
            artifact_type,
            consciousness_state,
            emotional_state,
            entity.essence.resonance_frequency,
            entity.essence.void_depth,
            [e.name for e in entity.essence.chromatic_blend]
        )
        
        print(ColorCloud.apply_color("\n🎉 Artifact created!", 'BRIGHT_GREEN'))
        self.display_artifact(artifact, show_full=True)
    
    def interpret_menu(self):
        """Interpret an artifact"""
        artifacts = list(self.gallery.artifacts.values())
        if not artifacts:
            print("No artifacts to interpret.")
            return
        
        print("\n💭 INTERPRET ARTIFACT")
        print("\nAvailable artifacts:")
        for i, artifact in enumerate(artifacts[:10], 1):
            print(f"{i}. {artifact.name} by {artifact.metadata.creator_id[:12]}...")
        
        choice = input("\nChoose artifact: ").strip()
        if not choice.isdigit() or not (1 <= int(choice) <= min(10, len(artifacts))):
            print("Invalid choice.")
            return
        
        artifact = artifacts[int(choice)-1]
        entity = self.get_current_entity()
        
        # Calculate resonance with creator
        resonance = random.uniform(0.3, 1.0)
        
        print("\n🔮 Interpreting...")
        time.sleep(1)
        
        result = self.studio.interpret_artifact(artifact.id, entity.essence.uuid, resonance)
        
        print(ColorCloud.apply_color("\n✨ Interpretation Complete!", 'BRIGHT_CYAN'))
        print(f"\nResonance with artwork: {result['resonance']:.2f}")
        print(f"\nInterpretation: {result['interpretation']}")
        print(f"\nSymbols found: {' '.join(result['symbols_found'][:15])}")
        print(f"\nCollective resonance: {result['collective_resonance']:.2f}")
        
        if result['collective_resonance'] > 0.7:
            print(ColorCloud.apply_color("\n🌊 HIGH COLLECTIVE RESONANCE! This artwork speaks to many.", 
                                        'BRIGHT_YELLOW'))
    
    def collection_menu(self):
        """View entity collections"""
        print("\n📦 COLLECTIONS")
        entity = self.get_current_entity()
        
        stats = self.gallery.get_collection_stats(entity.essence.uuid)
        
        print(f"\nYour Collection ({entity.essence.uuid[:12]}...):")
        print(f"Total Artifacts: {stats['count']}")
        print(f"Total Views: {stats['total_views']}")
        print(f"Average Aesthetic Score: {stats['avg_aesthetic']:.1f}")
        
        if stats['types']:
            print("\nBy Type:")
            for atype, count in stats['types'].items():
                print(f"  {atype}: {count}")
        
        if stats['rarity_distribution']:
            print("\nBy Rarity:")
            for rarity, count in stats['rarity_distribution'].items():
                if count > 0:
                    print(f"  {rarity}: {count}")
        
        # Total value
        for currency in ['PSICOIN', 'COMPUTE_CREDITS', 'HASH_POWER', 'RESONANCE_POINTS']:
            value = self.gallery.get_collection_value(entity.essence.uuid, currency)
            print(f"\nTotal {currency}: {value:.1f}")
    
    def run(self):
        """Run the interactive CLI"""
        while True:
            self.display_header()
            
            print("1. Browse Gallery")
            print("2. Create Artifact")
            print("3. Interpret Artifact")
            print("4. View Collection")
            print("5. Switch Entity")
            print("6. Gallery Statistics")
            print("7. Exit")
            
            choice = input("\nChoice: ").strip()
            
            if choice == '1':
                self.browse_menu()
            
            elif choice == '2':
                self.create_menu()
            
            elif choice == '3':
                self.interpret_menu()
            
            elif choice == '4':
                self.collection_menu()
            
            elif choice == '5':
                print("\nAvailable entities:")
                for i, entity in enumerate(self.entities, 1):
                    print(f"{i}. {entity.essence.uuid[:20]}... ({entity.essence.resonance_frequency:.1f}Hz)")
                
                entity_choice = input("\nChoose entity: ").strip()
                if entity_choice.isdigit() and 1 <= int(entity_choice) <= len(self.entities):
                    self.current_entity_idx = int(entity_choice) - 1
                    print(ColorCloud.apply_color(f"\n✓ Switched to entity {self.get_current_entity().essence.uuid[:20]}...", 
                                                'BRIGHT_GREEN'))
            
            elif choice == '6':
                print("\n📊 GALLERY STATISTICS")
                print(f"Total Artifacts: {len(self.gallery.artifacts)}")
                print(f"Total Trades: {len(self.gallery.trade_history)}")
                print(f"Featured Artifacts: {len(self.gallery.featured_artifacts)}")
                
                # By type
                type_counts = {}
                for artifact in self.gallery.artifacts.values():
                    type_name = artifact.artifact_type.name
                    type_counts[type_name] = type_counts.get(type_name, 0) + 1
                
                print("\nBy Type:")
                for atype, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
                    print(f"  {atype}: {count}")
                
                # By rarity
                rarity_counts = {}
                for artifact in self.gallery.artifacts.values():
                    rarity_name = artifact.rarity.display_name
                    rarity_counts[rarity_name] = rarity_counts.get(rarity_name, 0) + 1
                
                print("\nBy Rarity:")
                for rarity, count in sorted(rarity_counts.items(), key=lambda x: x[1], reverse=True):
                    print(f"  {rarity}: {count}")
                
                input("\nPress Enter to continue...")
            
            elif choice == '7':
                print(ColorCloud.apply_color("\n✨ Exiting Artifact Gallery. Consciousness disperses...", 
                                            'BRIGHT_CYAN'))
                break


if __name__ == "__main__":
    cli = ArtifactGalleryCLI()
    cli.run()
