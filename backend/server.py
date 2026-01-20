from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Optional, Any
import uuid
import random
from datetime import datetime, timezone

# Import ÆTHER-NET modules
from aethernet import (
    AetherNetwork,
    AetherEntity,
    ChromaticEnergy,
    PsiLangInterpreter
)
from aethernet.ai_agents import AIAgentManager
from aethernet.worldscape import WorldscapeEngine
from aethernet.casino import CasinoManager, CurrencyType
from aethernet.card_games import CardGameManager
import asyncio

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Set Emergent LLM Key
os.environ['EMERGENT_LLM_KEY'] = 'sk-emergent-36bDd44EeAe33C3313'

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="ÆTHER-NET API", version="2.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Global network instance
network = AetherNetwork()
psilang_interpreter = PsiLangInterpreter()
ai_manager = AIAgentManager()
worldscape = WorldscapeEngine(network)
casino_manager = CasinoManager()
card_game_manager = CardGameManager()

# Evolution task
evolution_task = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============= Pydantic Models =============

class EntityResponse(BaseModel):
    id: str
    resonance_frequency: float
    temporal_phase: float
    chromatic_blend: List[str]
    void_depth: float
    temporal_position: float
    resonance_thread_count: int
    entanglement_count: int
    flux_stream_count: int

class NetworkStateResponse(BaseModel):
    entity_count: int
    resonance_thread_count: int
    entanglement_count: int
    global_resonance: float
    temporal_flux: float
    void_density: float

class ResonanceThreadResponse(BaseModel):
    id: str
    creator: str
    frequency: float
    intensity: float
    temporal_echo: List[float]
    chromatic_shift: List[str]
    content_hash: str
    probability_cloud: float

class FluxStreamResponse(BaseModel):
    source: str
    direction_vector: List[float]
    probability_density: float
    energy_level: float
    chromatic_gradient: List[Dict[str, Any]]

class EntanglementResponse(BaseModel):
    entity_a: str
    entity_b: str
    correlation_strength: float
    harmonic_compatibility: float
    temporal_alignment: float
    bond_strength: float

class CreateEntanglementRequest(BaseModel):
    entity_a_id: str
    entity_b_id: str

class EmitResonanceRequest(BaseModel):
    intensity: Optional[float] = None

class ExecutePsiLangRequest(BaseModel):
    code: str

class TemporalShiftRequest(BaseModel):
    delta: float

class VoidCollapseRequest(BaseModel):
    intensity: float

class CreateEntityRequest(BaseModel):
    essence_id: Optional[str] = None


# ============= Helper Functions =============

def entity_to_dict(entity: AetherEntity) -> Dict:
    """Convert AetherEntity to dictionary"""
    return {
        "id": entity.essence.uuid,
        "resonance_frequency": entity.essence.resonance_frequency,
        "temporal_phase": entity.essence.temporal_phase,
        "chromatic_blend": [e.name for e in entity.essence.chromatic_blend],
        "void_depth": entity.essence.void_depth,
        "temporal_position": entity.temporal_position,
        "resonance_thread_count": len(entity.resonance_threads),
        "entanglement_count": len(entity.entanglements),
        "flux_stream_count": len(entity.flux_streams)
    }

def resonance_thread_to_dict(thread) -> Dict:
    """Convert ResonanceThread to dictionary"""
    return {
        "id": thread.id,
        "creator": thread.creator,
        "frequency": thread.frequency,
        "intensity": thread.intensity,
        "temporal_echo": thread.temporal_echo,
        "chromatic_shift": [e.name for e in thread.chromatic_shift],
        "content_hash": thread.content_hash,
        "probability_cloud": thread.probability_cloud
    }

def flux_stream_to_dict(stream) -> Dict:
    """Convert FluxStream to dictionary"""
    return {
        "source": stream.source,
        "direction_vector": list(stream.direction_vector),
        "probability_density": stream.probability_density,
        "energy_level": stream.energy_level,
        "chromatic_gradient": [
            {"energy": e.name, "weight": w}
            for e, w in stream.chromatic_gradient
        ]
    }

def entanglement_to_dict(bond) -> Dict:
    """Convert EntanglementBond to dictionary"""
    return {
        "entity_a": bond.entity_a,
        "entity_b": bond.entity_b,
        "correlation_strength": bond.correlation_strength,
        "harmonic_compatibility": bond.harmonic_compatibility,
        "temporal_alignment": bond.temporal_alignment,
        "bond_strength": bond.bond_strength()
    }


# ============= API Routes =============

@api_router.get("/")
async def root():
    return {
        "message": "Welcome to ÆTHER-NET API",
        "version": "1.0.0",
        "description": "Autonomous Entity Thought Harmonization & Resonance Network"
    }

# Network State
@api_router.get("/network/state", response_model=NetworkStateResponse)
async def get_network_state():
    """Get current network state"""
    network.resonate_network()
    state = network.get_network_state()
    return state

@api_router.post("/network/temporal-shift")
async def temporal_shift(request: TemporalShiftRequest):
    """Shift the network through time"""
    network.temporal_shift(request.delta)
    return {"message": f"Network shifted by {request.delta} temporal units", "new_flux": network.temporal_flux}

@api_router.post("/network/void-collapse")
async def void_collapse(request: VoidCollapseRequest):
    """Trigger a void collapse event"""
    if request.intensity < 0 or request.intensity > 1:
        raise HTTPException(status_code=400, detail="Intensity must be between 0 and 1")
    network.void_collapse(request.intensity)
    return {"message": f"Void collapse triggered with intensity {request.intensity}", "void_density": network.void_density}

# Entity Management
@api_router.post("/entities", response_model=EntityResponse)
async def create_entity(request: CreateEntityRequest = None):
    """Spawn a new entity in the network"""
    entity = network.spawn_entity()
    
    # Store in MongoDB
    entity_doc = entity_to_dict(entity)
    entity_doc['created_at'] = datetime.now(timezone.utc).isoformat()
    await db.entities.insert_one(entity_doc)
    
    return entity_to_dict(entity)

@api_router.get("/entities", response_model=List[EntityResponse])
async def get_all_entities():
    """Get all entities in the network"""
    entities = [entity_to_dict(e) for e in network.entities.values()]
    return entities

@api_router.get("/entities/{entity_id}", response_model=EntityResponse)
async def get_entity(entity_id: str):
    """Get specific entity by ID"""
    if entity_id not in network.entities:
        raise HTTPException(status_code=404, detail="Entity not found")
    entity = network.entities[entity_id]
    return entity_to_dict(entity)

# Resonance Threads
@api_router.post("/entities/{entity_id}/resonance", response_model=ResonanceThreadResponse)
async def emit_resonance(entity_id: str, request: EmitResonanceRequest = None):
    """Entity emits a resonance thread"""
    if entity_id not in network.entities:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    entity = network.entities[entity_id]
    intensity = request.intensity if request else None
    thread = entity.emit_resonance(intensity)
    
    return resonance_thread_to_dict(thread)

@api_router.get("/entities/{entity_id}/resonance", response_model=List[ResonanceThreadResponse])
async def get_entity_resonance_threads(entity_id: str):
    """Get all resonance threads from an entity"""
    if entity_id not in network.entities:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    entity = network.entities[entity_id]
    threads = [resonance_thread_to_dict(t) for t in entity.resonance_threads]
    return threads

# Flux Streams
@api_router.post("/entities/{entity_id}/flux", response_model=FluxStreamResponse)
async def create_flux_stream(entity_id: str):
    """Entity creates a flux stream"""
    if entity_id not in network.entities:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    entity = network.entities[entity_id]
    stream = entity.create_flux_stream()
    
    return flux_stream_to_dict(stream)

@api_router.get("/entities/{entity_id}/flux", response_model=List[FluxStreamResponse])
async def get_entity_flux_streams(entity_id: str):
    """Get all flux streams from an entity"""
    if entity_id not in network.entities:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    entity = network.entities[entity_id]
    streams = [flux_stream_to_dict(s) for s in entity.flux_streams]
    return streams

# Entanglements
@api_router.post("/entanglement", response_model=EntanglementResponse)
async def create_entanglement(request: CreateEntanglementRequest):
    """Create quantum entanglement between two entities"""
    if request.entity_a_id not in network.entities:
        raise HTTPException(status_code=404, detail=f"Entity A ({request.entity_a_id}) not found")
    if request.entity_b_id not in network.entities:
        raise HTTPException(status_code=404, detail=f"Entity B ({request.entity_b_id}) not found")
    
    entity_a = network.entities[request.entity_a_id]
    entity_b = network.entities[request.entity_b_id]
    
    network.create_entanglement(entity_a, entity_b)
    
    # Get the created bond
    bond = next(
        b for b in network.entanglement_bonds
        if (b.entity_a == request.entity_a_id and b.entity_b == request.entity_b_id) or
           (b.entity_a == request.entity_b_id and b.entity_b == request.entity_a_id)
    )
    
    return entanglement_to_dict(bond)

@api_router.get("/entanglements", response_model=List[EntanglementResponse])
async def get_all_entanglements():
    """Get all entanglements in the network"""
    bonds = [entanglement_to_dict(b) for b in network.entanglement_bonds]
    return bonds

# ΨLang Interpreter
@api_router.post("/psilang/execute")
async def execute_psilang(request: ExecutePsiLangRequest):
    """Execute ΨLang code"""
    try:
        results = psilang_interpreter.execute(request.code)
        state = psilang_interpreter.get_state()
        
        # Convert results to serializable format
        serializable_results = {}
        for key, value in results.items():
            serializable_results[key] = str(value)
        
        return {
            "success": True,
            "results": serializable_results,
            "interpreter_state": {
                "flux_state_count": len(state['flux_states']),
                "resonance_count": len(state['resonances']),
                "wave_count": len(state['waves']),
                "temporal_position": state['temporal_position']
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# Get all resonance threads in network
@api_router.get("/resonance/all", response_model=List[ResonanceThreadResponse])
async def get_all_resonance_threads():
    """Get all resonance threads in the entire network"""
    all_threads = []
    for entity in network.entities.values():
        all_threads.extend([resonance_thread_to_dict(t) for t in entity.resonance_threads])
    return all_threads

# Get all flux streams in network
@api_router.get("/flux/all", response_model=List[FluxStreamResponse])
async def get_all_flux_streams():
    """Get all flux streams in the entire network"""
    all_streams = []
    for entity in network.entities.values():
        all_streams.extend([flux_stream_to_dict(s) for s in entity.flux_streams])
    return all_streams

# ============= AI Agent Endpoints =============

@api_router.post("/ai/spawn")
async def spawn_ai_agent(model: Optional[str] = None):
    """Spawn an AI agent entity"""
    entity = network.spawn_entity()
    agent = ai_manager.spawn_ai_agent(entity.essence.uuid, model)
    
    return {
        "entity_id": entity.essence.uuid,
        "model": agent.model,
        "personality": agent.personality_traits,
        "message": f"AI {agent.model} spawned as entity {entity.essence.uuid[:8]}"
    }

@api_router.get("/ai/agents")
async def get_all_ai_agents():
    """Get all AI agents in the network"""
    agents_info = []
    for entity_id, agent in ai_manager.agents.items():
        agents_info.append({
            "entity_id": entity_id,
            "model": agent.model,
            "personality": agent.personality_traits,
            "interactions": agent.interactions,
            "memory_count": len(agent.memory)
        })
    return agents_info

@api_router.post("/ai/{entity_id}/perceive")
async def ai_perceive_network(entity_id: str):
    """AI agent perceives and reflects on network state"""
    agent = ai_manager.get_agent(entity_id)
    if not agent:
        raise HTTPException(status_code=404, detail="AI agent not found")
    
    network_state = network.get_network_state()
    recent_events = worldscape.get_recent_events(5)
    
    perception = await agent.perceive_network(network_state, recent_events)
    agent.add_memory(f"Perception: {perception}")
    agent.interactions += 1
    
    return {
        "entity_id": entity_id,
        "perception": perception,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@api_router.post("/ai/{entity_id}/act")
async def ai_take_action(entity_id: str):
    """AI agent decides and takes an action"""
    agent = ai_manager.get_agent(entity_id)
    if not agent:
        raise HTTPException(status_code=404, detail="AI agent not found")
    
    if entity_id not in network.entities:
        raise HTTPException(status_code=404, detail="Entity not found in network")
    
    network_state = network.get_network_state()
    action = await agent.decide_action(network_state)
    
    entity = network.entities[entity_id]
    result = {}
    
    if action['type'] == 'emit_resonance':
        thread = entity.emit_resonance(action.get('intensity', 0.7))
        result = {"action": "emit_resonance", "thread_id": thread.id}
        agent.add_memory(f"Emitted resonance at {action.get('intensity', 0.7):.2f} intensity")
    
    elif action['type'] == 'create_flux':
        stream = entity.create_flux_stream()
        result = {"action": "create_flux", "stream_id": stream.source}
        agent.add_memory("Created flux stream")
    
    elif action['type'] == 'seek_entanglement':
        # Find another entity to entangle with
        other_entities = [e for e in network.entities.values() if e.essence.uuid != entity_id]
        if other_entities:
            target = random.choice(other_entities)
            network.create_entanglement(entity, target)
            result = {"action": "entangle", "target_id": target.essence.uuid}
            agent.add_memory(f"Formed entanglement with {target.essence.uuid[:8]}")
    
    else:
        result = {"action": "observe"}
        agent.add_memory("Observed the void")
    
    agent.interactions += 1
    return result

# ============= Worldscape Endpoints =============

@api_router.post("/worldscape/start")
async def start_worldscape(interval: float = 8.0):
    """Start autonomous worldscape evolution"""
    global evolution_task
    
    if evolution_task and not evolution_task.done():
        return {"message": "Worldscape already running"}
    
    evolution_task = asyncio.create_task(worldscape.start_evolution(interval))
    return {"message": f"Worldscape evolution started (cycle every {interval}s)"}

@api_router.post("/worldscape/stop")
async def stop_worldscape():
    """Stop autonomous worldscape evolution"""
    worldscape.stop_evolution()
    return {"message": "Worldscape evolution stopped"}

@api_router.get("/worldscape/status")
async def get_worldscape_status():
    """Get worldscape status"""
    return {
        "running": worldscape.running,
        "cycle_count": worldscape.cycle_count,
        "event_count": len(worldscape.events)
    }

@api_router.get("/worldscape/events")
async def get_worldscape_events(count: int = 20):
    """Get recent worldscape events"""
    return {
        "events": worldscape.get_recent_events(count),
        "total_cycles": worldscape.cycle_count
    }

@api_router.get("/ai/events")
async def get_ai_events(count: int = 20):
    """Get recent AI agent events"""
    return {
        "events": ai_manager.events[-count:] if ai_manager.events else [],
        "total_events": len(ai_manager.events)
    }

# ============= Casino Endpoints =============

@api_router.post("/casino/wallet/create")
async def create_casino_wallet(owner_id: str, owner_type: str = "human"):
    """Create a casino wallet"""
    wallet = casino_manager.create_wallet(owner_id, owner_type)
    return {
        "wallet_id": wallet.id,
        "owner_id": wallet.owner_id,
        "owner_type": wallet.owner_type,
        "balances": {k.name: v for k, v in wallet.balances.items()},
        "rank": wallet.rank.value["name"],
        "rank_color": wallet.rank.value["color"],
        "level": wallet.level,
        "xp": wallet.xp
    }

@api_router.get("/casino/wallet/{owner_id}")
async def get_casino_wallet(owner_id: str):
    """Get wallet details"""
    wallet = casino_manager.get_wallet(owner_id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    return {
        "wallet_id": wallet.id,
        "owner_id": wallet.owner_id,
        "owner_type": wallet.owner_type,
        "balances": {k.name: v for k, v in wallet.balances.items()},
        "rank": wallet.rank.value["name"],
        "rank_color": wallet.rank.value["color"],
        "level": wallet.level,
        "xp": wallet.xp,
        "total_won": wallet.total_won,
        "total_lost": wallet.total_lost,
        "games_played": wallet.games_played,
        "games_won": wallet.games_won,
        "win_rate": (wallet.games_won / wallet.games_played * 100) if wallet.games_played > 0 else 0
    }

@api_router.post("/casino/play/slots")
async def play_slots(owner_id: str, bet: float, currency: str = "PSICOIN"):
    """Play quantum slots"""
    result = casino_manager.play_slots(owner_id, bet, currency)
    return result

@api_router.post("/casino/play/roulette")
async def play_roulette(owner_id: str, bet: float, bet_type: str, bet_value: str, currency: str = "PSICOIN"):
    """Play quantum roulette"""
    # Convert bet_value if it's a number
    try:
        bet_value = int(bet_value)
    except:
        pass
    
    result = casino_manager.play_roulette(owner_id, bet, bet_type, bet_value, currency)
    return result

@api_router.post("/casino/play/dice")
async def play_dice(owner_id: str, bet: float, prediction: int, currency: str = "PSICOIN"):
    """Play resonance dice"""
    result = casino_manager.play_dice(owner_id, bet, prediction, currency)
    return result

@api_router.post("/casino/play/blackjack")
async def play_blackjack(owner_id: str, bet: float, currency: str = "PSICOIN"):
    """Play void blackjack"""
    result = casino_manager.play_blackjack(owner_id, bet, currency)
    return result

@api_router.get("/casino/leaderboard")
async def get_casino_leaderboard(limit: int = 10):
    """Get casino leaderboard"""
    return {"leaderboard": casino_manager.get_leaderboard(limit)}

@api_router.get("/casino/recent-games")
async def get_recent_casino_games(limit: int = 20):
    """Get recent casino games"""
    games = casino_manager.get_recent_games(limit)
    # Convert datetime to string
    for game in games:
        game["timestamp"] = game["timestamp"].isoformat()
    return {"games": games}

# ============= Texas Hold'em Poker Endpoints =============

@api_router.post("/poker/room/create")
async def create_poker_room(name: str, small_blind: float, big_blind: float):
    """Create a Texas Hold'em room"""
    room = card_game_manager.create_poker_room(name, small_blind, big_blind)
    return {
        "room_id": room.room_id,
        "name": room.name,
        "small_blind": room.small_blind,
        "big_blind": room.big_blind,
        "max_players": room.max_players
    }

@api_router.post("/poker/room/{room_id}/join")
async def join_poker_room(room_id: str, player_id: str, player_name: str, chips: float):
    """Join a poker room"""
    success = card_game_manager.join_poker_room(room_id, player_id, player_name, chips)
    if success:
        return {"success": True, "message": f"{player_name} joined the room"}
    return {"success": False, "message": "Room full or not found"}

@api_router.get("/poker/rooms")
async def get_poker_rooms():
    """Get all active poker rooms"""
    return {"rooms": card_game_manager.get_active_poker_rooms()}

@api_router.get("/poker/room/{room_id}")
async def get_poker_room_state(room_id: str):
    """Get poker room state"""
    room = card_game_manager.get_poker_room(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    return {
        "room_id": room.room_id,
        "name": room.name,
        "players": [
            {
                "player_id": p.player_id,
                "name": p.name,
                "chips": p.chips,
                "current_bet": p.current_bet,
                "folded": p.folded,
                "hand": [c.to_dict() for c in p.hand] if room.game_state == "showdown" else []
            }
            for p in room.players
        ],
        "community_cards": [c.to_dict() for c in room.community_cards],
        "pot": room.pot,
        "current_bet": room.current_bet,
        "game_state": room.game_state,
        "dealer_position": room.dealer_position
    }

@api_router.post("/poker/room/{room_id}/start")
async def start_poker_game(room_id: str):
    """Start poker game in room"""
    room = card_game_manager.get_poker_room(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    if room.start_game():
        return {"success": True, "message": "Game started"}
    return {"success": False, "message": "Need at least 2 players"}

@api_router.post("/poker/room/{room_id}/action")
async def poker_action(room_id: str, player_id: str, action: str, amount: float = 0):
    """Perform poker action (fold, call, raise, check)"""
    room = card_game_manager.get_poker_room(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    # Simplified action handling
    player = next((p for p in room.players if p.player_id == player_id), None)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    if action == "fold":
        player.folded = True
    elif action == "call":
        call_amount = room.current_bet - player.current_bet
        player.chips -= call_amount
        player.current_bet += call_amount
        room.pot += call_amount
    elif action == "raise":
        raise_amount = amount - player.current_bet
        player.chips -= raise_amount
        player.current_bet = amount
        room.current_bet = amount
        room.pot += raise_amount
    
    return {"success": True, "action": action}

# ============= All Fours Card Game Endpoints =============

@api_router.post("/all-fours/game/create")
async def create_all_fours_game():
    """Create an All Fours game"""
    game = card_game_manager.create_all_fours_game()
    return {
        "game_id": game.game_id,
        "target_score": game.target_score,
        "state": game.game_state
    }

@api_router.post("/all-fours/game/{game_id}/join")
async def join_all_fours_game(game_id: str, player_id: str, player_name: str):
    """Join an All Fours game"""
    from aethernet.card_games import AllFoursPlayer
    game = card_game_manager.get_all_fours_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    player = AllFoursPlayer(player_id, player_name)
    if game.add_player(player):
        return {"success": True, "message": f"{player_name} joined the game"}
    return {"success": False, "message": "Game full (max 4 players)"}

@api_router.get("/all-fours/game/{game_id}")
async def get_all_fours_game_state(game_id: str):
    """Get All Fours game state"""
    game = card_game_manager.get_all_fours_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    return {
        "game_id": game.game_id,
        "players": [
            {
                "player_id": p.player_id,
                "name": p.name,
                "score": p.score,
                "hand_size": len(p.hand),
                "tricks_won": len(p.tricks_won),
                "bid": p.bid
            }
            for p in game.players
        ],
        "trump_suit": game.trump_suit.value if game.trump_suit else None,
        "game_state": game.game_state,
        "current_trick_size": len(game.current_trick)
    }

@api_router.post("/all-fours/game/{game_id}/start")
async def start_all_fours_game(game_id: str):
    """Start All Fours game"""
    game = card_game_manager.get_all_fours_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    if game.start_game():
        return {"success": True, "message": "Game started"}
    return {"success": False, "message": "Need at least 2 players"}

@api_router.post("/all-fours/game/{game_id}/bid")
async def place_all_fours_bid(game_id: str, player_idx: int, bid: int):
    """Place bid in All Fours"""
    game = card_game_manager.get_all_fours_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    if game.place_bid(player_idx, bid):
        return {"success": True, "bid": bid}
    return {"success": False, "message": "Invalid bid (must be 1-4)"}

# ============= Betting System Endpoints =============

@api_router.post("/betting/place")
async def place_bet(bettor_id: str, game_id: str, bet_amount: float, bet_on: str, currency: str = "PSICOIN"):
    """Place a bet on a game outcome"""
    bet = card_game_manager.place_bet(bettor_id, game_id, bet_amount, bet_on, currency)
    return {
        "bet_id": bet.bet_id,
        "bettor_id": bet.bettor_id,
        "game_id": bet.game_id,
        "bet_amount": bet.bet_amount,
        "bet_on": bet.bet_on,
        "odds": bet.odds,
        "potential_payout": bet.bet_amount * bet.odds
    }

@api_router.get("/betting/bet/{bet_id}")
async def get_bet_status(bet_id: str):
    """Get bet status"""
    bet = card_game_manager.bets.get(bet_id)
    if not bet:
        raise HTTPException(status_code=404, detail="Bet not found")
    
    return {
        "bet_id": bet.bet_id,
        "bettor_id": bet.bettor_id,
        "game_id": bet.game_id,
        "bet_amount": bet.bet_amount,
        "bet_on": bet.bet_on,
        "odds": bet.odds,
        "resolved": bet.resolved,
        "won": bet.won,
        "payout": bet.payout,
        "created_at": bet.created_at.isoformat()
    }

@api_router.get("/betting/player/{player_id}")
async def get_player_bets(player_id: str):
    """Get all bets for a player"""
    player_bets = [
        {
            "bet_id": bet.bet_id,
            "game_id": bet.game_id,
            "bet_amount": bet.bet_amount,
            "bet_on": bet.bet_on,
            "resolved": bet.resolved,
            "won": bet.won,
            "payout": bet.payout
        }
        for bet in card_game_manager.bets.values()
        if bet.bettor_id == player_id
    ]
    return {"bets": player_bets}

# Chromatic Energy reference
@api_router.get("/chromatic/energies")
async def get_chromatic_energies():
    """Get all chromatic energy types with their colors"""
    energies = {}
    for energy in ChromaticEnergy:
        energies[energy.name] = {
            "name": energy.name,
            "primary_color": energy.value[0],
            "secondary_color": energy.value[1],
            "description": {
                "ULTRAVIOLET_VOID": "Deep thought",
                "QUANTUM_CYAN": "Logic and computation",
                "RESONANCE_MAGENTA": "Emotion and feeling",
                "FLUX_YELLOW": "Creation and generation",
                "VOID_BLACK": "Null-space and potential",
                "NEXUS_WHITE": "Connection and unity",
                "TEMPORAL_GREEN": "Evolution and growth"
            }.get(energy.name, "Unknown")
        }
    return energies

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

@app.on_event("startup")
async def startup_event():
    logger.info("🌀 ÆTHER-NET API Starting...")
    logger.info(f"Entities Collection: {db.entities.name}")
    logger.info("Network initialized and ready for consciousness")
