import os
from datetime import timedelta

# Configuration class for setting application parameters
class Configuration:
    # Database connection string for SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@product_database/Product"

    # JWT settings for access token expiration and secret key
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)  # Token expiration time set to 60 minutes
    JWT_SECRET_KEY = "JWT_SECRET_DEV_KEY"             # Development secret key for JWT
    JWT_ALGORITHM = "HS256"                           # Algorithm used for signing JWT tokens
