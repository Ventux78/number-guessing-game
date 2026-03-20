import { useState, useEffect } from 'react'
import { io, Socket } from 'socket.io-client'
import './App.css'

type GameScreen = 'room' | 'setup' | 'game'

function App() {
  const [socket, setSocket] = useState<Socket | null>(null)
  const [currentScreen, setCurrentScreen] = useState<GameScreen>('room')
  const [roomCode, setRoomCode] = useState('')
  const [secretNumber, setSecretNumber] = useState('')
  const [guess, setGuess] = useState('')
  const [validRange, setValidRange] = useState({ min: 1, max: 100 })
  const [guessHistory, setGuessHistory] = useState<Array<{ player: string; guess: number; time: string }>>([])
  const [error, setError] = useState('')
  const [isConnected, setIsConnected] = useState(false)

  // Initialize Socket.IO connection
  useEffect(() => {
    const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:5000'
    const newSocket = io(backendUrl, {
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: 5
    })

    newSocket.on('connect', () => {
      setIsConnected(true)
      setError('')
    })

    newSocket.on('disconnect', () => {
      setIsConnected(false)
    })

    newSocket.on('error', (err) => {
      setError(`Connection error: ${err}`)
    })

    setSocket(newSocket)

    return () => {
      newSocket.disconnect()
    }
  }, [])

  const handleCreateRoom = () => {
    if (!socket || !isConnected) {
      setError('Not connected to server')
      return
    }
    socket.emit('create_room', {}, (response: any) => {
      if (response.success) {
        setRoomCode(response.room_code)
        setError('')
      } else {
        setError(response.error || 'Failed to create room')
      }
    })
  }

  const handleJoinRoom = () => {
    if (!roomCode.trim()) {
      setError('Room code cannot be empty')
      return
    }
    if (!socket || !isConnected) {
      setError('Not connected to server')
      return
    }
    socket.emit('join_room', { room_code: roomCode }, (response: any) => {
      if (response.success) {
        setCurrentScreen('setup')
        setError('')
      } else {
        setError(response.error || 'Failed to join room')
      }
    })
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
    if (!socket || !isConnected) {
      setError('Not connected to server')
      return
    }
    socket.emit('submit_number', { secret_number: num }, (response: any) => {
      if (response.success) {
        setCurrentScreen('game')
        setError('')
      } else {
        setError(response.error || 'Failed to submit number')
      }
    })
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
    if (!socket || !isConnected) {
      setError('Not connected to server')
      return
    }
    socket.emit('submit_guess', { guess: num }, (response: any) => {
      if (response.success) {
        const now = new Date().toLocaleTimeString()
        setGuessHistory([...guessHistory, { player: 'You', guess: num, time: now }])
        setGuess('')
        setError('')
      } else {
        setError(response.error || 'Failed to submit guess')
      }
    })
  }

  const handleReset = () => {
    setCurrentScreen('room')
    setRoomCode('')
    setSecretNumber('')
    setGuess('')
    setGuessHistory([])
    setError('')
    setValidRange({ min: 1, max: 100 })
  }

  return (
    <div className="app-container">
      {!isConnected && (
        <div className="connection-warning">
          ⚠️ Connecting to server...
        </div>
      )}
      
      {currentScreen === 'room' && (
        <div className="screen room-screen">
          <h1>🎮 Number Guessing Game</h1>
          <p className="subtitle">Challenge a friend to guess your secret number!</p>
          
          <div className="room-actions">
            <button className="btn btn-primary" onClick={handleCreateRoom} disabled={!isConnected}>
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
              <button className="btn btn-secondary" onClick={handleJoinRoom} disabled={!isConnected}>
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
            <button className="btn btn-primary" onClick={handleSubmitNumber} disabled={!isConnected}>
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
            <button className="btn btn-primary" onClick={handleSubmitGuess} disabled={!isConnected}>
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
