/**
 * SetupScreen component for secret number submission
 */
import { useState } from 'react'

interface SetupScreenProps {
  secretNumber: string
  onSecretNumberChange: (num: string) => void
  onSubmitNumber: () => void
  error: string
}

export const SetupScreen = ({ secretNumber, onSecretNumberChange, onSubmitNumber, error }: SetupScreenProps) => {
  const [isWaiting, setIsWaiting] = useState(false)

  const handleSubmit = () => {
    const num = parseInt(secretNumber, 10)

    if (!secretNumber.trim()) {
      return
    }

    if (isNaN(num) || num < 1 || num > 100) {
      return
    }

    onSubmitNumber()
    setIsWaiting(true)
  }

  return (
    <div className="setup-screen">
      <h2>Choose Your Secret Number</h2>
      <p>Pick a number between 1 and 100 for your opponent to guess</p>
      <div className="setup-form">
        <input
          type="number"
          min="1"
          max="100"
          placeholder="Enter number (1-100)"
          value={secretNumber}
          onChange={(e) => {
            onSecretNumberChange(e.target.value)
          }}
          disabled={isWaiting}
        />
        <button onClick={handleSubmit} disabled={isWaiting}>
          {isWaiting ? 'Waiting for opponent...' : 'Confirm'}
        </button>
      </div>
      {error && <div className="error">{error}</div>}
    </div>
  )
}
