import os
import sys

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from main import create_app, socketio
from app.models.models import db
from app.core.config import Config

# Force Local Dev Settings
class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev_itd.db'
    REDIS_URL = None # Disable Redis broker for local dev
    CELERY_BROKER_URL = None
    SQLALCHEMY_ENGINE_OPTIONS = {} # Disable pooling for SQLite

from flask_jwt_extended import create_access_token

def run_local():
    app = create_app(config_object=DevConfig)
    
    @app.route('/test/token')
    def get_test_token():
        return {"access_token": create_access_token(identity="test_admin")}
    
    with app.app_context():
        print("[*] Initializing local development database (SQLite Fallback)...")
        db.create_all()
        print("[+] Database ready.")

    print("\n" + "="*50)
    print(" ITD PLATFORM - LOCAL DEVELOPMENT RUNNER")
    print(" mode: SYNCHRONOUS FALLBACK")
    print(" url: http://127.0.0.1:8000")
    print("="*50 + "\n")
    
    socketio.init_app(app, message_queue=None) # Override Redis queue
    socketio.run(app, host='127.0.0.1', port=8000, debug=True, allow_unsafe_werkzeug=True)

if __name__ == "__main__":
    run_local()
