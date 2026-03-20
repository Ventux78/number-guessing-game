"""Game engine for number guessing game logic."""
from typing import Dict, Tuple, Optional
from models import GameState, Guess


class GameEngine:
    """Handles all game logic including validation, range updates, and win detection."""
    
    @staticmethod
    def validate_guess(guess: int, valid_range: Dict[str, int]) -> Tuple[bool, Optional[str]]:
        """
        Validate a guess against the current valid range.
        
        Args:
            guess: The guess value to validate
            valid_range: Dict with 'min' and 'max' keys
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not isinstance(guess, int):
            return False, "Guess must be a valid integer"
        
        if guess < valid_range["min"] or guess > valid_range["max"]:
            return False, f"Guess must be between {valid_range['min']} and {valid_range['max']}"
        
        return True, None
    
    @staticmethod
    def calculate_range_update(
        guess: int,
        secret_number: int,
        current_range: Dict[str, int]
    ) -> Dict[str, int]:
        """
        Calculate the updated valid range based on a guess.
        
        Args:
            guess: The guess value
            secret_number: The secret number to guess
            current_range: Current valid range
            
        Returns:
            Updated range dict with 'min' and 'max' keys
        """
        new_range = current_range.copy()
        
        if guess < secret_number:
            # Guess is too low, update minimum
            new_range["min"] = max(new_range["min"], guess + 1)
        elif guess > secret_number:
            # Guess is too high, update maximum
            new_range["max"] = min(new_range["max"], guess - 1)
        
        return new_range
    
    @staticmethod
    def check_win_condition(guess: int, secret_number: int) -> bool:
        """
        Check if the guess equals the secret number.
        
        Args:
            guess: The guess value
            secret_number: The secret number
            
        Returns:
            True if guess equals secret number, False otherwise
        """
        return guess == secret_number
    
    @staticmethod
    def process_guess(
        game_state: GameState,
        player_id: str,
        guess: int,
        opponent_secret: int
    ) -> Tuple[bool, str, Optional[Dict]]:
        """
        Process a guess and update game state.
        
        Args:
            game_state: Current game state
            player_id: ID of the player making the guess
            guess: The guess value
            opponent_secret: The opponent's secret number
            
        Returns:
            Tuple of (success, feedback, updated_range or None)
        """
        # Check if game is finished
        if game_state.game_state == "finished":
            return False, "Game is already finished", None
        
        # Validate guess is in range
        is_valid, error_msg = GameEngine.validate_guess(guess, game_state.valid_range)
        if not is_valid:
            return False, error_msg, None
        
        # Check for duplicate guess
        if any(g.guess == guess and g.player_id == player_id for g in game_state.guess_history):
            return False, "You already guessed this number", None
        
        # Check win condition
        if GameEngine.check_win_condition(guess, opponent_secret):
            return True, "correct", game_state.valid_range
        
        # Update range
        new_range = GameEngine.calculate_range_update(guess, opponent_secret, game_state.valid_range)
        
        # Determine feedback
        if guess < opponent_secret:
            feedback = "too_low"
        else:
            feedback = "too_high"
        
        return True, feedback, new_range