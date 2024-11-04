from flask_jwt_extended import get_jwt
from flask_jwt_extended import verify_jwt_in_request 
from flask_jwt_extended import jwt_required
from flask import jsonify
from functools import wraps


def role_check ( role ):
    def decorator ( function ):
        @jwt_required ( )
        @wraps ( function )
        def wrapper ( *args, **kwargs ):
            claims = get_jwt ( )
            if ( role in claims["roles"] ):
                return function ( *args, **kwargs )
            else:
                return jsonify({"msg": "Missing Authorization Header"}),401


        return wrapper

    return decorator
