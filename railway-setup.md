# Railway Deployment Guide for AgenticSeek

## Overview
This guide will help you deploy the AgenticSeek application to Railway. **Note**: This is a simplified cloud deployment that may not include all features from the full local setup described in the main README.

## Prerequisites
1. Railway account (sign up at railway.app)
2. GitHub repository with your code
3. OpenAI API key (or other LLM provider)

## ⚠️ **Important Limitations for Railway Deployment**

**Missing Services**: The full AgenticSeek setup includes several Docker services that are not included in this Railway deployment:
- **SearXNG**: Local search engine (normally at localhost:8080)
- **Frontend**: React web interface (normally at localhost:3000)
- **File System**: Limited to ephemeral storage

**Available Features**:
- ✅ Core AI agents and processing
- ✅ API endpoints (/health, /query, etc.)
- ✅ Text-to-Speech (if audio libs install successfully)
- ✅ Browser automation (limited)
- ⚠️ Speech-to-Text (cloud environment dependent)

## Step-by-Step Deployment

### Phase 1: Prepare Your Repository
✅ **Already Done:** The following files have been created:
- `Procfile` - Tells Railway how to start the app
- `railway.toml` - Railway configuration
- `requirements-railway.txt` - Optimized dependencies for cloud deployment
- `railway.env.example` - Environment variables template
- `config-railway.ini` - Cloud-optimized configuration

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

**Search Service Variables:**
```
SEARXNG_URL=http://localhost:8080
SEARXNG_BASE_URL=http://localhost:8080
```

### Phase 4: Update Configuration
**Replace config.ini for Railway**:
```bash
cp config-railway.ini config.ini
```

### Phase 5: Update Requirements File
**Option A:** Replace current requirements.txt
- Rename `requirements.txt` to `requirements-original.txt`
- Rename `requirements-railway.txt` to `requirements.txt`

**Option B:** Keep both (Railway will use requirements.txt by default)

## Known Limitations & Workarounds

### 🚨 **Missing SearXNG Service**
**Problem**: App expects SearXNG search engine at localhost:8080
**Workarounds**:
1. **Deploy SearXNG separately** on Railway (advanced)
2. **Use alternative search APIs** (modify code)
3. **Accept limited search functionality**

### 🚨 **No Frontend Web Interface**
**Problem**: The React frontend (normally at localhost:3000) is not deployed
**Workarounds**:
1. **API-only deployment** - Use curl/Postman to test endpoints
2. **Deploy frontend separately** on Vercel/Netlify
3. **Use CLI mode locally** with Railway backend

### 🚨 **File Storage Limitations**
**Problem**: Railway has ephemeral storage, app expects persistent work_dir
**Workarounds**:
1. **Use external storage** (AWS S3, Google Drive API)
2. **Accept temporary file storage**
3. **Modify work_dir handling** in code

### 🚨 **Browser Automation Issues**
**Problem**: Chrome driver may not work in Railway's container environment
**Expected Behavior**: Browser features may be disabled but app should still start

## Testing Your Deployment

Once deployed, test these endpoints:

1. **Health Check**: `GET https://your-app.railway.app/health`
   - Should return: `{"status": "healthy", "version": "0.1.0"}`

2. **Query Endpoint**: `POST https://your-app.railway.app/query`
   ```json
   {
     "query": "Hello, can you help me?"
   }
   ```

3. **Check Status**: `GET https://your-app.railway.app/is_active`

## Comparison with Full Setup

| Feature | Local Setup (README) | Railway Deployment |
|---------|---------------------|-------------------|
| AI Agents | ✅ Full support | ✅ Full support |
| Web Search | ✅ SearXNG | ⚠️ Limited/None |
| Browser Automation | ✅ Full Chrome | ⚠️ Limited |
| TTS/STT | ✅ Full audio | ⚠️ Depends on container |
| File Operations | ✅ Persistent | ⚠️ Ephemeral |
| Web Interface | ✅ React frontend | ❌ API only |
| Local Models | ✅ Ollama/LM-Studio | ❌ API only |

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
- Check if SearXNG errors are causing failures

## Alternative: Full Docker Deployment
For a more complete deployment matching the README:
1. Fix Chrome driver issues in Dockerfile.backend
2. Deploy SearXNG, Redis, and Frontend as separate Railway services
3. Use Railway's Docker builder instead of Nixpacks 