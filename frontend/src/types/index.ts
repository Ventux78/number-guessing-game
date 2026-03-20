/**
 * Type definitions for the Number Guessing Game
 */

export interface Player {
  id: string
  socketId: string
  secretNumber: number | null
  isReady: boolean
  isConnected: boolean
  lastHeartbeat: number
}

export interface Guess {
  playerId: string
  guess: number
  timestamp: number
  feedback?: 'too_low' | 'too_high' | 'correct'
}

export interface GameState {
  roomCode: string
  players: Record<string, Player>
  gameState: 'waiting_for_players' | 'setup_phase' | 'guessing_phase' | 'finished'
  guessHistory: Guess[]
  validRange: {
    min: number
    max: number
  }
  winner: string | null
  createdAt: number
  lastActivity: number
}
