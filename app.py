from flask import Flask, render_template, session, redirect, url_for
from utils.config import Config
from database.models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()

    # Register Blueprints (to be created next)
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.api import api_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(api_bp)
    
    @app.route("/")
    def index():
        if 'user_id' in session:
            return redirect(url_for('dashboard.index'))
        return redirect(url_for('auth.login'))

    return app

# Expose app globally for Vercel's serverless environment
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
application = app