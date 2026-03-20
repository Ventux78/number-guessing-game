# Implementation Plan: Real-Time Number Guessing Game

## Overview

This implementation plan breaks down the feature into discrete coding tasks. The backend uses Python/Flask with python-socketio for real-time communication, while the frontend uses React with TypeScript for type safety and mobile optimization. Tasks are ordered to build incrementally, with testing integrated throughout.

## Tasks

- [x] 1. Set up project structure and dependencies
  - Create backend directory structure (app.py, config.py, models.py, handlers.py)
  - Create frontend directory structure (src/components, src/hooks, src/types)
  - Install backend dependencies: Flask, python-socketio, python-engineio, python-dotenv
  - Install frontend dependencies: React, TypeScript, Socket.IO client, Vite
  - Create .gitignore and README with setup instructions
  - _Requirements: 1.1, 1.2, 1.3_

- [x] 2. Implement backend Socket.IO server and room management
  - Set up Flask app with Socket.IO integration and CORS configuration
  - Implement RoomManager class with createRoom(), joinRoom(), getRoom(), deleteRoom() methods
  - Implement room code generation (6-character alphanumeric)
  - Implement Socket.IO event handlers for "connect", "disconnect", "create_room", "join_room"
  - Implement player connection tracking and room state management
  - _Requirements: 1.1, 1.2, 1.3, 1.6_

- [x] 2.1 Write property tests for room management
  - **Property 1: Room Code Uniqueness**
  - **Property 2: Room Join Validation**
  - **Property 3: Game State Transition on Second Join**
  - **Property 4: Invalid Room Code Rejection**
  - **Property 5: Room Capacity Enforcement**
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

- [x] 3. Implement backend game engine and state management
  - Create GameState class to store per-room game data (players, secret numbers, guesses, range, state)
  - Implement GameEngine class with validateGuess(), calculateRangeUpdate(), checkWinCondition() methods
  - Implement game state transitions (waiting → setup → guessing → finished)
  - Implement secret number storage and validation (1-100 range)
  - _Requirements: 2.2, 2.3, 2.4, 3.1, 3.2, 3.3_

- [ ] 3.1 Write property tests for game engine
  - **Property 6: Secret Number Storage**
  - **Property 7: Secret Number Validation**
  - **Property 8: Setup to Guessing Transition**
  - **Property 9: Initial Range Initialization**
  - **Property 10: Guess Range Validation**
  - _Requirements: 2.2, 2.3, 2.4, 3.1, 3.2, 3.3_

- [x] 4. Implement backend guess processing and range updates
  - Implement guess validation (integer, within range, not duplicate)
  - Implement range update logic (update min/max based on guess vs secret)
  - Implement win condition detection (guess equals secret)
  - Implement guess history recording with timestamps
  - Implement Socket.IO event handlers for "submit_number", "submit_guess"
  - _Requirements: 3.2, 3.3, 3.4, 3.5, 3.6, 3.8_

- [x] 4.1 Write property tests for guess processing
  - **Property 11: Range Update on Low Guess**
  - **Property 12: Range Update on High Guess**
  - **Property 13: Win Condition Detection**
  - **Property 15: Guess History Recording**
  - **Property 22: Non-Integer Guess Rejection**
  - **Property 23: Duplicate Guess Prevention**
  - **Property 24: Empty Input Rejection**
  - _Requirements: 3.2, 3.3, 3.4, 3.5, 3.6, 3.8, 7.1, 7.2, 7.4_

- [x] 5. Implement backend real-time broadcasting
  - Implement broadcast of range updates to both players
  - Implement broadcast of guess results to both players
  - Implement broadcast of game state changes
  - Implement broadcast of win notifications
  - Ensure all broadcasts use Socket.IO rooms for targeted delivery
  - _Requirements: 3.7, 3.8, 4.1, 5.1, 5.2, 5.3_

- [x] 5.1 Write property tests for broadcasting
  - **Property 14: Range Update Broadcast**
  - **Property 15: Guess History Recording**
  - _Requirements: 3.7, 3.8_

- [x] 6. Implement backend game completion and reset
  - Implement game state transition to "finished" on win
  - Implement prevention of further guesses after game ends
  - Implement "play again" functionality that resets game state
  - Implement clearing of previous game data while keeping room intact
  - _Requirements: 4.3, 4.5_

- [x] 6.1 Write property tests for game completion
  - **Property 16: Game State Transition on Win**
  - **Property 17: Game Reset on Play Again**
  - _Requirements: 4.3, 4.5_

- [x] 7. Implement backend disconnection handling
  - Implement player disconnection detection
  - Implement marking of disconnected players
  - Implement 30-second reconnection timeout
  - Implement game end on timeout expiration
  - Implement cleanup of abandoned rooms
  - _Requirements: 6.1, 6.3, 6.4, 6.5_

- [x] 7.1 Write property tests for disconnection handling
  - **Property 18: Disconnection Marking**
  - **Property 19: Reconnection State Restoration**
  - **Property 20: Disconnection Timeout**
  - **Property 21: Intentional Disconnect Cleanup**
  - _Requirements: 6.1, 6.3, 6.4, 6.5_

- [x] 8. Checkpoint - Backend implementation complete
  - Ensure all backend tests pass
  - Verify Socket.IO server starts without errors
  - Test manual room creation and joining via Socket.IO client
  - Ask the user if questions arise

- [x] 9. Implement frontend project setup and routing
  - Set up React app with TypeScript and Vite
  - Create main App component with routing structure
  - Create RoomScreen, SetupScreen, GameScreen components (stubs)
  - Implement Socket.IO client connection with error handling
  - Create custom hooks for Socket.IO event management
  - _Requirements: 1.1, 1.2, 8.1, 8.2_

- [x] 10. Implement frontend RoomScreen component
  - Create input field for room code
  - Implement "Create Room" button that emits "create_room" event
  - Implement "Join Room" button that emits "join_room" event with room code
  - Display created room code to user
  - Display error messages for invalid room codes or full rooms
  - Implement mobile-responsive layout
  - _Requirements: 1.1, 1.2, 8.1, 8.2, 8.3_

- [x] 11. Implement frontend SetupScreen component
  - Create input field for secret number (1-100)
  - Implement "Confirm" button that emits "submit_number" event
  - Display validation errors for invalid numbers
  - Display "Waiting for opponent" message when only one player ready
  - Implement mobile-responsive layout
  - _Requirements: 2.2, 2.3, 8.1, 8.2, 8.3_

- [x] 12. Implement frontend GameScreen component
  - Display current valid range [min, max]
  - Create input field for guess submission
  - Implement "Submit Guess" button that emits "submit_guess" event
  - Display guess history with player names and timestamps
  - Display game status (playing/won/opponent won)
  - Display "Play Again" button when game finished
  - Implement mobile-responsive layout with scrollable guess history
  - _Requirements: 3.1, 3.2, 3.7, 3.8, 4.1, 8.1, 8.2, 8.3, 9.1, 9.2, 9.3_

- [x] 13. Implement frontend Socket.IO event listeners
  - Listen for "room_created" and display room code
  - Listen for "player_joined" and transition to setup screen
  - Listen for "game_started" and transition to game screen
  - Listen for "guess_result" and update range display
  - Listen for "game_won" and display winner
  - Listen for "opponent_disconnected" and display message
  - Listen for "error" and display error messages
  - _Requirements: 1.3, 3.7, 3.8, 4.1, 5.1, 5.2, 5.3_

- [x] 14. Implement frontend input validation and error handling
  - Validate room code input (non-empty, alphanumeric)
  - Validate secret number input (integer, 1-100)
  - Validate guess input (integer, non-empty, within range)
  - Display clear error messages for each validation failure
  - Prevent submission of invalid inputs
  - _Requirements: 7.1, 7.2, 7.3, 7.4_

- [x] 15. Implement frontend mobile responsiveness
  - Ensure all screens adapt to mobile viewport (320px+)
  - Ensure buttons are touch-friendly (minimum 44x44 pixels)
  - Implement responsive font sizes and spacing
  - Test layout on portrait and landscape orientations
  - Ensure no horizontal scrolling on mobile
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [x] 16. Implement frontend disconnection handling
  - Display "Waiting for opponent to reconnect" message on opponent disconnect
  - Implement automatic reconnection attempts
  - Restore game state after reconnection
  - Display "Opponent disconnected" message after 30-second timeout
  - _Requirements: 6.1, 6.3, 6.4, 6.5_

- [x] 17. Checkpoint - Frontend implementation complete
  - Ensure all frontend tests pass
  - Test room creation and joining flow
  - Test secret number submission
  - Test guess submission and range updates
  - Test win condition and game reset
  - Test disconnection and reconnection
  - Ask the user if questions arise

- [x] 18. Integration testing and end-to-end validation
  - Test complete game flow: create room → join → setup → guessing → win
  - Test multiple concurrent games in different rooms
  - Test disconnection and reconnection scenarios
  - Test edge cases: duplicate guesses, out-of-range guesses, invalid inputs
  - Test mobile responsiveness on actual devices or emulators
  - _Requirements: 1.1, 1.2, 1.3, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 4.1, 4.3, 4.5, 6.1, 6.3, 6.4, 6.5, 7.1, 7.2, 7.3, 7.4_

- [x] 19. Final checkpoint - All tests pass and game is playable
  - Ensure all unit tests pass
  - Ensure all property-based tests pass
  - Ensure integration tests pass
  - Verify game is playable end-to-end
  - Ask the user if questions arise

## Notes

- Tasks marked with `*` are optional property-based tests and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
- All code should follow PEP 8 (Python) and ESLint (TypeScript) standards
- Use type hints in Python and TypeScript for better code quality

