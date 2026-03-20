/**
 * RoomScreen component for creating or joining a game room
 */

interface RoomScreenProps {
  roomCode: string
  onCreateRoom: () => void
  onJoinRoom: () => void
  onRoomCodeChange: (code: string) => void
  error: string
}

export const RoomScreen = ({ roomCode, onCreateRoom, onJoinRoom, onRoomCodeChange, error }: RoomScreenProps) => {
  const handleCreateRoom = () => {
    onCreateRoom()
  }

  const handleJoinRoom = () => {
    if (!roomCode.trim()) {
      return
    }
    onJoinRoom()
  }

  return (
    <div className="room-screen">
      <h1>Number Guessing Game</h1>
      <div className="room-actions">
        <button onClick={handleCreateRoom}>Create Room</button>
        <div className="join-section">
          <input
            type="text"
            placeholder="Enter room code"
            value={roomCode}
            onChange={(e) => {
              onRoomCodeChange(e.target.value)
            }}
          />
          <button onClick={handleJoinRoom}>Join Room</button>
        </div>
      </div>
      {error && <div className="error">{error}</div>}
    </div>
  )
}
