import os
from datetime import timedelta

# Configuration class to store database and JWT settings
class Configuration:
    # URI for connecting to the MySQL database with SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@product_database/Product"
    
    # Expiration time for JWT access tokens set to 60 minutes
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)
    
    # Secret key for encoding JWTs
    JWT_SECRET_KEY = "JWT_SECRET_DEV_KEY"
    
    # Algorithm used for JWT encoding
    JWT_ALGORITHM = "HS256"
