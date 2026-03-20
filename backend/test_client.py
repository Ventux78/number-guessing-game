"""Test client for the number guessing game - simulates two players."""
import socketio
import time
import threading

# Create Socket.IO clients
sio1 = socketio.Client()
sio2 = socketio.Client()

# Game state
game_state = {
    'player1_id': None,
    'player2_id': None,
    'room_code': None,
    'player1_secret': 42,
    'player2_secret': 75,
    'game_started': False,
    'guesses': []
}

# Player 1 Event Handlers
@sio1.on('connection_response')
def on_connect_p1(data):
    print(f"✅ Player 1 connected: {data}")
    game_state['player1_id'] = data['player_id']

@sio1.on('room_created')
def on_room_created(data):
    print(f"🎮 Room created: {data['room_code']}")
    game_state['room_code'] = data['room_code']
    # Player 2 joins after a short delay
    time.sleep(1)
    print(f"🚪 Player 2 joining room {data['room_code']}...")
    sio2.emit('join_room', {'room_code': data['room_code']})

@sio1.on('player_joined')
def on_player_joined_p1(data):
    print(f"👥 Player joined: {data}")
    if data['players_count'] == 2:
        print("🎯 Both players in room! Submitting secret numbers...")
        time.sleep(0.5)
        sio1.emit('submit_number', {'secret_number': game_state['player1_secret']})

@sio1.on('game_started')
def on_game_started_p1(data):
    print(f"🎮 Game started: {data}")

@sio1.on('number_submitted')
def on_number_submitted_p1(data):
    print(f"✓ Number submitted (P1): {data}")

@sio1.on('game_ready')
def on_game_ready_p1(data):
    print(f"✨ Game ready: {data}")
    game_state['game_started'] = True
    time.sleep(0.5)
    print("🎯 Player 1 making first guess...")
    sio1.emit('submit_guess', {'guess': 50})

@sio1.on('guess_result')
def on_guess_result_p1(data):
    print(f"📊 Guess result: Player {data['player_id']} guessed {data['guess']} - {data['feedback']}")
    print(f"   Valid range now: {data['valid_range']['min']} - {data['valid_range']['max']}")
    game_state['guesses'].append(data)
    
    # Player 2 makes next guess after a delay
    if data['player_id'] == game_state['player1_id']:
        time.sleep(1)
        if data['feedback'] != 'correct':
            print("🎯 Player 2 making guess...")
            if data['feedback'] == 'too_low':
                guess = data['valid_range']['min'] + 10
            else:
                guess = data['valid_range']['max'] - 10
            sio2.emit('submit_guess', {'guess': guess})

@sio1.on('game_won')
def on_game_won_p1(data):
    print(f"🏆 GAME WON! Winner: {data['winner_id']}, Secret: {data['secret_number']}")

@sio1.on('error')
def on_error_p1(data):
    print(f"❌ Error (Player 1): {data['message']}")

# Player 2 Event Handlers
@sio2.on('connection_response')
def on_connect_p2(data):
    print(f"✅ Player 2 connected: {data}")
    game_state['player2_id'] = data['player_id']

@sio2.on('player_joined')
def on_player_joined_p2(data):
    print(f"👥 Player joined (P2): {data}")

@sio2.on('game_started')
def on_game_started_p2(data):
    print(f"🎮 Game started (P2): {data}")
    time.sleep(0.5)
    print("🎯 Player 2 submitting secret number...")
    sio2.emit('submit_number', {'secret_number': game_state['player2_secret']})

@sio2.on('number_submitted')
def on_number_submitted_p2(data):
    print(f"✓ Number submitted (P2): {data}")

@sio2.on('game_ready')
def on_game_ready_p2(data):
    print(f"✨ Game ready (P2): {data}")
    time.sleep(0.5)
    print("🎯 Player 2 submitting secret number...")
    sio2.emit('submit_number', {'secret_number': game_state['player2_secret']})

@sio2.on('guess_result')
def on_guess_result_p2(data):
    print(f"📊 Guess result (P2): Player {data['player_id']} guessed {data['guess']} - {data['feedback']}")
    print(f"   Valid range now: {data['valid_range']['min']} - {data['valid_range']['max']}")
    
    # Player 1 makes next guess
    if data['player_id'] == game_state['player2_id']:
        time.sleep(1)
        if data['feedback'] != 'correct':
            print("🎯 Player 1 making next guess...")
            if data['feedback'] == 'too_low':
                guess = data['valid_range']['min'] + 5
            else:
                guess = data['valid_range']['max'] - 5
            sio1.emit('submit_guess', {'guess': guess})

@sio2.on('game_won')
def on_game_won_p2(data):
    print(f"🏆 GAME WON! Winner: {data['winner_id']}, Secret: {data['secret_number']}")

@sio2.on('error')
def on_error_p2(data):
    print(f"❌ Error (Player 2): {data['message']}")

def run_test():
    """Run the two-player game test."""
    print("=" * 60)
    print("🎮 NUMBER GUESSING GAME - TWO PLAYER TEST")
    print("=" * 60)
    
    try:
        # Connect both players
        print("\n📡 Connecting players...")
        sio1.connect('http://localhost:5000')
        time.sleep(0.5)
        sio2.connect('http://localhost:5000')
        time.sleep(0.5)
        
        # Player 1 creates room
        print("\n🎮 Player 1 creating room...")
        sio1.emit('create_room')
        
        # Wait for game to complete
        print("\n⏳ Waiting for game to complete...")
        time.sleep(30)
        
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"Total guesses: {len(game_state['guesses'])}")
        print(f"Player 1 secret: {game_state['player1_secret']}")
        print(f"Player 2 secret: {game_state['player2_secret']}")
        print(f"Room code: {game_state['room_code']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Disconnect
        if sio1.connected:
            sio1.disconnect()
        if sio2.connected:
            sio2.disconnect()
        print("\n✅ Test completed!")

if __name__ == '__main__':
    run_test()
