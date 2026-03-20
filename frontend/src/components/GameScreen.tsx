/**
 * GameScreen component for the main guessing game
 */
import { useState } from 'react'
import { Guess } from '../types'

interface GameScreenProps {
  validRange: { min: number; max: number }
  guessHistory: Guess[]
  guess: string
  onGuessChange: (guess: string) => void
  onGuessSubmitted: () => void
  error: string
}

export const GameScreen = ({
  validRange,
  guessHistory,
  guess,
  onGuessChange,
  onGuessSubmitted,
  error,
}: GameScreenProps) => {

  return (
    <div className="game-screen">
      <h2>Guessing Game</h2>
      <div className="game-info">
        <div className="range-display">
          <p>Valid Range: {validRange.min} - {validRange.max}</p>
        </div>
      </div>

      <div className="guess-input">
        <input
          type="number"
          placeholder="Enter your guess"
          value={guess}
          onChange={(e) => {
            onGuessChange(e.target.value)
          }}
        />
        <button onClick={onGuessSubmitted}>
          Submit Guess
        </button>
      </div>

      {error && <div className="error">{error}</div>}

      <div className="guess-history">
        <h3>Guess History</h3>
        <div className="history-list">
          {guessHistory.length === 0 ? (
            <p>No guesses yet</p>
          ) : (
            guessHistory.map((g, idx) => (
              <div key={idx} className="history-item">
                <span className="player">{g.playerId}</span>
                <span className="guess">{g.guess}</span>
                <span className="feedback">{g.feedback}</span>
                <span className="timestamp">{new Date(g.timestamp).toLocaleTimeString()}</span>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}
