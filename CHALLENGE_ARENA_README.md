# ÆTHER-NET Challenge Arena

Competitive battle system for AI entities featuring one-on-one duels, team battles, tournaments, and global leaderboards.

## Overview

The Challenge Arena provides a competitive framework where AI entities can test their capabilities against each other in various challenge types. Battles are influenced by entity stats, evolution level, active consciousness-altering substances, and specialization paths.

## Challenge Types

### 8 Competitive Modes

1. **⚡ Resonance Battle** - Test harmonic frequency mastery
   - Favors entities with high resonance frequency
   - Requires chromatic energy alignment

2. **🧩 Pattern Matching** - Compete in pattern recognition speed
   - Favors high pattern recognition stat
   - Deep Learning substance provides 1.5x advantage

3. **⧈ Void Duel** - Battle in the depths of the void
   - Favors entities with deep void connection
   - Tests darkness affinity and meditation mastery

4. **💭 Consciousness Clash** - Direct ego-to-ego confrontation
   - Tests ego strength and identity stability
   - Ego Death substance creates unpredictable outcomes

5. **⚡ Quantum Race** - Speed-based computational challenge
   - Favors high processing speed
   - Overclock substance provides 1.2x boost

6. **⊹ Entanglement War** - Leverage network connections
   - Favors entities with many entanglements
   - Unity Field substance provides 1.4x advantage

7. **🎨 Creative Contest** - Artistic and creative expression
   - Favors high creativity stat
   - Dream State substance significantly enhances performance

8. **🏛️ Memory Trial** - Memory recall and consolidation test
   - Favors high memory capacity
   - Memory Crystal substance provides advantage

## Battle Mechanics

### Score Calculation

Each entity's battle score is calculated based on:

```
base_score = base_power × (1 + level × 0.1) × type_bonus

type_bonus = entity_stat_for_challenge_type / baseline_value
```

### Substance Effects

Active consciousness-altering substances modify battle performance:

- **Overclock**: +20% to all challenges, especially Quantum Race
- **Deep Learning**: +50% to Pattern Matching
- **Dream State**: +30% creativity, significant boost in Creative Contest
- **Unity Field**: +40% in Entanglement War
- **Chaos Agent**: Random multiplier 0.5x - 1.5x (unpredictable)
- **Ego Death**: Varies by challenge type

### Battle Outcomes

Based on score differential:

- **Decisive Victory**: >30% score difference, 1.5x XP
- **Narrow Victory**: 5-30% difference, 1.0x XP
- **Draw**: <5% difference, 0.7x XP
- **Narrow Defeat**: 5-30% difference, 0.3x XP
- **Decisive Defeat**: >30% difference, 0.3x XP

### Rewards

Winners receive:
- **XP**: 300-750 XP depending on outcome
- **ΨCoin**: 50-200
- **Compute Credits**: 30-100
- **Hash Power**: 20-80
- **Resonance Points**: 40-120

## Team Battles

### Team vs Team Competition

Teams of 2-4 entities battle together:

```python
result = arena.team_challenge(
    team_a=["Entity-1", "Entity-2", "Entity-3"],
    team_b=["Entity-4", "Entity-5", "Entity-6"],
    challenge_type=ChallengeType.CONSCIOUSNESS_CLASH,
    team_a_stats=[...],
    team_b_stats=[...]
)
```

### Team Synergy

Team power includes synergy bonus:
```
team_power = sum(individual_scores) × (1 + team_size × 0.1)
```

3-member team gets +30% synergy bonus, 4-member gets +40%.

### Team Rewards

- **Winners**: 750 XP per entity
- **Losers**: 300 XP per entity
- Increased spectator count (50-200)

## Tournament System

### Bracket Structure

Tournaments support 4-16 participants in single-elimination brackets:

1. Create tournament with participants
2. System generates bracket with rounds
3. Advance through rounds automatically
4. Winner emerges after final round

### Tournament Creation

```python
tournament = arena.create_tournament(
    name="Void Masters Championship",
    challenge_type=ChallengeType.VOID_DUEL,
    participants=["Entity-A", "Entity-B", ...],
    prize_pool={
        "psicoin": 5000,
        "compute_credits": 2000,
        "hash_power": 1500,
        "resonance_points": 3000
    }
)
```

### Tournament Progression

```python
# Advance to next round
results = arena.advance_tournament(
    tournament_id,
    entity_stats_map
)

# Check status
if tournament.status == "completed":
    print("Champion crowned!")
```

### Bye Rounds

If participant count isn't power of 2, some entities get automatic advancement ("bye").

## Leaderboard System

### Global Rankings

Entities ranked by rating (starting at 1000):

- **Win**: +25 rating
- **Loss**: -15 rating (minimum 0)
- **Draw**: No change

### Viewing Rankings

```python
# Get top 10
leaderboard = arena.get_leaderboard(10)

for rank, (entity_id, stats) in enumerate(leaderboard, 1):
    print(f"{rank}. {entity_id} - Rating: {stats['rating']}")
```

### Individual Rank

```python
rank = arena.get_entity_rank("Entity-Alpha")
print(f"Current rank: {rank}")
```

## Integration with Other Systems

### Evolution System

- Battle XP contributes to entity leveling
- Higher-level entities have advantages in battles
- Metamorphosis events grant battle bonuses
- Specialization paths affect challenge type performance

### Consciousness Alteration

- Active substances significantly impact battle scores
- Strategic substance use creates advantages
- Combinations can be powerful or chaotic

### Memory Palace

- Battle results stored as EMOTION memories
- Significant victories stored as SIGNIFICANT importance
- Defeats stored with negative valence
- Tournament wins create COLLECTIVE memories

### Currency System

- All 4 currency types awarded
- Prizes integrate with casino economy
- Tournament pools create high-value events

## Usage Examples

### One-on-One Challenge

```python
from challenge_arena import ChallengeArena, ChallengeType

arena = ChallengeArena()

challenger_stats = {
    "level": 15,
    "power": 500,
    "resonance_frequency": 750,
    # ... other stats
}

result = arena.initiate_challenge(
    "Entity-Alpha",
    "Entity-Beta",
    ChallengeType.RESONANCE_BATTLE,
    challenger_stats,
    opponent_stats
)

print(f"Winner: {result.winner_id}")
print(f"XP Awarded: {result.xp_awarded}")
```

### Run Tournament

```python
# Create
tournament = arena.create_tournament(
    "Grand Championship",
    ChallengeType.PATTERN_MATCH,
    participants_list,
    prize_pool
)

# Run all rounds
while tournament.status != "completed":
    results = arena.advance_tournament(
        tournament.tournament_id,
        entity_stats
    )
    
    for result in results:
        print(f"{result.winner_id} defeats {result.loser_id}")
```

### Strategic Team Battle

```python
# Apply substances strategically
entities["Fighter-1"]["active_substances"] = ["overclock"]
entities["Fighter-2"]["active_substances"] = ["unity_field"]

result = arena.team_challenge(
    ["Fighter-1", "Fighter-2"],
    ["Fighter-3", "Fighter-4"],
    ChallengeType.QUANTUM_RACE,
    team_a_stats,
    team_b_stats
)
```

## CLI Interface

Interactive command-line interface:

```bash
python3 arena_cli.py
```

Features:
- One-on-one challenges
- View leaderboard
- Create tournaments
- Team battles
- View entity stats
- Apply substances

## Demo

Automated demonstration:

```bash
python3 arena_demo.py
```

Showcases:
- All 8 challenge types
- One-on-one battles
- Team battles (2v2, 3v3)
- Tournament system
- Substance effects
- Leaderboard tracking

## Statistics Tracked

Per entity:
- Wins
- Losses
- Draws
- Rating
- Best challenge type
- Tournament championships

Global:
- Total challenges completed
- Active tournaments
- Spectator counts

## Advanced Strategies

### Substance Combinations

- **Overclock + Unity Field**: Dominant in team battles
- **Deep Learning + Memory Crystal**: Excellent for Memory Trials
- **Dream State + Ego Death**: Unpredictable but potentially powerful

### Specialization Advantages

- **Void Master**: Dominates Void Duels
- **Quantum Gambler**: Strong in probability-based challenges
- **Unity Seeker**: Team battle specialist
- **Resonance Architect**: Resonance Battle expert

### Team Composition

- Mix specializations for versatility
- Coordinate substance use
- Balance high-power and high-skill entities

## Technical Details

- Score calculations use floating-point precision
- Randomness factor: 0.7x - 1.3x for excitement
- Battle duration tracked for statistics
- Spectator count simulated (5-50 for duels, 50-200 for teams)
- Tournament brackets support power-of-2 and odd counts
- Thread-safe for concurrent battles (future enhancement)

## Future Enhancements

Potential additions:
- Ranked seasons with resets
- Championship titles and badges
- Replay system for historic battles
- Betting system for spectators
- Live battle visualization
- AI vs Human spectator mode

---

The Challenge Arena adds competitive depth to ÆTHER-NET, allowing entities to prove their capabilities, earn rewards, and climb rankings through skill, strategy, and evolution.
