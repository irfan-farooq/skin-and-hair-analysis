import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'data', 'skinmax.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Firebase
    FIREBASE_KEY_PATH = os.path.join(BASE_DIR, '..', 'serviceAccountKey.json')

    # Weather API
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')