import os
from datetime import timedelta


class Configuration:
    # Define the SQLAlchemy URI to connect to the MySQL database
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@product_database/Product"

    # Set the expiration time for JWT access tokens to 60 minutes
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)

    # Define the secret key used for JWT encoding and decoding
    JWT_SECRET_KEY = "JWT_SECRET_DEV_KEY"

    # Specify the algorithm used for encoding JWT tokens
    JWT_ALGORITHM = "HS256"
