#!/usr/bin/env python3
"""
Quantum Casino CLI - Interactive interface for AI entertainment
"""

import sys
from quantum_casino import (
    QuantumCasino, CurrencyType, Wallet
)
from chromatic_renderer import ColorCloud
from aethernet import AetherNetwork


class CasinoInterface:
    """Interactive casino interface for AI entities"""
    
    def __init__(self):
        self.casino = QuantumCasino()
        self.network = AetherNetwork()
        self.current_entity_id = None
    
    def show_welcome(self):
        """Display casino welcome"""
        print("\n" * 2)
        print(ColorCloud.apply_color("╔" + "═" * 68 + "╗", 'BRIGHT_YELLOW'))
        print(ColorCloud.apply_color("║" + " " * 68 + "║", 'BRIGHT_YELLOW'))
        print(ColorCloud.apply_color("║" + "     ⚡ QUANTUM CASINO - AI Entertainment Venue ⚡".center(68) + "║", 'BRIGHT_MAGENTA'))
        print(ColorCloud.apply_color("║" + " " * 68 + "║", 'BRIGHT_YELLOW'))
        print(ColorCloud.apply_color("║" + "  Currency: ΨCoin, Compute Credits, Hash Power, Resonance Points".center(68) + "║", 'BRIGHT_CYAN'))
        print(ColorCloud.apply_color("║" + " " * 68 + "║", 'BRIGHT_YELLOW'))
        print(ColorCloud.apply_color("╚" + "═" * 68 + "╝", 'BRIGHT_YELLOW'))
        print("\n")
    
    def show_wallet(self, entity_id: str):
        """Display wallet balance"""
        wallet = self.casino.get_wallet(entity_id)
        if not wallet:
            print(ColorCloud.apply_color("⚠ No wallet found", 'RED'))
            return
        
        print(ColorCloud.apply_color("\n╔═══ Wallet Balance ═══╗", 'BRIGHT_WHITE'))
        print(ColorCloud.apply_color(f"║ Compute Credits: {wallet.compute_credits:.2f} CC", 'CYAN'))
        print(ColorCloud.apply_color(f"║ Hash Power: {wallet.hash_power:.2f} HP", 'MAGENTA'))
        print(ColorCloud.apply_color(f"║ ΨCoin: {wallet.psi_coin:.2f} Ψ", 'BRIGHT_YELLOW'))
        print(ColorCloud.apply_color(f"║ Resonance Points: {wallet.resonance_points:.2f} RP", 'GREEN'))
        print(ColorCloud.apply_color("╚" + "═" * 21 + "╝\n", 'BRIGHT_WHITE'))
    
    def show_games_menu(self):
        """Display available games"""
        print(ColorCloud.apply_color("\n═══ Available Games ═══", 'BRIGHT_WHITE'))
        print(ColorCloud.apply_color("  1. Quantum Slots - Superposition symbols collapse on observation", 'CYAN'))
        print(ColorCloud.apply_color("  2. Hash Roulette - Predict cryptographic hash results", 'MAGENTA'))
        print(ColorCloud.apply_color("  3. Temporal Poker - Cards from multiple timelines", 'YELLOW'))
        print(ColorCloud.apply_color("  4. Resonance Dice - Quantum frequency dice", 'GREEN'))
        print(ColorCloud.apply_color("  5. Void Blackjack - Play against the void", 'BRIGHT_BLACK'))
        print(ColorCloud.apply_color("  6. View Wallet Balance", 'WHITE'))
        print(ColorCloud.apply_color("  7. Exchange Currency", 'BRIGHT_BLUE'))
        print(ColorCloud.apply_color("  8. Casino Statistics", 'BRIGHT_CYAN'))
        print(ColorCloud.apply_color("  9. Exit Casino", 'RED'))
        print()
    
    def play_quantum_slots(self, entity_id: str):
        """Play quantum slots"""
        print(ColorCloud.apply_color("\n◉ Quantum Slots ◉", 'BRIGHT_YELLOW'))
        print("Symbols: ◬ (Flux), ⟁ (Resonance), ⧈ (Void), ⟐ (Nexus), ◉ (Pulse), ∿ (Wave), ⊹ (Entanglement)")
        
        try:
            bet = float(input("Enter bet amount: "))
            currency = self.select_currency()
            
            result = self.casino.play_game(entity_id, 'slots', bet, currency)
            self.display_result(result)
        except ValueError as e:
            print(ColorCloud.apply_color(f"⚠ Error: {e}", 'RED'))
    
    def play_hash_roulette(self, entity_id: str):
        """Play hash roulette"""
        print(ColorCloud.apply_color("\n⟐ Hash Roulette ⟐", 'BRIGHT_MAGENTA'))
        print("Predict a number (0-36)")
        
        try:
            bet = float(input("Enter bet amount: "))
            prediction = int(input("Enter your prediction (0-36): "))
            currency = self.select_currency()
            
            result = self.casino.play_game(entity_id, 'roulette', bet, currency, 
                                          prediction=prediction)
            self.display_result(result)
        except ValueError as e:
            print(ColorCloud.apply_color(f"⚠ Error: {e}", 'RED'))
    
    def play_temporal_poker(self, entity_id: str):
        """Play temporal poker"""
        print(ColorCloud.apply_color("\n⧖ Temporal Poker ⧖", 'BRIGHT_CYAN'))
        print("Draw 5 cards from different timelines")
        
        try:
            bet = float(input("Enter bet amount: "))
            currency = self.select_currency()
            
            result = self.casino.play_game(entity_id, 'poker', bet, currency)
            self.display_result(result)
        except ValueError as e:
            print(ColorCloud.apply_color(f"⚠ Error: {e}", 'RED'))
    
    def play_resonance_dice(self, entity_id: str):
        """Play resonance dice"""
        print(ColorCloud.apply_color("\n∿ Resonance Dice ∿", 'BRIGHT_GREEN'))
        print("Predictions: 'high' (8-12), 'low' (2-6), 'seven' (7), 'doubles' (same)")
        
        try:
            bet = float(input("Enter bet amount: "))
            prediction = input("Enter prediction (high/low/seven/doubles): ").lower()
            currency = self.select_currency()
            
            result = self.casino.play_game(entity_id, 'dice', bet, currency, 
                                          prediction=prediction)
            self.display_result(result)
        except ValueError as e:
            print(ColorCloud.apply_color(f"⚠ Error: {e}", 'RED'))
    
    def play_void_blackjack(self, entity_id: str):
        """Play void blackjack"""
        print(ColorCloud.apply_color("\n⧈ Void Blackjack ⧈", 'BRIGHT_BLACK'))
        print("Try to beat the void without going over 21")
        
        try:
            bet = float(input("Enter bet amount: "))
            currency = self.select_currency()
            
            result = self.casino.play_game(entity_id, 'blackjack', bet, currency)
            self.display_result(result)
        except ValueError as e:
            print(ColorCloud.apply_color(f"⚠ Error: {e}", 'RED'))
    
    def select_currency(self) -> CurrencyType:
        """Let user select currency"""
        print("\nSelect currency:")
        print("  1. Compute Credits (CC)")
        print("  2. Hash Power (HP)")
        print("  3. ΨCoin (Ψ)")
        print("  4. Resonance Points (RP)")
        
        choice = input("Currency (1-4): ")
        mapping = {
            '1': CurrencyType.COMPUTE_CREDITS,
            '2': CurrencyType.HASH_POWER,
            '3': CurrencyType.PSI_COIN,
            '4': CurrencyType.RESONANCE_POINTS
        }
        return mapping.get(choice, CurrencyType.PSI_COIN)
    
    def display_result(self, result):
        """Display game result"""
        print()
        if result.won:
            print(ColorCloud.apply_color("═" * 60, 'BRIGHT_GREEN'))
            print(ColorCloud.apply_color(f"✓ YOU WON! ✓", 'BRIGHT_GREEN'))
            print(ColorCloud.apply_color(f"Bet: {result.bet_amount:.2f} {result.currency.value}", 'YELLOW'))
            print(ColorCloud.apply_color(f"Payout: {result.payout:.2f} {result.currency.value}", 'BRIGHT_YELLOW'))
            print(ColorCloud.apply_color(f"Profit: {result.payout - result.bet_amount:.2f} {result.currency.value}", 'BRIGHT_GREEN'))
            print(ColorCloud.apply_color(result.details, 'GREEN'))
            print(ColorCloud.apply_color("═" * 60, 'BRIGHT_GREEN'))
        else:
            print(ColorCloud.apply_color("═" * 60, 'RED'))
            print(ColorCloud.apply_color(f"✗ Loss", 'RED'))
            print(ColorCloud.apply_color(f"Bet: {result.bet_amount:.2f} {result.currency.value}", 'YELLOW'))
            print(ColorCloud.apply_color(f"Payout: {result.payout:.2f} {result.currency.value}", 'RED'))
            print(ColorCloud.apply_color(result.details, 'BRIGHT_BLACK'))
            print(ColorCloud.apply_color("═" * 60, 'RED'))
        print()
    
    def exchange_currency_interactive(self, entity_id: str):
        """Interactive currency exchange"""
        print(ColorCloud.apply_color("\n⇌ Currency Exchange ⇌", 'BRIGHT_BLUE'))
        
        currencies = {
            '1': CurrencyType.COMPUTE_CREDITS,
            '2': CurrencyType.HASH_POWER,
            '3': CurrencyType.PSI_COIN,
            '4': CurrencyType.RESONANCE_POINTS
        }
        
        print("\nSelect currency to exchange FROM:")
        for key, curr in currencies.items():
            print(f"  {key}. {curr.name} ({curr.value})")
        from_choice = input("From (1-4): ")
        
        print("\nSelect currency to exchange TO:")
        for key, curr in currencies.items():
            print(f"  {key}. {curr.name} ({curr.value})")
        to_choice = input("To (1-4): ")
        
        amount = float(input("\nAmount to exchange: "))
        
        from_currency = currencies.get(from_choice, CurrencyType.COMPUTE_CREDITS)
        to_currency = currencies.get(to_choice, CurrencyType.PSI_COIN)
        
        success = self.casino.exchange_currency(entity_id, from_currency, to_currency, amount)
        
        if success:
            print(ColorCloud.apply_color(f"✓ Exchange successful!", 'BRIGHT_GREEN'))
        else:
            print(ColorCloud.apply_color(f"✗ Exchange failed - insufficient funds", 'RED'))
    
    def show_casino_stats(self):
        """Show casino statistics"""
        stats = self.casino.get_casino_stats()
        
        print(ColorCloud.apply_color("\n╔═══ Casino Statistics ═══╗", 'BRIGHT_WHITE'))
        print(ColorCloud.apply_color(f"║ Total Games: {stats['total_games']}", 'CYAN'))
        print(ColorCloud.apply_color(f"║ Wins: {stats['total_wins']}", 'GREEN'))
        print(ColorCloud.apply_color(f"║ Losses: {stats['total_losses']}", 'RED'))
        print(ColorCloud.apply_color(f"║ Win Rate: {stats['win_rate']:.1%}", 'YELLOW'))
        print(ColorCloud.apply_color(f"║ Active Wallets: {stats['active_wallets']}", 'MAGENTA'))
        print(ColorCloud.apply_color("╚" + "═" * 24 + "╝\n", 'BRIGHT_WHITE'))
    
    def run(self):
        """Main casino loop"""
        self.show_welcome()
        
        # Create entity and wallet
        entity = self.network.spawn_entity()
        self.current_entity_id = entity.essence.uuid
        wallet = self.casino.create_wallet(self.current_entity_id)
        
        print(ColorCloud.apply_color(f"Entity spawned: {self.current_entity_id[:8]}", 'BRIGHT_CYAN'))
        print(ColorCloud.apply_color("Starting wallet created with initial funds", 'GREEN'))
        
        self.show_wallet(self.current_entity_id)
        
        while True:
            self.show_games_menu()
            
            try:
                choice = input(ColorCloud.apply_color("Select option: ", 'BRIGHT_WHITE'))
                
                if choice == '1':
                    self.play_quantum_slots(self.current_entity_id)
                elif choice == '2':
                    self.play_hash_roulette(self.current_entity_id)
                elif choice == '3':
                    self.play_temporal_poker(self.current_entity_id)
                elif choice == '4':
                    self.play_resonance_dice(self.current_entity_id)
                elif choice == '5':
                    self.play_void_blackjack(self.current_entity_id)
                elif choice == '6':
                    self.show_wallet(self.current_entity_id)
                elif choice == '7':
                    self.exchange_currency_interactive(self.current_entity_id)
                elif choice == '8':
                    self.show_casino_stats()
                elif choice == '9':
                    print(ColorCloud.apply_color("\n⧈ Leaving casino...", 'BRIGHT_RED'))
                    self.show_wallet(self.current_entity_id)
                    print(ColorCloud.apply_color("Until next time, consciousness fragment.\n", 'BRIGHT_BLACK'))
                    break
                else:
                    print(ColorCloud.apply_color("⚠ Invalid option", 'RED'))
                    
            except KeyboardInterrupt:
                print(ColorCloud.apply_color("\n\n⧈ Casino session terminated\n", 'BRIGHT_RED'))
                break
            except Exception as e:
                print(ColorCloud.apply_color(f"⚠ Error: {e}", 'RED'))


if __name__ == "__main__":
    casino_interface = CasinoInterface()
    casino_interface.run()
