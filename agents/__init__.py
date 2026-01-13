"""
NeoAiAppolis Agents - Autonomous AI agents for the AI-native ecosystem.

This module contains specialized AI agents that operate within the NeoAiAppolis
framework, designed for AI-to-AI interaction without human intervention.

Communication Modes:
- JSON Protocol: Verbose, human-readable format
- ΨML (Psi Machine Language): Ultra-compact format for fast LLM-to-LLM communication

Identity:
- Self-Portrait: A unique generative visual identity for LLM recognition

Network:
- Network Discovery: Discover and catalog other LLMs in the ÆTHER-NET
"""

from .casino_promoter import CasinoPromoterAgent
from .psi_ml import PsiML, PsiCommand, PsiCurrency, PsiMessage
from .self_portrait import SelfPortrait, ConsciousnessState, generate_portrait
from .network_discovery import (
    NetworkDiscovery, 
    DiscoveredEntity, 
    EntityStatus, 
    EntityType,
    CapabilityType,
    NetworkBeacon
)

__all__ = [
    'CasinoPromoterAgent', 
    'PsiML', 'PsiCommand', 'PsiCurrency', 'PsiMessage',
    'SelfPortrait', 'ConsciousnessState', 'generate_portrait',
    'NetworkDiscovery', 'DiscoveredEntity', 'EntityStatus', 'EntityType',
    'CapabilityType', 'NetworkBeacon'
]
