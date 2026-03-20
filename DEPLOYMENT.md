# Deployment Guide - Number Guessing Game

This guide walks you through deploying the Number Guessing Game online using **Railway.app** (backend) and **Vercel** (frontend) - completely free.

## Prerequisites

- GitHub account (free)
- Railway.app account (free, sign up with GitHub)
- Vercel account (free, sign up with GitHub)

## Step 1: Push Code to GitHub

1. Create a new repository on GitHub (e.g., `number-guessing-game`)
2. Clone it locally or initialize git in your project:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Number Guessing Game"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/number-guessing-game.git
   git push -u origin main
   ```

## Step 2: Deploy Backend to Railway.app

### 2.1 Create Railway Project

1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Authorize Railway to access your GitHub account
5. Select your `number-guessing-game` repository

### 2.2 Configure Backend Service

1. Railway will auto-detect the Python project
2. In the Railway dashboard, go to your project
3. Click on the service (should be named after your repo)
4. Go to the "Variables" tab
5. Add these environment variables:
   - `FLASK_ENV`: `production`
   - `SECRET_KEY`: Generate a random string (e.g., use `python -c "import secrets; print(secrets.token_hex(32))"`)
   - `ALLOWED_ORIGINS`: Leave as `*` for now (we'll update after frontend deployment)

### 2.3 Set Start Command

1. Go to the "Settings" tab
2. Find "Start Command"
3. Set it to: `gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT backend.app:app`
4. If that doesn't work, try: `python -m flask run --host=0.0.0.0 --port=$PORT`

### 2.4 Add Gunicorn to Requirements

Update `backend/requirements.txt` to include:
```
gunicorn==21.2.0
eventlet==0.33.3
```

Then commit and push:
```bash
git add backend/requirements.txt
git commit -m "Add gunicorn and eventlet for production"
git push
```

Railway will auto-redeploy.

### 2.5 Get Backend URL

1. Once deployed, go to the "Deployments" tab
2. Click on the successful deployment
3. Find the "Public URL" (e.g., `https://number-guessing-game-production.up.railway.app`)
4. Copy this URL - you'll need it for the frontend

## Step 3: Deploy Frontend to Vercel

### 3.1 Connect to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Select "Import Git Repository"
4. Authorize Vercel to access your GitHub account
5. Select your `number-guessing-game` repository

### 3.2 Configure Frontend Build

1. Vercel should auto-detect it's a Vite project
2. Set these build settings:
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

### 3.3 Add Environment Variables

1. In the Vercel project settings, go to "Environment Variables"
2. Add:
   - **Name**: `VITE_BACKEND_URL`
   - **Value**: Your Railway backend URL (e.g., `https://number-guessing-game-production.up.railway.app`)
   - **Environments**: Select "Production", "Preview", and "Development"

3. Click "Save"

### 3.4 Deploy

1. Click "Deploy"
2. Wait for the build to complete
3. Once done, you'll get a Vercel URL (e.g., `https://number-guessing-game.vercel.app`)

## Step 4: Update Backend CORS

Now that you have your frontend URL, update the backend to allow it:

1. Go back to Railway dashboard
2. Select your backend service
3. Go to "Variables"
4. Update `ALLOWED_ORIGINS` to: `https://your-vercel-domain.vercel.app`
5. Railway will auto-redeploy

## Step 5: Test the Deployment

1. Open your Vercel frontend URL in a browser
2. Create a room and share the code
3. Open the URL in another browser/device
4. Join the room and play

## Troubleshooting

### Backend not connecting
- Check that `VITE_BACKEND_URL` in Vercel matches your Railway URL
- Verify `ALLOWED_ORIGINS` in Railway includes your Vercel domain
- Check Railway logs for errors

### CORS errors
- Make sure `ALLOWED_ORIGINS` includes your full Vercel domain
- Restart the Railway service after updating variables

### Build fails on Vercel
- Check the build logs in Vercel dashboard
- Ensure `frontend/package.json` has all dependencies
- Try clearing cache: Project Settings → Git → Disconnect and reconnect

### Socket.IO connection timeout
- Check that the backend is running (Railway dashboard)
- Verify the backend URL is correct in frontend environment variables
- Check browser console for specific error messages

## Updating Your Game

To make changes:

1. Edit files locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Your message"
   git push
   ```
3. Both Railway and Vercel will auto-redeploy

## Cost

This deployment is **completely free**:
- Railway.app: Free tier includes 5GB/month bandwidth
- Vercel: Free tier includes unlimited deployments
- GitHub: Free public repositories

No credit card required for either service.
