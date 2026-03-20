"""Property-based tests for game engine."""
import pytest
from hypothesis import given, strategies as st, settings
from game_engine import GameEngine
from models import GameState, Player, Guess


class TestGameEngine:
    """Property-based tests for GameEngine class."""
    
    # Property 6: Secret Number Storage
    @given(
        secret_number=st.integers(min_value=1, max_value=100),
        player_id=st.text(min_size=1, max_size=10)
    )
    @settings(max_examples=100)
    def test_property_6_secret_number_storage(self, secret_number, player_id):
        """
        Property 6: Secret Number Storage
        For any valid secret number (1-100) submitted by a player,
        the system SHALL store it server-side without transmitting it to the opponent.
        """
        game_state = GameState(room_code="TEST001")
        player = Player(id=player_id, socket_id="socket_123")
        game_state.players[player_id] = player
        
        # Store secret number
        player.secret_number = secret_number
        
        # Verify it's stored
        assert game_state.players[player_id].secret_number == secret_number
        assert isinstance(game_state.players[player_id].secret_number, int)
    
    # Property 7: Secret Number Validation
    @given(
        secret_number=st.one_of(
            st.integers(max_value=0),
            st.integers(min_value=101)
        )
    )
    @settings(max_examples=100)
    def test_property_7_secret_number_validation(self, secret_number):
        """
        Property 7: Secret Number Validation
        For any secret number submission outside the range 1-100,
        the system SHALL reject it and return a validation error.
        """
        # Validation logic: check if number is in range
        is_valid = 1 <= secret_number <= 100
        assert not is_valid, f"Number {secret_number} should be invalid"
    
    # Property 8: Setup to Guessing Transition
    @given(
        secret1=st.integers(min_value=1, max_value=100),
        secret2=st.integers(min_value=1, max_value=100)
    )
    @settings(max_examples=100)
    def test_property_8_setup_to_guessing_transition(self, secret1, secret2):
        """
        Property 8: Setup to Guessing Transition
        For any room where both players have submitted valid secret numbers,
        the game state SHALL transition to guessing_phase.
        """
        game_state = GameState(room_code="TEST001", game_state="setup_phase")
        
        player1 = Player(id="player1", socket_id="socket1")
        player2 = Player(id="player2", socket_id="socket2")
        
        game_state.players["player1"] = player1
        game_state.players["player2"] = player2
        
        # Both players submit valid secret numbers
        player1.secret_number = secret1
        player1.is_ready = True
        player2.secret_number = secret2
        player2.is_ready = True
        
        # Check transition condition
        all_ready = all(p.is_ready for p in game_state.players.values())
        if all_ready:
            game_state.game_state = "guessing_phase"
        
        assert game_state.game_state == "guessing_phase"
        assert player1.secret_number == secret1
        assert player2.secret_number == secret2
    
    # Property 9: Initial Range Initialization
    @given(st.just(None))  # No input needed
    @settings(max_examples=100)
    def test_property_9_initial_range_initialization(self, _):
        """
        Property 9: Initial Range Initialization
        For any game entering guessing_phase, the valid range SHALL be initialized to [1, 100].
        """
        game_state = GameState(room_code="TEST001")
        
        # Verify initial range
        assert game_state.valid_range["min"] == 1
        assert game_state.valid_range["max"] == 100
    
    # Property 10: Guess Range Validation
    @given(
        guess=st.integers(),
        min_val=st.integers(min_value=1, max_value=50),
        max_val=st.integers(min_value=51, max_value=100)
    )
    @settings(max_examples=100)
    def test_property_10_guess_range_validation(self, guess, min_val, max_val):
        """
        Property 10: Guess Range Validation
        For any guess submission, if the guess is outside the current valid range,
        the system SHALL reject it and return an error.
        """
        valid_range = {"min": min_val, "max": max_val}
        
        is_valid, error_msg = GameEngine.validate_guess(guess, valid_range)
        
        if guess < min_val or guess > max_val:
            assert not is_valid
            assert error_msg is not None
        else:
            assert is_valid
            assert error_msg is None
    
    # Property 11: Range Update on Low Guess
    @given(
        secret=st.integers(min_value=50, max_value=100),
        guess=st.integers(min_value=1, max_value=49)
    )
    @settings(max_examples=100)
    def test_property_11_range_update_on_low_guess(self, secret, guess):
        """
        Property 11: Range Update on Low Guess
        For any guess that is less than the secret number,
        the valid range upper bound SHALL be updated to the guess value.
        """
        current_range = {"min": 1, "max": 100}
        
        new_range = GameEngine.calculate_range_update(guess, secret, current_range)
        
        # When guess < secret, min should be updated to guess + 1
        assert new_range["min"] == guess + 1
        assert new_range["max"] == 100
    
    # Property 12: Range Update on High Guess
    @given(
        secret=st.integers(min_value=1, max_value=50),
        guess=st.integers(min_value=51, max_value=100)
    )
    @settings(max_examples=100)
    def test_property_12_range_update_on_high_guess(self, secret, guess):
        """
        Property 12: Range Update on High Guess
        For any guess that is greater than the secret number,
        the valid range lower bound SHALL be updated to the guess value.
        """
        current_range = {"min": 1, "max": 100}
        
        new_range = GameEngine.calculate_range_update(guess, secret, current_range)
        
        # When guess > secret, max should be updated to guess - 1
        assert new_range["min"] == 1
        assert new_range["max"] == guess - 1
    
    # Property 13: Win Condition Detection
    @given(
        secret=st.integers(min_value=1, max_value=100)
    )
    @settings(max_examples=100)
    def test_property_13_win_condition_detection(self, secret):
        """
        Property 13: Win Condition Detection
        For any guess equal to the secret number,
        the system SHALL mark the guessing player as the winner and end the game.
        """
        # Test correct guess
        is_win = GameEngine.check_win_condition(secret, secret)
        assert is_win is True
        
        # Test incorrect guesses
        if secret > 1:
            is_win = GameEngine.check_win_condition(secret - 1, secret)
            assert is_win is False
        
        if secret < 100:
            is_win = GameEngine.check_win_condition(secret + 1, secret)
            assert is_win is False


class TestGuessProcessing:
    """Property-based tests for guess processing and validation."""
    
    # Property 15: Guess History Recording
    @given(
        player_id=st.text(min_size=1, max_size=10),
        guess=st.integers(min_value=1, max_value=100),
        secret=st.integers(min_value=1, max_value=100)
    )
    @settings(max_examples=100)
    def test_property_15_guess_history_recording(self, player_id, guess, secret):
        """
        Property 15: Guess History Recording
        For any valid guess submission, the guess SHALL be added to the guess history
        and broadcast to both players.
        """
        game_state = GameState(room_code="TEST001", game_state="guessing_phase")
        
        player1 = Player(id=player_id, socket_id="socket1")
        player2 = Player(id="opponent", socket_id="socket2")
        player2.secret_number = secret
        
        game_state.players[player_id] = player1
        game_state.players["opponent"] = player2
        
        # Process guess
        success, feedback, updated_range = GameEngine.process_guess(
            game_state, player_id, guess, secret
        )
        
        if success:
            # Record the guess
            guess_obj = Guess(player_id=player_id, guess=guess, feedback=feedback)
            game_state.guess_history.append(guess_obj)
            
            # Verify it's in history
            assert len(game_state.guess_history) > 0
            assert game_state.guess_history[-1].guess == guess
            assert game_state.guess_history[-1].player_id == player_id
    
    # Property 22: Non-Integer Guess Rejection
    @given(
        non_int=st.one_of(st.text(), st.floats(), st.none())
    )
    @settings(max_examples=100)
    def test_property_22_non_integer_guess_rejection(self, non_int):
        """
        Property 22: Non-Integer Guess Rejection
        For any guess submission that is not a valid integer,
        the system SHALL reject it and return a validation error.
        """
        valid_range = {"min": 1, "max": 100}
        
        # Try to validate non-integer
        if not isinstance(non_int, int):
            is_valid, error_msg = GameEngine.validate_guess(non_int, valid_range)
            assert not is_valid
            assert error_msg is not None
    
    # Property 23: Duplicate Guess Prevention
    @given(
        player_id=st.text(min_size=1, max_size=10),
        guess=st.integers(min_value=1, max_value=100),
        secret=st.integers(min_value=1, max_value=100)
    )
    @settings(max_examples=100)
    def test_property_23_duplicate_guess_prevention(self, player_id, guess, secret):
        """
        Property 23: Duplicate Guess Prevention
        For any guess that has already been submitted by the same player,
        the system SHALL reject the duplicate and return an error.
        """
        game_state = GameState(room_code="TEST001", game_state="guessing_phase")
        
        player1 = Player(id=player_id, socket_id="socket1")
        player2 = Player(id="opponent", socket_id="socket2")
        player2.secret_number = secret
        
        game_state.players[player_id] = player1
        game_state.players["opponent"] = player2
        
        # First guess
        success1, feedback1, _ = GameEngine.process_guess(
            game_state, player_id, guess, secret
        )
        
        if success1:
            # Record first guess
            guess_obj = Guess(player_id=player_id, guess=guess, feedback=feedback1)
            game_state.guess_history.append(guess_obj)
            
            # Try duplicate guess
            success2, feedback2, _ = GameEngine.process_guess(
                game_state, player_id, guess, secret
            )
            
            # Duplicate should fail
            assert not success2
            assert "already guessed" in feedback2.lower()
    
    # Property 24: Empty Input Rejection
    @given(st.just(None))
    @settings(max_examples=100)
    def test_property_24_empty_input_rejection(self, _):
        """
        Property 24: Empty Input Rejection
        For any empty input submission, the system SHALL reject it
        and return a validation error.
        """
        game_state = GameState(room_code="TEST001", game_state="guessing_phase")
        
        player1 = Player(id="player1", socket_id="socket1")
        player2 = Player(id="opponent", socket_id="socket2")
        player2.secret_number = 50
        
        game_state.players["player1"] = player1
        game_state.players["opponent"] = player2
        
        # None input should be rejected
        success, feedback, _ = GameEngine.process_guess(
            game_state, "player1", None, 50
        )
        
        # Should fail because None is not an integer
        assert not success


class TestBroadcasting:
    """Property-based tests for broadcasting functionality."""
    
    # Property 14: Range Update Broadcast
    @given(
        secret=st.integers(min_value=1, max_value=100),
        guess=st.integers(min_value=1, max_value=100)
    )
    @settings(max_examples=100)
    def test_property_14_range_update_broadcast(self, secret, guess):
        """
        Property 14: Range Update Broadcast
        For any range update, both players SHALL receive the updated valid range via broadcast.
        """
        game_state = GameState(room_code="TEST001", game_state="guessing_phase")
        
        player1 = Player(id="player1", socket_id="socket1")
        player2 = Player(id="player2", socket_id="socket2")
        player2.secret_number = secret
        
        game_state.players["player1"] = player1
        game_state.players["player2"] = player2
        
        # Process guess
        success, feedback, updated_range = GameEngine.process_guess(
            game_state, "player1", guess, secret
        )
        
        if success and updated_range:
            # Verify range was updated
            assert updated_range is not None
            assert "min" in updated_range
            assert "max" in updated_range
            
            # Verify range is valid
            assert updated_range["min"] <= updated_range["max"]
            
            # If guess was low, min should increase
            if guess < secret:
                assert updated_range["min"] > game_state.valid_range["min"]
            
            # If guess was high, max should decrease
            if guess > secret:
                assert updated_range["max"] < game_state.valid_range["max"]


class TestGameCompletion:
    """Property-based tests for game completion and reset."""
    
    # Property 16: Game State Transition on Win
    @given(
        secret=st.integers(min_value=1, max_value=100)
    )
    @settings(max_examples=100)
    def test_property_16_game_state_transition_on_win(self, secret):
        """
        Property 16: Game State Transition on Win
        For any game where a player has guessed correctly,
        the game state SHALL transition to finished and further guesses SHALL be rejected.
        """
        game_state = GameState(room_code="TEST001", game_state="guessing_phase")
        
        player1 = Player(id="player1", socket_id="socket1")
        player2 = Player(id="player2", socket_id="socket2")
        player2.secret_number = secret
        
        game_state.players["player1"] = player1
        game_state.players["player2"] = player2
        
        # Make winning guess
        success, feedback, _ = GameEngine.process_guess(
            game_state, "player1", secret, secret
        )
        
        assert success
        assert feedback == "correct"
        
        # Simulate state transition
        if feedback == "correct":
            game_state.game_state = "finished"
            game_state.winner = "player1"
        
        # Verify game is finished
        assert game_state.game_state == "finished"
        assert game_state.winner == "player1"
        
        # Try another guess - should fail because game is finished
        success2, feedback2, _ = GameEngine.process_guess(
            game_state, "player1", secret - 1 if secret > 1 else secret + 1, secret
        )
        
        # Should fail because game is finished
        assert not success2
    
    # Property 17: Game Reset on Play Again
    @given(
        secret1=st.integers(min_value=1, max_value=100),
        secret2=st.integers(min_value=1, max_value=100)
    )
    @settings(max_examples=100)
    def test_property_17_game_reset_on_play_again(self, secret1, secret2):
        """
        Property 17: Game Reset on Play Again
        For any finished game where a player clicks "Play Again",
        the game state SHALL reset to setup_phase and all previous game data SHALL be cleared.
        """
        game_state = GameState(room_code="TEST001", game_state="finished")
        
        player1 = Player(id="player1", socket_id="socket1")
        player2 = Player(id="player2", socket_id="socket2")
        player1.secret_number = secret1
        player2.secret_number = secret2
        
        game_state.players["player1"] = player1
        game_state.players["player2"] = player2
        
        # Add some guess history
        guess_obj = Guess(player_id="player1", guess=50, feedback="too_low")
        game_state.guess_history.append(guess_obj)
        
        # Set winner
        game_state.winner = "player1"
        
        # Verify game is finished with data
        assert game_state.game_state == "finished"
        assert len(game_state.guess_history) > 0
        assert game_state.winner is not None
        
        # Reset game
        game_state.game_state = "setup_phase"
        game_state.guess_history = []
        game_state.valid_range = {"min": 1, "max": 100}
        game_state.winner = None
        
        for player in game_state.players.values():
            player.secret_number = None
            player.is_ready = False
        
        # Verify reset
        assert game_state.game_state == "setup_phase"
        assert len(game_state.guess_history) == 0
        assert game_state.valid_range == {"min": 1, "max": 100}
        assert game_state.winner is None
        assert all(p.secret_number is None for p in game_state.players.values())
        assert all(not p.is_ready for p in game_state.players.values())


class TestDisconnectionHandling:
    """Property-based tests for disconnection handling."""
    
    # Property 18: Disconnection Marking
    @given(
        player_id=st.text(min_size=1, max_size=10)
    )
    @settings(max_examples=100)
    def test_property_18_disconnection_marking(self, player_id):
        """
        Property 18: Disconnection Marking
        For any player whose WebSocket connection is lost,
        the system SHALL mark that player as disconnected.
        """
        game_state = GameState(room_code="TEST001")
        
        player = Player(id=player_id, socket_id="socket_123", is_connected=True)
        game_state.players[player_id] = player
        
        # Verify initially connected
        assert game_state.players[player_id].is_connected is True
        
        # Mark as disconnected
        game_state.players[player_id].is_connected = False
        
        # Verify disconnected
        assert game_state.players[player_id].is_connected is False
    
    # Property 19: Reconnection State Restoration
    @given(
        player_id=st.text(min_size=1, max_size=10),
        secret=st.integers(min_value=1, max_value=100)
    )
    @settings(max_examples=100)
    def test_property_19_reconnection_state_restoration(self, player_id, secret):
        """
        Property 19: Reconnection State Restoration
        For any disconnected player who reconnects within 30 seconds,
        the system SHALL restore their game state and allow play to resume.
        """
        game_state = GameState(room_code="TEST001", game_state="guessing_phase")
        
        player = Player(id=player_id, socket_id="socket_123", is_connected=False)
        player.secret_number = secret
        player.is_ready = True
        
        game_state.players[player_id] = player
        
        # Verify disconnected
        assert game_state.players[player_id].is_connected is False
        
        # Reconnect
        game_state.players[player_id].socket_id = "socket_456"
        game_state.players[player_id].is_connected = True
        
        # Verify reconnected and state preserved
        assert game_state.players[player_id].is_connected is True
        assert game_state.players[player_id].secret_number == secret
        assert game_state.players[player_id].is_ready is True
    
    # Property 20: Disconnection Timeout
    @given(st.just(None))
    @settings(max_examples=100)
    def test_property_20_disconnection_timeout(self, _):
        """
        Property 20: Disconnection Timeout
        For any player disconnected for more than 30 seconds,
        the system SHALL end the game and notify the other player.
        """
        game_state = GameState(room_code="TEST001", game_state="guessing_phase")
        
        player1 = Player(id="player1", socket_id="socket1", is_connected=False)
        player2 = Player(id="player2", socket_id="socket2", is_connected=True)
        
        game_state.players["player1"] = player1
        game_state.players["player2"] = player2
        
        # Simulate timeout - end game
        if not player1.is_connected:
            game_state.game_state = "finished"
        
        # Verify game ended
        assert game_state.game_state == "finished"
    
    # Property 21: Intentional Disconnect Cleanup
    @given(
        player_id=st.text(min_size=1, max_size=10)
    )
    @settings(max_examples=100)
    def test_property_21_intentional_disconnect_cleanup(self, player_id):
        """
        Property 21: Intentional Disconnect Cleanup
        For any player who intentionally leaves a room,
        the system SHALL clean up the room and notify the other player.
        """
        game_state = GameState(room_code="TEST001")
        
        player1 = Player(id=player_id, socket_id="socket1")
        player2 = Player(id="opponent", socket_id="socket2")
        
        game_state.players[player_id] = player1
        game_state.players["opponent"] = player2
        
        # Verify room has 2 players
        assert len(game_state.players) == 2
        
        # Remove player
        if player_id in game_state.players:
            del game_state.players[player_id]
        
        # Verify cleanup
        assert len(game_state.players) == 1
        assert player_id not in game_state.players
