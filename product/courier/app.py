from flask import Flask, request, jsonify
from models import database, Order, Status
from configuration import Configuration
from flask_migrate import Migrate
from flask_jwt_extended import get_jwt, jwt_required, decode_token, JWTManager
from functools import wraps

# Initialize Flask application and load configuration
application = Flask(__name__)
application.config.from_object(Configuration)

# Initialize database with application and set up migrations
database.init_app(application)
migrate = Migrate(application, database)

# Set up JWT manager for handling authentication
jwt = JWTManager(application)

# Role check decorator to verify user's role in JWT claims
def role_check(role):
    def decorator(function):
        @jwt_required()
        @wraps(function)
        def wrapper(*args, **kwargs):
            # Check if Authorization header is present
            if 'Authorization' not in request.headers:
                return jsonify({"msg": "Missing Authorization Header"}), 401
            
            # Get JWT claims and decode token to verify it
            claims = get_jwt()
            try:
                decode_token(request.headers.get('Authorization').split('Bearer ')[1])
            except Exception as e:
                return jsonify({"msg": "Missing Authorization Header"}), 401
            
            # Check if specified role is in JWT claims
            if role in claims["roles"]:
                return function(*args, **kwargs)
            else:
                return jsonify({"msg": "Missing Authorization Header"}), 401

        return wrapper
    return decorator

# Helper function to check if string is a positive integer
def isPositiveNumber(string):
    try:
        number = int(string)
        return number > 0
    except ValueError:
        return False

# Route to get orders with "CREATED" status for delivery
@application.route("/orders_to_deliver", methods=["GET"])
@role_check("courier")
def orders_to_deliver():
    orders = []
    created_status_id = Status.query.filter_by(name='CREATED').first().statusID
    ord = Order.query.filter_by(statusID=created_status_id)
    
    # Append each order's ID and buyer email to orders list
    for order in ord:
        orders.append({
            "id": order.orderID,
            "email": order.buyer
        })
    
    return jsonify({"orders": orders}), 200

# Route to update order status to "PENDING" for pickup
@application.route("/pick_up_order", methods=["POST"])
@role_check("courier")
def pick_up_order():
    # Check if 'id' field is present in JSON request
    if 'id' not in request.json:
        return jsonify({"message": "Missing order id."}), 400

    id = request.json.get('id')

    # Validate that provided id is a positive number
    if not isPositiveNumber(id):
        return jsonify({"message": "Invalid order id."}), 400

    # Get 'CREATED' status ID and find order by ID
    created_status_id = Status.query.filter_by(name='CREATED').first().statusID
    order = Order.query.get(id)

    # Verify if order exists and has the "CREATED" status
    if not order or order.statusID != created_status_id:
        return jsonify({"message": "Invalid order id."}), 400

    # Update order status to "PENDING" and commit changes
    pending_status_id = Status.query.filter_by(name='PENDING').first().statusID
    order.statusID = pending_status_id
    database.session.commit()
    return ''

# Root route for testing connection
@application.route("/", methods=["GET"])
def index():
    return "Hello world from courier"

# Run the application on specified host and port
if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5003)
