# Vercel serverless entry point
# Vercel looks for a handler in api/index.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from main import app

# Vercel expects the ASGI app to be named 'app'
handler = app
