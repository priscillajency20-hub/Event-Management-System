import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Just a random key for security
    SECRET_KEY = "my_super_secret_final_project_key" 
    
    # THIS IS THE FIX: We use SQLite instead of MySQL
    # It will create a file named 'final_project.db' in your folder automatically.
    SQLALCHEMY_DATABASE_URI = "sqlite:///final_project.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False