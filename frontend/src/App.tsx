import { useState } from 'react'
import './App.css'

type GameScreen = 'room' | 'setup' | 'game'

function App() {
  const [currentScreen, setCurrentScreen] = useState<GameScreen>('room')
  const [roomCode, setRoomCode] = useState('')
  const [secretNumber, setSecretNumber] = useState('')
  const [guess, setGuess] = useState('')
  const [validRange, setValidRange] = useState({ min: 1, max: 100 })
  const [guessHistory, setGuessHistory] = useState<Array<{ player: string; guess: number; time: string }>>([])
  const [error, setError] = useState('')
  const [currentTurn, setCurrentTurn] = useState(1)

  const handleCreateRoom = () => {
    const code = Math.random().toString(36).substring(2, 8).toUpperCase()
    setRoomCode(code)
    setError('')
  }

  const handleJoinRoom = () => {
    if (!roomCode.trim()) {
      setError('Room code cannot be empty')
      return
    }
    setCurrentScreen('setup')
    setError('')
  }

  const handleSubmitNumber = () => {
    const num = parseInt(secretNumber, 10)
    if (!secretNumber.trim()) {
      setError('Number cannot be empty')
      return
    }
    if (isNaN(num) || num < 1 || num > 100) {
      setError('Number must be between 1 and 100')
      return
    }
    setCurrentScreen('game')
    setError('')
  }

  const handleSubmitGuess = () => {
    const num = parseInt(guess, 10)
    if (!guess.trim()) {
      setError('Guess cannot be empty')
      return
    }
    if (isNaN(num)) {
      setError('Guess must be a valid integer')
      return
    }
    if (num < validRange.min || num > validRange.max) {
      setError(`Guess must be between ${validRange.min} and ${validRange.max}`)
      return
    }
    
    const now = new Date().toLocaleTimeString()
    setGuessHistory([...guessHistory, { player: currentTurn === 1 ? 'You' : 'Opponent', guess: num, time: now }])
    setGuess('')
    setError('')
    
    // Sırayı değiştir
    setCurrentTurn(currentTurn === 1 ? 2 : 1)
  }

  const handleReset = () => {
    setCurrentScreen('room')
    setRoomCode('')
    setSecretNumber('')
    setGuess('')
    setGuessHistory([])
    setError('')
    setValidRange({ min: 1, max: 100 })
    setCurrentTurn(1)
  }

  return (
    <div className="app-container">
      {currentScreen === 'room' && (
        <div className="screen room-screen">
          <h1>🎮 Number Guessing Game</h1>
          <p className="subtitle">Challenge a friend to guess your secret number!</p>
          
          <div className="room-actions">
            <button className="btn btn-primary" onClick={handleCreateRoom}>
              ➕ Create Room
            </button>
            {roomCode && (
              <div className="room-code-display">
                <p>Your Room Code:</p>
                <div className="code">{roomCode}</div>
                <p className="hint">Share this code with your friend</p>
              </div>
            )}
            
            <div className="divider">OR</div>
            
            <div className="join-section">
              <input
                type="text"
                placeholder="Enter room code"
                value={roomCode}
                onChange={(e) => {
                  setRoomCode(e.target.value.toUpperCase())
                  setError('')
                }}
                className="input"
              />
              <button className="btn btn-secondary" onClick={handleJoinRoom}>
                🚪 Join Room
              </button>
            </div>
          </div>
          {error && <div className="error-message">{error}</div>}
        </div>
      )}

      {currentScreen === 'setup' && (
        <div className="screen setup-screen">
          <h2>Choose Your Secret Number</h2>
          <p className="subtitle">Pick a number between 1 and 100 for your opponent to guess</p>
          
          <div className="setup-form">
            <input
              type="number"
              min="1"
              max="100"
              placeholder="Enter number (1-100)"
              value={secretNumber}
              onChange={(e) => {
                setSecretNumber(e.target.value)
                setError('')
              }}
              className="input"
            />
            <button className="btn btn-primary" onClick={handleSubmitNumber}>
              ✓ Confirm Number
            </button>
          </div>
          <p className="waiting-message">⏳ Waiting for opponent to choose their number...</p>
          {error && <div className="error-message">{error}</div>}
        </div>
      )}

      {currentScreen === 'game' && (
        <div className="screen game-screen">
          <h2>🎯 Guessing Game</h2>
          
          <div className="game-info">
            <div className="range-display">
              <p className="range-label">Valid Range:</p>
              <p className="range-value">{validRange.min} — {validRange.max}</p>
            </div>
          </div>

          <div className="guess-input-section">
            <input
              type="number"
              placeholder="Enter your guess"
              value={guess}
              onChange={(e) => {
                setGuess(e.target.value)
                setError('')
              }}
              className="input"
            />
            <button className="btn btn-primary" onClick={handleSubmitGuess}>
              📤 Submit Guess
            </button>
          </div>

          {error && <div className="error-message">{error}</div>}

          <div className="guess-history-section">
            <h3>📋 Guess History</h3>
            <div className="history-list">
              {guessHistory.length === 0 ? (
                <p className="empty-state">No guesses yet. Make your first guess!</p>
              ) : (
                guessHistory.map((g, idx) => (
                  <div key={idx} className="history-item">
                    <span className="player-name">{g.player}</span>
                    <span className="guess-value">{g.guess}</span>
                    <span className="timestamp">{g.time}</span>
                  </div>
                ))
              )}
            </div>
          </div>

          <button className="btn btn-secondary" onClick={handleReset}>
            🏠 Back to Room
          </button>
        </div>
      )}
    </div>
  )
}

export default App
