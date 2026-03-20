# Troubleshooting Guide

## Common Issues and Solutions

### Backend Issues

#### Backend won't start on Railway
**Symptoms**: Deployment fails or service keeps restarting

**Solutions**:
1. Check Railway logs:
   - Go to Railway dashboard → Your service → Deployments
   - Click on failed deployment → View logs
2. Verify environment variables:
   - `FLASK_ENV` should be `production`
   - `SECRET_KEY` should be set to any random string
3. Check `requirements.txt`:
   - Ensure all dependencies are listed
   - Run locally: `pip install -r requirements.txt`
4. Verify Python version:
   - Railway uses Python 3.11 by default
   - Should work with 3.9+

#### Backend crashes after deployment
**Symptoms**: Deployment succeeds but service keeps restarting

**Solutions**:
1. Check for import errors:
   ```bash
   cd backend
   python -c "from app import create_app; create_app()"
   ```
2. Verify all imports in `app.py`:
   - `from flask_cors import CORS` should work
   - `from handlers import register_handlers` should work
3. Check for missing dependencies:
   - Run `pip install -r requirements.txt` locally
   - Verify no import errors

#### Port issues
**Symptoms**: Backend won't bind to port

**Solutions**:
1. Railway automatically assigns `$PORT` environment variable
2. Ensure start command uses `$PORT`:
   ```
   gunicorn --bind 0.0.0.0:$PORT app:app
   ```
3. Don't hardcode port 5000 in production

---

### Frontend Issues

#### Frontend won't connect to backend
**Symptoms**: 
- Browser console shows connection errors
- "Cannot connect to server" message
- WebSocket connection fails

**Solutions**:
1. Check `VITE_BACKEND_URL` environment variable:
   - Go to Vercel project → Settings → Environment Variables
   - Verify it matches your Railway URL exactly
   - Should be like: `https://your-project.up.railway.app`
2. Verify backend is running:
   - Visit your Railway URL in browser
   - Should see Flask response (not connection error)
3. Check CORS configuration:
   - Backend `ALLOWED_ORIGINS` should include your Vercel domain
   - Should be like: `https://your-project.vercel.app`
4. Check browser console for specific errors:
   - Open DevTools (F12) → Console tab
   - Look for error messages about connection

#### Build fails on Vercel
**Symptoms**: Deployment fails during build phase

**Solutions**:
1. Check Vercel build logs:
   - Go to Vercel project → Deployments
   - Click failed deployment → View logs
2. Common build errors:
   - Missing dependencies: Add to `frontend/package.json`
   - TypeScript errors: Run `npm run build` locally to test
   - Environment variables: Ensure `VITE_BACKEND_URL` is set
3. Clear cache and redeploy:
   - Vercel project → Settings → Git
   - Disconnect and reconnect repository
   - Redeploy

#### Frontend shows blank page
**Symptoms**: Page loads but nothing displays

**Solutions**:
1. Check browser console for errors (F12)
2. Verify `index.html` exists in `frontend/`
3. Check Vite build output:
   - Run `npm run build` locally
   - Verify `dist/` folder is created
4. Check Vercel build settings:
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`

---

### CORS Issues

#### CORS error: "Access to XMLHttpRequest blocked"
**Symptoms**: Browser console shows CORS error

**Solutions**:
1. Update `ALLOWED_ORIGINS` in Railway:
   - Go to Railway → Your service → Variables
   - Set `ALLOWED_ORIGINS` to your Vercel domain
   - Example: `https://my-game.vercel.app`
2. Wait for Railway to redeploy (usually 1-2 minutes)
3. Hard refresh browser (Ctrl+Shift+R or Cmd+Shift+R)
4. Check exact domain match:
   - No trailing slash
   - Include `https://`
   - Match exactly what's in browser address bar

#### CORS error after updating ALLOWED_ORIGINS
**Symptoms**: Still getting CORS error after updating

**Solutions**:
1. Wait for Railway to redeploy:
   - Check Railway dashboard for green checkmark
   - May take 1-2 minutes
2. Hard refresh browser:
   - Ctrl+Shift+R (Windows)
   - Cmd+Shift+R (Mac)
3. Clear browser cache:
   - DevTools → Application → Clear storage
4. Try incognito/private window:
   - Helps rule out cache issues

---

### Socket.IO Connection Issues

#### WebSocket connection timeout
**Symptoms**: Connection takes forever or times out

**Solutions**:
1. Verify backend is running:
   - Check Railway logs for errors
   - Visit Railway URL in browser
2. Check network connectivity:
   - Ensure you have internet connection
   - Try from different network
3. Check firewall/proxy:
   - Some networks block WebSocket
   - Try from different network
4. Verify Socket.IO configuration:
   - Check `useSocket.ts` has correct backend URL
   - Verify reconnection settings

#### Socket.IO connects but no events received
**Symptoms**: Connection shows as connected but game doesn't work

**Solutions**:
1. Check backend event handlers:
   - Verify `handlers.py` has all event listeners
   - Check for errors in backend logs
2. Verify event names match:
   - Frontend sends: `create_room`, `join_room`, etc.
   - Backend listens for same names
3. Check browser console for errors
4. Restart backend service:
   - Go to Railway → Your service
   - Click "Restart" button

---

### Game Logic Issues

#### Game won't start after joining room
**Symptoms**: Stuck on setup screen

**Solutions**:
1. Verify both players submitted numbers:
   - Both players need to submit secret number
   - Check for error messages
2. Check backend logs for errors:
   - Go to Railway → Deployments → View logs
3. Try creating new room:
   - Sometimes room state gets corrupted
   - Create fresh room and try again

#### Guesses not being processed
**Symptoms**: Submit guess but nothing happens

**Solutions**:
1. Check valid range:
   - Guess must be within displayed range
   - Try a number in the middle of range
2. Check for duplicate guesses:
   - Can't guess same number twice
   - Try different number
3. Check backend logs for errors
4. Refresh page and try again

#### Range not updating
**Symptoms**: After guess, range stays the same

**Solutions**:
1. Check backend logs for errors
2. Verify guess was actually submitted:
   - Check guess history
   - Look for your guess in list
3. Try refreshing page
4. Check browser console for errors

---

### Deployment Issues

#### Changes not deploying
**Symptoms**: Push to GitHub but changes don't appear online

**Solutions**:
1. Verify push was successful:
   - Run `git log` to see commits
   - Check GitHub repository for changes
2. Wait for auto-deployment:
   - Railway and Vercel auto-deploy on push
   - May take 1-2 minutes
   - Check deployment status in dashboards
3. Check for build errors:
   - Go to Railway/Vercel dashboard
   - Check deployment logs
4. Manual redeploy:
   - Railway: Click "Redeploy" button
   - Vercel: Click "Redeploy" button

#### Environment variables not working
**Symptoms**: Backend/frontend can't access environment variables

**Solutions**:
1. Verify variables are set:
   - Railway: Service → Variables
   - Vercel: Project Settings → Environment Variables
2. Redeploy after setting variables:
   - Changes to variables require redeploy
   - Click "Redeploy" button
3. Check variable names:
   - Backend: `FLASK_ENV`, `SECRET_KEY`, `ALLOWED_ORIGINS`
   - Frontend: `VITE_BACKEND_URL`
4. Verify no typos in names

---

### Local Development Issues

#### Backend won't start locally
**Symptoms**: `python app.py` fails

**Solutions**:
1. Verify virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Check for import errors:
   ```bash
   python -c "from app import create_app"
   ```
4. Verify Python version:
   - Should be 3.9 or higher
   - Check with `python --version`

#### Frontend won't start locally
**Symptoms**: `npm run dev` fails

**Solutions**:
1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Check Node version:
   - Should be 16 or higher
   - Check with `node --version`
3. Clear npm cache:
   ```bash
   npm cache clean --force
   npm install
   ```
4. Check for port conflicts:
   - Default port is 3000
   - If in use, Vite will use next available port

#### Tests fail locally
**Symptoms**: `pytest` or `npm test` fails

**Solutions**:
1. Backend tests:
   ```bash
   cd backend
   pip install -r requirements.txt
   python -m pytest -v
   ```
2. Frontend tests:
   ```bash
   cd frontend
   npm install
   npm run test:run
   ```
3. Check for missing dependencies
4. Verify Python/Node versions

---

## Getting Help

If you're still stuck:

1. Check the logs:
   - Railway: Dashboard → Service → Deployments → View logs
   - Vercel: Dashboard → Deployments → View logs
   - Browser: DevTools → Console tab

2. Review documentation:
   - [DEPLOYMENT.md](./DEPLOYMENT.md) - Full guide
   - [QUICK_DEPLOY.md](./QUICK_DEPLOY.md) - Quick start
   - [README.md](./README.md) - Project overview

3. Common fixes:
   - Hard refresh browser (Ctrl+Shift+R)
   - Clear browser cache
   - Restart services (Railway/Vercel redeploy)
   - Check environment variables
   - Verify domain names match exactly

4. Debug locally:
   - Run backend locally: `python backend/app.py`
   - Run frontend locally: `npm run dev`
   - Test Socket.IO connection in browser console
   - Check browser DevTools for errors

---

## Still Need Help?

- Check Railway documentation: https://docs.railway.app
- Check Vercel documentation: https://vercel.com/docs
- Check Socket.IO documentation: https://socket.io/docs
- Check Flask documentation: https://flask.palletsprojects.com
