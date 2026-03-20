# Design Document: Real-Time Number Guessing Game

## Overview

This document describes the architecture and implementation strategy for a real-time two-player number guessing game. The system uses WebSocket communication via Socket.IO to enable instant synchronization between players, with a Node.js/Express backend managing game state and a React frontend providing a mobile-optimized interface.

The core design principle is to maintain authoritative game state on the server while providing responsive UI feedback on the client. All game logic (validation, range updates, win detection) executes server-side to prevent cheating.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Layer (React)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Room Screen  │  │ Setup Screen │  │ Game Screen  │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│         │                 │                  │               │
│         └─────────────────┴──────────────────┘               │
│                    Socket.IO Client                          │
└─────────────────────────────────────────────────────────────┘
                            │
                    WebSocket Connection
                            │
┌─────────────────────────────────────────────────────────────┐
│                  Server Layer (Node.js)                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Socket.IO Server                        │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │  Room Manager                                 │  │   │
│  │  │  - Create/Join rooms                          │  │   │
│  │  │  - Manage player connections                  │  │   │
│  │  │  - Handle disconnections                      │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │  Game Engine                                  │  │   │
│  │  │  - Validate guesses                           │  │   │
│  │  │  - Calculate range updates                    │  │   │
│  │  │  - Detect win conditions                      │  │   │
│  │  │  - Manage game state transitions              │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │  Game State Store                             │  │   │
│  │  │  - Per-room game state                        │  │   │
│  │  │  - Player data (secret numbers, guesses)      │  │   │
│  │  │  - Range tracking                             │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Communication Flow

1. **Room Creation**: Player 1 connects → Server generates room code → Client displays code
2. **Room Join**: Player 2 enters code → Server validates → Adds to room → Broadcasts to both players
3. **Setup Phase**: Both players submit secret numbers → Server validates → Transitions to guessing phase
4. **Guessing Phase**: Player submits guess → Server validates → Updates range → Broadcasts to both → Checks win condition
5. **Game End**: Winner detected → Server broadcasts result → Both players see outcome

## Components and Interfaces

### Backend Components

#### 1. Socket.IO Server Setup
- Initialize Socket.IO with CORS configuration
- Handle connection/disconnection events
- Manage socket namespaces for rooms

#### 2. Room Manager
```
RoomManager:
  - createRoom() → roomCode
  - joinRoom(roomCode, playerId) → success/error
  - getRoom(roomCode) → Room object
  - deleteRoom(roomCode) → void
  - handlePlayerDisconnect(roomCode, playerId) → void
```

#### 3. Game Engine
```
GameEngine:
  - validateGuess(guess, validRange) → valid/invalid
  - calculateRangeUpdate(guess, secretNumber, currentRange) → newRange
  - checkWinCondition(guess, secretNumber) → boolean
  - processGuess(roomCode, playerId, guess) → result
```

#### 4. Game State Store
```
GameState (per room):
  - roomCode: string
  - players: [Player1, Player2]
  - gameState: "waiting" | "setup" | "guessing" | "finished"
  - secretNumbers: { playerId: number }
  - guessHistory: [{ playerId, guess, timestamp }]
  - validRange: { min, max }
  - winner: playerId | null
```

### Frontend Components

#### 1. RoomScreen
- Input field for room code
- "Create Room" button
- "Join Room" button
- Display created room code

#### 2. SetupScreen
- Display "Waiting for opponent" if only one player
- Input field for secret number (1-100)
- "Confirm" button
- Validation messages

#### 3. GameScreen
- Display current valid range [min, max]
- Input field for guess
- "Submit Guess" button
- Guess history (scrollable list)
- Game status (playing/won/opponent won)
- "Play Again" button (when game finished)

#### 4. Socket.IO Client
- Emit events: "create_room", "join_room", "submit_number", "submit_guess"
- Listen events: "room_created", "player_joined", "game_started", "guess_result", "game_won", "opponent_disconnected"

## Data Models

### Room Object
```typescript
{
  roomCode: string,
  players: {
    player1: {
      id: string,
      socketId: string,
      secretNumber: number | null,
      isReady: boolean,
      isConnected: boolean,
      lastHeartbeat: timestamp
    },
    player2: {
      id: string,
      socketId: string,
      secretNumber: number | null,
      isReady: boolean,
      isConnected: boolean,
      lastHeartbeat: timestamp
    }
  },
  gameState: "waiting_for_players" | "setup_phase" | "guessing_phase" | "finished",
  guessHistory: [
    {
      playerId: string,
      guess: number,
      timestamp: number,
      feedback: "too_low" | "too_high" | "correct"
    }
  ],
  validRange: {
    min: number,
    max: number
  },
  winner: string | null,
  createdAt: timestamp,
  lastActivity: timestamp
}
```

### Player Object
```typescript
{
  id: string,
  socketId: string,
  secretNumber: number | null,
  isReady: boolean,
  isConnected: boolean,
  lastHeartbeat: timestamp
}
```

### Guess Object
```typescript
{
  playerId: string,
  guess: number,
  timestamp: number,
  feedback: "too_low" | "too_high" | "correct"
}
```

## Correctness Properties

A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.


### Property 1: Room Code Uniqueness
*For any* sequence of room creation requests, each generated room code SHALL be unique and not previously generated.
**Validates: Requirements 1.1**

### Property 2: Room Join Validation
*For any* room with exactly one player, a second player SHALL successfully join the room when providing the correct room code.
**Validates: Requirements 1.2**

### Property 3: Game State Transition on Second Join
*For any* room in waiting_for_players state, when a second player joins, the game state SHALL transition to setup_phase.
**Validates: Requirements 1.3**

### Property 4: Invalid Room Code Rejection
*For any* join attempt with a non-existent room code, the system SHALL reject the join and return an error.
**Validates: Requirements 1.4**

### Property 5: Room Capacity Enforcement
*For any* room with two players, attempting to add a third player SHALL fail and return an error.
**Validates: Requirements 1.5**

### Property 6: Secret Number Storage
*For any* valid secret number (1-100) submitted by a player, the system SHALL store it server-side without transmitting it to the opponent.
**Validates: Requirements 2.2, 2.5**

### Property 7: Secret Number Validation
*For any* secret number submission outside the range 1-100, the system SHALL reject it and return a validation error.
**Validates: Requirements 2.3**

### Property 8: Setup to Guessing Transition
*For any* room where both players have submitted valid secret numbers, the game state SHALL transition to guessing_phase.
**Validates: Requirements 2.4**

### Property 9: Initial Range Initialization
*For any* game entering guessing_phase, the valid range SHALL be initialized to [1, 100].
**Validates: Requirements 3.1**

### Property 10: Guess Range Validation
*For any* guess submission, if the guess is outside the current valid range, the system SHALL reject it and return an error.
**Validates: Requirements 3.2, 3.3**

### Property 11: Range Update on Low Guess
*For any* guess that is less than the secret number, the valid range upper bound SHALL be updated to the guess value.
**Validates: Requirements 3.4**

### Property 12: Range Update on High Guess
*For any* guess that is greater than the secret number, the valid range lower bound SHALL be updated to the guess value.
**Validates: Requirements 3.5**

### Property 13: Win Condition Detection
*For any* guess equal to the secret number, the system SHALL mark the guessing player as the winner and end the game.
**Validates: Requirements 3.6, 4.1**

### Property 14: Range Update Broadcast
*For any* range update, both players SHALL receive the updated valid range via broadcast.
**Validates: Requirements 3.7**

### Property 15: Guess History Recording
*For any* valid guess submission, the guess SHALL be added to the guess history and broadcast to both players.
**Validates: Requirements 3.8**

### Property 16: Game State Transition on Win
*For any* game where a player has guessed correctly, the game state SHALL transition to finished and further guesses SHALL be rejected.
**Validates: Requirements 4.3**

### Property 17: Game Reset on Play Again
*For any* finished game where a player clicks "Play Again", the game state SHALL reset to setup_phase and all previous game data SHALL be cleared.
**Validates: Requirements 4.5**

### Property 18: Disconnection Marking
*For any* player whose WebSocket connection is lost, the system SHALL mark that player as disconnected.
**Validates: Requirements 6.1**

### Property 19: Reconnection State Restoration
*For any* disconnected player who reconnects within 30 seconds, the system SHALL restore their game state and allow play to resume.
**Validates: Requirements 6.3**

### Property 20: Disconnection Timeout
*For any* player disconnected for more than 30 seconds, the system SHALL end the game and notify the other player.
**Validates: Requirements 6.4**

### Property 21: Intentional Disconnect Cleanup
*For any* player who intentionally leaves a room, the system SHALL clean up the room and notify the other player.
**Validates: Requirements 6.5**

### Property 22: Non-Integer Guess Rejection
*For any* guess submission that is not a valid integer, the system SHALL reject it and return a validation error.
**Validates: Requirements 7.1**

### Property 23: Duplicate Guess Prevention
*For any* guess that has already been submitted by the same player, the system SHALL reject the duplicate and return an error.
**Validates: Requirements 7.2**

### Property 24: Empty Input Rejection
*For any* empty input submission, the system SHALL reject it and return a validation error.
**Validates: Requirements 7.4**

## Error Handling

### Validation Errors
- Invalid room codes: Return "Room not found" error
- Invalid secret numbers: Return "Number must be between 1 and 100" error
- Invalid guesses: Return "Guess must be a valid integer" error
- Out-of-range guesses: Return "Guess must be between [min] and [max]" error
- Duplicate guesses: Return "You already guessed this number" error
- Empty inputs: Return "Input cannot be empty" error

### Connection Errors
- WebSocket disconnection: Mark player as disconnected, start 30-second timeout
- Reconnection within timeout: Restore game state and resume
- Reconnection timeout: End game and notify other player
- Room full: Return "Room is full" error

### State Errors
- Guess submitted in wrong game state: Return "Game is not in guessing phase" error
- Secret number submitted in wrong game state: Return "Game is not in setup phase" error
- Play again in wrong game state: Return "Game must be finished to play again" error

## Testing Strategy

### Unit Testing
- Test room creation generates unique codes
- Test room join validation (valid/invalid codes, room capacity)
- Test secret number validation (range, duplicates, empty)
- Test guess validation (range, duplicates, empty, non-integer)
- Test range update calculations (low guess, high guess, edge cases)
- Test win condition detection
- Test game state transitions
- Test disconnection handling and timeouts
- Test error message generation

### Property-Based Testing

Each correctness property will be implemented as a property-based test using a PBT library (e.g., fast-check for JavaScript):

**Property Test Configuration**:
- Minimum 100 iterations per property test
- Each test tagged with: `Feature: number-guessing-game, Property N: [property_text]`
- Tests will use generators for:
  - Random room codes
  - Random player IDs
  - Random secret numbers (1-100)
  - Random guesses (including out-of-range values)
  - Random game state sequences

**Example Property Test Structure**:
```javascript
// Feature: number-guessing-game, Property 11: Range Update on Low Guess
test('Property 11: Range Update on Low Guess', () => {
  fc.assert(
    fc.property(
      fc.integer({ min: 1, max: 100 }),  // secret number
      fc.integer({ min: 1, max: 99 }),   // guess less than secret
      (secret, guess) => {
        const result = calculateRangeUpdate(guess, secret, { min: 1, max: 100 });
        return result.max === guess;  // upper bound should be guess
      }
    ),
    { numRuns: 100 }
  );
});
```

### Testing Approach
- Unit tests verify specific examples and edge cases
- Property tests verify universal properties across all inputs
- Together they provide comprehensive coverage
- Tests will be co-located with implementation code
- All tests must pass before task completion

