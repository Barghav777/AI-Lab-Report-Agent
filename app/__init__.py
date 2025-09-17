from flask import Flask
import os

# Import the configuration class from the root config.py file
from config import Config

def create_app(config_class=Config):
    """
    Creates and configures an instance of the Flask application.
    This is the application factory.
    """
    # Create the Flask app instance
    app = Flask(__name__)
    
    # Load the configuration from the Config object
    app.config.from_object(config_class)
    
    # Ensure the instance folder exists (if needed for databases, etc.)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
        
    # --- Register Blueprints ---
    # Blueprints help organize your routes into different modules.
    
    # Import the 'main' blueprint from the routes.py file in the same directory
    from .routes import main as main_blueprint
    
    # Register the blueprint with the app
    app.register_blueprint(main_blueprint)
    
    # You can add more blueprints here as your app grows
    # from .api import api as api_blueprint
    # app.register_blueprint(api_blueprint, url_prefix='/api')

    return app