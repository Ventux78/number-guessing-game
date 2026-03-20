# Quick Deployment Guide (5 Minutes)

## TL;DR - Deploy in 5 Steps

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Number Guessing Game"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/number-guessing-game.git
git push -u origin main
```

### Step 2: Deploy Backend (Railway)
1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway auto-deploys - wait for green checkmark
5. Copy the public URL from the deployment

### Step 3: Deploy Frontend (Vercel)
1. Go to https://vercel.com
2. Click "New Project" → "Import Git Repository"
3. Select your repository
4. Add environment variable:
   - Name: `VITE_BACKEND_URL`
   - Value: Your Railway URL from Step 2
5. Click "Deploy"

### Step 4: Update Backend CORS
1. Go back to Railway dashboard
2. Select your service → Variables
3. Set `ALLOWED_ORIGINS` to your Vercel URL (e.g., `https://your-project.vercel.app`)
4. Railway auto-redeploys

### Step 5: Play!
Open your Vercel URL and start playing!

## Environment Variables Needed

**Railway (Backend):**
- `FLASK_ENV`: `production`
- `SECRET_KEY`: Any random string
- `ALLOWED_ORIGINS`: Your Vercel domain

**Vercel (Frontend):**
- `VITE_BACKEND_URL`: Your Railway URL

## That's It!

Your game is now live and completely free. No credit card needed.

For detailed instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md)
