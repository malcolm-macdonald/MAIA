#!/usr/bin/env python3
"""
Railway startup script for AgenticSeek
Handles missing services and environment setup before starting the main application
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def setup_environment():
    """Set up environment variables and directories for Railway deployment."""
    print("🚀 Setting up AgenticSeek for Railway deployment...")
    
    # Create workspace directory
    workspace_dir = Path("/app/workspace")
    workspace_dir.mkdir(exist_ok=True)
    print(f"✅ Created workspace directory: {workspace_dir}")
    
    # Create screenshots directory
    screenshots_dir = Path("/app/.screenshots")
    screenshots_dir.mkdir(exist_ok=True)
    print(f"✅ Created screenshots directory: {screenshots_dir}")
    
    # Copy Railway config if needed
    if Path("config-railway.ini").exists() and not Path("config.ini").exists():
        shutil.copy("config-railway.ini", "config.ini")
        print("✅ Copied Railway configuration")
    
    # Set default environment variables if not set
    env_defaults = {
        "SEARXNG_URL": "http://localhost:8080",
        "SEARXNG_BASE_URL": "http://localhost:8080",
        "REDIS_URL": os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        "PORT": "8000",
        "PYTHONPATH": "/app"
    }
    
    for key, default_value in env_defaults.items():
        if not os.getenv(key):
            os.environ[key] = default_value
            print(f"✅ Set default {key}={default_value}")
    
    print("🎯 Environment setup complete!")

def check_dependencies():
    """Check if critical dependencies are available."""
    print("🔍 Checking dependencies...")
    
    # Check for Chrome/Chromium
    chrome_paths = ["/usr/bin/google-chrome", "/usr/bin/chromium-browser", "/usr/bin/chromium"]
    chrome_found = any(Path(path).exists() for path in chrome_paths)
    
    if chrome_found:
        print("✅ Chrome/Chromium found")
    else:
        print("⚠️ Chrome/Chromium not found - browser features may be limited")
    
    # Check for ChromeDriver
    chromedriver_paths = ["/usr/bin/chromedriver", "/usr/local/bin/chromedriver"]
    chromedriver_found = any(Path(path).exists() for path in chromedriver_paths)
    
    if chromedriver_found:
        print("✅ ChromeDriver found")
    else:
        print("⚠️ ChromeDriver not found - browser features may be limited")

def start_application():
    """Start the main AgenticSeek application."""
    print("🚀 Starting AgenticSeek API server...")
    
    try:
        # Import and run the main application
        sys.path.insert(0, '/app')
        import api
        print("✅ AgenticSeek started successfully!")
        
    except ImportError as e:
        print(f"❌ Failed to import main application: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        setup_environment()
        check_dependencies()
        start_application()
    except KeyboardInterrupt:
        print("\n👋 Shutting down AgenticSeek...")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Startup failed: {e}")
        sys.exit(1) 