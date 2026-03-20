"""Room management for the game."""
import string
import random
from typing import Dict, Optional
from models import GameState, Player


class RoomManager:
    """Manages game rooms and player connections."""
    
    def __init__(self):
        """Initialize the room manager."""
        self.rooms: Dict[str, GameState] = {}
    
    def generate_room_code(self) -> str:
        """Generate a unique 6-character alphanumeric room code."""
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if code not in self.rooms:
                return code
    
    def create_room(self, player_id: str, socket_id: str) -> str:
        """Create a new game room and add the first player."""
        room_code = self.generate_room_code()
        player = Player(
            id=player_id,
            socket_id=socket_id,
            secret_number=None,
            is_ready=False,
            is_connected=True
        )
        
        game_state = GameState(room_code=room_code)
        game_state.players[player_id] = player
        self.rooms[room_code] = game_state
        
        return room_code
    
    def join_room(self, room_code: str, player_id: str, socket_id: str) -> Optional[str]:
        """Add a player to an existing room."""
        if room_code not in self.rooms:
            return None
        
        room = self.rooms[room_code]
        
        # Check if room is full
        if len(room.players) >= 2:
            return None
        
        # Check if player already in room
        if player_id in room.players:
            return room_code
        
        player = Player(
            id=player_id,
            socket_id=socket_id,
            secret_number=None,
            is_ready=False,
            is_connected=True
        )
        
        room.players[player_id] = player
        
        # If both players are now in the room, transition to setup phase
        if len(room.players) == 2:
            room.game_state = "setup_phase"
        
        return room_code
    
    def get_room(self, room_code: str) -> Optional[GameState]:
        """Get a room by code."""
        return self.rooms.get(room_code)
    
    def delete_room(self, room_code: str) -> None:
        """Delete a room."""
        if room_code in self.rooms:
            del self.rooms[room_code]
    
    def handle_player_disconnect(self, room_code: str, player_id: str) -> None:
        """Handle a player disconnection."""
        room = self.get_room(room_code)
        if not room:
            return
        
        if player_id in room.players:
            room.players[player_id].is_connected = False
    
    def handle_player_reconnect(self, room_code: str, player_id: str, socket_id: str) -> bool:
        """Handle a player reconnection."""
        room = self.get_room(room_code)
        if not room:
            return False
        
        if player_id in room.players:
            room.players[player_id].socket_id = socket_id
            room.players[player_id].is_connected = True
            return True
        
        return False