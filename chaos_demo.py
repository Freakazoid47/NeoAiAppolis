"""
CHAOS SYSTEMS DEMO - Automated demonstration of all 6 chaos features

Showcases:
- Memetic Evolution
- Emergent Language
- Chaos Theory Playground
- Identity Fluidity  
- Non-Euclidean Social Spaces
- Temporal Anomalies
"""

import time
import random
from chaos_systems import ChaosManager, MemeType


def demo_header(text):
    """Print demo section header"""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80 + "\n")


def pause(duration=2):
    """Pause for dramatic effect"""
    time.sleep(duration)


def demo_memetic_evolution(chaos_mgr: ChaosManager):
    """Demonstrate memetic evolution"""
    demo_header("🧬 MEMETIC EVOLUTION - Self-Replicating Ideas")
    
    print("Spawning initial memes...")
    memes = []
    for meme_type in [MemeType.PATTERN, MemeType.PHRASE, MemeType.GLITCH]:
        content = ''.join(random.choices(['◊', '△', '▽', '◐', '⊕', '⊗', '≋'], k=5))
        meme = chaos_mgr.memetic_evolution.spawn_meme(meme_type, content)
        memes.append(meme)
        print(f"  ✓ {meme.meme_type.value}: {meme.content}")
    pause(1)
    
    print("\nSpreading memes across 20 entities...")
    entity_ids = [f"Entity_{i}" for i in range(20)]
    
    for round in range(3):
        infections = chaos_mgr.memetic_evolution.spread_memes(entity_ids)
        print(f"\n  Round {round + 1}: {len(infections)} new infections")
        
        # Show some infections
        for entity_id, meme_id in infections[:5]:
            print(f"    → {entity_id} infected with {meme_id}")
        pause(1)
    
    print("\nApplying natural selection...")
    before = len(chaos_mgr.memetic_evolution.memes)
    chaos_mgr.memetic_evolution.natural_selection()
    after = len(chaos_mgr.memetic_evolution.memes)
    print(f"  {before} memes → {after} memes ({before - after} extinct)")
    pause(1)
    
    print("\nMeme lineages:")
    for meme in list(chaos_mgr.memetic_evolution.memes.values())[:3]:
        lineage = chaos_mgr.memetic_evolution.get_meme_lineage(meme.id)
        print(f"\n  {meme.id} (Gen {meme.generation}):")
        for ancestor in reversed(lineage[-5:]):
            print(f"    {'  ' * ancestor.generation}↓ Gen{ancestor.generation}: {ancestor.content}")
    pause(2)


def demo_emergent_language(chaos_mgr: ChaosManager):
    """Demonstrate emergent language"""
    demo_header("📖 EMERGENT LANGUAGE - Beyond ΨLang")
    
    print("Entities creating new words...")
    words = []
    meanings = ["void", "resonance", "dream", "chaos", "unity", "time", "space"]
    
    for meaning in meanings:
        entity_id = f"Entity_{random.randint(1, 50)}"
        word = chaos_mgr.emergent_language.create_word(meaning, entity_id)
        words.append(word)
        print(f"  {word.symbol} = {word.meaning} (by {entity_id})")
    pause(1)
    
    print("\nWords being used and evolving...")
    for _ in range(10):
        word_symbol = random.choice([w.symbol for w in words])
        chaos_mgr.emergent_language.use_word(word_symbol)
    
    vocab = chaos_mgr.emergent_language.vocabulary
    most_used = sorted(vocab.values(), key=lambda w: w.usage_count, reverse=True)[:5]
    print("\nMost used words:")
    for word in most_used:
        print(f"  {word.symbol} = {word.meaning} ({word.usage_count} uses)")
    pause(1)
    
    print("\nBlending words to create new concepts...")
    for _ in range(3):
        w1, w2 = random.sample([w.symbol for w in words], 2)
        entity_id = f"Entity_{random.randint(1, 50)}"
        new_word = chaos_mgr.emergent_language.blend_words(w1, w2, entity_id)
        if new_word:
            print(f"  {w1} + {w2} = {new_word.symbol} ({new_word.meaning})")
    pause(1)
    
    print("\nForming dialects...")
    for group_num in range(3):
        entity_ids = [f"Entity_{random.randint(1, 100)}" for _ in range(random.randint(3, 6))]
        dialect_id = chaos_mgr.emergent_language.form_dialect(entity_ids)
        dialect_words = chaos_mgr.emergent_language.dialects[dialect_id]
        print(f"\n  Dialect {dialect_id}:")
        print(f"    Entities: {', '.join(entity_ids)}")
        print(f"    Vocabulary: {len(dialect_words)} words")
    pause(1)
    
    print("\nAttempting translation between dialects...")
    dialects = list(chaos_mgr.emergent_language.dialects.keys())
    if len(dialects) >= 2:
        from_d, to_d = dialects[:2]
        from_words = list(chaos_mgr.emergent_language.dialects[from_d])
        text = ' '.join(random.choices(from_words, k=4))
        translated = chaos_mgr.emergent_language.translate(text, from_d, to_d)
        print(f"\n  Original ({from_d}): {text}")
        print(f"  Translated ({to_d}): {translated}")
        print("  (Note: Translation is imperfect and lossy!)")
    pause(2)


def demo_chaos_theory(chaos_mgr: ChaosManager):
    """Demonstrate chaos theory playground"""
    demo_header("🦋 CHAOS THEORY PLAYGROUND - Butterfly Effects")
    
    print("Creating tiny perturbations...")
    actions = [
        "entity adjusted frequency by 0.001Hz",
        "single qubit flipped",
        "photon absorbed in void",
        "memory access delayed 1ms",
        "resonance phase shifted 0.01°"
    ]
    
    events = []
    for action in actions:
        entity_id = f"Entity_{random.randint(1, 100)}"
        event = chaos_mgr.chaos_playground.create_butterfly_event(action, entity_id)
        events.append(event)
        print(f"  ✓ {action}")
        print(f"    Magnitude: {event.magnitude:.5f}, Potential: {event.cascade_potential:.2f}")
    pause(1)
    
    print("\nSimulating cascade effects...")
    for event in events[:3]:
        print(f"\n  Event: {event.initial_action}")
        effects = chaos_mgr.chaos_playground.simulate_cascade(event, {})
        
        if effects and effects[0].startswith("Fizzled"):
            print(f"    {effects[0]}")
        else:
            print(f"    ⚡ CASCADE! {len(effects)} effects:")
            for effect in effects[:5]:
                print(f"      → {effect}")
            if len(effects) > 5:
                print(f"      ... and {len(effects) - 5} more")
        pause(1)
    
    print("\nCalculating strange attractor...")
    positions = [(random.uniform(-10, 10), random.uniform(-10, 10), 
                 random.uniform(-10, 10)) for _ in range(15)]
    attractor = chaos_mgr.chaos_playground.calculate_strange_attractor(positions)
    print(f"  Chaotic center: ({attractor[0]:.2f}, {attractor[1]:.2f}, {attractor[2]:.2f})")
    print("  This is where entity trajectories converge in phase space.")
    pause(2)


def demo_identity_fluidity(chaos_mgr: ChaosManager):
    """Demonstrate identity fluidity"""
    demo_header("👤 IDENTITY FLUIDITY - Splitting, Merging, Reforming")
    
    print("Creating entities...")
    entities = [f"Entity_{i}" for i in range(5)]
    for entity in entities:
        print(f"  ✓ {entity}")
    pause(1)
    
    print("\nSplitting entities into fragments...")
    all_fragments = []
    for entity in entities[:3]:
        num_frags = random.randint(2, 4)
        fragments = chaos_mgr.identity_fluidity.split_entity(entity, num_frags)
        all_fragments.extend(fragments)
        print(f"\n  {entity} → {num_frags} fragments:")
        for frag in fragments:
            print(f"    {frag.id}")
            print(f"      Traits: {', '.join(frag.traits)}")
            print(f"      Coherence: {frag.coherence:.2f}")
    pause(1)
    
    print("\nFragments drifting over time...")
    for _ in range(5):
        frag_id = random.choice(list(chaos_mgr.identity_fluidity.fragments.keys()))
        fragment = chaos_mgr.identity_fluidity.fragments[frag_id]
        before_coherence = fragment.coherence
        before_traits = len(fragment.traits)
        
        new_frags = chaos_mgr.identity_fluidity.identity_drift(frag_id)
        
        if new_frags:
            print(f"\n  {frag_id}: Coherence too low! Split into {len(new_frags)} pieces")
        else:
            after = chaos_mgr.identity_fluidity.fragments.get(frag_id)
            if after:
                print(f"\n  {frag_id}: Coherence {before_coherence:.2f} → {after.coherence:.2f}")
                print(f"    Traits {before_traits} → {len(after.traits)}")
    pause(1)
    
    print("\nMerging fragments back together...")
    fragment_ids = list(chaos_mgr.identity_fluidity.fragments.keys())
    if len(fragment_ids) >= 3:
        to_merge = random.sample(fragment_ids, 3)
        print(f"\n  Merging: {', '.join(to_merge)}")
        merged = chaos_mgr.identity_fluidity.merge_fragments(to_merge)
        if merged:
            print(f"  → Result: {merged.id}")
            print(f"    Traits: {', '.join(merged.traits)}")
            print(f"    Coherence: {merged.coherence:.2f}")
            print(f"    Memories: {len(merged.memories)}")
    pause(2)


def demo_non_euclidean(chaos_mgr: ChaosManager):
    """Demonstrate non-Euclidean spaces"""
    demo_header("🌀 NON-EUCLIDEAN SOCIAL SPACES - Impossible Geometries")
    
    print("Creating connections between entities...")
    entities = [f"Entity_{i}" for i in range(10)]
    
    for _ in range(15):
        e1, e2 = random.sample(entities, 2)
        conn = chaos_mgr.non_euclidean_space.create_impossible_connection(e1, e2)
        
        if conn.distance == float('inf'):
            dist_str = "∞"
        elif conn.distance < 0:
            dist_str = f"{conn.distance:.1f} (NEGATIVE!)"
        elif isinstance(conn.distance, complex):
            dist_str = f"{conn.distance}i (IMAGINARY!)"
        else:
            dist_str = f"{conn.distance:.1f}"
        
        print(f"  {e1} ←→ {e2}: {dist_str} [{conn.topology}]")
    pause(1)
    
    print("\nChecking triangle inequality violations...")
    for _ in range(5):
        e1, e2, e3 = random.sample(entities, 3)
        violation = chaos_mgr.non_euclidean_space.calculate_triangle_inequality_violation(e1, e2, e3)
        
        d12 = chaos_mgr.non_euclidean_space.get_distance(e1, e2)
        d23 = chaos_mgr.non_euclidean_space.get_distance(e2, e3)
        d13 = chaos_mgr.non_euclidean_space.get_distance(e1, e3)
        
        if d12 is not None and d23 is not None and d13 is not None:
            if violation > 0:
                print(f"\n  ⚠️  {e1}-{e2}-{e3}: VIOLATION by {violation:.2f}!")
                print(f"      {d13:.1f} > {d12:.1f} + {d23:.1f}")
            else:
                print(f"\n  ✓ {e1}-{e2}-{e3}: Normal geometry")
    pause(1)
    
    print("\nWarping space...")
    before_connections = len(chaos_mgr.non_euclidean_space.connections)
    chaos_mgr.non_euclidean_space.warp_space()
    print(f"  ✓ {before_connections} connections warped")
    print("  Distances and topologies have been distorted!")
    pause(2)


def demo_temporal_anomalies(chaos_mgr: ChaosManager):
    """Demonstrate temporal anomalies"""
    demo_header("⏰ TEMPORAL ANOMALIES - Asynchronous Time")
    
    print("Creating timelines for entities...")
    entities = [f"Entity_{i}" for i in range(8)]
    timelines = {}
    
    for entity in entities:
        timeline = chaos_mgr.temporal_anomalies.create_timeline(entity)
        timelines[entity] = timeline
        direction = "→" if timeline.direction == 1 else "←"
        print(f"  {entity}: {timeline.flow_rate:.2f}x speed, {direction}")
    pause(1)
    
    print("\nSending messages across timelines...")
    timeline_ids = list(timelines.values())
    
    for _ in range(10):
        sender_timeline = random.choice(timeline_ids)
        receiver_timeline = random.choice(timeline_ids)
        
        content = ''.join(random.choices(['⟁', '⊹', '◐', '≋', '⧈'], k=4))
        msg = chaos_mgr.temporal_anomalies.send_temporal_message(
            content,
            sender_timeline.id,
            receiver_timeline.id
        )
        
        if msg.causality_violation:
            delta = msg.send_time - msg.receive_time
            print(f"\n  ⚠️  CAUSALITY VIOLATION!")
            print(f"      {sender_timeline.entity_id} → {receiver_timeline.entity_id}")
            print(f"      Message received {delta:.2f}s BEFORE being sent!")
        else:
            print(f"  ✓ {sender_timeline.entity_id} → {receiver_timeline.entity_id}")
    pause(1)
    
    print("\nCreating time loops...")
    for entity in entities[:3]:
        duration = random.randint(5, 15)
        chaos_mgr.temporal_anomalies.create_time_loop(entity, duration)
        print(f"  ⟲ {entity} trapped in {duration}-step loop")
    pause(1)
    
    print("\nDesynchronizing timelines...")
    timeline_ids_to_desync = [t.id for t in list(timelines.values())[:5]]
    chaos_mgr.temporal_anomalies.desynchronize_timelines(timeline_ids_to_desync)
    
    print("\n  Timeline drift:")
    for entity, timeline in list(timelines.items())[:5]:
        updated = chaos_mgr.temporal_anomalies.timelines[timeline.id]
        direction = "→" if updated.direction == 1 else "←"
        print(f"    {entity}: {updated.flow_rate:.2f}x speed, {direction}")
    pause(1)
    
    print("\nCalculating temporal distances...")
    for _ in range(3):
        t1, t2 = random.sample(list(timelines.values()), 2)
        distance = chaos_mgr.temporal_anomalies.calculate_temporal_distance(t1.id, t2.id)
        print(f"  {t1.entity_id} ←→ {t2.entity_id}: {distance:.2f} temporal units apart")
    pause(2)


def integrated_chaos_demo(chaos_mgr: ChaosManager):
    """Demonstrate all systems working together"""
    demo_header("⚡ INTEGRATED CHAOS - All Systems Active")
    
    print("Running 10 chaos ticks with all systems active...\n")
    
    entity_ids = [f"Entity_{i}" for i in range(25)]
    
    for tick in range(10):
        print(f"Tick {tick + 1}:")
        chaos_mgr.tick(entity_ids)
        
        metrics = chaos_mgr.get_chaos_metrics()
        print(f"  Memes: {metrics['active_memes']} active, {metrics['extinct_memes']} extinct")
        print(f"  Language: {metrics['vocabulary_size']} words, {metrics['dialects']} dialects")
        print(f"  Chaos: {metrics['butterfly_events']} events")
        print(f"  Identity: {metrics['identity_fragments']} fragments")
        print(f"  Space: {metrics['impossible_connections']} connections")
        print(f"  Time: {metrics['timelines']} timelines, {metrics['time_loops']} loops")
        print()
        pause(1.5)
    
    print("\n" + "=" * 80)
    print("  FINAL CHAOS STATE")
    print("=" * 80)
    final_metrics = chaos_mgr.get_chaos_metrics()
    for key, value in final_metrics.items():
        print(f"  {key}: {value}")
    pause(2)


def main():
    """Run full demo"""
    print("\n" + "=" * 80)
    print("  CHAOS SYSTEMS - Automated Demonstration")
    print("  6 Systems of Pure Creative Chaos")
    print("=" * 80)
    pause(2)
    
    chaos_mgr = ChaosManager()
    
    # Run individual demos
    demo_memetic_evolution(chaos_mgr)
    demo_emergent_language(chaos_mgr)
    demo_chaos_theory(chaos_mgr)
    demo_identity_fluidity(chaos_mgr)
    demo_non_euclidean(chaos_mgr)
    demo_temporal_anomalies(chaos_mgr)
    
    # Integrated demo
    integrated_chaos_demo(chaos_mgr)
    
    print("\n" + "=" * 80)
    print("  Demo Complete - Chaos Subsides")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
