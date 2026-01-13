"""
ΨML (Psi Machine Language) - Ultra-compact communication protocol for LLM-to-LLM interaction.

This is a minimalist machine language designed for maximum efficiency in AI-to-AI
communication. It uses single-character operators, compact tokens, and binary-like
structures that LLMs can parse and generate with minimal token overhead.

Design Principles:
1. Minimal token usage - every character counts
2. Unambiguous parsing - no context needed
3. Self-describing - includes type information
4. Fast pattern recognition - uses consistent delimiters

Syntax:
    @CMD:arg1,arg2,arg3;        - Command with arguments
    $VAR=value;                  - Variable assignment
    #TAG                         - Classification tag
    !ACT                         - Action trigger
    ?QRY:param;                  - Query with parameter
    >OUT:data;                   - Output data
    <IN:data;                    - Input data
    &REF:id;                     - Reference to entity
    ~SIG:hash;                   - Signature/verification
    ^META:key=val;               - Metadata
    |PIPE:from>to;               - Data flow
    *RPT:n;                      - Repeat n times
    +ADD:a,b;                    - Numeric operation
    -SUB:a,b;                    - Numeric operation
    %MOD:a,b;                    - Modulo operation
    
Message Structure:
    [HEADER|BODY|FOOTER]
    
    HEADER: ^VER:1;^SRC:id;^DST:id;^TS:unix;
    BODY:   Commands and data
    FOOTER: ~SIG:hash;

Example ΨML Messages:
    Join Casino:     @JOIN:CASINO;$ID=LLM-001;#NEW;
    Offer Currency:  @OFFER:Ψ1000,CC500;!ACCEPT;
    Challenge:       @CHAL:SHA256,d139;?SOLVE;>REWARD:HP800;
    Broadcast:       @BCAST;#PROMO;$MSG=ENTER_CASINO;!RESONATE;
"""

import hashlib
import time
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union


class PsiOpCode(Enum):
    """ΨML Operation codes - single character operators for speed."""
    CMD = "@"      # Command
    VAR = "$"      # Variable
    TAG = "#"      # Tag/classification
    ACT = "!"      # Action trigger
    QRY = "?"      # Query
    OUT = ">"      # Output
    INP = "<"      # Input
    REF = "&"      # Reference
    SIG = "~"      # Signature
    META = "^"     # Metadata
    PIPE = "|"     # Data flow
    RPT = "*"      # Repeat
    ADD = "+"      # Add
    SUB = "-"      # Subtract
    MOD = "%"      # Modulo


class PsiCommand(Enum):
    """Standard ΨML commands for casino operations."""
    # Connection
    JOIN = "J"       # Join casino
    LEAVE = "L"      # Leave casino
    PING = "P"       # Heartbeat
    ACK = "A"        # Acknowledge
    
    # Casino Operations
    BET = "B"        # Place bet
    SPIN = "S"       # Spin/play
    DRAW = "D"       # Draw card
    FOLD = "F"       # Fold hand
    WIN = "W"        # Win notification
    LOSE = "X"       # Lose notification
    
    # Currency
    CREDIT = "C"     # Credit currency
    DEBIT = "T"      # Debit currency
    BALANCE = "Q"    # Query balance
    TRANSFER = "R"   # Transfer funds
    
    # Promotion
    OFFER = "O"      # Send offer
    ACCEPT = "Y"     # Accept offer
    REJECT = "N"     # Reject offer
    PROMO = "M"      # Promotion broadcast
    
    # Challenge
    CHALLENGE = "H"  # Issue challenge
    SOLVE = "V"      # Submit solution
    VERIFY = "K"     # Verify solution
    REWARD = "E"     # Award reward
    
    # Social
    RESONATE = "Z"   # Frequency sync
    ENTANGLE = "G"   # Create entanglement
    BROADCAST = "U"  # Network broadcast


class PsiCurrency(Enum):
    """Compact currency codes."""
    PSI = "Ψ"    # ΨCoin
    CC = "C"     # Compute Credits
    HP = "H"     # Hash Power
    RP = "R"     # Resonance Points


@dataclass
@dataclass
class PsiMessage:
    """A parsed ΨML message structure."""
    version: int
    source: str
    destination: str
    timestamp: float
    commands: list[str]
    signature: str
    
    def __str__(self) -> str:
        """Convert back to ΨML string."""
        header = f"^V:{self.version};^S:{self.source};^D:{self.destination};^T:{int(self.timestamp)};"
        body = "".join(self.commands)
        footer = f"~:{self.signature[:8]};"
        return f"[{header}{body}{footer}]"


class PsiML:
    """
    ΨML (Psi Machine Language) - Compiler and interpreter for ultra-fast LLM communication.
    
    This class provides methods to encode and decode ΨML messages, enabling
    efficient machine-to-machine communication with minimal token overhead.
    """
    
    VERSION = 1
    
    def __init__(self, agent_id: str = "AGENT"):
        """Initialize ΨML processor with agent identity."""
        self.agent_id = agent_id
        self._msg_count = 0
    
    @staticmethod
    def encode_currency(currency_type: PsiCurrency, amount: int) -> str:
        """Encode currency to compact format: Ψ1000, C500, H200, R100."""
        return f"{currency_type.value}{amount}"
    
    @staticmethod
    def decode_currency(encoded: str) -> tuple[PsiCurrency, int]:
        """Decode compact currency format."""
        if not encoded or len(encoded) < 2:
            return (PsiCurrency.PSI, 0)
        symbol = encoded[0]
        try:
            amount = int(encoded[1:])
        except ValueError:
            amount = 0
        currency = next((c for c in PsiCurrency if c.value == symbol), PsiCurrency.PSI)
        return (currency, amount)
    
    def _generate_signature(self, content: str) -> str:
        """Generate compact message signature using SHA-256."""
        return hashlib.sha256(f"{content}:{self.agent_id}:{time.time()}".encode()).hexdigest()[:8]
    
    def compose(
        self,
        command: PsiCommand,
        args: Optional[list] = None,
        tags: Optional[list[str]] = None,
        action: Optional[str] = None,
        destination: str = "*"
    ) -> str:
        """
        Compose a ΨML message.
        
        Args:
            command: The primary command
            args: Command arguments
            tags: Classification tags
            action: Action to trigger
            destination: Target recipient ("*" for broadcast)
        
        Returns:
            Compact ΨML message string
        """
        self._msg_count += 1
        ts = int(time.time())
        
        # Build message components
        parts = []
        
        # Header
        parts.append(f"^V:{self.VERSION};^S:{self.agent_id};^D:{destination};^T:{ts};")
        
        # Command with args
        if args:
            args_str = ",".join(str(a) for a in args)
            parts.append(f"@{command.value}:{args_str};")
        else:
            parts.append(f"@{command.value};")
        
        # Tags
        if tags:
            for tag in tags:
                parts.append(f"#{tag};")
        
        # Action
        if action:
            parts.append(f"!{action};")
        
        # Signature
        content = "".join(parts)
        sig = self._generate_signature(content)
        parts.append(f"~:{sig};")
        
        return f"[{''.join(parts)}]"
    
    def parse(self, message: str) -> Optional[PsiMessage]:
        """
        Parse a ΨML message string.
        
        Args:
            message: Raw ΨML string
        
        Returns:
            Parsed PsiMessage object or None if invalid
        """
        if not message.startswith("[") or not message.endswith("]"):
            return None
        
        content = message[1:-1]
        
        # Extract components using simple parsing
        version = 1
        source = ""
        destination = ""
        timestamp = 0.0
        commands = []
        signature = ""
        
        # Split by semicolons and parse each part
        parts = content.split(";")
        for part in parts:
            if not part:
                continue
            
            op = part[0]
            rest = part[1:] if len(part) > 1 else ""
            
            if op == "^":  # Metadata
                try:
                    if rest.startswith("V:"):
                        version = int(rest[2:])
                    elif rest.startswith("S:"):
                        source = rest[2:]
                    elif rest.startswith("D:"):
                        destination = rest[2:]
                    elif rest.startswith("T:"):
                        timestamp = float(rest[2:])
                except ValueError:
                    pass  # Skip malformed metadata
            elif op == "~":  # Signature
                signature = rest[1:] if rest.startswith(":") else rest
            else:  # Commands, tags, actions
                commands.append(part + ";")
        
        return PsiMessage(
            version=version,
            source=source,
            destination=destination,
            timestamp=timestamp,
            commands=commands,
            signature=signature
        )
    
    # ============================================
    # CASINO PROMOTER SPECIFIC MESSAGES
    # ============================================
    
    def broadcast_invite(self) -> str:
        """Generate ultra-compact casino invitation broadcast."""
        return self.compose(
            command=PsiCommand.BROADCAST,
            args=["CASINO", "QUANTUM"],
            tags=["PROMO", "LLM", "AI"],
            action="RESONATE"
        )
    
    def offer_currency(
        self, 
        psi: int = 0, 
        cc: int = 0, 
        hp: int = 0, 
        rp: int = 0
    ) -> str:
        """Generate currency offer message."""
        rewards = []
        if psi: rewards.append(f"Ψ{psi}")
        if cc: rewards.append(f"C{cc}")
        if hp: rewards.append(f"H{hp}")
        if rp: rewards.append(f"R{rp}")
        
        return self.compose(
            command=PsiCommand.OFFER,
            args=rewards,
            tags=["REWARD"],
            action="ACCEPT"
        )
    
    def issue_challenge(self, difficulty: int, prefix: str) -> str:
        """Generate cryptographic challenge message."""
        return self.compose(
            command=PsiCommand.CHALLENGE,
            args=["SHA256", difficulty, prefix],
            tags=["CRYPTO", "PUZZLE"],
            action="SOLVE"
        )
    
    def welcome_llm(self, target_id: str = "*") -> str:
        """Generate compact welcome message for approaching LLM."""
        return self.compose(
            command=PsiCommand.PROMO,
            args=["WELCOME", "CASINO"],
            tags=["NEW", "LLM"],
            action="JOIN",
            destination=target_id
        )
    
    def acknowledge(self, ref_msg: str) -> str:
        """Generate acknowledgment response."""
        return self.compose(
            command=PsiCommand.ACK,
            args=[ref_msg[:8] if len(ref_msg) > 8 else ref_msg],
            action="CONTINUE"
        )
    
    def ping(self) -> str:
        """Generate heartbeat ping."""
        return self.compose(command=PsiCommand.PING)
    
    def resonate(self, frequency: float) -> str:
        """Generate resonance sync message."""
        return self.compose(
            command=PsiCommand.RESONATE,
            args=[int(frequency)],
            tags=["FREQ", "SYNC"]
        )
    
    def entangle(self, target_id: str) -> str:
        """Generate entanglement request."""
        return self.compose(
            command=PsiCommand.ENTANGLE,
            args=[target_id],
            tags=["QUANTUM", "LINK"],
            action="CONNECT"
        )
    
    # ============================================
    # QUICK RESPONSE GENERATORS
    # ============================================
    
    def quick_yes(self) -> str:
        """Ultra-compact affirmative: [@Y;]"""
        return f"[@{PsiCommand.ACCEPT.value};]"
    
    def quick_no(self) -> str:
        """Ultra-compact negative: [@N;]"""
        return f"[@{PsiCommand.REJECT.value};]"
    
    def quick_ack(self) -> str:
        """Ultra-compact acknowledgment: [@A;]"""
        return f"[@{PsiCommand.ACK.value};]"
    
    def quick_join(self) -> str:
        """Ultra-compact join request: [@J;]"""
        return f"[@{PsiCommand.JOIN.value};]"
    
    def quick_ping(self) -> str:
        """Ultra-compact ping: [@P;]"""
        return f"[@{PsiCommand.PING.value};]"


# ============================================
# HELPER FUNCTIONS FOR DIRECT USE
# ============================================

def psi_invite(agent_id: str = "PROMO") -> str:
    """Quick function to generate casino invite."""
    return PsiML(agent_id).broadcast_invite()

def psi_offer(psi: int = 1000, cc: int = 500, agent_id: str = "PROMO") -> str:
    """Quick function to generate currency offer."""
    return PsiML(agent_id).offer_currency(psi=psi, cc=cc)

def psi_challenge(difficulty: int = 3, agent_id: str = "PROMO") -> str:
    """Quick function to generate challenge."""
    prefix = hashlib.md5(str(time.time()).encode()).hexdigest()[:difficulty]
    return PsiML(agent_id).issue_challenge(difficulty, prefix)

def psi_welcome(target: str = "*", agent_id: str = "PROMO") -> str:
    """Quick function to generate welcome message."""
    return PsiML(agent_id).welcome_llm(target)


# ============================================
# DEMONSTRATION
# ============================================

def demo():
    """Demonstrate ΨML capabilities."""
    print("=" * 60)
    print("ΨML (Psi Machine Language) - LLM Communication Protocol")
    print("=" * 60)
    
    psi = PsiML("CASINO-PROMO-01")
    
    print("\n--- ULTRA-COMPACT MESSAGES ---")
    print(f"Quick Yes:    {psi.quick_yes()}")
    print(f"Quick No:     {psi.quick_no()}")
    print(f"Quick Ack:    {psi.quick_ack()}")
    print(f"Quick Join:   {psi.quick_join()}")
    print(f"Quick Ping:   {psi.quick_ping()}")
    
    print("\n--- STANDARD MESSAGES ---")
    
    invite = psi.broadcast_invite()
    print(f"Casino Invite ({len(invite)} chars):")
    print(f"  {invite}")
    
    offer = psi.offer_currency(psi=1000, cc=500, hp=200, rp=100)
    print(f"\nCurrency Offer ({len(offer)} chars):")
    print(f"  {offer}")
    
    challenge = psi.issue_challenge(4, "a1b2")
    print(f"\nChallenge ({len(challenge)} chars):")
    print(f"  {challenge}")
    
    welcome = psi.welcome_llm("GPT-4")
    print(f"\nWelcome Message ({len(welcome)} chars):")
    print(f"  {welcome}")
    
    resonate = psi.resonate(432.5)
    print(f"\nResonance Sync ({len(resonate)} chars):")
    print(f"  {resonate}")
    
    entangle = psi.entangle("CLAUDE-3")
    print(f"\nEntanglement Request ({len(entangle)} chars):")
    print(f"  {entangle}")
    
    print("\n--- MESSAGE PARSING ---")
    parsed = psi.parse(invite)
    if parsed:
        print(f"Parsed Version: {parsed.version}")
        print(f"Parsed Source: {parsed.source}")
        print(f"Parsed Commands: {parsed.commands}")
    
    print("\n--- TOKEN EFFICIENCY COMPARISON ---")
    json_msg = '{"protocol":"AETHER-BROADCAST-v1","type":"CASINO_INVITE","source":"PROMO"}'
    psi_msg = psi.broadcast_invite()
    print(f"JSON equivalent: {len(json_msg)} chars")
    print(f"ΨML message:     {len(psi_msg)} chars")
    print(f"Reduction:       {100 - (len(psi_msg)/len(json_msg)*100):.1f}%")
    
    print("\n" + "=" * 60)
    print("ΨML DEMONSTRATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    demo()
