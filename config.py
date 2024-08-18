"""
This module contains configuration settings for the application.

It loads environment variables from a .env file (if it exists) or from the system environment.
It also defines configuration settings for the database, Flask app, and Marvel API.
"""

from os import environ, path

from dotenv import load_dotenv


class Config:
    """Set application configuration variables from environment file."""

    # Load the environment file, if it exists
    dotenv_path = path.join(path.dirname(__file__), ".env")
    if path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    # Get the environment from the .env file
    ENVIRONMENT = environ.get("ENVIRONMENT", "development")

    # Set the environment specific variables
    if ENVIRONMENT == "production":
        DEBUG = False
        TESTING = False
        DATABASE_URI = environ.get("PROD_DATABASE_URI")
    else:
        DEBUG = True
        TESTING = True
        DATABASE_URI = environ.get("DEV_DATABASE_URI")

    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = environ.get("SECRET_KEY", "very_hard_to_guess-secret-key")

    MARVEL_API_PUBLIC_KEY = environ.get("MARVEL_API_PUBLIC_KEY")
    MARVEL_API_PRIVATE_KEY = environ.get("MARVEL_API_PRIVATE_KEY")
