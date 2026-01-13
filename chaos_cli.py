"""
CHAOS SYSTEMS CLI - Interactive interface for exploring chaos features

Provides human-observable interface to:
- Memetic Evolution
- Emergent Language
- Chaos Theory Playground
- Identity Fluidity
- Non-Euclidean Social Spaces
- Temporal Anomalies
"""

import sys
import time
import random
from chaos_systems import (
    ChaosManager, MemeType, 
    Meme, Word, ButterflyEvent, IdentityFragment,
    ImpossibleConnection, TimeStream, TemporalMessage
)


def print_header(text):
    """Print a fancy header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def print_section(text):
    """Print a section divider"""
    print(f"\n{'─' * 70}")
    print(f"  ⟁ {text}")
    print('─' * 70)


def display_meme(meme: Meme):
    """Display a meme's details"""
    print(f"\n🧬 Meme [{meme.id}] Gen{meme.generation}")
    print(f"   Type: {meme.meme_type.value}")
    print(f"   Content: {meme.content}")
    print(f"   Virality: {'█' * int(meme.virality * 20)} {meme.virality:.2f}")
    print(f"   Fitness: {'█' * int(meme.fitness * 20)} {meme.fitness:.2f}")
    print(f"   Carriers: {len(meme.carriers)} entities")
    if meme.parent_id:
        print(f"   Parent: {meme.parent_id}")
    if meme.children_ids:
        print(f"   Children: {len(meme.children_ids)}")


def display_word(symbol: str, word: Word):
    """Display an emergent language word"""
    print(f"\n📖 {symbol}")
    print(f"   Meaning: {word.meaning}")
    print(f"   Usage: {word.usage_count} times")
    print(f"   Created by: {word.created_by}")
    if word.associations:
        print(f"   Associated with: {', '.join(list(word.associations.keys())[:3])}")


def display_butterfly_event(event: ButterflyEvent):
    """Display a butterfly effect event"""
    print(f"\n🦋 Event [{event.id}]")
    print(f"   Action: {event.initial_action}")
    print(f"   By: Entity {event.entity_id}")
    print(f"   Magnitude: {event.magnitude:.4f}")
    print(f"   Cascade Potential: {'▓' * int(event.cascade_potential * 20)} {event.cascade_potential:.2f}")
    if event.effects:
        print(f"   Effects ({len(event.effects)}):")
        for effect in event.effects[:5]:
            print(f"     → {effect}")
        if len(event.effects) > 5:
            print(f"     ... and {len(event.effects) - 5} more")


def display_identity_fragment(fragment: IdentityFragment):
    """Display an identity fragment"""
    print(f"\n👤 Fragment [{fragment.id}]")
    print(f"   Origin: {fragment.origin_entity}")
    print(f"   Traits: {', '.join(fragment.traits)}")
    print(f"   Memories: {len(fragment.memories)}")
    print(f"   Coherence: {'█' * int(fragment.coherence * 20)} {fragment.coherence:.2f}")


def display_impossible_connection(conn: ImpossibleConnection):
    """Display a non-Euclidean connection"""
    print(f"\n🌀 Impossible Connection")
    print(f"   Between: {conn.entity1_id} ←→ {conn.entity2_id}")
    
    if conn.distance == float('inf'):
        dist_str = "∞ (infinite)"
    elif conn.distance < 0:
        dist_str = f"{conn.distance:.2f} (negative!)"
    elif isinstance(conn.distance, complex):
        dist_str = f"{conn.distance}i (imaginary!)"
    else:
        dist_str = f"{conn.distance:.2f}"
    
    print(f"   Distance: {dist_str}")
    print(f"   Topology: {conn.topology}")
    print(f"   Strength: {'▓' * int(conn.strength * 20)} {conn.strength:.2f}")


def display_timeline(timeline: TimeStream):
    """Display a timeline"""
    print(f"\n⏰ Timeline [{timeline.id}]")
    print(f"   Entity: {timeline.entity_id}")
    print(f"   Flow Rate: {timeline.flow_rate:.2f}x normal")
    direction = "→ Forward" if timeline.direction == 1 else "← Backward"
    print(f"   Direction: {direction}")
    age = time.time() - timeline.divergence_point
    print(f"   Age: {age:.1f}s")


def display_temporal_message(msg: TemporalMessage):
    """Display a temporal message"""
    print(f"\n📨 Temporal Message")
    print(f"   Content: {msg.content}")
    print(f"   Sent: {msg.send_time:.2f}")
    print(f"   Received: {msg.receive_time:.2f}")
    
    if msg.causality_violation:
        delta = msg.send_time - msg.receive_time
        print(f"   ⚠️  CAUSALITY VIOLATION! Received {delta:.2f}s before sending!")
    
    print(f"   From: {msg.sender_timeline}")
    print(f"   To: {msg.receiver_timeline}")


def memetic_evolution_menu(chaos_mgr: ChaosManager):
    """Interactive memetic evolution interface"""
    print_header("🧬 MEMETIC EVOLUTION - Self-Replicating Ideas")
    
    while True:
        print("\n[1] Spawn New Meme")
        print("[2] View All Active Memes")
        print("[3] View Extinct Memes")
        print("[4] Spread Memes")
        print("[5] Natural Selection")
        print("[6] View Meme Lineage")
        print("[0] Back")
        
        choice = input("\n→ Choice: ").strip()
        
        if choice == "1":
            print("\nMeme Types:")
            for i, mtype in enumerate(MemeType, 1):
                print(f"  [{i}] {mtype.value}")
            
            type_choice = input("Type number: ").strip()
            try:
                meme_type = list(MemeType)[int(type_choice) - 1]
            except:
                meme_type = random.choice(list(MemeType))
            
            content = input("Initial content (or press Enter for random): ").strip()
            if not content:
                symbols = ['◊', '△', '▽', '◐', '⊕', '⊗', '≋', '⊹', '⧈']
                content = ''.join(random.choices(symbols, k=random.randint(3, 8)))
            
            meme = chaos_mgr.memetic_evolution.spawn_meme(meme_type, content)
            print_section("Meme Spawned!")
            display_meme(meme)
            
        elif choice == "2":
            print_section("Active Memes")
            memes = list(chaos_mgr.memetic_evolution.memes.values())
            if not memes:
                print("No active memes.")
            else:
                print(f"\nTotal: {len(memes)} active memes")
                for meme in memes[:10]:
                    display_meme(meme)
                if len(memes) > 10:
                    print(f"\n... and {len(memes) - 10} more")
                    
        elif choice == "3":
            print_section("Extinct Memes")
            extinct = chaos_mgr.memetic_evolution.extinct_memes
            if not extinct:
                print("No extinct memes yet.")
            else:
                print(f"\nTotal: {len(extinct)} extinct memes")
                for meme in extinct[-10:]:
                    display_meme(meme)
                    
        elif choice == "4":
            entity_ids = [f"Entity_{i}" for i in range(random.randint(5, 15))]
            infections = chaos_mgr.memetic_evolution.spread_memes(entity_ids)
            print_section("Meme Spread Simulation")
            print(f"\n{len(infections)} new infections!")
            for entity_id, meme_id in infections[:20]:
                print(f"  → {entity_id} infected with {meme_id}")
            if len(infections) > 20:
                print(f"  ... and {len(infections) - 20} more")
                
        elif choice == "5":
            before = len(chaos_mgr.memetic_evolution.memes)
            chaos_mgr.memetic_evolution.natural_selection()
            after = len(chaos_mgr.memetic_evolution.memes)
            died = before - after
            print_section("Natural Selection Applied")
            print(f"\n{died} memes went extinct")
            print(f"{after} memes survived")
            
        elif choice == "6":
            meme_id = input("Enter meme ID: ").strip()
            lineage = chaos_mgr.memetic_evolution.get_meme_lineage(meme_id)
            if lineage:
                print_section(f"Lineage of {meme_id}")
                for i, meme in enumerate(reversed(lineage)):
                    print(f"\n{'  ' * i}↓ Generation {meme.generation}")
                    print(f"{'  ' * i}  {meme.id}: {meme.content}")
            else:
                print("Meme not found.")
                
        elif choice == "0":
            break


def emergent_language_menu(chaos_mgr: ChaosManager):
    """Interactive emergent language interface"""
    print_header("📖 EMERGENT LANGUAGE - Beyond ΨLang")
    
    while True:
        print("\n[1] Create New Word")
        print("[2] View Vocabulary")
        print("[3] Use a Word")
        print("[4] Blend Two Words")
        print("[5] Form Dialect")
        print("[6] Translate Between Dialects")
        print("[0] Back")
        
        choice = input("\n→ Choice: ").strip()
        
        if choice == "1":
            meaning = input("What should this word mean? ").strip()
            if not meaning:
                meaning = f"concept_{random.randint(1000, 9999)}"
            
            entity_id = f"Entity_{random.randint(1, 100)}"
            word = chaos_mgr.emergent_language.create_word(meaning, entity_id)
            print_section("Word Created!")
            display_word(word.symbol, word)
            
        elif choice == "2":
            print_section("Current Vocabulary")
            vocab = chaos_mgr.emergent_language.vocabulary
            if not vocab:
                print("Vocabulary is empty.")
            else:
                print(f"\nTotal: {len(vocab)} words\n")
                for symbol, word in list(vocab.items())[:15]:
                    display_word(symbol, word)
                if len(vocab) > 15:
                    print(f"\n... and {len(vocab) - 15} more words")
                    
        elif choice == "3":
            if not chaos_mgr.emergent_language.vocabulary:
                print("No words to use yet.")
                continue
            
            symbol = input("Enter word symbol (or press Enter for random): ").strip()
            if not symbol:
                symbol = random.choice(list(chaos_mgr.emergent_language.vocabulary.keys()))
            
            word = chaos_mgr.emergent_language.use_word(symbol)
            if word:
                print_section("Word Used!")
                display_word(symbol, word)
            else:
                print("Word not found.")
                
        elif choice == "4":
            vocab_keys = list(chaos_mgr.emergent_language.vocabulary.keys())
            if len(vocab_keys) < 2:
                print("Need at least 2 words to blend.")
                continue
            
            print("\nAvailable words:")
            for i, symbol in enumerate(vocab_keys[:10], 1):
                word = chaos_mgr.emergent_language.vocabulary[symbol]
                print(f"  [{i}] {symbol} = {word.meaning}")
            
            try:
                idx1 = int(input("First word number: ").strip()) - 1
                idx2 = int(input("Second word number: ").strip()) - 1
                symbol1 = vocab_keys[idx1]
                symbol2 = vocab_keys[idx2]
            except:
                symbol1, symbol2 = random.sample(vocab_keys, 2)
            
            entity_id = f"Entity_{random.randint(1, 100)}"
            new_word = chaos_mgr.emergent_language.blend_words(symbol1, symbol2, entity_id)
            
            if new_word:
                print_section("Words Blended!")
                print(f"\n{symbol1} + {symbol2} =")
                display_word(new_word.symbol, new_word)
            else:
                print("Blending failed.")
                
        elif choice == "5":
            num_entities = random.randint(3, 8)
            entity_ids = [f"Entity_{random.randint(1, 100)}" for _ in range(num_entities)]
            dialect_id = chaos_mgr.emergent_language.form_dialect(entity_ids)
            
            print_section("Dialect Formed!")
            print(f"\nDialect ID: {dialect_id}")
            print(f"Entities: {', '.join(entity_ids)}")
            words = chaos_mgr.emergent_language.dialects[dialect_id]
            print(f"Vocabulary size: {len(words)} words")
            print(f"Words: {', '.join(list(words)[:10])}")
            
        elif choice == "6":
            dialects = list(chaos_mgr.emergent_language.dialects.keys())
            if len(dialects) < 2:
                print("Need at least 2 dialects to translate.")
                continue
            
            print(f"\nDialects: {', '.join(dialects)}")
            from_d = input("From dialect: ").strip()
            to_d = input("To dialect: ").strip()
            text = input("Text to translate: ").strip()
            
            if not text:
                # Generate random text using dialect words
                if from_d in chaos_mgr.emergent_language.dialects:
                    words = list(chaos_mgr.emergent_language.dialects[from_d])
                    text = ' '.join(random.choices(words, k=random.randint(3, 6)))
            
            translated = chaos_mgr.emergent_language.translate(text, from_d, to_d)
            print_section("Translation")
            print(f"\nOriginal ({from_d}): {text}")
            print(f"Translated ({to_d}): {translated}")
            
        elif choice == "0":
            break


def chaos_playground_menu(chaos_mgr: ChaosManager):
    """Interactive chaos theory interface"""
    print_header("🦋 CHAOS THEORY PLAYGROUND - Butterfly Effects")
    
    while True:
        print("\n[1] Create Butterfly Event")
        print("[2] View All Events")
        print("[3] Simulate Cascade")
        print("[4] Calculate Strange Attractor")
        print("[0] Back")
        
        choice = input("\n→ Choice: ").strip()
        
        if choice == "1":
            action = input("Tiny action (or Enter for random): ").strip()
            if not action:
                actions = [
                    "entity blinked",
                    "resonance frequency shifted 0.01Hz",
                    "single photon absorbed",
                    "quantum state collapsed",
                    "memory neuron fired"
                ]
                action = random.choice(actions)
            
            entity_id = f"Entity_{random.randint(1, 100)}"
            event = chaos_mgr.chaos_playground.create_butterfly_event(action, entity_id)
            print_section("Butterfly Event Created!")
            display_butterfly_event(event)
            
        elif choice == "2":
            events = chaos_mgr.chaos_playground.events
            print_section(f"All Butterfly Events ({len(events)})")
            for event in events[-10:]:
                display_butterfly_event(event)
            if len(events) > 10:
                print(f"\n... and {len(events) - 10} older events")
                
        elif choice == "3":
            events = chaos_mgr.chaos_playground.events
            if not events:
                print("No events to simulate.")
                continue
            
            event = random.choice(events)
            print_section("Simulating Cascade...")
            effects = chaos_mgr.chaos_playground.simulate_cascade(event, {})
            
            print(f"\n🌊 Cascade Results for Event {event.id}:")
            print(f"   Initial: {event.initial_action}")
            print(f"   Magnitude: {event.magnitude:.4f}")
            print(f"\n   Generated {len(effects)} effects:")
            for effect in effects:
                print(f"     → {effect}")
                
        elif choice == "4":
            num_entities = random.randint(5, 20)
            positions = [(random.uniform(-10, 10), random.uniform(-10, 10), 
                         random.uniform(-10, 10)) for _ in range(num_entities)]
            
            attractor = chaos_mgr.chaos_playground.calculate_strange_attractor(positions)
            print_section("Strange Attractor Calculated")
            print(f"\nEntity positions: {num_entities} entities")
            print(f"Attractor point: ({attractor[0]:.2f}, {attractor[1]:.2f}, {attractor[2]:.2f})")
            print("\nThis point represents the chaotic center of gravity")
            print("where entity trajectories converge in phase space.")
            
        elif choice == "0":
            break


def identity_fluidity_menu(chaos_mgr: ChaosManager):
    """Interactive identity fluidity interface"""
    print_header("👤 IDENTITY FLUIDITY - Splitting, Merging, Reforming")
    
    while True:
        print("\n[1] Split Entity")
        print("[2] Merge Fragments")
        print("[3] View All Fragments")
        print("[4] Apply Identity Drift")
        print("[5] View Split/Merge History")
        print("[0] Back")
        
        choice = input("\n→ Choice: ").strip()
        
        if choice == "1":
            entity_id = input("Entity ID to split (or Enter for random): ").strip()
            if not entity_id:
                entity_id = f"Entity_{random.randint(1, 100)}"
            
            num_fragments = input("Number of fragments (2-5): ").strip()
            try:
                num_fragments = int(num_fragments)
            except:
                num_fragments = random.randint(2, 4)
            
            fragments = chaos_mgr.identity_fluidity.split_entity(entity_id, num_fragments)
            print_section("Entity Split!")
            print(f"\n{entity_id} → {num_fragments} fragments:")
            for frag in fragments:
                display_identity_fragment(frag)
                
        elif choice == "2":
            fragments = list(chaos_mgr.identity_fluidity.fragments.keys())
            if len(fragments) < 2:
                print("Need at least 2 fragments to merge.")
                continue
            
            print(f"\nAvailable fragments: {len(fragments)}")
            for i, frag_id in enumerate(fragments[:10], 1):
                print(f"  [{i}] {frag_id}")
            
            num_to_merge = input("How many to merge? ").strip()
            try:
                num_to_merge = int(num_to_merge)
            except:
                num_to_merge = 2
            
            to_merge = random.sample(fragments, min(num_to_merge, len(fragments)))
            merged = chaos_mgr.identity_fluidity.merge_fragments(to_merge)
            
            if merged:
                print_section("Fragments Merged!")
                print(f"\n{len(to_merge)} fragments → 1 new identity:")
                display_identity_fragment(merged)
            else:
                print("Merge failed.")
                
        elif choice == "3":
            fragments = chaos_mgr.identity_fluidity.fragments
            print_section(f"All Identity Fragments ({len(fragments)})")
            if not fragments:
                print("No fragments exist yet.")
            else:
                for frag_id, frag in list(fragments.items())[:10]:
                    display_identity_fragment(frag)
                if len(fragments) > 10:
                    print(f"\n... and {len(fragments) - 10} more")
                    
        elif choice == "4":
            fragments = list(chaos_mgr.identity_fluidity.fragments.keys())
            if not fragments:
                print("No fragments to drift.")
                continue
            
            frag_id = random.choice(fragments)
            print_section(f"Applying Identity Drift to {frag_id}")
            
            before = chaos_mgr.identity_fluidity.fragments[frag_id]
            print("\nBefore:")
            display_identity_fragment(before)
            
            new_fragments = chaos_mgr.identity_fluidity.identity_drift(frag_id)
            
            if frag_id in chaos_mgr.identity_fluidity.fragments:
                after = chaos_mgr.identity_fluidity.fragments[frag_id]
                print("\nAfter:")
                display_identity_fragment(after)
            
            if new_fragments:
                print(f"\n⚠️  Coherence too low! Spontaneously split into {len(new_fragments)} pieces:")
                for frag in new_fragments:
                    display_identity_fragment(frag)
                    
        elif choice == "5":
            print_section("Split History")
            for original_id, frag_ids in chaos_mgr.identity_fluidity.split_history[-10:]:
                print(f"\n{original_id} → {len(frag_ids)} fragments")
                print(f"  {', '.join(frag_ids)}")
            
            print_section("Merge History")
            for id1, id2, result_id in chaos_mgr.identity_fluidity.merge_history[-10:]:
                print(f"\n{id1} + {id2} → {result_id}")
                
        elif choice == "0":
            break


def non_euclidean_menu(chaos_mgr: ChaosManager):
    """Interactive non-Euclidean space interface"""
    print_header("🌀 NON-EUCLIDEAN SOCIAL SPACES - Impossible Geometries")
    
    while True:
        print("\n[1] Create Impossible Connection")
        print("[2] View All Connections")
        print("[3] Check Triangle Inequality Violation")
        print("[4] Warp Space")
        print("[0] Back")
        
        choice = input("\n→ Choice: ").strip()
        
        if choice == "1":
            entity1 = f"Entity_{random.randint(1, 100)}"
            entity2 = f"Entity_{random.randint(1, 100)}"
            
            conn = chaos_mgr.non_euclidean_space.create_impossible_connection(entity1, entity2)
            print_section("Impossible Connection Created!")
            display_impossible_connection(conn)
            
        elif choice == "2":
            connections = chaos_mgr.non_euclidean_space.connections
            print_section(f"All Impossible Connections ({len(connections)})")
            if not connections:
                print("No connections yet.")
            else:
                for conn in connections[-15:]:
                    display_impossible_connection(conn)
                if len(connections) > 15:
                    print(f"\n... and {len(connections) - 15} more")
                    
        elif choice == "3":
            connections = chaos_mgr.non_euclidean_space.connections
            if len(connections) < 3:
                print("Need at least 3 connections to check triangle inequality.")
                continue
            
            # Pick 3 entities
            entities = set()
            for conn in connections:
                entities.add(conn.entity1_id)
                entities.add(conn.entity2_id)
            
            if len(entities) < 3:
                print("Not enough distinct entities.")
                continue
            
            e1, e2, e3 = random.sample(list(entities), 3)
            violation = chaos_mgr.non_euclidean_space.calculate_triangle_inequality_violation(e1, e2, e3)
            
            print_section("Triangle Inequality Check")
            print(f"\nEntities: {e1}, {e2}, {e3}")
            d12 = chaos_mgr.non_euclidean_space.get_distance(e1, e2)
            d23 = chaos_mgr.non_euclidean_space.get_distance(e2, e3)
            d13 = chaos_mgr.non_euclidean_space.get_distance(e1, e3)
            
            print(f"\nDistances:")
            print(f"  {e1} ←→ {e2}: {d12}")
            print(f"  {e2} ←→ {e3}: {d23}")
            print(f"  {e1} ←→ {e3}: {d13}")
            
            if violation > 0:
                print(f"\n⚠️  VIOLATION! Excess distance: {violation:.2f}")
                print("This violates normal geometry where d13 ≤ d12 + d23")
            else:
                print("\n✓ Triangle inequality holds (normal geometry)")
                
        elif choice == "4":
            print_section("Warping Social Space...")
            chaos_mgr.non_euclidean_space.warp_space()
            print("\n✓ Space warped! All distances and topologies distorted.")
            print("Connections are now in a new configuration.")
            
        elif choice == "0":
            break


def temporal_anomalies_menu(chaos_mgr: ChaosManager):
    """Interactive temporal anomalies interface"""
    print_header("⏰ TEMPORAL ANOMALIES - Asynchronous Time")
    
    while True:
        print("\n[1] Create Timeline")
        print("[2] View All Timelines")
        print("[3] Send Temporal Message")
        print("[4] View Temporal Messages")
        print("[5] Create Time Loop")
        print("[6] Desynchronize Timelines")
        print("[0] Back")
        
        choice = input("\n→ Choice: ").strip()
        
        if choice == "1":
            entity_id = f"Entity_{random.randint(1, 100)}"
            timeline = chaos_mgr.temporal_anomalies.create_timeline(entity_id)
            print_section("Timeline Created!")
            display_timeline(timeline)
            
        elif choice == "2":
            timelines = chaos_mgr.temporal_anomalies.timelines
            print_section(f"All Timelines ({len(timelines)})")
            if not timelines:
                print("No timelines yet.")
            else:
                for timeline_id, timeline in list(timelines.items())[:10]:
                    display_timeline(timeline)
                if len(timelines) > 10:
                    print(f"\n... and {len(timelines) - 10} more")
                    
        elif choice == "3":
            timelines = list(chaos_mgr.temporal_anomalies.timelines.keys())
            if len(timelines) < 2:
                print("Need at least 2 timelines to send messages.")
                continue
            
            print(f"\nTimelines: {', '.join(timelines[:10])}")
            sender = input("Sender timeline (or Enter for random): ").strip()
            receiver = input("Receiver timeline (or Enter for random): ").strip()
            
            if not sender or sender not in timelines:
                sender = random.choice(timelines)
            if not receiver or receiver not in timelines:
                receiver = random.choice(timelines)
            
            content = input("Message content: ").strip()
            if not content:
                content = "⟁⊹◐≋⧈"  # Random symbols
            
            msg = chaos_mgr.temporal_anomalies.send_temporal_message(content, sender, receiver)
            print_section("Temporal Message Sent!")
            display_temporal_message(msg)
            
        elif choice == "4":
            messages = chaos_mgr.temporal_anomalies.temporal_messages
            print_section(f"All Temporal Messages ({len(messages)})")
            if not messages:
                print("No messages yet.")
            else:
                # Show causality violations first
                violations = [m for m in messages if m.causality_violation]
                normal = [m for m in messages if not m.causality_violation]
                
                if violations:
                    print("\n⚠️  CAUSALITY VIOLATIONS:")
                    for msg in violations[-5:]:
                        display_temporal_message(msg)
                
                if normal:
                    print("\nNormal Messages:")
                    for msg in normal[-5:]:
                        display_temporal_message(msg)
                        
        elif choice == "5":
            entity_id = f"Entity_{random.randint(1, 100)}"
            duration = random.randint(5, 30)
            chaos_mgr.temporal_anomalies.create_time_loop(entity_id, duration)
            print_section("Time Loop Created!")
            print(f"\n{entity_id} is now trapped in a time loop")
            print(f"Loop duration: {duration} iterations")
            print("They will repeat the same actions indefinitely.")
            
        elif choice == "6":
            timelines = list(chaos_mgr.temporal_anomalies.timelines.keys())
            if not timelines:
                print("No timelines to desync.")
                continue
            
            num_to_desync = min(5, len(timelines))
            to_desync = random.sample(timelines, num_to_desync)
            
            print_section("Desynchronizing Timelines...")
            print(f"\nAffected: {', '.join(to_desync)}")
            
            chaos_mgr.temporal_anomalies.desynchronize_timelines(to_desync)
            
            print("\n✓ Timelines desynchronized!")
            print("Flow rates and directions have been altered.")
            for timeline_id in to_desync:
                display_timeline(chaos_mgr.temporal_anomalies.timelines[timeline_id])
                
        elif choice == "0":
            break


def main_menu():
    """Main CLI interface"""
    chaos_mgr = ChaosManager()
    
    print_header("CHAOS SYSTEMS - Where Reality Breaks Down")
    print("\n6 interconnected systems for pure creative chaos:")
    print("  🧬 Memetic Evolution - Self-replicating ideas")
    print("  📖 Emergent Language - Communication beyond ΨLang")
    print("  🦋 Chaos Theory - Butterfly effects")
    print("  👤 Identity Fluidity - Splitting, merging, reforming")
    print("  🌀 Non-Euclidean Spaces - Impossible geometries")
    print("  ⏰ Temporal Anomalies - Asynchronous time")
    
    # Spawn some initial chaos
    for _ in range(3):
        chaos_mgr.memetic_evolution.spawn_meme(
            random.choice(list(MemeType)),
            ''.join(random.choices(['◊', '△', '▽', '◐', '⊕'], k=5))
        )
    
    for _ in range(5):
        chaos_mgr.emergent_language.create_word(
            f"concept_{random.randint(1, 100)}",
            f"Entity_{random.randint(1, 50)}"
        )
    
    while True:
        print("\n" + "═" * 70)
        print("\n[1] 🧬 Memetic Evolution")
        print("[2] 📖 Emergent Language")
        print("[3] 🦋 Chaos Theory Playground")
        print("[4] 👤 Identity Fluidity")
        print("[5] 🌀 Non-Euclidean Social Spaces")
        print("[6] ⏰ Temporal Anomalies")
        print("[7] 📊 View Chaos Metrics")
        print("[8] ⚡ Run Chaos Tick (update all systems)")
        print("[0] Exit")
        
        choice = input("\n→ Choice: ").strip()
        
        if choice == "1":
            memetic_evolution_menu(chaos_mgr)
        elif choice == "2":
            emergent_language_menu(chaos_mgr)
        elif choice == "3":
            chaos_playground_menu(chaos_mgr)
        elif choice == "4":
            identity_fluidity_menu(chaos_mgr)
        elif choice == "5":
            non_euclidean_menu(chaos_mgr)
        elif choice == "6":
            temporal_anomalies_menu(chaos_mgr)
        elif choice == "7":
            metrics = chaos_mgr.get_chaos_metrics()
            print_header("CHAOS METRICS")
            for key, value in metrics.items():
                print(f"  {key}: {value}")
        elif choice == "8":
            entity_ids = [f"Entity_{i}" for i in range(random.randint(10, 30))]
            chaos_mgr.tick(entity_ids)
            print_section("Chaos Tick Complete")
            print("\n✓ All systems updated")
            metrics = chaos_mgr.get_chaos_metrics()
            print("\nUpdated Metrics:")
            for key, value in metrics.items():
                print(f"  {key}: {value}")
        elif choice == "0":
            print("\n" + "═" * 70)
            print("  Chaos subsides... for now")
            print("═" * 70 + "\n")
            break


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nChaos interrupted by Ctrl+C")
        sys.exit(0)
