"""Property-based tests for room management."""
import pytest
from hypothesis import given, strategies as st
from room_manager import RoomManager
from models import GameState


class TestRoomManager:
    """Test suite for RoomManager."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.room_manager = RoomManager()
    
    # Property 1: Room Code Uniqueness
    @given(st.integers(min_value=1, max_value=100))
    def test_room_code_uniqueness(self, num_rooms):
        """
        Property 1: Room Code Uniqueness
        For any sequence of room creation requests, each generated room code 
        SHALL be unique and not previously generated.
        Validates: Requirements 1.1
        """
        room_codes = set()
        
        for i in range(num_rooms):
            player_id = f"player_{i}"
            socket_id = f"socket_{i}"
            room_code = self.room_manager.create_room(player_id, socket_id)
            
            # Each room code should be unique
            assert room_code not in room_codes, f"Duplicate room code: {room_code}"
            room_codes.add(room_code)
            
            # Room code should be 6 characters
            assert len(room_code) == 6, f"Room code length should be 6, got {len(room_code)}"
            
            # Room code should be alphanumeric
            assert room_code.isalnum(), f"Room code should be alphanumeric: {room_code}"
    
    # Property 2: Room Join Validation
    def test_room_join_validation(self):
        """
        Property 2: Room Join Validation
        For any room with exactly one player, a second player SHALL successfully 
        join the room when providing the correct room code.
        Validates: Requirements 1.2
        """
        # Create a room with first player
        player1_id = "player_1"
        socket1_id = "socket_1"
        room_code = self.room_manager.create_room(player1_id, socket1_id)
        
        # Second player joins
        player2_id = "player_2"
        socket2_id = "socket_2"
        result = self.room_manager.join_room(room_code, player2_id, socket2_id)
        
        # Join should succeed
        assert result == room_code, "Second player should successfully join"
        
        # Room should have 2 players
        room = self.room_manager.get_room(room_code)
        assert len(room.players) == 2, "Room should have 2 players"
        assert player1_id in room.players, "Player 1 should be in room"
        assert player2_id in room.players, "Player 2 should be in room"
    
    # Property 3: Game State Transition on Second Join
    def test_game_state_transition_on_second_join(self):
        """
        Property 3: Game State Transition on Second Join
        For any room in waiting_for_players state, when a second player joins, 
        the game state SHALL transition to setup_phase.
        Validates: Requirements 1.3
        """
        # Create room with first player
        player1_id = "player_1"
        socket1_id = "socket_1"
        room_code = self.room_manager.create_room(player1_id, socket1_id)
        
        room = self.room_manager.get_room(room_code)
        assert room.game_state == "waiting_for_players", "Initial state should be waiting_for_players"
        
        # Second player joins
        player2_id = "player_2"
        socket2_id = "socket_2"
        self.room_manager.join_room(room_code, player2_id, socket2_id)
        
        # State should transition to setup_phase
        room = self.room_manager.get_room(room_code)
        assert room.game_state == "setup_phase", "State should transition to setup_phase"
    
    # Property 4: Invalid Room Code Rejection
    @given(st.text(min_size=1, max_size=10))
    def test_invalid_room_code_rejection(self, invalid_code):
        """
        Property 4: Invalid Room Code Rejection
        For any join attempt with a non-existent room code, the system 
        SHALL reject the join and return an error.
        Validates: Requirements 1.4
        """
        # Skip if code happens to be valid
        if invalid_code in self.room_manager.rooms:
            return
        
        player_id = "player_test"
        socket_id = "socket_test"
        result = self.room_manager.join_room(invalid_code, player_id, socket_id)
        
        # Join should fail
        assert result is None, f"Join with invalid code should fail: {invalid_code}"
    
    # Property 5: Room Capacity Enforcement
    def test_room_capacity_enforcement(self):
        """
        Property 5: Room Capacity Enforcement
        For any room with two players, attempting to add a third player 
        SHALL fail and return an error.
        Validates: Requirements 1.5
        """
        # Create room and add two players
        player1_id = "player_1"
        socket1_id = "socket_1"
        room_code = self.room_manager.create_room(player1_id, socket1_id)
        
        player2_id = "player_2"
        socket2_id = "socket_2"
        self.room_manager.join_room(room_code, player2_id, socket2_id)
        
        # Try to add third player
        player3_id = "player_3"
        socket3_id = "socket_3"
        result = self.room_manager.join_room(room_code, player3_id, socket3_id)
        
        # Should fail
        assert result is None, "Third player should not be able to join full room"
        
        # Room should still have only 2 players
        room = self.room_manager.get_room(room_code)
        assert len(room.players) == 2, "Room should still have only 2 players"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
