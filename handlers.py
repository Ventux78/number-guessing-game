"""Socket.IO event handlers."""
from flask import request
from flask_socketio import emit, join_room, leave_room
from room_manager import RoomManager
from game_engine import GameEngine
from models import Guess
import uuid

# Global room manager
room_manager = RoomManager()

# Track player socket mappings
player_sockets = {}  # socket_id -> player_id
socket_rooms = {}    # socket_id -> room_code


def register_handlers(socketio):
    """Register all Socket.IO event handlers."""
    
    @socketio.on("connect")
    def handle_connect():
        """Handle client connection."""
        player_id = str(uuid.uuid4())[:8]
        player_sockets[request.sid] = player_id
        print(f"Client connected: {request.sid} (Player: {player_id})")
        emit("connection_response", {"data": "Connected to server", "player_id": player_id})
    
    @socketio.on("disconnect")
    def handle_disconnect():
        """Handle client disconnection."""
        socket_id = request.sid
        print(f"Client disconnected: {socket_id}")
        
        if socket_id in player_sockets:
            player_id = player_sockets[socket_id]
            del player_sockets[socket_id]
            
            # Handle room disconnection
            if socket_id in socket_rooms:
                room_code = socket_rooms[socket_id]
                room_manager.handle_player_disconnect(room_code, player_id)
                del socket_rooms[socket_id]
    
    @socketio.on("create_room")
    def handle_create_room():
        """Handle room creation."""
        socket_id = request.sid
        player_id = player_sockets.get(socket_id)
        
        if not player_id:
            emit("error", {"message": "Player not found"})
            return
        
        room_code = room_manager.create_room(player_id, socket_id)
        socket_rooms[socket_id] = room_code
        join_room(room_code)
        
        print(f"Room created: {room_code} by {player_id}")
        emit("room_created", {"room_code": room_code})
    
    @socketio.on("join_room")
    def handle_join_room(data):
        """Handle room join."""
        socket_id = request.sid
        player_id = player_sockets.get(socket_id)
        room_code = data.get("room_code", "").upper()
        
        if not player_id:
            emit("error", {"message": "Player not found"})
            return
        
        if not room_code:
            emit("error", {"message": "Room code is required"})
            return
        
        result = room_manager.join_room(room_code, player_id, socket_id)
        
        if result is None:
            emit("error", {"message": "Room not found or is full"})
            return
        
        socket_rooms[socket_id] = room_code
        join_room(room_code)
        
        room = room_manager.get_room(room_code)
        print(f"Player {player_id} joined room {room_code}")
        
        # Notify both players
        socketio.emit("player_joined", {
            "player_id": player_id,
            "players_count": len(room.players)
        }, room=room_code)
        
        # If both players are ready, start the game
        if len(room.players) == 2:
            socketio.emit("game_started", {
                "message": "Both players joined. Enter your secret numbers."
            }, room=room_code)
    
    @socketio.on("submit_number")
    def handle_submit_number(data):
        """Handle secret number submission."""
        socket_id = request.sid
        player_id = player_sockets.get(socket_id)
        room_code = socket_rooms.get(socket_id)
        secret_number = data.get("secret_number")
        
        if not player_id or not room_code:
            emit("error", {"message": "Invalid session"})
            return
        
        if secret_number is None:
            emit("error", {"message": "Secret number is required"})
            return
        
        try:
            secret_number = int(secret_number)
            if secret_number < 1 or secret_number > 100:
                emit("error", {"message": "Number must be between 1 and 100"})
                return
        except (ValueError, TypeError):
            emit("error", {"message": "Invalid number format"})
            return
        
        room = room_manager.get_room(room_code)
        if not room:
            emit("error", {"message": "Room not found"})
            return
        
        if player_id not in room.players:
            emit("error", {"message": "Player not in room"})
            return
        
        room.players[player_id].secret_number = secret_number
        room.players[player_id].is_ready = True
        
        print(f"Player {player_id} submitted secret number in room {room_code}")
        
        # Check if both players are ready
        all_ready = all(p.is_ready for p in room.players.values())
        
        if all_ready:
            room.game_state = "guessing_phase"
            socketio.emit("game_ready", {
                "message": "Both players ready. Start guessing!",
                "valid_range": {"min": room.valid_range["min"], "max": room.valid_range["max"]}
            }, room=room_code)
            print(f"Game started in room {room_code}")
        else:
            emit("number_submitted", {"message": "Waiting for opponent..."})
    
    @socketio.on("submit_guess")
    def handle_submit_guess(data):
        """Handle guess submission using GameEngine."""
        socket_id = request.sid
        player_id = player_sockets.get(socket_id)
        room_code = socket_rooms.get(socket_id)
        guess = data.get("guess")
        
        if not player_id or not room_code:
            emit("error", {"message": "Invalid session"})
            return
        
        if guess is None:
            emit("error", {"message": "Guess is required"})
            return
        
        try:
            guess = int(guess)
        except (ValueError, TypeError):
            emit("error", {"message": "Guess must be a valid integer"})
            return
        
        room = room_manager.get_room(room_code)
        if not room:
            emit("error", {"message": "Room not found"})
            return
        
        if room.game_state != "guessing_phase":
            emit("error", {"message": "Game is not in guessing phase"})
            return
        
        if player_id not in room.players:
            emit("error", {"message": "Player not in room"})
            return
        
        player = room.players[player_id]
        
        # Find opponent
        opponent_id = None
        for pid in room.players:
            if pid != player_id:
                opponent_id = pid
                break
        
        if not opponent_id:
            emit("error", {"message": "Opponent not found"})
            return
        
        opponent = room.players[opponent_id]
        secret_number = opponent.secret_number
        
        # Use GameEngine to process guess
        success, feedback, updated_range = GameEngine.process_guess(
            room, player_id, guess, secret_number
        )
        
        if not success:
            emit("error", {"message": feedback})
            return
        
        # Record guess
        guess_obj = Guess(
            player_id=player_id,
            guess=guess,
            feedback=feedback
        )
        room.guess_history.append(guess_obj)
        
        # Update range if provided
        if updated_range:
            room.valid_range = updated_range
        
        print(f"Player {player_id} guessed {guess} in room {room_code} - {feedback}")
        
        # Broadcast result
        socketio.emit("guess_result", {
            "player_id": player_id,
            "guess": guess,
            "feedback": feedback,
            "valid_range": room.valid_range
        }, room=room_code)
        
        # Check win condition
        if feedback == "correct":
            room.winner = player_id
            room.game_state = "finished"
            socketio.emit("game_won", {
                "winner_id": player_id,
                "secret_number": secret_number
            }, room=room_code)
            print(f"Player {player_id} won in room {room_code}")

    @socketio.on("play_again")
    def handle_play_again():
        """Handle play again request."""
        socket_id = request.sid
        player_id = player_sockets.get(socket_id)
        room_code = socket_rooms.get(socket_id)
        
        if not player_id or not room_code:
            emit("error", {"message": "Invalid session"})
            return
        
        room = room_manager.get_room(room_code)
        if not room:
            emit("error", {"message": "Room not found"})
            return
        
        if room.game_state != "finished":
            emit("error", {"message": "Game is not finished"})
            return
        
        # Reset game state
        room.game_state = "setup_phase"
        room.guess_history = []
        room.valid_range = {"min": 1, "max": 100}
        room.winner = None
        
        # Reset player states
        for player in room.players.values():
            player.secret_number = None
            player.is_ready = False
        
        print(f"Game reset in room {room_code}")
        
        # Notify both players
        socketio.emit("game_reset", {
            "message": "Game reset. Enter your secret numbers again."
        }, room=room_code)