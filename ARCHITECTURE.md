# Architecture & Deployment Diagram

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         INTERNET                                │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │
                ┌─────────────┴─────────────┐
                │                           │
                ▼                           ▼
        ┌──────────────┐          ┌──────────────────┐
        │   VERCEL     │          │   RAILWAY.APP    │
        │  (Frontend)  │          │   (Backend)      │
        │              │          │                  │
        │ React App    │◄────────►│ Flask + Socket.IO│
        │ TypeScript   │ WebSocket│ Python           │
        │ Vite Build   │          │ Gunicorn         │
        └──────────────┘          └──────────────────┘
             │                            │
             │                            │
        HTTPS/WS                    HTTPS/WS
             │                            │
             ▼                            ▼
        ┌──────────────┐          ┌──────────────────┐
        │   Browser    │          │  Game Server     │
        │   Player 1   │          │  Room Manager    │
        │              │          │  Game Engine     │
        └──────────────┘          └──────────────────┘
             │
             │ Share Room Code
             │
             ▼
        ┌──────────────┐
        │   Browser    │
        │   Player 2   │
        │              │
        └──────────────┘
```

## Deployment Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    YOUR LOCAL MACHINE                           │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Backend     │  │  Frontend    │  │  Tests       │         │
│  │  (Python)    │  │  (React)     │  │  (Pytest)    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│         │                  │                  │                │
│         └──────────────────┼──────────────────┘                │
│                            │                                   │
│                      git push                                  │
│                            │                                   │
└────────────────────────────┼───────────────────────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  GITHUB REPO    │
                    │                 │
                    │ Webhook Trigger │
                    └────────┬────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
        ┌──────────────┐          ┌──────────────┐
        │  RAILWAY.APP │          │    VERCEL    │
        │              │          │              │
        │ 1. Pull code │          │ 1. Pull code │
        │ 2. Install   │          │ 2. Install   │
        │ 3. Build     │          │ 3. Build     │
        │ 4. Deploy    │          │ 4. Deploy    │
        │ 5. Start     │          │ 5. Start     │
        │              │          │              │
        │ ✓ Running    │          │ ✓ Running    │
        └──────────────┘          └──────────────┘
```

## Data Flow During Game

```
Player 1 (Browser)          WebSocket          Player 2 (Browser)
       │                                               │
       │  1. Create Room                              │
       ├──────────────────────────────────────────────►
       │                                               │
       │                    2. Room Created           │
       │◄──────────────────────────────────────────────┤
       │                                               │
       │                                    3. Join Room
       │                                               ├──────────┐
       │                                               │          │
       │                    4. Player Joined          │          │
       │◄──────────────────────────────────────────────┤          │
       │                                               │          │
       │  5. Submit Secret Number                     │          │
       ├──────────────────────────────────────────────►          │
       │                                               │          │
       │                                    6. Submit Secret
       │                                               ├──────────┘
       │                                               │
       │                    7. Game Started           │
       │◄──────────────────────────────────────────────┤
       │                                               │
       │  8. Submit Guess                             │
       ├──────────────────────────────────────────────►
       │                                               │
       │                    9. Guess Result           │
       │◄──────────────────────────────────────────────┤
       │                                               │
       │                                    10. Submit Guess
       │                                               ├──────────┐
       │                                               │          │
       │                    11. Guess Result          │          │
       │◄──────────────────────────────────────────────┤          │
       │                                               │          │
       │  ... (repeat until win)                      │          │
       │                                               │          │
       │                    12. Game Won              │          │
       │◄──────────────────────────────────────────────┤          │
       │                                               │          │
```

## Backend Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Flask Application                            │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    Socket.IO Server                      │  │
│  │                                                          │  │
│  │  ┌────────────────────────────────────────────────────┐ │  │
│  │  │              Event Handlers                        │ │  │
│  │  │                                                    │ │  │
│  │  │  • connect / disconnect                           │ │  │
│  │  │  • create_room / join_room                        │ │  │
│  │  │  • submit_number / submit_guess                  │ │  │
│  │  │  • play_again                                     │ │  │
│  │  └────────────────────────────────────────────────────┘ │  │
│  │                        │                                 │  │
│  │                        ▼                                 │  │
│  │  ┌────────────────────────────────────────────────────┐ │  │
│  │  │           RoomManager                             │ │  │
│  │  │                                                    │ │  │
│  │  │  • createRoom()                                   │ │  │
│  │  │  • joinRoom()                                     │ │  │
│  │  │  • getRoom()                                      │ │  │
│  │  │  • deleteRoom()                                   │ │  │
│  │  └────────────────────────────────────────────────────┘ │  │
│  │                        │                                 │  │
│  │                        ▼                                 │  │
│  │  ┌────────────────────────────────────────────────────┐ │  │
│  │  │           GameEngine                              │ │  │
│  │  │                                                    │ │  │
│  │  │  • validateGuess()                                │ │  │
│  │  │  • calculateRangeUpdate()                         │ │  │
│  │  │  • checkWinCondition()                            │ │  │
│  │  │  • resetGame()                                    │ │  │
│  │  └────────────────────────────────────────────────────┘ │  │
│  │                        │                                 │  │
│  │                        ▼                                 │  │
│  │  ┌────────────────────────────────────────────────────┐ │  │
│  │  │           GameState (Per Room)                    │ │  │
│  │  │                                                    │ │  │
│  │  │  • players: [Player1, Player2]                    │ │  │
│  │  │  • secretNumbers: {player1: num, player2: num}   │ │  │
│  │  │  • guesses: [...]                                 │ │  │
│  │  │  • validRange: {min, max}                         │ │  │
│  │  │  • state: waiting/setup/guessing/finished        │ │  │
│  │  └────────────────────────────────────────────────────┘ │  │
│  │                                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Frontend Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    React Application                            │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    App Component                         │  │
│  │                                                          │  │
│  │  State:                                                 │  │
│  │  • currentScreen: room | setup | game                  │  │
│  │  • roomCode, secretNumber, guess                       │  │
│  │  • validRange, guessHistory, currentTurn              │  │
│  │  • error                                                │  │
│  │                                                          │  │
│  │  ┌────────────────────────────────────────────────────┐ │  │
│  │  │  useSocket Hook                                    │ │  │
│  │  │                                                    │ │  │
│  │  │  • Connects to backend via Socket.IO              │ │  │
│  │  │  • Uses VITE_BACKEND_URL env variable            │ │  │
│  │  │  • Handles reconnection                           │ │  │
│  │  │  • Emits/listens to events                        │ │  │
│  │  └────────────────────────────────────────────────────┘ │  │
│  │                        │                                 │  │
│  │                        ▼                                 │  │
│  │  ┌────────────────────────────────────────────────────┐ │  │
│  │  │  Screen Components                                │ │  │
│  │  │                                                    │ │  │
│  │  │  • RoomScreen: Create/Join room                  │ │  │
│  │  │  • SetupScreen: Choose secret number             │ │  │
│  │  │  • GameScreen: Play game, view history           │ │  │
│  │  └────────────────────────────────────────────────────┘ │  │
│  │                                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      PRODUCTION                                 │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    RAILWAY.APP                           │  │
│  │                                                          │  │
│  │  ┌────────────────────────────────────────────────────┐ │  │
│  │  │  Gunicorn Server (Port $PORT)                     │ │  │
│  │  │                                                    │ │  │
│  │  │  ┌──────────────────────────────────────────────┐ │ │  │
│  │  │  │  Flask App                                   │ │ │  │
│  │  │  │  • Socket.IO Server                          │ │ │  │
│  │  │  │  • Event Handlers                            │ │ │  │
│  │  │  │  • Game Logic                                │ │ │  │
│  │  │  └──────────────────────────────────────────────┘ │ │  │
│  │  │                                                    │ │  │
│  │  │  Environment Variables:                          │ │  │
│  │  │  • FLASK_ENV=production                          │ │  │
│  │  │  • SECRET_KEY=***                                │ │  │
│  │  │  • ALLOWED_ORIGINS=https://vercel-domain        │ │  │
│  │  └────────────────────────────────────────────────┘ │  │
│  │                                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                      VERCEL                             │  │
│  │                                                          │  │
│  │  ┌────────────────────────────────────────────────────┐ │  │
│  │  │  Static Site (CDN)                                │ │  │
│  │  │                                                    │ │  │
│  │  │  ┌──────────────────────────────────────────────┐ │ │  │
│  │  │  │  React App (Built with Vite)                │ │ │  │
│  │  │  │  • HTML/CSS/JS                              │ │ │  │
│  │  │  │  • Socket.IO Client                         │ │ │  │
│  │  │  │  • Connects to Railway backend              │ │ │  │
│  │  │  └──────────────────────────────────────────────┘ │ │  │
│  │  │                                                    │ │  │
│  │  │  Environment Variables:                          │ │  │
│  │  │  • VITE_BACKEND_URL=https://railway-domain      │ │  │
│  │  └────────────────────────────────────────────────┘ │  │
│  │                                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Technology Stack

### Backend
- **Framework**: Flask 2.3.3
- **Real-time**: Socket.IO 5.9.0
- **Server**: Gunicorn + Eventlet
- **Language**: Python 3.9+
- **Testing**: Pytest + Hypothesis

### Frontend
- **Framework**: React 18.2.0
- **Language**: TypeScript 5.2.2
- **Build Tool**: Vite 5.0.0
- **Real-time**: Socket.IO Client 4.7.2
- **Testing**: Vitest + fast-check

### Deployment
- **Backend**: Railway.app (Docker-based)
- **Frontend**: Vercel (Edge Network)
- **Repository**: GitHub
- **CI/CD**: GitHub Actions

## Security Considerations

1. **CORS**: Configured to allow only frontend domain
2. **Environment Variables**: Sensitive data stored securely
3. **Input Validation**: All inputs validated server-side
4. **Game State**: Managed server-side (not client-side)
5. **WebSocket**: Secure WSS connection in production
6. **Secret Numbers**: Never sent to opponent

## Scalability

- **Current**: Handles multiple concurrent games
- **Rooms**: Unlimited room creation
- **Players**: 2 players per room (by design)
- **Concurrent Users**: Limited by Railway/Vercel tier
- **Upgrade Path**: Scale to paid tiers if needed

## Monitoring

- **Railway**: Built-in logs and metrics
- **Vercel**: Built-in analytics and logs
- **GitHub Actions**: Test results on each push
- **Browser Console**: Client-side debugging

---

For deployment instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md)
