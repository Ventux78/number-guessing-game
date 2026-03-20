# Real-Time Number Guessing Game

A mobile-friendly web application that enables two players to compete in a real-time number guessing game over the internet.

## Project Structure

```
.
├── backend/                 # Python Flask backend with Socket.IO
│   ├── app.py              # Main Flask application
│   ├── config.py           # Configuration settings
│   ├── models.py           # Data models
│   ├── handlers.py         # Socket.IO event handlers
│   └── requirements.txt    # Python dependencies
├── frontend/               # React TypeScript frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── hooks/          # Custom React hooks
│   │   ├── types/          # TypeScript type definitions
│   │   ├── App.tsx         # Main App component
│   │   └── main.tsx        # Entry point
│   ├── package.json        # Node dependencies
│   ├── tsconfig.json       # TypeScript configuration
│   └── vite.config.ts      # Vite configuration
└── README.md               # This file
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file (optional):
   ```
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-here
   ```

6. Run the backend server:
   ```bash
   python app.py
   ```

   The server will start on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

   The application will be available at `http://localhost:3000`

4. Build for production:
   ```bash
   npm run build
   ```

## Running Tests

### Backend Tests

```bash
cd backend
python -m pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

To run tests once without watch mode:
```bash
npm run test:run
```

## Deployment

To deploy this game online for free, see [DEPLOYMENT.md](./DEPLOYMENT.md) for step-by-step instructions using Railway.app (backend) and Vercel (frontend).

**Quick Summary:**
1. Push code to GitHub
2. Deploy backend to Railway.app
3. Deploy frontend to Vercel
4. Update environment variables
5. Done - completely free!

## Game Flow

1. **Room Creation/Joining**: Players create a new room or join an existing one using a room code
2. **Setup Phase**: Both players secretly choose a number between 1-100
3. **Guessing Phase**: Players take turns guessing each other's number with real-time range feedback
4. **Game End**: First player to guess correctly wins
5. **Play Again**: Players can start a new game in the same room

## Features

- Real-time WebSocket communication via Socket.IO
- Mobile-responsive UI optimized for small screens
- Secure server-side game state management
- Automatic reconnection handling
- Input validation and error handling
- Guess history tracking with timestamps

## Technology Stack

### Backend
- Flask 2.3.3
- python-socketio 5.9.0
- python-engineio 4.7.1
- python-dotenv 1.0.0

### Frontend
- React 18.2.0
- TypeScript 5.2.2
- Socket.IO Client 4.7.2
- Vite 5.0.0
- Vitest 0.34.6
- fast-check 3.13.0 (Property-based testing)

## Development

### Code Style

- Backend: Follow PEP 8 standards
- Frontend: Follow ESLint configuration

### Testing Strategy

- Unit tests for specific examples and edge cases
- Property-based tests for universal correctness properties
- Integration tests for end-to-end game flows

## License

MIT
