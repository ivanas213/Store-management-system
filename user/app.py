from flask import Flask, request, jsonify
from configuration import Configuration
from user_models import User
from user_models import database
from user_models import UserRole
from user_models import Role
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from flask_migrate import Migrate
from email_validator import validate_email, EmailNotValidError

# Initialize Flask application
application = Flask(__name__)
application.config.from_object(Configuration)  # Load configuration settings
database.init_app(application)  # Initialize database

migrate = Migrate(application, database)  # Set up database migrations

# Route to register a new customer
@application.route("/register_customer", methods=["POST"])
def register_customer():
    forename = request.json.get("forename", "")
    surname = request.json.get("surname", "")
    email = request.json.get("email", "")
    password = request.json.get("password", "")
    
    # Check for missing fields
    if len(forename) == 0:
        return jsonify({"message": "Field forename is missing."}), 400
    if len(surname) == 0:
        return jsonify({"message": "Field surname is missing."}), 400
    if len(email) == 0:
        return jsonify({"message": "Field email is missing."}), 400
    if len(password) == 0:
        return jsonify({"message": "Field password is missing."}), 400

    # Validate email format
    try:
        v = validate_email(email)
        email = v["email"]
    except EmailNotValidError as e:
        return jsonify({"message": "Invalid email."}), 400

    # Check for password length
    if len(password) < 8:
        return jsonify({"message": "Invalid password."}), 400

    # Check if user with this email already exists
    user = User.query.filter_by(email=email).first()
    if user is None:
        # Create new user and assign "customer" role
        new_user = User(forename=forename, surname=surname, email=email, password=password)
        database.session.add(new_user)
        database.session.commit()
        
        new_user_role = UserRole(userID=new_user.userID, roleID=Role.query.filter_by(name="customer").first().roleID)
        database.session.add(new_user_role)
        database.session.commit()
        
        return ''
    else:
        return jsonify({"message": "Email already exists."}), 400

# Route to register a new courier
@application.route("/register_courier", methods=["POST"])
def register_courier():
    forename = request.json.get("forename", "")
    surname = request.json.get("surname", "")
    email = request.json.get("email", "")
    password = request.json.get("password", "")
    
    # Check for missing fields
    if len(forename) == 0:
        return jsonify({"message": "Field forename is missing."}), 400
    if len(surname) == 0:
        return jsonify({"message": "Field surname is missing."}), 400
    if len(email) == 0:
        return jsonify({"message": "Field email is missing."}), 400
    if len(password) == 0:
        return jsonify({"message": "Field password is missing."}), 400

    # Validate email format
    try:
        v = validate_email(email)
        email = v["email"]
    except EmailNotValidError as e:
        return jsonify({"message": "Invalid email."}), 400

    # Check for password length
    if len(password) < 8:
        return jsonify({"message": "Invalid password."}), 400

    # Check if user with this email already exists
    user = User.query.filter_by(email=email).first()
    if user is not None:
        return jsonify({"message": "Email already exists."}), 400

    # Create new user and assign "courier" role
    new_user = User(forename=forename, surname=surname, email=email, password=password)
    database.session.add(new_user)
    database.session.commit()
    
    new_user_role = UserRole(userID=new_user.userID, roleID=Role.query.filter_by(name="courier").first().roleID)
    database.session.add(new_user_role)
    database.session.commit()
    
    return ''

# Initialize JWT for authentication
jwt = JWTManager(application)

# Route to log in a user
@application.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", "")
    password = request.json.get("password", "")
    
    # Check for missing fields
    if len(email) == 0:
        return jsonify({"message": "Field email is missing."}), 400
    if len(password) == 0:
        return jsonify({"message": "Field password is missing."}), 400

    # Validate email format
    try:
        v = validate_email(email)
        email = v["email"]
    except EmailNotValidError as e:
        return jsonify({"message": "Invalid email."}), 400

    # Authenticate user
    user = User.query.filter_by(email=email, password=password).first()
    if user is None:
        return jsonify({"message": "Invalid credentials."}), 400

    # Generate access token with additional user claims
    claims = {
        "forename": user.forename,
        "surname": user.surname,
        "roles": [role.name for role in user.roles]
    }
    access_token = create_access_token(identity=user.email, additional_claims=claims)

    return jsonify(accessToken=access_token)

# Route to delete a user, accessible only to authenticated users
@application.route("/delete", methods=["POST"])
@jwt_required()
def delete():
    if 'Authorization' not in request.headers:
        return jsonify({"msg": "Missing Authorization Header"}), 401

    # Get the current user's email from JWT token
    user_email = get_jwt_identity()
    user = User.query.filter(User.email == user_email).first()

    # If user exists, delete from database
    if user:
        database.session.delete(user)
        database.session.commit()
        return ''
    else:
        return jsonify({"message": "Unknown user."}), 400

# Default route
@application.route("/", methods=["GET"])
def index():
    return "Hello world"

# Run application
if __name__ == '__main__':
    application.run(host='0.0.0.0')
