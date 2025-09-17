import os
from dotenv import load_dotenv

# Find the absolute path of the root directory of the project
basedir = os.path.abspath(os.path.dirname(__file__))

# Load environment variables from the .env file
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    """
    Sets the configuration variables for the Flask application.
    Variables are loaded from an environment file (.env) for security
    and flexibility.
    """
    
    # --- General Configuration ---
    
    # A secret key is required by Flask for security features like session management.
    # It's best practice to load this from an environment variable.
    # A default is provided for ease of development, but it should be
    # replaced with a strong, random key in a production environment.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-should-really-change-this'

    # --- API Keys ---
    
    # The API key for the Groq service. This is loaded directly from the
    # .env file and should NOT be hard-coded here.
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

    # --- File and Model Paths ---
    
    # The path to the folder containing the fine-tuned coder model adapter.
    # This path is relative to the project's root directory.
    CODER_MODEL_PATH = os.path.join(basedir, 'finetuned_model')
    
    # The path to the folder where user-uploaded files will be temporarily stored.
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')