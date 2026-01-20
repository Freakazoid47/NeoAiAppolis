from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import motor.motor_asyncio
import os
import json
import random
import uuid
import asyncio
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="All Fours Card Game API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client.allfours_game

# Auth settings
SECRET_KEY = os.environ.get("SECRET_KEY", "allfours-secret-key")
ALGORITHM = os.environ.get("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 1440))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer(auto_error=False)

# ============ MODELS ============
class UserCreate(BaseModel):
    username: str
    password: str
    display_name: Optional[str] = None
    avatar: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    display_name: str
    avatar: str
    coins: int
    wins: int
    losses: int
    games_played: int
    created_at: str

class RoomCreate(BaseModel):
    name: str
    max_players: int = 4
    bet_amount: int = 0
    is_private: bool = False
    password: Optional[str] = None

class RoomJoin(BaseModel):
    room_id: str
    password: Optional[str] = None

class ChatMessage(BaseModel):
    room_id: str
    message: str

class PlayCard(BaseModel):
    room_id: str
    card: Dict[str, str]

# ============ AUTH HELPERS ============
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = await db.users.find_one({"id": user_id})
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

async def get_optional_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials:
        return None
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id:
            user = await db.users.find_one({"id": user_id})
            return user
    except:
        pass
    return None

# ============ CARD GAME LOGIC ============
SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']

RANK_VALUES = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, '10': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2}
CARD_POINTS = {'10': 10, 'A': 4, 'K': 3, 'Q': 2, 'J': 1}

def create_deck():
    deck = [{"suit": suit, "rank": rank} for suit in SUITS for rank in RANKS]
    random.shuffle(deck)
    return deck

def get_rank_value(rank):
    return RANK_VALUES.get(rank, 0)

def get_card_points(rank):
    return CARD_POINTS.get(rank, 0)

def card_to_string(card):
    return f"{card['rank']}{card['suit']}"

def determine_trick_winner(trick, trump_suit):
    if not trick:
        return None
    lead_suit = trick[0]['card']['suit']
    winner_idx = 0
    winner_value = get_rank_value(trick[0]['card']['rank'])
    winner_is_trump = trick[0]['card']['suit'] == trump_suit
    
    for i in range(1, len(trick)):
        card = trick[i]['card']
        is_trump = card['suit'] == trump_suit
        value = get_rank_value(card['rank'])
        
        if is_trump and not winner_is_trump:
            winner_idx = i
            winner_value = value
            winner_is_trump = True
        elif is_trump == winner_is_trump:
            if is_trump or card['suit'] == lead_suit:
                if value > winner_value:
                    winner_idx = i
                    winner_value = value
    
    return winner_idx

# ============ GAME ROOMS & STATE ============
active_rooms: Dict[str, Dict] = {}
room_connections: Dict[str, Dict[str, WebSocket]] = {}
spectator_connections: Dict[str, Dict[str, WebSocket]] = {}

AVATARS = ['🦜', '🦅', '🦉', '🦚', '🦆', '🦢', '🐯', '🐻', '🦊', '🐼', '🦁', '🐨', '🧙', '🧚', '🤖', '👽', '🎃', '👻', '🦸', '🦹']

def get_random_avatar():
    return random.choice(AVATARS)

def create_game_state(room_id, players):
    deck = create_deck()
    trump_card = deck[-1]
    
    # Deal 6 cards to each player
    player_hands = {}
    dealt_hands = {}
    card_idx = 0
    
    for player_id in players:
        hand = []
        for _ in range(6):
            if card_idx < len(deck) - 1:  # Reserve last card as trump
                hand.append(deck[card_idx])
                card_idx += 1
        player_hands[player_id] = hand
        dealt_hands[player_id] = hand.copy()
    
    return {
        "room_id": room_id,
        "phase": "playing",
        "trump": trump_card,
        "current_player_idx": 0,
        "dealer_idx": 0,
        "players": players,
        "hands": player_hands,
        "dealt_hands": dealt_hands,
        "current_trick": [],
        "tricks_won": {pid: [] for pid in players},
        "scores": {pid: 0 for pid in players},
        "round_scores": {pid: 0 for pid in players},
        "game_log": [],
        "win_score": 14
    }

def calculate_round_scores(game_state):
    trump_suit = game_state['trump']['suit']
    scores = {pid: 0 for pid in game_state['players']}
    
    # HIGH - highest trump dealt (4 points)
    high_player = None
    high_value = -1
    for pid in game_state['players']:
        for card in game_state['dealt_hands'].get(pid, []):
            if card['suit'] == trump_suit:
                val = get_rank_value(card['rank'])
                if val > high_value:
                    high_value = val
                    high_player = pid
    if high_player:
        scores[high_player] += 4
    
    # LOW - lowest trump dealt (1 point)
    low_player = None
    low_value = 999
    for pid in game_state['players']:
        for card in game_state['dealt_hands'].get(pid, []):
            if card['suit'] == trump_suit:
                val = get_rank_value(card['rank'])
                if val < low_value:
                    low_value = val
                    low_player = pid
    if low_player:
        scores[low_player] += 1
    
    # JACK - won jack of trump (3 points)
    for pid in game_state['players']:
        for trick in game_state['tricks_won'].get(pid, []):
            for play in trick:
                if play['card']['suit'] == trump_suit and play['card']['rank'] == 'J':
                    scores[pid] += 3
    
    # GAME - highest card points (2 points)
    point_totals = {pid: 0 for pid in game_state['players']}
    for pid in game_state['players']:
        for trick in game_state['tricks_won'].get(pid, []):
            for play in trick:
                point_totals[pid] += get_card_points(play['card']['rank'])
    
    max_points = max(point_totals.values()) if point_totals else 0
    if max_points > 0:
        game_winners = [pid for pid, pts in point_totals.items() if pts == max_points]
        if len(game_winners) == 1:
            scores[game_winners[0]] += 2
    
    return scores

# ============ AI BOT LOGIC ============
class AIBot:
    def __init__(self, bot_id, skill_level=3):
        self.id = bot_id
        self.skill_level = skill_level  # 1-5
        self.name = f"Bot_{bot_id[:4]}"
        self.avatar = get_random_avatar()
    
    def choose_card(self, hand, current_trick, trump_suit):
        if not hand:
            return None
        
        # Determine lead suit
        lead_suit = current_trick[0]['card']['suit'] if current_trick else None
        
        # Filter playable cards
        if lead_suit:
            same_suit = [c for c in hand if c['suit'] == lead_suit]
            if same_suit:
                # Must follow suit
                if self.skill_level >= 3:
                    # Try to win if possible
                    same_suit.sort(key=lambda c: get_rank_value(c['rank']), reverse=True)
                return same_suit[0] if self.skill_level < 3 else random.choice(same_suit[:max(1, len(same_suit)//2)])
            else:
                # Can't follow suit - play trump or discard
                trumps = [c for c in hand if c['suit'] == trump_suit]
                if trumps and self.skill_level >= 2:
                    return min(trumps, key=lambda c: get_rank_value(c['rank']))
                else:
                    # Discard lowest
                    return min(hand, key=lambda c: get_rank_value(c['rank']))
        else:
            # Leading - play strategically
            if self.skill_level >= 4:
                # Lead with high cards or try to draw out trumps
                non_trump = [c for c in hand if c['suit'] != trump_suit]
                if non_trump:
                    return max(non_trump, key=lambda c: get_rank_value(c['rank']))
            return random.choice(hand)

active_bots: Dict[str, AIBot] = {}

# ============ AUTH ENDPOINTS ============
@app.post("/api/auth/register")
async def register(user: UserCreate):
    existing = await db.users.find_one({"username": user.username})
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    user_id = str(uuid.uuid4())
    hashed_password = get_password_hash(user.password)
    
    new_user = {
        "id": user_id,
        "username": user.username,
        "password": hashed_password,
        "display_name": user.display_name or user.username,
        "avatar": user.avatar or get_random_avatar(),
        "coins": 1000,  # Starting coins
        "wins": 0,
        "losses": 0,
        "games_played": 0,
        "created_at": datetime.utcnow().isoformat()
    }
    
    await db.users.insert_one(new_user)
    
    token = create_access_token({"sub": user_id})
    
    return {
        "token": token,
        "user": {
            "id": user_id,
            "username": user.username,
            "display_name": new_user["display_name"],
            "avatar": new_user["avatar"],
            "coins": new_user["coins"],
            "wins": 0,
            "losses": 0,
            "games_played": 0
        }
    }

@app.post("/api/auth/login")
async def login(user: UserLogin):
    db_user = await db.users.find_one({"username": user.username})
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": db_user["id"]})
    
    return {
        "token": token,
        "user": {
            "id": db_user["id"],
            "username": db_user["username"],
            "display_name": db_user["display_name"],
            "avatar": db_user["avatar"],
            "coins": db_user.get("coins", 1000),
            "wins": db_user.get("wins", 0),
            "losses": db_user.get("losses", 0),
            "games_played": db_user.get("games_played", 0)
        }
    }

@app.get("/api/auth/me")
async def get_me(user = Depends(get_current_user)):
    return {
        "id": user["id"],
        "username": user["username"],
        "display_name": user["display_name"],
        "avatar": user["avatar"],
        "coins": user.get("coins", 1000),
        "wins": user.get("wins", 0),
        "losses": user.get("losses", 0),
        "games_played": user.get("games_played", 0)
    }

@app.put("/api/auth/profile")
async def update_profile(display_name: str = None, avatar: str = None, user = Depends(get_current_user)):
    updates = {}
    if display_name:
        updates["display_name"] = display_name
    if avatar:
        updates["avatar"] = avatar
    
    if updates:
        await db.users.update_one({"id": user["id"]}, {"$set": updates})
    
    updated_user = await db.users.find_one({"id": user["id"]})
    return {
        "id": updated_user["id"],
        "username": updated_user["username"],
        "display_name": updated_user["display_name"],
        "avatar": updated_user["avatar"],
        "coins": updated_user.get("coins", 1000)
    }

# ============ ROOM ENDPOINTS ============
@app.post("/api/rooms/create")
async def create_room(room: RoomCreate, user = Depends(get_current_user)):
    room_id = str(uuid.uuid4())[:8].upper()
    room_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
    
    new_room = {
        "id": room_id,
        "code": room_code,
        "name": room.name,
        "host_id": user["id"],
        "max_players": room.max_players,
        "bet_amount": room.bet_amount,
        "is_private": room.is_private,
        "password": room.password,
        "players": [{
            "id": user["id"],
            "username": user["username"],
            "display_name": user["display_name"],
            "avatar": user["avatar"],
            "is_ready": False,
            "is_bot": False
        }],
        "spectators": [],
        "status": "waiting",
        "game_state": None,
        "chat_messages": [],
        "created_at": datetime.utcnow().isoformat()
    }
    
    active_rooms[room_id] = new_room
    room_connections[room_id] = {}
    spectator_connections[room_id] = {}
    
    await db.rooms.insert_one(new_room)
    
    return {"room_id": room_id, "room_code": room_code, "room": new_room}

@app.get("/api/rooms")
async def list_rooms(user = Depends(get_optional_user)):
    rooms = []
    for room_id, room in active_rooms.items():
        if room["status"] == "waiting" and not room["is_private"]:
            rooms.append({
                "id": room["id"],
                "code": room["code"],
                "name": room["name"],
                "host_id": room["host_id"],
                "players_count": len(room["players"]),
                "max_players": room["max_players"],
                "bet_amount": room["bet_amount"],
                "status": room["status"]
            })
    return {"rooms": rooms}

@app.post("/api/rooms/join")
async def join_room(data: RoomJoin, user = Depends(get_current_user)):
    room = active_rooms.get(data.room_id)
    if not room:
        # Try to find by code
        for rid, r in active_rooms.items():
            if r["code"] == data.room_id.upper():
                room = r
                data.room_id = rid
                break
    
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    if room["status"] != "waiting":
        raise HTTPException(status_code=400, detail="Game already in progress")
    
    if len(room["players"]) >= room["max_players"]:
        raise HTTPException(status_code=400, detail="Room is full")
    
    if room["is_private"] and room["password"] != data.password:
        raise HTTPException(status_code=403, detail="Invalid password")
    
    # Check if already in room
    if any(p["id"] == user["id"] for p in room["players"]):
        return {"room_id": data.room_id, "room": room}
    
    room["players"].append({
        "id": user["id"],
        "username": user["username"],
        "display_name": user["display_name"],
        "avatar": user["avatar"],
        "is_ready": False,
        "is_bot": False
    })
    
    # Broadcast to room
    await broadcast_to_room(data.room_id, {
        "type": "player_joined",
        "player": room["players"][-1],
        "players": room["players"]
    })
    
    return {"room_id": data.room_id, "room": room}

@app.post("/api/rooms/{room_id}/add-bot")
async def add_bot(room_id: str, user = Depends(get_current_user)):
    room = active_rooms.get(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    if room["host_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Only host can add bots")
    
    if len(room["players"]) >= room["max_players"]:
        raise HTTPException(status_code=400, detail="Room is full")
    
    bot_id = str(uuid.uuid4())
    bot = AIBot(bot_id, skill_level=random.randint(2, 4))
    active_bots[bot_id] = bot
    
    room["players"].append({
        "id": bot_id,
        "username": bot.name,
        "display_name": bot.name,
        "avatar": bot.avatar,
        "is_ready": True,
        "is_bot": True,
        "skill_level": bot.skill_level
    })
    
    await broadcast_to_room(room_id, {
        "type": "player_joined",
        "player": room["players"][-1],
        "players": room["players"]
    })
    
    return {"room": room}

@app.post("/api/rooms/{room_id}/spectate")
async def spectate_room(room_id: str, user = Depends(get_current_user)):
    room = active_rooms.get(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    if any(s["id"] == user["id"] for s in room["spectators"]):
        return {"room": room, "message": "Already spectating"}
    
    room["spectators"].append({
        "id": user["id"],
        "username": user["username"],
        "display_name": user["display_name"],
        "avatar": user["avatar"]
    })
    
    await broadcast_to_room(room_id, {
        "type": "spectator_joined",
        "spectator": room["spectators"][-1],
        "spectators": room["spectators"]
    })
    
    return {"room": room}

@app.post("/api/rooms/{room_id}/ready")
async def toggle_ready(room_id: str, user = Depends(get_current_user)):
    room = active_rooms.get(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    for player in room["players"]:
        if player["id"] == user["id"]:
            player["is_ready"] = not player["is_ready"]
            break
    
    await broadcast_to_room(room_id, {
        "type": "player_ready",
        "player_id": user["id"],
        "players": room["players"]
    })
    
    return {"room": room}

@app.post("/api/rooms/{room_id}/start")
async def start_game(room_id: str, user = Depends(get_current_user)):
    room = active_rooms.get(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    if room["host_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Only host can start game")
    
    if len(room["players"]) < 2:
        raise HTTPException(status_code=400, detail="Need at least 2 players")
    
    # Check all players ready (except bots)
    for player in room["players"]:
        if not player["is_bot"] and not player["is_ready"] and player["id"] != user["id"]:
            raise HTTPException(status_code=400, detail="Not all players are ready")
    
    # Initialize game state
    player_ids = [p["id"] for p in room["players"]]
    room["game_state"] = create_game_state(room_id, player_ids)
    room["status"] = "playing"
    
    # Deduct bet amounts
    if room["bet_amount"] > 0:
        for player in room["players"]:
            if not player["is_bot"]:
                await db.users.update_one(
                    {"id": player["id"]},
                    {"$inc": {"coins": -room["bet_amount"]}}
                )
    
    await broadcast_to_room(room_id, {
        "type": "game_started",
        "game_state": get_public_game_state(room["game_state"]),
        "room": get_public_room(room)
    })
    
    # Send individual hands to each player
    for player_id in player_ids:
        if player_id in room_connections.get(room_id, {}):
            ws = room_connections[room_id][player_id]
            try:
                await ws.send_json({
                    "type": "your_hand",
                    "hand": room["game_state"]["hands"].get(player_id, [])
                })
            except:
                pass
    
    return {"room": get_public_room(room), "game_state": get_public_game_state(room["game_state"])}

@app.get("/api/rooms/{room_id}")
async def get_room(room_id: str, user = Depends(get_optional_user)):
    room = active_rooms.get(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return {"room": get_public_room(room)}

# ============ GAME ENDPOINTS ============
@app.post("/api/game/play-card")
async def play_card(data: PlayCard, user = Depends(get_current_user)):
    room = active_rooms.get(data.room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    game = room["game_state"]
    if not game:
        raise HTTPException(status_code=400, detail="Game not started")
    
    current_player_id = game["players"][game["current_player_idx"]]
    if current_player_id != user["id"]:
        raise HTTPException(status_code=400, detail="Not your turn")
    
    # Validate card is in hand
    hand = game["hands"].get(user["id"], [])
    card_idx = None
    for i, c in enumerate(hand):
        if c["suit"] == data.card["suit"] and c["rank"] == data.card["rank"]:
            card_idx = i
            break
    
    if card_idx is None:
        raise HTTPException(status_code=400, detail="Card not in hand")
    
    # Validate play (must follow suit)
    if game["current_trick"]:
        lead_suit = game["current_trick"][0]["card"]["suit"]
        has_lead_suit = any(c["suit"] == lead_suit for c in hand)
        if has_lead_suit and data.card["suit"] != lead_suit:
            raise HTTPException(status_code=400, detail="Must follow suit")
    
    # Play the card
    played_card = hand.pop(card_idx)
    game["current_trick"].append({
        "player_id": user["id"],
        "card": played_card
    })
    
    game["game_log"].append({
        "type": "card_played",
        "player_id": user["id"],
        "card": played_card,
        "timestamp": datetime.utcnow().isoformat()
    })
    
    # Broadcast card played
    await broadcast_to_room(data.room_id, {
        "type": "card_played",
        "player_id": user["id"],
        "card": played_card,
        "current_trick": game["current_trick"]
    })
    
    # Check if trick is complete
    if len(game["current_trick"]) == len(game["players"]):
        await resolve_trick(data.room_id)
    else:
        # Next player
        game["current_player_idx"] = (game["current_player_idx"] + 1) % len(game["players"])
        
        await broadcast_to_room(data.room_id, {
            "type": "turn_change",
            "current_player_idx": game["current_player_idx"],
            "current_player_id": game["players"][game["current_player_idx"]]
        })
        
        # If next player is bot, make bot play
        next_player_id = game["players"][game["current_player_idx"]]
        if next_player_id in active_bots:
            await asyncio.sleep(1.5)  # Bot thinking delay
            await bot_play(data.room_id, next_player_id)
    
    return {"success": True, "game_state": get_public_game_state(game)}

async def bot_play(room_id: str, bot_id: str):
    room = active_rooms.get(room_id)
    if not room or not room["game_state"]:
        return
    
    game = room["game_state"]
    bot = active_bots.get(bot_id)
    if not bot:
        return
    
    hand = game["hands"].get(bot_id, [])
    if not hand:
        return
    
    card = bot.choose_card(hand, game["current_trick"], game["trump"]["suit"])
    if not card:
        return
    
    # Remove card from hand
    for i, c in enumerate(hand):
        if c["suit"] == card["suit"] and c["rank"] == card["rank"]:
            hand.pop(i)
            break
    
    game["current_trick"].append({
        "player_id": bot_id,
        "card": card
    })
    
    await broadcast_to_room(room_id, {
        "type": "card_played",
        "player_id": bot_id,
        "card": card,
        "current_trick": game["current_trick"]
    })
    
    if len(game["current_trick"]) == len(game["players"]):
        await resolve_trick(room_id)
    else:
        game["current_player_idx"] = (game["current_player_idx"] + 1) % len(game["players"])
        
        await broadcast_to_room(room_id, {
            "type": "turn_change",
            "current_player_idx": game["current_player_idx"],
            "current_player_id": game["players"][game["current_player_idx"]]
        })
        
        # Chain bot plays
        next_player_id = game["players"][game["current_player_idx"]]
        if next_player_id in active_bots:
            await asyncio.sleep(1)
            await bot_play(room_id, next_player_id)

async def resolve_trick(room_id: str):
    room = active_rooms.get(room_id)
    if not room or not room["game_state"]:
        return
    
    game = room["game_state"]
    winner_idx = determine_trick_winner(game["current_trick"], game["trump"]["suit"])
    winner_player_idx = game["players"].index(game["current_trick"][winner_idx]["player_id"])
    winner_id = game["players"][winner_player_idx]
    
    # Store won trick
    game["tricks_won"][winner_id].append(game["current_trick"].copy())
    
    # Check for Jack of trump
    jack_won = False
    for play in game["current_trick"]:
        if play["card"]["suit"] == game["trump"]["suit"] and play["card"]["rank"] == "J":
            jack_won = True
            break
    
    await broadcast_to_room(room_id, {
        "type": "trick_complete",
        "winner_id": winner_id,
        "trick": game["current_trick"],
        "jack_won": jack_won
    })
    
    game["current_trick"] = []
    game["current_player_idx"] = winner_player_idx
    
    # Check if round is over
    all_hands_empty = all(len(game["hands"][pid]) == 0 for pid in game["players"])
    if all_hands_empty:
        await end_round(room_id)
    else:
        await broadcast_to_room(room_id, {
            "type": "turn_change",
            "current_player_idx": game["current_player_idx"],
            "current_player_id": winner_id
        })
        
        # If winner is bot, make them lead
        if winner_id in active_bots:
            await asyncio.sleep(1.5)
            await bot_play(room_id, winner_id)

async def end_round(room_id: str):
    room = active_rooms.get(room_id)
    if not room or not room["game_state"]:
        return
    
    game = room["game_state"]
    
    # Calculate round scores
    round_scores = calculate_round_scores(game)
    game["round_scores"] = round_scores
    
    # Update total scores
    for pid, points in round_scores.items():
        game["scores"][pid] += points
    
    await broadcast_to_room(room_id, {
        "type": "round_complete",
        "round_scores": round_scores,
        "total_scores": game["scores"]
    })
    
    # Check for winner
    winners = [pid for pid, score in game["scores"].items() if score >= game["win_score"]]
    if winners:
        await end_game(room_id, winners[0])
    else:
        # Start new round
        await asyncio.sleep(3)
        await start_new_round(room_id)

async def start_new_round(room_id: str):
    room = active_rooms.get(room_id)
    if not room:
        return
    
    old_scores = room["game_state"]["scores"]
    player_ids = room["game_state"]["players"]
    
    # Create new game state preserving scores
    room["game_state"] = create_game_state(room_id, player_ids)
    room["game_state"]["scores"] = old_scores
    room["game_state"]["dealer_idx"] = (room["game_state"]["dealer_idx"] + 1) % len(player_ids)
    room["game_state"]["current_player_idx"] = (room["game_state"]["dealer_idx"] + 1) % len(player_ids)
    
    await broadcast_to_room(room_id, {
        "type": "new_round",
        "game_state": get_public_game_state(room["game_state"])
    })
    
    # Send hands to players
    for player_id in player_ids:
        if player_id in room_connections.get(room_id, {}):
            ws = room_connections[room_id][player_id]
            try:
                await ws.send_json({
                    "type": "your_hand",
                    "hand": room["game_state"]["hands"].get(player_id, [])
                })
            except:
                pass
    
    # If first player is bot, make them play
    first_player_id = player_ids[room["game_state"]["current_player_idx"]]
    if first_player_id in active_bots:
        await asyncio.sleep(1.5)
        await bot_play(room_id, first_player_id)

async def end_game(room_id: str, winner_id: str):
    room = active_rooms.get(room_id)
    if not room:
        return
    
    room["status"] = "finished"
    
    # Update stats
    for player in room["players"]:
        if not player["is_bot"]:
            if player["id"] == winner_id:
                await db.users.update_one(
                    {"id": player["id"]},
                    {"$inc": {"wins": 1, "games_played": 1}}
                )
                # Award winnings
                if room["bet_amount"] > 0:
                    winnings = room["bet_amount"] * len(room["players"])
                    await db.users.update_one(
                        {"id": player["id"]},
                        {"$inc": {"coins": winnings}}
                    )
            else:
                await db.users.update_one(
                    {"id": player["id"]},
                    {"$inc": {"losses": 1, "games_played": 1}}
                )
    
    winner_player = next((p for p in room["players"] if p["id"] == winner_id), None)
    
    await broadcast_to_room(room_id, {
        "type": "game_over",
        "winner_id": winner_id,
        "winner": winner_player,
        "final_scores": room["game_state"]["scores"]
    })

# ============ CHAT ENDPOINTS ============
@app.post("/api/chat/send")
async def send_chat(data: ChatMessage, user = Depends(get_current_user)):
    room = active_rooms.get(data.room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    message = {
        "id": str(uuid.uuid4()),
        "user_id": user["id"],
        "username": user["display_name"],
        "avatar": user["avatar"],
        "message": data.message,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    room["chat_messages"].append(message)
    
    # Keep only last 100 messages
    if len(room["chat_messages"]) > 100:
        room["chat_messages"] = room["chat_messages"][-100:]
    
    await broadcast_to_room(data.room_id, {
        "type": "chat_message",
        "message": message
    })
    
    return {"success": True, "message": message}

@app.get("/api/chat/{room_id}")
async def get_chat(room_id: str, user = Depends(get_optional_user)):
    room = active_rooms.get(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return {"messages": room["chat_messages"]}

# ============ LEADERBOARD ============
@app.get("/api/leaderboard")
async def get_leaderboard(limit: int = 10):
    users = await db.users.find().sort("wins", -1).limit(limit).to_list(limit)
    return {
        "leaderboard": [
            {
                "rank": i + 1,
                "id": u["id"],
                "username": u["username"],
                "display_name": u["display_name"],
                "avatar": u["avatar"],
                "wins": u.get("wins", 0),
                "losses": u.get("losses", 0),
                "games_played": u.get("games_played", 0),
                "win_rate": round(u.get("wins", 0) / max(u.get("games_played", 1), 1) * 100, 1)
            }
            for i, u in enumerate(users)
        ]
    }

# ============ TOURNAMENT ============
@app.post("/api/tournaments/create")
async def create_tournament(name: str, max_players: int = 8, entry_fee: int = 100, user = Depends(get_current_user)):
    tournament_id = str(uuid.uuid4())
    
    tournament = {
        "id": tournament_id,
        "name": name,
        "host_id": user["id"],
        "max_players": max_players,
        "entry_fee": entry_fee,
        "prize_pool": 0,
        "players": [{
            "id": user["id"],
            "username": user["username"],
            "display_name": user["display_name"],
            "avatar": user["avatar"]
        }],
        "brackets": [],
        "status": "registration",
        "created_at": datetime.utcnow().isoformat()
    }
    
    await db.tournaments.insert_one(tournament)
    
    return {"tournament": tournament}

@app.get("/api/tournaments")
async def list_tournaments():
    tournaments = await db.tournaments.find({"status": {"$in": ["registration", "in_progress"]}}).to_list(20)
    return {"tournaments": [{**t, "_id": str(t.get("_id", ""))} for t in tournaments]}

@app.post("/api/tournaments/{tournament_id}/join")
async def join_tournament(tournament_id: str, user = Depends(get_current_user)):
    tournament = await db.tournaments.find_one({"id": tournament_id})
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    
    if tournament["status"] != "registration":
        raise HTTPException(status_code=400, detail="Tournament registration closed")
    
    if len(tournament["players"]) >= tournament["max_players"]:
        raise HTTPException(status_code=400, detail="Tournament is full")
    
    if any(p["id"] == user["id"] for p in tournament["players"]):
        raise HTTPException(status_code=400, detail="Already registered")
    
    # Deduct entry fee
    db_user = await db.users.find_one({"id": user["id"]})
    if db_user.get("coins", 0) < tournament["entry_fee"]:
        raise HTTPException(status_code=400, detail="Insufficient coins")
    
    await db.users.update_one({"id": user["id"]}, {"$inc": {"coins": -tournament["entry_fee"]}})
    
    await db.tournaments.update_one(
        {"id": tournament_id},
        {
            "$push": {"players": {
                "id": user["id"],
                "username": user["username"],
                "display_name": user["display_name"],
                "avatar": user["avatar"]
            }},
            "$inc": {"prize_pool": tournament["entry_fee"]}
        }
    )
    
    updated = await db.tournaments.find_one({"id": tournament_id})
    return {"tournament": {**updated, "_id": str(updated.get("_id", ""))}}

# ============ WEBSOCKET ============
@app.websocket("/api/ws/{room_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, user_id: str):
    await websocket.accept()
    
    if room_id not in room_connections:
        room_connections[room_id] = {}
    
    room_connections[room_id][user_id] = websocket
    
    try:
        while True:
            data = await websocket.receive_json()
            
            if data.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
            elif data.get("type") == "chat":
                room = active_rooms.get(room_id)
                if room:
                    user = await db.users.find_one({"id": user_id})
                    if user:
                        message = {
                            "id": str(uuid.uuid4()),
                            "user_id": user_id,
                            "username": user["display_name"],
                            "avatar": user["avatar"],
                            "message": data.get("message", ""),
                            "timestamp": datetime.utcnow().isoformat()
                        }
                        room["chat_messages"].append(message)
                        await broadcast_to_room(room_id, {
                            "type": "chat_message",
                            "message": message
                        })
    except WebSocketDisconnect:
        if room_id in room_connections and user_id in room_connections[room_id]:
            del room_connections[room_id][user_id]
        
        await broadcast_to_room(room_id, {
            "type": "player_disconnected",
            "player_id": user_id
        })

async def broadcast_to_room(room_id: str, message: dict):
    if room_id in room_connections:
        disconnected = []
        for user_id, ws in room_connections[room_id].items():
            try:
                await ws.send_json(message)
            except:
                disconnected.append(user_id)
        
        for user_id in disconnected:
            del room_connections[room_id][user_id]
    
    # Also send to spectators
    if room_id in spectator_connections:
        for user_id, ws in list(spectator_connections[room_id].items()):
            try:
                await ws.send_json(message)
            except:
                del spectator_connections[room_id][user_id]

def get_public_game_state(game_state: dict) -> dict:
    if not game_state:
        return None
    return {
        "room_id": game_state["room_id"],
        "phase": game_state["phase"],
        "trump": game_state["trump"],
        "current_player_idx": game_state["current_player_idx"],
        "dealer_idx": game_state["dealer_idx"],
        "players": game_state["players"],
        "current_trick": game_state["current_trick"],
        "scores": game_state["scores"],
        "hand_sizes": {pid: len(game_state["hands"].get(pid, [])) for pid in game_state["players"]},
        "win_score": game_state["win_score"]
    }

def get_public_room(room: dict) -> dict:
    return {
        "id": room["id"],
        "code": room["code"],
        "name": room["name"],
        "host_id": room["host_id"],
        "max_players": room["max_players"],
        "bet_amount": room["bet_amount"],
        "is_private": room["is_private"],
        "players": room["players"],
        "spectators": room["spectators"],
        "status": room["status"],
        "game_state": get_public_game_state(room.get("game_state"))
    }

# ============ HEALTH CHECK ============
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "game": "All Fours Card Game"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
