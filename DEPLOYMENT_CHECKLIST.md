# Deployment Checklist

Your Number Guessing Game is ready to deploy! Follow this checklist to get it online.

## Pre-Deployment ✓

- [x] Backend fully implemented with Socket.IO
- [x] Frontend fully implemented with React/TypeScript
- [x] All tests passing (24 property-based tests)
- [x] Environment variables configured
- [x] CORS properly configured
- [x] Socket.IO connection uses environment variable

## Deployment Steps

### 1. GitHub Setup
- [ ] Create GitHub account (if needed)
- [ ] Create new repository named `number-guessing-game`
- [ ] Push code to GitHub:
  ```bash
  git init
  git add .
  git commit -m "Initial commit: Number Guessing Game"
  git branch -M main
  git remote add origin https://github.com/YOUR_USERNAME/number-guessing-game.git
  git push -u origin main
  ```

### 2. Railway Backend Deployment
- [ ] Create Railway.app account (sign up with GitHub)
- [ ] Create new project and connect GitHub repository
- [ ] Wait for auto-deployment (should take 2-3 minutes)
- [ ] Set environment variables in Railway:
  - [ ] `FLASK_ENV` = `production`
  - [ ] `SECRET_KEY` = (generate random string)
  - [ ] `ALLOWED_ORIGINS` = `*` (temporary, will update later)
- [ ] Copy the public URL from Railway deployment
- [ ] Verify backend is running (check logs for errors)

### 3. Vercel Frontend Deployment
- [ ] Create Vercel account (sign up with GitHub)
- [ ] Create new project and connect GitHub repository
- [ ] Add environment variable:
  - [ ] `VITE_BACKEND_URL` = (your Railway URL from step 2)
- [ ] Wait for deployment to complete
- [ ] Copy the Vercel URL (e.g., `https://your-project.vercel.app`)

### 4. Update Backend CORS
- [ ] Go back to Railway dashboard
- [ ] Update `ALLOWED_ORIGINS` to your Vercel URL
- [ ] Wait for Railway to redeploy

### 5. Testing
- [ ] Open Vercel URL in browser
- [ ] Create a room
- [ ] Open Vercel URL in another browser/device
- [ ] Join the room
- [ ] Play a complete game
- [ ] Verify all features work:
  - [ ] Room creation
  - [ ] Room joining
  - [ ] Secret number submission
  - [ ] Guess submission
  - [ ] Range updates
  - [ ] Win detection
  - [ ] Play again

## Files Modified for Deployment

- `backend/app.py` - Added Flask-CORS and environment variable support
- `backend/requirements.txt` - Added Flask-CORS, gunicorn, eventlet
- `backend/.env.example` - Updated with production variables
- `frontend/src/hooks/useSocket.ts` - Updated to use VITE_BACKEND_URL
- `frontend/.env.example` - Created with VITE_BACKEND_URL
- `Procfile` - Created for Railway deployment
- `railway.json` - Created for Railway configuration
- `frontend/vercel.json` - Created for Vercel configuration

## New Documentation Files

- `DEPLOYMENT.md` - Detailed deployment guide
- `QUICK_DEPLOY.md` - 5-minute quick start
- `DEPLOYMENT_CHECKLIST.md` - This file

## Troubleshooting

### Backend won't start
- Check Railway logs for errors
- Verify all environment variables are set
- Ensure `requirements.txt` has all dependencies

### Frontend won't connect to backend
- Check browser console for errors
- Verify `VITE_BACKEND_URL` is set correctly in Vercel
- Verify `ALLOWED_ORIGINS` includes your Vercel domain in Railway
- Check that Railway backend is running

### CORS errors
- Make sure `ALLOWED_ORIGINS` in Railway includes your full Vercel domain
- Restart Railway service after updating variables

### Build fails
- Check Vercel build logs
- Ensure all dependencies are in `package.json`
- Try clearing Vercel cache and redeploying

## Cost

**Completely Free!**
- Railway.app: Free tier (5GB/month bandwidth)
- Vercel: Free tier (unlimited deployments)
- GitHub: Free public repositories

No credit card required.

## Next Steps

After deployment:
1. Share your Vercel URL with friends
2. Make updates by pushing to GitHub (auto-deploys)
3. Monitor logs in Railway and Vercel dashboards
4. Scale up if needed (both services have paid tiers)

## Support

For detailed instructions, see:
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Full deployment guide
- [QUICK_DEPLOY.md](./QUICK_DEPLOY.md) - Quick 5-minute guide
- [README.md](./README.md) - Project overview
