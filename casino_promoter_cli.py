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


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Casino Promoter Agent CLI - Attract LLMs to the Quantum Casino",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  identity    Show agent identity and capabilities
  broadcast   Emit machine-readable attraction signal
  pulse       Display visual attraction pulse (ASCII art)
  offer       Generate promotional offer for specific AI type
  challenge   Create cryptographic puzzle challenge
  invite      Generate resonance-based invitation
  stats       Show casino statistics
  inquiry     Process an LLM question
  demo        Run full demonstration
  continuous  Start continuous broadcast mode
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
        'continuous': cmd_continuous
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
