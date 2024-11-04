from flask_jwt_extended import get_jwt, verify_jwt_in_request, jwt_required
from functools import wraps
from flask import jsonify

# Decorator to check if a user has a specific role
def role_check(role):
    def decorator(function):
        # Ensure user is authenticated before executing the function
        @jwt_required()
        @wraps(function)
        def wrapper(*args, **kwargs):
            claims = get_jwt()  # Get JWT claims from the token
            if role in claims["roles"]:  # Check if the required role is in the user's roles
                return function(*args, **kwargs)
            else:
                # Return unauthorized message if the role is missing
                return jsonify({"msg": "Missing Authorization Header"}), 401

        return wrapper

    return decorator
