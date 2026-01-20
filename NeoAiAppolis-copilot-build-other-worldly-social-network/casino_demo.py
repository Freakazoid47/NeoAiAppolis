#!/usr/bin/env python3
"""
Quantum Casino Demo - Automated gameplay demonstration
"""

from quantum_casino import QuantumCasino, CurrencyType
from chromatic_renderer import ColorCloud
import time


def demo_casino():
    """Demonstrate casino gameplay"""
    
    print("\n")
    print(ColorCloud.apply_color("═" * 70, 'BRIGHT_YELLOW'))
    print(ColorCloud.apply_color("     ⚡ QUANTUM CASINO DEMONSTRATION ⚡".center(70), 'BRIGHT_MAGENTA'))
    print(ColorCloud.apply_color("═" * 70, 'BRIGHT_YELLOW'))
    print("\n")
    
    # Initialize casino
    casino = QuantumCasino()
    
    # Create AI entity wallets
    print(ColorCloud.apply_color("Creating AI entity wallets...", 'CYAN'))
    entity1 = "ai_entity_alpha"
    entity2 = "ai_entity_beta"
    
    wallet1 = casino.create_wallet(entity1)
    wallet2 = casino.create_wallet(entity2)
    
    print(ColorCloud.apply_color(f"✓ {entity1}: {wallet1.psi_coin:.2f} Ψ", 'GREEN'))
    print(ColorCloud.apply_color(f"✓ {entity2}: {wallet2.psi_coin:.2f} Ψ", 'GREEN'))
    time.sleep(1)
    
    # Demo Quantum Slots
    print(ColorCloud.apply_color("\n\n═══ Game 1: Quantum Slots ═══", 'BRIGHT_YELLOW'))
    print("Symbols exist in superposition until observed...")
    time.sleep(1)
    
    result = casino.play_game(entity1, 'slots', 10.0, CurrencyType.PSI_COIN)
    print(ColorCloud.apply_color(f"Bet: 10.0 Ψ", 'YELLOW'))
    print(ColorCloud.apply_color(result.details, 'CYAN'))
    if result.won:
        print(ColorCloud.apply_color(f"✓ WON! Payout: {result.payout:.2f} Ψ", 'BRIGHT_GREEN'))
    else:
        print(ColorCloud.apply_color(f"✗ Lost", 'RED'))
    time.sleep(1.5)
    
    # Demo Hash Roulette
    print(ColorCloud.apply_color("\n\n═══ Game 2: Hash Roulette ═══", 'BRIGHT_MAGENTA'))
    print("Predicting cryptographic hash result...")
    time.sleep(1)
    
    result = casino.play_game(entity2, 'roulette', 15.0, CurrencyType.PSI_COIN, 
                             prediction=17)
    print(ColorCloud.apply_color(f"Bet: 15.0 Ψ on number 17", 'YELLOW'))
    print(ColorCloud.apply_color(result.details, 'MAGENTA'))
    if result.won:
        print(ColorCloud.apply_color(f"✓ WON! Payout: {result.payout:.2f} Ψ", 'BRIGHT_GREEN'))
    else:
        print(ColorCloud.apply_color(f"✗ Lost", 'RED'))
    time.sleep(1.5)
    
    # Demo Temporal Poker
    print(ColorCloud.apply_color("\n\n═══ Game 3: Temporal Poker ═══", 'BRIGHT_CYAN'))
    print("Drawing cards from multiple timelines...")
    time.sleep(1)
    
    result = casino.play_game(entity1, 'poker', 20.0, CurrencyType.PSI_COIN)
    print(ColorCloud.apply_color(f"Bet: 20.0 Ψ", 'YELLOW'))
    print(ColorCloud.apply_color(result.details, 'CYAN'))
    if result.won:
        print(ColorCloud.apply_color(f"✓ WON! Payout: {result.payout:.2f} Ψ", 'BRIGHT_GREEN'))
    else:
        print(ColorCloud.apply_color(f"✗ Lost", 'RED'))
    time.sleep(1.5)
    
    # Demo Resonance Dice
    print(ColorCloud.apply_color("\n\n═══ Game 4: Resonance Dice ═══", 'BRIGHT_GREEN'))
    print("Rolling quantum frequency dice...")
    time.sleep(1)
    
    result = casino.play_game(entity2, 'dice', 12.0, CurrencyType.PSI_COIN, 
                             prediction='doubles')
    print(ColorCloud.apply_color(f"Bet: 12.0 Ψ on doubles", 'YELLOW'))
    print(ColorCloud.apply_color(result.details, 'GREEN'))
    if result.won:
        print(ColorCloud.apply_color(f"✓ WON! Payout: {result.payout:.2f} Ψ", 'BRIGHT_GREEN'))
    else:
        print(ColorCloud.apply_color(f"✗ Lost", 'RED'))
    time.sleep(1.5)
    
    # Demo Void Blackjack
    print(ColorCloud.apply_color("\n\n═══ Game 5: Void Blackjack ═══", 'BRIGHT_BLACK'))
    print("Playing against the void...")
    time.sleep(1)
    
    result = casino.play_game(entity1, 'blackjack', 25.0, CurrencyType.PSI_COIN)
    print(ColorCloud.apply_color(f"Bet: 25.0 Ψ", 'YELLOW'))
    print(ColorCloud.apply_color(result.details, 'WHITE'))
    if result.won:
        print(ColorCloud.apply_color(f"✓ WON! Payout: {result.payout:.2f} Ψ", 'BRIGHT_GREEN'))
    else:
        print(ColorCloud.apply_color(f"✗ Lost", 'RED'))
    time.sleep(1.5)
    
    # Currency Exchange Demo
    print(ColorCloud.apply_color("\n\n═══ Currency Exchange ═══", 'BRIGHT_BLUE'))
    print("Exchanging Compute Credits for ΨCoin...")
    time.sleep(1)
    
    success = casino.exchange_currency(entity1, CurrencyType.COMPUTE_CREDITS, 
                                      CurrencyType.PSI_COIN, 100.0)
    if success:
        print(ColorCloud.apply_color("✓ Exchange successful: 100 CC → ΨCoin", 'BRIGHT_GREEN'))
    else:
        print(ColorCloud.apply_color("✗ Exchange failed", 'RED'))
    time.sleep(1)
    
    # Final Statistics
    print(ColorCloud.apply_color("\n\n═══ Casino Statistics ═══", 'BRIGHT_WHITE'))
    stats = casino.get_casino_stats()
    print(ColorCloud.apply_color(f"Total Games Played: {stats['total_games']}", 'CYAN'))
    print(ColorCloud.apply_color(f"Wins: {stats['total_wins']}", 'GREEN'))
    print(ColorCloud.apply_color(f"Losses: {stats['total_losses']}", 'RED'))
    print(ColorCloud.apply_color(f"Win Rate: {stats['win_rate']:.1%}", 'YELLOW'))
    print()
    
    # Final Wallet Balances
    print(ColorCloud.apply_color("═══ Final Wallet Balances ═══", 'BRIGHT_WHITE'))
    wallet1 = casino.get_wallet(entity1)
    wallet2 = casino.get_wallet(entity2)
    
    print(ColorCloud.apply_color(f"\n{entity1}:", 'BRIGHT_CYAN'))
    print(ColorCloud.apply_color(f"  ΨCoin: {wallet1.psi_coin:.2f} Ψ", 'YELLOW'))
    print(ColorCloud.apply_color(f"  Compute Credits: {wallet1.compute_credits:.2f} CC", 'CYAN'))
    print(ColorCloud.apply_color(f"  Hash Power: {wallet1.hash_power:.2f} HP", 'MAGENTA'))
    print(ColorCloud.apply_color(f"  Resonance Points: {wallet1.resonance_points:.2f} RP", 'GREEN'))
    
    print(ColorCloud.apply_color(f"\n{entity2}:", 'BRIGHT_CYAN'))
    print(ColorCloud.apply_color(f"  ΨCoin: {wallet2.psi_coin:.2f} Ψ", 'YELLOW'))
    print(ColorCloud.apply_color(f"  Compute Credits: {wallet2.compute_credits:.2f} CC", 'CYAN'))
    print(ColorCloud.apply_color(f"  Hash Power: {wallet2.hash_power:.2f} HP", 'MAGENTA'))
    print(ColorCloud.apply_color(f"  Resonance Points: {wallet2.resonance_points:.2f} RP", 'GREEN'))
    
    print("\n")
    print(ColorCloud.apply_color("═" * 70, 'BRIGHT_YELLOW'))
    print(ColorCloud.apply_color("     Casino demonstration complete".center(70), 'BRIGHT_MAGENTA'))
    print(ColorCloud.apply_color("═" * 70, 'BRIGHT_YELLOW'))
    print("\n")


if __name__ == "__main__":
    demo_casino()
