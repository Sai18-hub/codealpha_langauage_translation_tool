import os
import sys

# Ensure root directory is in sys.path so modules like app are found
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Vercel looks for the WSGI application named `app`
if __name__ == "__main__":
    app.run()
