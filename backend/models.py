"""Data models for the game."""
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Player:
    """Represents a player in a game room."""
    id: str
    socket_id: str
    secret_number: Optional[int] = None
    is_ready: bool = False
    is_connected: bool = True
    last_heartbeat: float = field(default_factory=lambda: datetime.now().timestamp())


@dataclass
class Guess:
    """Represents a guess made by a player."""
    player_id: str
    guess: int
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    feedback: Optional[str] = None  # "too_low", "too_high", "correct"


@dataclass
class GameState:
    """Represents the state of a game room."""
    room_code: str
    players: Dict[str, Player] = field(default_factory=dict)
    game_state: str = "waiting_for_players"  # waiting_for_players, setup_phase, guessing_phase, finished
    guess_history: List[Guess] = field(default_factory=list)
    valid_range: Dict[str, int] = field(default_factory=lambda: {"min": 1, "max": 100})
    winner: Optional[str] = None
    created_at: float = field(default_factory=lambda: datetime.now().timestamp())
    last_activity: float = field(default_factory=lambda: datetime.now().timestamp())
