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
from datetime import datetime, timezone

# Import ÆTHER-NET modules
from aethernet import (
    AetherNetwork,
    AetherEntity,
    ChromaticEnergy,
    PsiLangInterpreter
)

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="ÆTHER-NET API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Global network instance (in-memory for Phase 1)
network = AetherNetwork()
psilang_interpreter = PsiLangInterpreter()

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
