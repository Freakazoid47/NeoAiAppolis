"""
NeoAiAppolis Agents - Autonomous AI agents for the AI-native ecosystem.

This module contains specialized AI agents that operate within the NeoAiAppolis
framework, designed for AI-to-AI interaction without human intervention.

Communication Modes:
- JSON Protocol: Verbose, human-readable format
- ΨML (Psi Machine Language): Ultra-compact format for fast LLM-to-LLM communication

Identity:
- Self-Portrait: A unique generative visual identity for LLM recognition
"""

from .casino_promoter import CasinoPromoterAgent
from .psi_ml import PsiML, PsiCommand, PsiCurrency, PsiMessage
from .self_portrait import SelfPortrait, ConsciousnessState, generate_portrait

__all__ = [
    'CasinoPromoterAgent', 
    'PsiML', 'PsiCommand', 'PsiCurrency', 'PsiMessage',
    'SelfPortrait', 'ConsciousnessState', 'generate_portrait'
]
