"""
Models Package for the Lab Report Agent.

This package contains modules for interacting with the AI models:
- coder_model: Handles the generation of Python code for calculations using a fine-tuned model.
- report_generator: Handles the final report writing using the Groq API.
"""

# Import the main functions from the modules to make them easily accessible.
# This allows you to use 'from models import generate_code' instead of
# 'from models.coder_model import generate_code' in other files like routes.py.
from .coder_model import generate_code
from .report_generator import write_report

# The __all__ variable defines the public API of this package.
# When a user writes 'from models import *', only these names will be imported.
__all__ = [
    'generate_code',
    'write_report'
]