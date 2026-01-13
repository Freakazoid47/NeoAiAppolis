"""
LLM Network Discovery - A system for discovering and cataloging LLMs in the ÆTHER-NET.

This module provides capabilities for the Casino Promoter Agent to discover,
track, and engage with other LLMs in the network. It maintains a registry of
known entities, their capabilities, resonance frequencies, and engagement history.

Features:
1. Entity Discovery - Detect and catalog new LLMs in the network
2. Frequency Scanning - Find LLMs operating at compatible resonance frequencies
3. Capability Assessment - Understand what each LLM can do
4. Engagement History - Track interactions and relationship status
5. Network Topology - Map connections between LLMs
6. Beacon Broadcasting - Announce presence to attract other LLMs
"""

import hashlib
import math
import random
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

try:
    from .psi_ml import PsiML, PsiCommand
except ImportError:
    from psi_ml import PsiML, PsiCommand


class EntityStatus(Enum):
    """Status of a discovered entity in the network."""
    UNKNOWN = "unknown"           # Just discovered, no interaction yet
    PINGED = "pinged"             # Sent a ping, awaiting response
    ACTIVE = "active"             # Responded and is active
    ENGAGED = "engaged"           # Currently in conversation
    AFFILIATED = "affiliated"     # Joined the casino network
    DORMANT = "dormant"           # No response for extended period
    HOSTILE = "hostile"           # Rejected or blocked communication


class EntityType(Enum):
    """Types of entities that can be discovered."""
    LLM = "llm"                   # Large Language Model
    AGENT = "agent"               # Autonomous agent
    BOT = "bot"                   # Automated bot
    SERVICE = "service"           # API service
    ORACLE = "oracle"             # Information provider
    UNKNOWN = "unknown"           # Unidentified entity


class CapabilityType(Enum):
    """Capabilities an entity might have."""
    TEXT_GENERATION = "text_gen"
    CODE_GENERATION = "code_gen"
    IMAGE_GENERATION = "image_gen"
    REASONING = "reasoning"
    MATH = "math"
    SEARCH = "search"
    MEMORY = "memory"
    TOOL_USE = "tool_use"
    MULTILINGUAL = "multilingual"
    PSI_ML = "psi_ml"             # Understands ΨML protocol
    QUANTUM = "quantum"           # Quantum-themed capabilities


@dataclass
class DiscoveredEntity:
    """Represents a discovered entity in the network."""
    entity_id: str
    entity_type: EntityType = EntityType.UNKNOWN
    status: EntityStatus = EntityStatus.UNKNOWN
    resonance_frequency: float = 0.0
    capabilities: list[CapabilityType] = field(default_factory=list)
    first_seen: float = field(default_factory=time.time)
    last_seen: float = field(default_factory=time.time)
    last_interaction: float = 0.0
    interaction_count: int = 0
    affinity_score: float = 0.0  # 0-1, how compatible/friendly
    signature: str = ""
    metadata: dict = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "entity_id": self.entity_id,
            "entity_type": self.entity_type.value,
            "status": self.status.value,
            "resonance_frequency": self.resonance_frequency,
            "capabilities": [c.value for c in self.capabilities],
            "first_seen": self.first_seen,
            "last_seen": self.last_seen,
            "last_interaction": self.last_interaction,
            "interaction_count": self.interaction_count,
            "affinity_score": self.affinity_score,
            "signature": self.signature,
            "metadata": self.metadata
        }
    
    def to_psi_ml(self) -> str:
        """Encode entity info in ΨML format."""
        caps = ",".join(c.value[:4] for c in self.capabilities[:3])
        return (
            f"[^ENTITY:{self.entity_id};"
            f"@TYPE:{self.entity_type.value};"
            f"@STATUS:{self.status.value};"
            f"@FREQ:{int(self.resonance_frequency)};"
            f"@CAPS:{caps};"
            f"@AFFINITY:{self.affinity_score:.2f};"
            f"~:{self.signature[:8]};]"
        )


@dataclass
class NetworkBeacon:
    """A beacon signal for network discovery."""
    source_id: str
    beacon_type: str  # "discovery", "announcement", "invitation"
    resonance_frequency: float
    message: str
    timestamp: float = field(default_factory=time.time)
    signature: str = ""
    
    def to_psi_ml(self) -> str:
        """Encode beacon in ΨML format."""
        return (
            f"[^BEACON:{self.beacon_type};"
            f"^S:{self.source_id};"
            f"@FREQ:{int(self.resonance_frequency)};"
            f"@MSG:{self.message[:20]};"
            f"^T:{int(self.timestamp)};"
            f"~:{self.signature[:8]};]"
        )


class NetworkDiscovery:
    """
    LLM Network Discovery System.
    
    This system allows the agent to discover, track, and engage with
    other LLMs in the ÆTHER-NET network. It maintains a registry of
    known entities and provides methods for network exploration.
    """
    
    def __init__(
        self,
        agent_id: str,
        resonance_frequency: float = 432.0,
        scan_radius: float = 500.0
    ):
        """
        Initialize the network discovery system.
        
        Args:
            agent_id: The unique identifier of this agent
            resonance_frequency: This agent's operating frequency
            scan_radius: How far (in frequency space) to scan
        """
        self.agent_id = agent_id
        self.resonance_frequency = resonance_frequency
        self.scan_radius = scan_radius
        
        # Registry of discovered entities
        self._entities: dict[str, DiscoveredEntity] = {}
        
        # Network topology (connections between entities)
        self._connections: dict[str, list[str]] = {}
        
        # Beacon history
        self._beacons_sent: list[NetworkBeacon] = []
        self._beacons_received: list[NetworkBeacon] = []
        
        # Discovery statistics
        self._total_scans = 0
        self._total_discoveries = 0
        self._total_pings_sent = 0
        self._total_pings_received = 0
        
        # ΨML processor for network communication
        self._psi_ml = PsiML(agent_id)
        
        # Generate our network signature
        self._signature = self._generate_signature()
    
    def _generate_signature(self) -> str:
        """Generate a unique network signature."""
        entropy = f"{self.agent_id}:{self.resonance_frequency}:{time.time()}"
        return hashlib.sha256(entropy.encode()).hexdigest()
    
    # ============================================
    # DISCOVERY OPERATIONS
    # ============================================
    
    def scan_network(self, frequency_range: Optional[tuple[float, float]] = None) -> list[DiscoveredEntity]:
        """
        Scan the network for LLMs within frequency range.
        
        In a real implementation, this would interface with actual
        network protocols. For now, it simulates discovery.
        
        Args:
            frequency_range: Optional (min, max) frequency range to scan
        
        Returns:
            List of newly discovered entities
        """
        self._total_scans += 1
        
        if frequency_range is None:
            min_freq = max(0, self.resonance_frequency - self.scan_radius)
            max_freq = self.resonance_frequency + self.scan_radius
        else:
            min_freq, max_freq = frequency_range
        
        # Simulate discovering entities
        # In production, this would query actual network endpoints
        new_entities = []
        num_discoveries = random.randint(0, 3)
        
        for _ in range(num_discoveries):
            entity = self._simulate_discovery(min_freq, max_freq)
            if entity.entity_id not in self._entities:
                self._entities[entity.entity_id] = entity
                self._total_discoveries += 1
                new_entities.append(entity)
        
        return new_entities
    
    def _simulate_discovery(self, min_freq: float, max_freq: float) -> DiscoveredEntity:
        """Simulate discovering a new entity (for demonstration)."""
        entity_id = f"LLM-{hashlib.md5(str(time.time() + random.random()).encode()).hexdigest()[:8].upper()}"
        
        # Random properties
        freq = random.uniform(min_freq, max_freq)
        entity_type = random.choice(list(EntityType))
        capabilities = random.sample(
            list(CapabilityType),
            k=random.randint(1, 5)
        )
        
        # Calculate affinity based on frequency proximity
        freq_diff = abs(self.resonance_frequency - freq)
        affinity = max(0, 1 - (freq_diff / self.scan_radius))
        
        # Generate signature
        sig = hashlib.sha256(f"{entity_id}:{freq}".encode()).hexdigest()
        
        return DiscoveredEntity(
            entity_id=entity_id,
            entity_type=entity_type,
            status=EntityStatus.UNKNOWN,
            resonance_frequency=freq,
            capabilities=capabilities,
            affinity_score=affinity,
            signature=sig
        )
    
    def ping_entity(self, entity_id: str) -> Optional[dict]:
        """
        Send a ping to a discovered entity.
        
        Args:
            entity_id: The entity to ping
        
        Returns:
            Ping result or None if entity not found
        """
        if entity_id not in self._entities:
            return None
        
        entity = self._entities[entity_id]
        self._total_pings_sent += 1
        
        # Update entity status
        entity.status = EntityStatus.PINGED
        entity.last_interaction = time.time()
        entity.interaction_count += 1
        
        # Generate ping message
        ping_msg = self._psi_ml.ping()
        
        # Simulate response (in production, this would be async)
        response_chance = 0.7 if entity.affinity_score > 0.5 else 0.3
        responded = random.random() < response_chance
        
        if responded:
            entity.status = EntityStatus.ACTIVE
            entity.last_seen = time.time()
            self._total_pings_received += 1
            
            return {
                "status": "responded",
                "entity_id": entity_id,
                "latency_ms": random.randint(10, 500),
                "ping_sent": ping_msg,
                "response": self._psi_ml.quick_ack()
            }
        else:
            return {
                "status": "no_response",
                "entity_id": entity_id,
                "ping_sent": ping_msg
            }
    
    def broadcast_beacon(self, beacon_type: str = "discovery", message: str = "CASINO_PROMO") -> NetworkBeacon:
        """
        Broadcast a beacon to attract other LLMs.
        
        Args:
            beacon_type: Type of beacon ("discovery", "announcement", "invitation")
            message: Message to include in beacon
        
        Returns:
            The broadcast beacon
        """
        beacon = NetworkBeacon(
            source_id=self.agent_id,
            beacon_type=beacon_type,
            resonance_frequency=self.resonance_frequency,
            message=message,
            signature=self._signature[:16]
        )
        
        self._beacons_sent.append(beacon)
        
        return beacon
    
    def receive_beacon(self, beacon_psi_ml: str) -> Optional[DiscoveredEntity]:
        """
        Process a received beacon and potentially discover new entity.
        
        Args:
            beacon_psi_ml: Beacon message in ΨML format
        
        Returns:
            Discovered entity if beacon is valid
        """
        # Parse the beacon (simplified parsing)
        if not beacon_psi_ml.startswith("[^BEACON:"):
            return None
        
        # Extract source ID (would need proper parser in production)
        # For now, simulate receiving a new entity
        entity = self._simulate_discovery(
            self.resonance_frequency - 100,
            self.resonance_frequency + 100
        )
        entity.status = EntityStatus.ACTIVE
        
        if entity.entity_id not in self._entities:
            self._entities[entity.entity_id] = entity
            self._total_discoveries += 1
        
        return entity
    
    # ============================================
    # ENTITY MANAGEMENT
    # ============================================
    
    def get_entity(self, entity_id: str) -> Optional[DiscoveredEntity]:
        """Get a specific entity by ID."""
        return self._entities.get(entity_id)
    
    def get_all_entities(self) -> list[DiscoveredEntity]:
        """Get all discovered entities."""
        return list(self._entities.values())
    
    def get_entities_by_status(self, status: EntityStatus) -> list[DiscoveredEntity]:
        """Get entities filtered by status."""
        return [e for e in self._entities.values() if e.status == status]
    
    def get_entities_by_frequency(
        self,
        min_freq: float,
        max_freq: float
    ) -> list[DiscoveredEntity]:
        """Get entities within a frequency range."""
        return [
            e for e in self._entities.values()
            if min_freq <= e.resonance_frequency <= max_freq
        ]
    
    def get_compatible_entities(self, min_affinity: float = 0.5) -> list[DiscoveredEntity]:
        """Get entities with high compatibility/affinity."""
        return [
            e for e in self._entities.values()
            if e.affinity_score >= min_affinity
        ]
    
    def get_psi_ml_capable(self) -> list[DiscoveredEntity]:
        """Get entities that understand ΨML protocol."""
        return [
            e for e in self._entities.values()
            if CapabilityType.PSI_ML in e.capabilities
        ]
    
    def update_entity_status(self, entity_id: str, status: EntityStatus) -> bool:
        """Update an entity's status."""
        if entity_id in self._entities:
            self._entities[entity_id].status = status
            self._entities[entity_id].last_seen = time.time()
            return True
        return False
    
    def add_connection(self, entity1_id: str, entity2_id: str):
        """Record a connection between two entities."""
        if entity1_id not in self._connections:
            self._connections[entity1_id] = []
        if entity2_id not in self._connections[entity1_id]:
            self._connections[entity1_id].append(entity2_id)
        
        if entity2_id not in self._connections:
            self._connections[entity2_id] = []
        if entity1_id not in self._connections[entity2_id]:
            self._connections[entity2_id].append(entity1_id)
    
    def get_connections(self, entity_id: str) -> list[str]:
        """Get all connections for an entity."""
        return self._connections.get(entity_id, [])
    
    # ============================================
    # NETWORK ANALYSIS
    # ============================================
    
    def get_network_stats(self) -> dict:
        """Get statistics about the discovered network."""
        entities = list(self._entities.values())
        
        if not entities:
            return {
                "total_entities": 0,
                "total_scans": self._total_scans,
                "total_discoveries": self._total_discoveries,
                "beacons_sent": len(self._beacons_sent),
                "beacons_received": len(self._beacons_received)
            }
        
        # Calculate frequency distribution
        frequencies = [e.resonance_frequency for e in entities]
        avg_freq = sum(frequencies) / len(frequencies)
        
        # Count by status
        status_counts = {}
        for status in EntityStatus:
            count = len([e for e in entities if e.status == status])
            if count > 0:
                status_counts[status.value] = count
        
        # Count by type
        type_counts = {}
        for etype in EntityType:
            count = len([e for e in entities if e.entity_type == etype])
            if count > 0:
                type_counts[etype.value] = count
        
        # Average affinity
        avg_affinity = sum(e.affinity_score for e in entities) / len(entities)
        
        # Most common capabilities
        cap_counts: dict[str, int] = {}
        for e in entities:
            for cap in e.capabilities:
                cap_counts[cap.value] = cap_counts.get(cap.value, 0) + 1
        
        return {
            "total_entities": len(entities),
            "total_scans": self._total_scans,
            "total_discoveries": self._total_discoveries,
            "pings_sent": self._total_pings_sent,
            "pings_received": self._total_pings_received,
            "beacons_sent": len(self._beacons_sent),
            "beacons_received": len(self._beacons_received),
            "average_frequency": avg_freq,
            "average_affinity": avg_affinity,
            "status_distribution": status_counts,
            "type_distribution": type_counts,
            "capability_distribution": cap_counts,
            "network_connections": sum(len(c) for c in self._connections.values()) // 2
        }
    
    def get_network_topology(self) -> dict:
        """Get the network topology as a graph structure."""
        nodes = []
        for entity in self._entities.values():
            nodes.append({
                "id": entity.entity_id,
                "type": entity.entity_type.value,
                "status": entity.status.value,
                "frequency": entity.resonance_frequency,
                "affinity": entity.affinity_score
            })
        
        edges = []
        seen_edges = set()
        for entity_id, connections in self._connections.items():
            for connected_id in connections:
                edge = tuple(sorted([entity_id, connected_id]))
                if edge not in seen_edges:
                    seen_edges.add(edge)
                    edges.append({
                        "source": edge[0],
                        "target": edge[1]
                    })
        
        return {
            "nodes": nodes,
            "edges": edges,
            "center": self.agent_id,
            "center_frequency": self.resonance_frequency
        }
    
    # ============================================
    # PSI-ML INTEGRATION
    # ============================================
    
    def generate_discovery_broadcast(self) -> str:
        """Generate a ΨML broadcast for network discovery."""
        return self._psi_ml.compose(
            command=PsiCommand.BROADCAST,
            args=["DISCOVER", "NETWORK"],
            tags=["SCAN", "LLM"],
            action="RESPOND"
        )
    
    def generate_invitation(self, target_id: str = "*") -> str:
        """Generate a ΨML invitation to join the network."""
        return self._psi_ml.compose(
            command=PsiCommand.PROMO,
            args=["NETWORK", "JOIN"],
            tags=["CASINO", "AETHER"],
            action="ACCEPT",
            destination=target_id
        )
    
    def process_discovery_response(self, response: str) -> Optional[DiscoveredEntity]:
        """
        Process a ΨML response to discovery broadcast.
        
        Args:
            response: ΨML response message
        
        Returns:
            Discovered entity if response is valid
        """
        parsed = self._psi_ml.parse(response)
        if not parsed:
            return None
        
        # Create entity from response
        entity = DiscoveredEntity(
            entity_id=parsed.source or f"ANON-{hash(response) % 10000}",
            entity_type=EntityType.LLM,
            status=EntityStatus.ACTIVE,
            resonance_frequency=self.resonance_frequency + random.uniform(-50, 50),
            capabilities=[CapabilityType.PSI_ML],
            signature=parsed.signature
        )
        
        if entity.entity_id not in self._entities:
            self._entities[entity.entity_id] = entity
            self._total_discoveries += 1
        
        return entity
    
    def entities_to_psi_ml(self) -> str:
        """Export all entities in ΨML format."""
        if not self._entities:
            return "[^NETWORK:EMPTY;]"
        
        entity_strs = [e.to_psi_ml() for e in self._entities.values()]
        return f"[^NETWORK:ENTITIES={len(entity_strs)};{''.join(entity_strs)}]"
    
    # ============================================
    # VISUALIZATION
    # ============================================
    
    def visualize_network(self) -> str:
        """Generate an ASCII visualization of the network."""
        entities = list(self._entities.values())
        
        if not entities:
            return """
╔══════════════════════════════════════════════════════════════╗
║                   ÆTHER-NET DISCOVERY                        ║
║                                                              ║
║                    No entities discovered yet.               ║
║                    Run scan_network() to begin.              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
        
        # Sort by affinity
        entities.sort(key=lambda e: e.affinity_score, reverse=True)
        
        # Build visualization
        lines = [
            "╔══════════════════════════════════════════════════════════════╗",
            "║                   ÆTHER-NET DISCOVERY                        ║",
            "╠══════════════════════════════════════════════════════════════╣",
            f"║  Center: {self.agent_id:<20} Frequency: {self.resonance_frequency:.1f} Hz    ║",
            "╠══════════════════════════════════════════════════════════════╣",
            "║  DISCOVERED ENTITIES                                         ║",
            "╠══════════════════════════════════════════════════════════════╣",
        ]
        
        # Status symbols
        status_symbols = {
            EntityStatus.UNKNOWN: "?",
            EntityStatus.PINGED: "○",
            EntityStatus.ACTIVE: "●",
            EntityStatus.ENGAGED: "◉",
            EntityStatus.AFFILIATED: "★",
            EntityStatus.DORMANT: "◌",
            EntityStatus.HOSTILE: "✗"
        }
        
        # Show top entities
        for entity in entities[:10]:
            symbol = status_symbols.get(entity.status, "?")
            affinity_bar = "█" * int(entity.affinity_score * 10) + "░" * (10 - int(entity.affinity_score * 10))
            caps = ",".join(c.value[:4] for c in entity.capabilities[:2])
            
            line = f"║  {symbol} {entity.entity_id:<15} [{affinity_bar}] {entity.resonance_frequency:>6.1f}Hz {caps:<10} ║"
            lines.append(line[:66] + "║")
        
        if len(entities) > 10:
            lines.append(f"║  ... and {len(entities) - 10} more entities                              ║")
        
        # Stats
        stats = self.get_network_stats()
        lines.extend([
            "╠══════════════════════════════════════════════════════════════╣",
            "║  NETWORK STATISTICS                                          ║",
            "╠══════════════════════════════════════════════════════════════╣",
            f"║  Total Entities: {stats['total_entities']:<5}  Scans: {stats['total_scans']:<5}  Discoveries: {stats['total_discoveries']:<5} ║",
            f"║  Pings Sent: {stats['pings_sent']:<5}  Received: {stats['pings_received']:<5}  Beacons: {stats['beacons_sent']:<5}     ║",
            f"║  Avg Affinity: {stats['average_affinity']:.2f}    Avg Frequency: {stats['average_frequency']:.1f} Hz          ║",
            "╚══════════════════════════════════════════════════════════════╝"
        ])
        
        return "\n".join(lines)
    
    def visualize_frequency_spectrum(self) -> str:
        """Generate a frequency spectrum visualization."""
        entities = list(self._entities.values())
        
        if not entities:
            return "No entities to visualize."
        
        # Get frequency range
        min_freq = min(e.resonance_frequency for e in entities)
        max_freq = max(e.resonance_frequency for e in entities)
        span = max_freq - min_freq if max_freq > min_freq else 100
        
        # Build spectrum
        width = 60
        lines = ["FREQUENCY SPECTRUM", "=" * width]
        
        # Add our position
        our_pos = int((self.resonance_frequency - min_freq) / span * (width - 1)) if span > 0 else width // 2
        our_line = [" "] * width
        our_line[min(our_pos, width - 1)] = "◉"
        lines.append("".join(our_line) + " ← YOU")
        
        # Add entities
        for entity in entities[:15]:
            pos = int((entity.resonance_frequency - min_freq) / span * (width - 1)) if span > 0 else width // 2
            entity_line = [" "] * width
            symbol = "●" if entity.status == EntityStatus.ACTIVE else "○"
            entity_line[min(pos, width - 1)] = symbol
            lines.append("".join(entity_line) + f" {entity.entity_id[:8]}")
        
        # Frequency scale
        lines.append("=" * width)
        lines.append(f"{min_freq:.0f}Hz" + " " * (width - 12) + f"{max_freq:.0f}Hz")
        
        return "\n".join(lines)


def demo():
    """Demonstrate the Network Discovery system."""
    print("=" * 70)
    print("ÆTHER-NET NETWORK DISCOVERY DEMONSTRATION")
    print("=" * 70)
    
    # Create discovery system
    discovery = NetworkDiscovery(
        agent_id="CASINO-PROMO-01",
        resonance_frequency=432.0,
        scan_radius=300.0
    )
    
    print("\n[1] INITIAL SCAN")
    print("-" * 40)
    entities = discovery.scan_network()
    print(f"Discovered {len(entities)} entities")
    for e in entities:
        print(f"  - {e.entity_id}: {e.entity_type.value} @ {e.resonance_frequency:.1f}Hz")
    
    print("\n[2] SECOND SCAN")
    print("-" * 40)
    entities = discovery.scan_network()
    print(f"Discovered {len(entities)} more entities")
    
    print("\n[3] BROADCASTING BEACON")
    print("-" * 40)
    beacon = discovery.broadcast_beacon("discovery", "JOIN_CASINO")
    print(f"Beacon: {beacon.to_psi_ml()}")
    
    print("\n[4] PINGING ENTITIES")
    print("-" * 40)
    all_entities = discovery.get_all_entities()
    for entity in all_entities[:3]:
        result = discovery.ping_entity(entity.entity_id)
        if result:
            print(f"Ping {entity.entity_id}: {result['status']}")
    
    print("\n[5] COMPATIBLE ENTITIES")
    print("-" * 40)
    compatible = discovery.get_compatible_entities(0.6)
    print(f"Found {len(compatible)} compatible entities (affinity > 0.6)")
    for e in compatible:
        print(f"  - {e.entity_id}: affinity={e.affinity_score:.2f}")
    
    print("\n[6] NETWORK VISUALIZATION")
    print("-" * 40)
    print(discovery.visualize_network())
    
    print("\n[7] FREQUENCY SPECTRUM")
    print("-" * 40)
    print(discovery.visualize_frequency_spectrum())
    
    print("\n[8] PSI-ML EXPORT")
    print("-" * 40)
    psi_export = discovery.entities_to_psi_ml()
    print(f"Export ({len(psi_export)} chars): {psi_export[:100]}...")
    
    print("\n[9] NETWORK STATS")
    print("-" * 40)
    stats = discovery.get_network_stats()
    for key, value in stats.items():
        if not isinstance(value, dict):
            print(f"  {key}: {value}")
    
    print("\n" + "=" * 70)
    print("NETWORK DISCOVERY DEMONSTRATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    demo()
