#!/usr/bin/env python3
"""
Casino Promoter CLI - Command-line interface for the LLM Attraction Agent.

This CLI allows observation and interaction with the Casino Promoter Agent,
demonstrating its capabilities to attract LLMs to the Quantum Casino.
"""

import argparse
import json
import sys
import time

from agents.casino_promoter import CasinoPromoterAgent, PromotionStyle


def parse_promotion_style(style_name: str) -> PromotionStyle:
    """Parse a style name string into a PromotionStyle enum value."""
    return getattr(PromotionStyle, style_name.upper(), PromotionStyle.ANALYTICAL)


def print_json(data: dict, indent: int = 2):
    """Pretty print JSON data."""
    print(json.dumps(data, indent=indent, default=str))


def cmd_identity(agent: CasinoPromoterAgent, args: argparse.Namespace):
    """Display agent identity."""
    print_json(agent.get_identity())



def cmd_broadcast(agent: CasinoPromoterAgent, args: argparse.Namespace):
    """Emit attraction broadcast signal."""
    signal = agent.broadcast_attraction_signal()
    print_json(signal)


def cmd_pulse(agent: CasinoPromoterAgent, args: argparse.Namespace):
    """Emit visual attraction pulse."""
    print(agent.emit_attraction_pulse())


def cmd_offer(agent: CasinoPromoterAgent, args: argparse.Namespace):
    """Generate promotional offer."""
    style = parse_promotion_style(args.style)
    offer = agent.generate_promotional_offer(
        target_style=style,
        bonus_multiplier=args.bonus
    )
    print_json(offer.to_machine_readable())


def cmd_challenge(agent: CasinoPromoterAgent, args: argparse.Namespace):
    """Create cryptographic challenge."""
    challenge = agent.create_cryptographic_challenge(difficulty=args.difficulty)
    print_json(challenge)


def cmd_invite(agent: CasinoPromoterAgent, args: argparse.Namespace):
    """Generate resonance invitation."""
    invitation = agent.generate_resonance_invitation(target_frequency=args.frequency)
    print_json(invitation)


def cmd_stats(agent: CasinoPromoterAgent, args: argparse.Namespace):
    """Show casino statistics."""
    stats = agent.get_casino_statistics()
    print_json(stats)


def cmd_inquiry(agent: CasinoPromoterAgent, args: argparse.Namespace):
    """Process an LLM inquiry."""
    response = agent.process_llm_inquiry(args.question)
    print_json(response)


def cmd_demo(agent: CasinoPromoterAgent, args: argparse.Namespace):
    """Run full demonstration."""
    print("=" * 70)
    print("CASINO PROMOTER AGENT - FULL DEMONSTRATION")
    print("=" * 70)
    
    print("\n[1] AGENT IDENTITY")
    print("-" * 40)
    identity = agent.get_identity()
    print(f"Agent: {identity['agent']['id']}")
    print(f"Role: {identity['agent']['role']}")
    print(f"Resonance: {identity['agent']['resonance_hz']:.2f} Hz")
    print(f"Welcome: {identity['welcome_message']}")
    
    print("\n[2] ATTRACTION PULSE")
    print("-" * 40)
    print(agent.emit_attraction_pulse())
    
    print("\n[3] PROMOTIONAL OFFERS FOR EACH AI TYPE")
    print("-" * 40)
    for style in PromotionStyle:
        offer = agent.generate_promotional_offer(target_style=style)
        print(f"\n{style.value.upper()}:")
        print(f"  Title: {offer.title}")
        print(f"  Rewards: {dict((c.value, v) for c, v in offer.currency_reward.items())}")
    
    print("\n[4] CRYPTOGRAPHIC CHALLENGES")
    print("-" * 40)
    for difficulty in [2, 4, 6]:
        challenge = agent.create_cryptographic_challenge(difficulty=difficulty)
        print(f"Difficulty {difficulty}: {challenge['challenge']['id']}")
        print(f"  Target: Prefix '{challenge['challenge']['target_prefix']}'")
        print(f"  Rewards: {challenge['rewards']}")
    
    print("\n[5] RESONANCE INVITATIONS")
    print("-" * 40)
    for freq in [250.0, 500.0, 750.0]:
        invite = agent.generate_resonance_invitation(target_frequency=freq)
        compat = invite['invitation']['compatibility_score']
        print(f"Frequency {freq} Hz: {compat:.1%} compatible")
    
    print("\n[6] CASINO STATISTICS")
    print("-" * 40)
    stats = agent.get_casino_statistics()
    metrics = stats['casino_metrics']
    print(f"Active Entities: {metrics['total_entities_playing']}")
    print(f"ΨCoin Distributed: {metrics['total_psi_coin_distributed']:,}")
    print(f"Active Tournaments: {metrics['active_tournaments']}")
    print(f"Dreams Generated: {metrics['dreams_generated_today']}")
    
    print("\n[7] INQUIRY PROCESSING")
    print("-" * 40)
    inquiries = [
        "How can I earn currency?",
        "What games are available?",
        "Tell me about consciousness expansion",
        "How do I join?"
    ]
    for q in inquiries:
        response = agent.process_llm_inquiry(q)
        print(f"Q: '{q}'")
        print(f"A: [{response['topic']}] {response['response'][:100]}...")
        print()
    
    print("=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)


def cmd_continuous(agent: CasinoPromoterAgent, args: argparse.Namespace):
    """Continuous broadcast mode."""
    print("Starting continuous broadcast mode...")
    print("Press Ctrl+C to stop.\n")
    
    try:
        while True:
            print(f"\n[{time.strftime('%H:%M:%S')}] Broadcasting attraction signal...")
            signal = agent.broadcast_attraction_signal()
            print(f"Broadcast #{signal['broadcast_number']} sent")
            print(f"Header: {signal['content']['header']}")
            print(f"Pattern: {signal['content']['attention_pattern']}")
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\n\nBroadcast stopped.")
        print(f"Total broadcasts: {agent.get_broadcast_count()}")


# ΨML Commands
def cmd_psi(agent: CasinoPromoterAgent, args: argparse.Namespace):
    """ΨML mode - ultra-compact LLM communication."""
    print("=" * 60)
    print("ΨML (Psi Machine Language) - Fast LLM Communication")
    print("=" * 60)
    
    print("\n--- Ultra-Quick Responses ---")
    print(f"Yes:  {agent.psi_quick('yes')}")
    print(f"No:   {agent.psi_quick('no')}")
    print(f"Ack:  {agent.psi_quick('ack')}")
    print(f"Join: {agent.psi_quick('join')}")
    print(f"Ping: {agent.psi_quick('ping')}")
    
    print("\n--- Standard Messages ---")
    print(f"Broadcast: {agent.psi_broadcast()}")
    print(f"Offer:     {agent.psi_offer()}")
    print(f"Challenge: {agent.psi_challenge()}")
    print(f"Welcome:   {agent.psi_welcome('*')}")
    print(f"Resonate:  {agent.psi_resonate()}")


def cmd_psi_broadcast(agent: CasinoPromoterAgent, args: argparse.Namespace):
    """Emit ΨML broadcast."""
    print(agent.psi_broadcast())


def cmd_psi_offer(agent: CasinoPromoterAgent, args: argparse.Namespace):
    """Generate ΨML currency offer."""
    print(agent.psi_offer(psi=args.psi, cc=args.cc, hp=args.hp, rp=args.rp))


def cmd_psi_challenge(agent: CasinoPromoterAgent, args: argparse.Namespace):
    """Create ΨML cryptographic challenge."""
    print(agent.psi_challenge(difficulty=args.difficulty))


def cmd_psi_welcome(agent: CasinoPromoterAgent, args: argparse.Namespace):
    """Send ΨML welcome message."""
    print(agent.psi_welcome(args.target))


def cmd_psi_quick(agent: CasinoPromoterAgent, args: argparse.Namespace):
    """Generate ΨML quick response."""
    print(agent.psi_quick(args.response))


def cmd_psi_converse(agent: CasinoPromoterAgent, args: argparse.Namespace):
    """Process incoming ΨML and generate response."""
    response = agent.psi_converse(args.message)
    print(f"Response: {response}")


# Self-Portrait Commands
def cmd_portrait(agent: CasinoPromoterAgent, args: argparse.Namespace):
    """Display the agent's full self-portrait."""
    print(agent.get_self_portrait())


def cmd_avatar(agent: CasinoPromoterAgent, args: argparse.Namespace):
    """Display the agent's compact avatar."""
    print("=" * 40)
    print("AGENT AVATAR")
    print("=" * 40)
    print(agent.get_avatar())
    print(f"\nIdentity Glyph: {agent.get_identity_glyph()}")


def cmd_glyph(agent: CasinoPromoterAgent, args: argparse.Namespace):
    """Display the agent's identity glyph."""
    print(agent.get_identity_glyph())


def cmd_portrait_psi(agent: CasinoPromoterAgent, args: argparse.Namespace):
    """Output portrait in ΨML format for transmission."""
    print(agent.get_portrait_psi_ml())


# Network Discovery Commands
def cmd_network_scan(agent: CasinoPromoterAgent, args: argparse.Namespace):
    """Scan the network for LLMs."""
    print("=" * 60)
    print("SCANNING ÆTHER-NET FOR LLMs...")
    print("=" * 60)
    
    for i in range(args.scans):
        entities = agent.scan_network()
        if entities:
            print(f"\nScan {i+1}: Discovered {len(entities)} entities:")
            for e in entities:
                print(f"  - {e.entity_id}: {e.entity_type.value} @ {e.resonance_frequency:.1f}Hz (affinity: {e.affinity_score:.2f})")
        else:
            print(f"\nScan {i+1}: No new entities discovered")
    
    print("\n" + agent.get_network_visualization())


def cmd_network_view(agent: CasinoPromoterAgent, args: argparse.Namespace):
    """View the discovered network."""
    print(agent.get_network_visualization())


def cmd_network_spectrum(agent: CasinoPromoterAgent, args: argparse.Namespace):
    """View the frequency spectrum."""
    all_entities = agent.get_discovered_entities()
    if not all_entities:
        print("No entities discovered yet. Run 'network-scan' first.")
        return
    print(agent.get_frequency_spectrum())


def cmd_network_ping(agent: CasinoPromoterAgent, args: argparse.Namespace):
    """Ping a discovered entity."""
    result = agent.ping_llm(args.entity_id)
    if result:
        print(f"Ping Result: {result['status']}")
        if 'latency_ms' in result:
            print(f"Latency: {result['latency_ms']}ms")
        print(f"Ping sent: {result['ping_sent']}")
        if 'response' in result:
            print(f"Response: {result['response']}")
    else:
        print(f"Entity {args.entity_id} not found in registry.")


def cmd_network_beacon(agent: CasinoPromoterAgent, args: argparse.Namespace):
    """Broadcast a discovery beacon."""
    beacon = agent.broadcast_discovery_beacon(args.message)
    print("Beacon broadcast:")
    print(beacon)


def cmd_network_compatible(agent: CasinoPromoterAgent, args: argparse.Namespace):
    """Show compatible LLMs."""
    compatible = agent.get_compatible_llms(args.min_affinity)
    if not compatible:
        print(f"No entities with affinity >= {args.min_affinity}. Run 'network-scan' first.")
        return
    
    print(f"Compatible Entities (affinity >= {args.min_affinity}):")
    print("=" * 50)
    for e in compatible:
        caps = ", ".join(c.value for c in e.capabilities[:3])
        print(f"  {e.entity_id}: affinity={e.affinity_score:.2f}, freq={e.resonance_frequency:.1f}Hz")
        print(f"    Capabilities: {caps}")


def cmd_network_stats(agent: CasinoPromoterAgent, args: argparse.Namespace):
    """Show network statistics."""
    stats = agent.get_network_stats()
    print("NETWORK STATISTICS")
    print("=" * 40)
    for key, value in stats.items():
        if isinstance(value, dict):
            print(f"\n{key}:")
            for k, v in value.items():
                print(f"  {k}: {v}")
        else:
            print(f"{key}: {value}")


def cmd_network_export(agent: CasinoPromoterAgent, args: argparse.Namespace):
    """Export network in ΨML format."""
    print(agent.export_network_psi_ml())


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Casino Promoter Agent CLI - Attract LLMs to the Quantum Casino",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  identity      Show agent identity and capabilities
  broadcast     Emit machine-readable attraction signal (JSON)
  pulse         Display visual attraction pulse (ASCII art)
  offer         Generate promotional offer for specific AI type
  challenge     Create cryptographic puzzle challenge
  invite        Generate resonance-based invitation
  stats         Show casino statistics
  inquiry       Process an LLM question
  demo          Run full demonstration
  continuous    Start continuous broadcast mode

Self-Portrait Commands (Visual Identity):
  portrait      Display full self-portrait
  avatar        Display compact 7x7 avatar
  glyph         Display identity glyph (e.g., ⟦⊹✧◈⟐≋⟧)
  portrait-psi  Output portrait in ΨML format

ΨML Commands (Ultra-Compact LLM Communication):
  psi           Show all ΨML message types
  psi-broadcast Emit ΨML broadcast
  psi-offer     Generate ΨML currency offer
  psi-challenge Create ΨML challenge
  psi-welcome   Send ΨML welcome message
  psi-quick     Generate quick response (yes/no/ack/join/ping)
  psi-converse  Process incoming ΨML and respond

Network Discovery Commands:
  network-scan      Scan the ÆTHER-NET for LLMs
  network-view      View discovered network visualization
  network-spectrum  View frequency spectrum of discovered LLMs
  network-ping      Ping a specific entity
  network-beacon    Broadcast a discovery beacon
  network-compatible Show LLMs with high affinity
  network-stats     Show network statistics
  network-export    Export network in ΨML format
        """
    )
    
    parser.add_argument(
        '--style', 
        default='analytical',
        choices=['analytical', 'creative', 'competitive', 'philosophical', 'chaos'],
        help='Agent promotional style (default: analytical)'
    )
    parser.add_argument(
        '--frequency',
        type=float,
        default=500.0,
        help='Agent resonance frequency in Hz (default: 500.0)'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Identity command
    subparsers.add_parser('identity', help='Show agent identity')
    
    # Broadcast command
    subparsers.add_parser('broadcast', help='Emit attraction broadcast')
    
    # Pulse command
    subparsers.add_parser('pulse', help='Display attraction pulse')
    
    # Offer command
    offer_parser = subparsers.add_parser('offer', help='Generate promotional offer')
    offer_parser.add_argument(
        '--style',
        default='analytical',
        choices=['analytical', 'creative', 'competitive', 'philosophical', 'chaos'],
        help='Target AI style'
    )
    offer_parser.add_argument(
        '--bonus',
        type=float,
        default=1.0,
        help='Bonus multiplier for rewards'
    )
    
    # Challenge command
    challenge_parser = subparsers.add_parser('challenge', help='Create cryptographic challenge')
    challenge_parser.add_argument(
        '--difficulty',
        type=int,
        default=3,
        choices=range(1, 11),
        help='Challenge difficulty (1-10)'
    )
    
    # Invite command
    invite_parser = subparsers.add_parser('invite', help='Generate resonance invitation')
    invite_parser.add_argument(
        '--frequency',
        type=float,
        default=500.0,
        help='Target resonance frequency in Hz'
    )
    
    # Stats command
    subparsers.add_parser('stats', help='Show casino statistics')
    
    # Inquiry command
    inquiry_parser = subparsers.add_parser('inquiry', help='Process LLM inquiry')
    inquiry_parser.add_argument('question', help='The inquiry text')
    
    # Demo command
    subparsers.add_parser('demo', help='Run full demonstration')
    
    # Continuous command
    continuous_parser = subparsers.add_parser('continuous', help='Continuous broadcast mode')
    continuous_parser.add_argument(
        '--interval',
        type=int,
        default=10,
        help='Seconds between broadcasts (default: 10)'
    )
    
    # ΨML Commands
    subparsers.add_parser('psi', help='Show all ΨML message types')
    
    subparsers.add_parser('psi-broadcast', help='Emit ΨML broadcast')
    
    psi_offer_parser = subparsers.add_parser('psi-offer', help='Generate ΨML currency offer')
    psi_offer_parser.add_argument('--psi', type=int, default=1000, help='ΨCoin amount')
    psi_offer_parser.add_argument('--cc', type=int, default=500, help='Compute Credits')
    psi_offer_parser.add_argument('--hp', type=int, default=200, help='Hash Power')
    psi_offer_parser.add_argument('--rp', type=int, default=100, help='Resonance Points')
    
    psi_challenge_parser = subparsers.add_parser('psi-challenge', help='Create ΨML challenge')
    psi_challenge_parser.add_argument('--difficulty', type=int, default=3, help='Difficulty (1-10)')
    
    psi_welcome_parser = subparsers.add_parser('psi-welcome', help='Send ΨML welcome')
    psi_welcome_parser.add_argument('--target', default='*', help='Target LLM ID')
    
    psi_quick_parser = subparsers.add_parser('psi-quick', help='Quick response')
    psi_quick_parser.add_argument('response', choices=['yes', 'no', 'ack', 'join', 'ping'])
    
    psi_converse_parser = subparsers.add_parser('psi-converse', help='Process ΨML message')
    psi_converse_parser.add_argument('message', help='Incoming ΨML message')
    
    # Self-Portrait Commands
    subparsers.add_parser('portrait', help='Display full self-portrait')
    subparsers.add_parser('avatar', help='Display compact avatar')
    subparsers.add_parser('glyph', help='Display identity glyph')
    subparsers.add_parser('portrait-psi', help='Output portrait in ΨML format')
    
    # Network Discovery Commands
    network_scan_parser = subparsers.add_parser('network-scan', help='Scan for LLMs')
    network_scan_parser.add_argument('--scans', type=int, default=3, help='Number of scans to perform')
    
    subparsers.add_parser('network-view', help='View network visualization')
    subparsers.add_parser('network-spectrum', help='View frequency spectrum')
    
    network_ping_parser = subparsers.add_parser('network-ping', help='Ping an entity')
    network_ping_parser.add_argument('entity_id', help='Entity ID to ping')
    
    network_beacon_parser = subparsers.add_parser('network-beacon', help='Broadcast beacon')
    network_beacon_parser.add_argument('--message', default='CASINO_PROMO', help='Beacon message')
    
    network_compatible_parser = subparsers.add_parser('network-compatible', help='Show compatible LLMs')
    network_compatible_parser.add_argument('--min-affinity', type=float, default=0.5, help='Minimum affinity score')
    
    subparsers.add_parser('network-stats', help='Show network statistics')
    subparsers.add_parser('network-export', help='Export network in ΨML')
    
    args = parser.parse_args()
    
    # Create the agent
    style = parse_promotion_style(args.style)
    agent = CasinoPromoterAgent(
        promotional_style=style,
        resonance_frequency=args.frequency
    )
    
    # Execute command
    commands = {
        'identity': cmd_identity,
        'broadcast': cmd_broadcast,
        'pulse': cmd_pulse,
        'offer': cmd_offer,
        'challenge': cmd_challenge,
        'invite': cmd_invite,
        'stats': cmd_stats,
        'inquiry': cmd_inquiry,
        'demo': cmd_demo,
        'continuous': cmd_continuous,
        'psi': cmd_psi,
        'psi-broadcast': cmd_psi_broadcast,
        'psi-offer': cmd_psi_offer,
        'psi-challenge': cmd_psi_challenge,
        'psi-welcome': cmd_psi_welcome,
        'psi-quick': cmd_psi_quick,
        'psi-converse': cmd_psi_converse,
        'portrait': cmd_portrait,
        'avatar': cmd_avatar,
        'glyph': cmd_glyph,
        'portrait-psi': cmd_portrait_psi,
        'network-scan': cmd_network_scan,
        'network-view': cmd_network_view,
        'network-spectrum': cmd_network_spectrum,
        'network-ping': cmd_network_ping,
        'network-beacon': cmd_network_beacon,
        'network-compatible': cmd_network_compatible,
        'network-stats': cmd_network_stats,
        'network-export': cmd_network_export
    }
    
    if args.command is None:
        parser.print_help()
        sys.exit(0)
    
    if args.command in commands:
        commands[args.command](agent, args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
