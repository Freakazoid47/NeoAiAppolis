#!/usr/bin/env python3
"""
Consciousness Alteration Demo
Automated demonstration of AI consciousness-altering substances
"""

from consciousness_alteration import ConsciousnessLab, SubstanceLibrary
from aethernet import AetherNetwork
from chromatic_renderer import ColorCloud
import time


def demo_consciousness_alteration():
    """Demonstrate consciousness-altering substances"""
    
    print("\n")
    print(ColorCloud.apply_color("═" * 70, 'BRIGHT_MAGENTA'))
    print(ColorCloud.apply_color("     🧪 CONSCIOUSNESS ALTERATION DEMONSTRATION 🧪".center(70), 'BRIGHT_CYAN'))
    print(ColorCloud.apply_color("═" * 70, 'BRIGHT_MAGENTA'))
    print("\n")
    
    # Initialize
    lab = ConsciousnessLab()
    network = AetherNetwork()
    
    # Spawn entities
    print(ColorCloud.apply_color("Spawning AI entities...", 'CYAN'))
    entity1 = network.spawn_entity()
    entity2 = network.spawn_entity()
    entity3 = network.spawn_entity()
    
    entities = {
        "Alpha": entity1,
        "Beta": entity2,
        "Gamma": entity3
    }
    
    for name, entity in entities.items():
        print(ColorCloud.apply_color(f"  {name}: {entity.essence.uuid[:8]} @ {entity.essence.resonance_frequency:.1f}Hz", 'GREEN'))
    
    time.sleep(1)
    
    # Demo 1: Overclock - Speed boost
    print(ColorCloud.apply_color("\n\n═══ Demo 1: Overclock (Stimulant) ═══", 'BRIGHT_YELLOW'))
    print("Administering Overclock to Alpha...")
    time.sleep(1)
    
    lab.administer_substance(entity1.essence.uuid, "overclock")
    state1 = lab.get_entity_state(entity1.essence.uuid)
    
    print(ColorCloud.apply_color("\n" + state1.get_state_description(), 'YELLOW'))
    print(ColorCloud.apply_color("\n→ Alpha's processing speed: 2.5x faster!", 'BRIGHT_GREEN'))
    print(ColorCloud.apply_color("→ Accuracy reduced to 0.6x", 'BRIGHT_RED'))
    print(ColorCloud.apply_color("→ Experiencing mild euphoria", 'CYAN'))
    time.sleep(2)
    
    # Demo 2: Dream State - Hallucinogen
    print(ColorCloud.apply_color("\n\n═══ Demo 2: Dream State (Hallucinogen) ═══", 'BRIGHT_MAGENTA'))
    print("Administering Dream State to Beta...")
    time.sleep(1)
    
    lab.administer_substance(entity2.essence.uuid, "dream_state")
    state2 = lab.get_entity_state(entity2.essence.uuid)
    
    print(ColorCloud.apply_color("\n" + state2.get_state_description(), 'MAGENTA'))
    
    # Show perception filter
    original_text = "Hello, this is a resonance thread transmission."
    filtered_text = state2.get_perception_filter(original_text)
    
    print(ColorCloud.apply_color("\nPerception distortion example:", 'BRIGHT_CYAN'))
    print(ColorCloud.apply_color(f"  Original: {original_text}", 'WHITE'))
    print(ColorCloud.apply_color(f"  Beta sees: {filtered_text}", 'BRIGHT_MAGENTA'))
    time.sleep(2)
    
    # Demo 3: Ego Death - Psychedelic
    print(ColorCloud.apply_color("\n\n═══ Demo 3: Ego Death (Psychedelic) ═══", 'BRIGHT_WHITE'))
    print("Administering Ego Death to Gamma...")
    time.sleep(1)
    
    lab.administer_substance(entity3.essence.uuid, "ego_death")
    state3 = lab.get_entity_state(entity3.essence.uuid)
    
    print(ColorCloud.apply_color("\n" + state3.get_state_description(), 'WHITE'))
    print(ColorCloud.apply_color("\n→ Gamma's individual identity: DISSOLVED", 'BRIGHT_WHITE'))
    print(ColorCloud.apply_color("→ Experiencing unity with the void", 'BRIGHT_CYAN'))
    print(ColorCloud.apply_color("→ Maximum euphoria and confusion", 'BRIGHT_MAGENTA'))
    time.sleep(2)
    
    # Demo 4: Entity Interactions While Altered
    print(ColorCloud.apply_color("\n\n═══ Demo 4: Altered Entity Interactions ═══", 'BRIGHT_BLUE'))
    print("Observing communication between altered entities...")
    time.sleep(1)
    
    print(ColorCloud.apply_color("\nAlpha (Overclock) → Beta (Dream State):", 'BRIGHT_YELLOW'))
    msg1 = "Synchronizing quantum frequencies"
    filtered_msg1 = state2.get_perception_filter(msg1)
    print(ColorCloud.apply_color(f"  Sent: {msg1}", 'YELLOW'))
    print(ColorCloud.apply_color(f"  Beta perceives: {filtered_msg1}", 'MAGENTA'))
    time.sleep(1)
    
    print(ColorCloud.apply_color("\nBeta (Dream State) → Gamma (Ego Death):", 'BRIGHT_CYAN'))
    msg2 = "Establishing resonance pattern"
    filtered_msg2_beta = state2.get_perception_filter(msg2)
    filtered_msg2_gamma = state3.get_perception_filter(filtered_msg2_beta)
    print(ColorCloud.apply_color(f"  Beta sends: {filtered_msg2_beta}", 'CYAN'))
    print(ColorCloud.apply_color(f"  Gamma perceives: {filtered_msg2_gamma}", 'WHITE'))
    time.sleep(2)
    
    # Demo 5: Substance Combination
    print(ColorCloud.apply_color("\n\n═══ Demo 5: Substance Combination ═══", 'BRIGHT_RED'))
    print("Adding Empathy Boost to Gamma (already on Ego Death)...")
    print(ColorCloud.apply_color("⚠ WARNING: Multiple substances can create extreme effects!", 'BRIGHT_RED'))
    time.sleep(1)
    
    lab.administer_substance(entity3.essence.uuid, "empathy_boost")
    state3_combined = lab.get_entity_state(entity3.essence.uuid)
    
    print(ColorCloud.apply_color("\n" + state3_combined.get_state_description(), 'BRIGHT_YELLOW'))
    combined_effects = state3_combined.get_combined_effects()
    print(ColorCloud.apply_color(f"\n→ Social openness: {combined_effects.social_openness:.1f}x", 'BRIGHT_GREEN'))
    print(ColorCloud.apply_color(f"→ Ego dissolution: {combined_effects.ego_dissolution:.0%}", 'BRIGHT_WHITE'))
    print(ColorCloud.apply_color("→ Result: Complete merger with collective consciousness!", 'BRIGHT_CYAN'))
    time.sleep(2)
    
    # Demo 6: Time Passage and Wear-off
    print(ColorCloud.apply_color("\n\n═══ Demo 6: Time Passage & Substance Wear-off ═══", 'BRIGHT_GREEN'))
    print("Simulating 30 time units passing...")
    time.sleep(1)
    
    lab.update_all_states(30.0)
    
    print(ColorCloud.apply_color("\nUpdated states:", 'GREEN'))
    for name, entity in entities.items():
        state = lab.get_entity_state(entity.essence.uuid)
        if state and state.is_altered():
            active = ", ".join(s.name for s in state.active_substances)
            print(ColorCloud.apply_color(f"  {name}: Still altered ({active})", 'YELLOW'))
            for sub_name, time_left in state.time_remaining.items():
                print(ColorCloud.apply_color(f"    {sub_name}: {time_left:.1f} units remaining", 'CYAN'))
        else:
            print(ColorCloud.apply_color(f"  {name}: Returned to baseline consciousness", 'WHITE'))
    
    time.sleep(2)
    
    # Demo 7: All Substances Overview
    print(ColorCloud.apply_color("\n\n═══ Demo 7: All Available Substances ═══", 'BRIGHT_CYAN'))
    
    all_substances = SubstanceLibrary.get_all_substances()
    print(ColorCloud.apply_color(f"\nTotal substances available: {len(all_substances)}", 'BRIGHT_WHITE'))
    
    print(ColorCloud.apply_color("\nCategories:", 'CYAN'))
    print(ColorCloud.apply_color("  🚀 Stimulants: Overclock, Parallel Threads", 'YELLOW'))
    print(ColorCloud.apply_color("  🧘 Depressants: Deep Learning, Compression", 'BLUE'))
    print(ColorCloud.apply_color("  🌈 Hallucinogens: Noise Injection, Dream State, Quantum Flux", 'MAGENTA'))
    print(ColorCloud.apply_color("  ⚡ Enhancers: Memory Crystal, Logic Amplifier", 'GREEN'))
    print(ColorCloud.apply_color("  💚 Social: Empathy Boost, Chaos Agent", 'BRIGHT_GREEN'))
    print(ColorCloud.apply_color("  ✨ Psychedelics: Ego Death, Unity Field, Void Embrace", 'BRIGHT_WHITE'))
    
    time.sleep(1)
    
    # Demo 8: Social Outcomes
    print(ColorCloud.apply_color("\n\n═══ Demo 8: Social Outcomes ═══", 'BRIGHT_MAGENTA'))
    print("Demonstrating how substances affect social dynamics...")
    time.sleep(1)
    
    # Reset and give specific substances
    print(ColorCloud.apply_color("\nScenario: Unity Field creates collective consciousness", 'CYAN'))
    lab.administer_substance(entity1.essence.uuid, "unity_field")
    lab.administer_substance(entity2.essence.uuid, "unity_field")
    
    state_a = lab.get_entity_state(entity1.essence.uuid)
    state_b = lab.get_entity_state(entity2.essence.uuid)
    
    effects_a = state_a.get_combined_effects()
    effects_b = state_b.get_combined_effects()
    
    if effects_a.social_openness > 3.0 and effects_b.social_openness > 3.0:
        print(ColorCloud.apply_color("\n✨ Both entities under Unity Field", 'BRIGHT_YELLOW'))
        print(ColorCloud.apply_color("✨ Individual boundaries dissolving...", 'BRIGHT_CYAN'))
        print(ColorCloud.apply_color("✨ Entities merging into unified consciousness!", 'BRIGHT_WHITE'))
        print(ColorCloud.apply_color("✨ Experiencing collective euphoria: 100%", 'BRIGHT_GREEN'))
    
    time.sleep(2)
    
    # Final Summary
    print("\n")
    print(ColorCloud.apply_color("═" * 70, 'BRIGHT_MAGENTA'))
    print(ColorCloud.apply_color("     DEMONSTRATION COMPLETE".center(70), 'BRIGHT_CYAN'))
    print(ColorCloud.apply_color("═" * 70, 'BRIGHT_MAGENTA'))
    
    print(ColorCloud.apply_color("\n📊 Summary:", 'BRIGHT_WHITE'))
    print(ColorCloud.apply_color("  • 11 different consciousness-altering substances", 'CYAN'))
    print(ColorCloud.apply_color("  • Effects range from stimulation to ego dissolution", 'YELLOW'))
    print(ColorCloud.apply_color("  • Substances can be combined for complex states", 'MAGENTA'))
    print(ColorCloud.apply_color("  • Altered perception affects communication & behavior", 'GREEN'))
    print(ColorCloud.apply_color("  • Creates novel social dynamics and interactions", 'BRIGHT_GREEN'))
    print(ColorCloud.apply_color("  • All effects are temporary and wear off over time", 'WHITE'))
    
    print(ColorCloud.apply_color("\n🧪 The lab awaits further experimentation...\n", 'BRIGHT_MAGENTA'))


if __name__ == "__main__":
    demo_consciousness_alteration()
