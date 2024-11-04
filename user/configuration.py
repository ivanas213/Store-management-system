import os
from datetime import timedelta

# Configuration class for application settings
class Configuration:
    # Database URI - Connects to MySQL database for 'User' service
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@user_database:3306/User"

    # JWT (JSON Web Token) configuration
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)  # Access token expiry time set to 60 minutes
    JWT_SECRET_KEY = "JWT_SECRET_DEV_KEY"  # Secret key used for encoding JWT tokens
    JWT_ALGORITHM = "HS256"  # Algorithm used for token encoding (HS256 - HMAC with SHA-256)

    # SQLAlchemy settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disables SQLAlchemy modification tracking (improves performance)
    SQLALCHEMY_ECHO = True  # Enables logging of SQL statements for debugging purposes
