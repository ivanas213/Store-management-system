import os
from datetime import timedelta

#DATABASE_URL = "product_database" if ( "PRODUCTION" in os.environ ) else "localhost"

class Configuration:
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:root@product_database/Product"
    JWT_ACCESS_TOKEN_EXPIRES  = timedelta ( minutes = 60 )
    JWT_SECRET_KEY            = "JWT_SECRET_DEV_KEY"
    JWT_ALGORITHM             = "HS256"

