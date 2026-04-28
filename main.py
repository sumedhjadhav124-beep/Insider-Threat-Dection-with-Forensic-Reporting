from flask import Flask
from flask_login import LoginManager
from app.models.models import db, User
from app.core.config import Config
from app.api.telemetry import telemetry_bp
from app.routes.dashboard import dashboard_bp
from app.routes.auth import auth_bp
from app.routes.alerts import alerts_bp
from app.routes.employee import employee_bp
from app.routes.files import files_bp
from app.routes.forensic import forensic_bp
from app.routes.employee_portal import employee_portal_bp
from app.services.notification_service import socketio
from flask_jwt_extended import JWTManager

def create_app(config_object=Config):
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    app.config.from_object(config_object)

    # Initialize Extensions
    db.init_app(app)
    JWTManager(app)
    socketio.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    app.register_blueprint(telemetry_bp, url_prefix='/api/v1/telemetry')
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(alerts_bp, url_prefix='/alerts')
    app.register_blueprint(employee_bp, url_prefix='/employees')
    app.register_blueprint(files_bp, url_prefix='/files')
    app.register_blueprint(forensic_bp, url_prefix='/forensics')
    app.register_blueprint(employee_portal_bp)

    @app.context_processor
    def inject_now():
        from datetime import datetime
        return {'now': datetime.utcnow()}

    @app.route('/health')
    def health():
        return {"status": "healthy"}, 200

    return app

app = create_app()

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=8000, debug=True)
