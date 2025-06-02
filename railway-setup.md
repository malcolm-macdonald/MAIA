# Railway Deployment Guide for AgenticSeek

## Overview
This guide will help you deploy the AgenticSeek application to Railway. The app requires several services and configurations to work properly.

## Prerequisites
1. Railway account (sign up at railway.app)
2. GitHub repository with your code
3. OpenAI API key (or other LLM provider)

## Step-by-Step Deployment

### Phase 1: Prepare Your Repository
✅ **Already Done:** The following files have been created:
- `Procfile` - Tells Railway how to start the app
- `railway.toml` - Railway configuration
- `requirements-railway.txt` - Optimized dependencies for cloud deployment
- `railway.env.example` - Environment variables template

### Phase 2: Railway Project Setup
1. **Create New Project**
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Choose "Deploy from GitHub repo"
   - Select your repository

2. **Add Redis Database**
   - In your Railway project dashboard
   - Click "New" → "Database" → "Add Redis"
   - This will automatically provide `REDIS_URL` environment variable

### Phase 3: Configure Environment Variables
In your Railway project dashboard, go to Variables tab and add:

**Required Variables:**
```
OPENAI_API_KEY=your_actual_openai_key
PROVIDER_NAME=openai
PROVIDER_MODEL=gpt-3.5-turbo
PROVIDER_SERVER_ADDRESS=https://api.openai.com/v1
IS_LOCAL=false
PORT=8000
PYTHONPATH=/app
```

**Optional Browser Variables (if needed):**
```
CHROME_BIN=/usr/bin/google-chrome
CHROMEDRIVER_PATH=/usr/bin/chromedriver
```

### Phase 4: Update Requirements File
**Option A:** Replace current requirements.txt
- Rename `requirements.txt` to `requirements-original.txt`
- Rename `requirements-railway.txt` to `requirements.txt`

**Option B:** Keep both (Railway will use requirements.txt by default)

### Phase 5: Configuration File Updates
You may need to update `config.ini` for Railway environment:
- Set Redis URL to use environment variable
- Configure for headless browser mode
- Adjust file paths for cloud environment

## Important Notes

### 🚨 Known Issues to Address:
1. **SearXNG Dependency**: Your app expects SearXNG at `localhost:8080`
   - Either deploy SearXNG separately on Railway
   - Or modify code to use alternative search APIs

2. **File Storage**: App creates screenshots and logs
   - Railway has ephemeral storage
   - Consider using external storage (AWS S3, Cloudinary)

3. **Chrome Driver**: Browser automation in cloud environment
   - May need additional system packages
   - Consider using Railway's browser support

### 🔧 Manual Configuration Required:
1. **Get your OpenAI API key** from openai.com
2. **Update config.ini** for cloud environment
3. **Test browser functionality** - may need adjustments
4. **Set up external search** if SearXNG issues persist

## Deployment Commands
After setup, Railway will automatically:
1. Install dependencies from requirements.txt
2. Run the command from Procfile: `python api.py`
3. Health check at `/health` endpoint

## Troubleshooting
- Check Railway logs for startup errors
- Verify all environment variables are set
- Test Redis connection
- Ensure all required system packages are available

## Alternative: Docker Deployment
If Nixpacks deployment fails, you can use Docker by:
1. Fixing Chrome driver issues in Dockerfile.backend
2. Creating docker-compose setup for Railway
3. Using Railway's Docker builder instead of Nixpacks 