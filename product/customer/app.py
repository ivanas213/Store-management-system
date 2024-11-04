from flask import Flask, request, jsonify, json
from models import database, Product, Category, ProductQuantity, Order, Status
from configuration import Configuration
from flask_migrate import Migrate
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager
from sqlalchemy import func
from flask_jwt_extended import get_jwt, jwt_required, decode_token
from functools import wraps

# Initialize Flask application and configuration
application = Flask(__name__)
application.config.from_object(Configuration)

# Set up SQLAlchemy database and migrations
database.init_app(application)
migrate = Migrate(application, database)

# Initialize JWT for authentication
jwt = JWTManager(application)

# Helper function to check if a string represents a positive integer
def isPositiveNumber(string):
    try:
        number = int(string)
        # Check if the number is greater than zero
        if number > 0:
            return True
        else:
            return False
    except ValueError:
        return False

# Decorator to enforce role-based access control
def role_check(role):
    # Decorator function to enforce a specific role
    def decorator(function):
        @jwt_required()  # Require JWT authentication
        @wraps(function)
        def wrapper(*args, **kwargs):
            # Check for Authorization header in the request
            if 'Authorization' not in request.headers:
                return jsonify({"msg": "Missing Authorization Header"}), 401
            # Retrieve JWT claims
            claims = get_jwt()
            try:
                # Decode the token from the Authorization header
                decode_token(request.headers.get('Authorization').split('Bearer ')[1])
            except Exception as e:
                return jsonify({"msg": "Missing Authorization Header"}), 401
                # Return error if token cannot be decoded
                # return jsonify({"msg": "Nije dobro dekodiran"}),401
            # Check if the role is present in claims
            if role in claims["roles"]:
                return function(*args, **kwargs)
            else:
                return jsonify({"msg": "Missing Authorization Header"}), 401
                # Return error if user lacks required role
        return wrapper
    return decorator

@application.route("/search", methods=["GET"])
@role_check("customer")  # Ensure that only customers can access this route
def search():
    # Retrieve search parameters from query string
    product_name = request.args.get('name', '')  # Get name parameter, default to an empty string
    product_category = request.args.get('category', '')  # Get category parameter, default to an empty string
    products = []

    # Search products by name if provided; otherwise, retrieve all products
    if len(product_name) != 0:
        products += Product.query.filter(Product.name.ilike(f"%{product_name}%")).all()
    else:
        products += Product.query.all()

    # Initialize lists to store processed products and categories
    prod = []  # List of unique products based on category match
    ret_products = []  # List to hold final product data for response
    category_names = []  # List to store unique category names matching criteria

    # Iterate through products to match against the category name filter
    for p in products:
        found = False  # Track if a category match is found for the product
        for c in p.categories:
            if product_category in c.name:  # Check if the category matches the search filter
                if not found:
                    found = True  # Mark as found to avoid duplicate addition
                if c.name not in category_names:  # Add category name if unique
                    category_names.append(c.name)
        if found and p not in prod:  # Add product if it matches the category filter
            prod.append(p)

    # Prepare the product data for the response
    for p in prod:
        prod_cat = []  # List to store category names for each product
        for c in p.categories:
            prod_cat.append(c.name)  # Collect category names for the product
        # Extract product details for response
        prod_id = p.productID
        prod_name = p.name
        prod_price = p.price
        ret_products.append({"categories": prod_cat, "id": prod_id, "name": prod_name, "price": prod_price})
    
    # Return the response with matching categories and products
    return jsonify({"categories": category_names, "products": ret_products}), 200

@application.route("/order", methods=["POST"])
@jwt_required()  # Ensure the user is authenticated
@role_check("customer")  # Ensure that only users with the customer role can access this route
def order():
    requests = []
    price = 0.0

    # Check if the requests field is in the JSON payload
    if "requests" not in request.json:
        return jsonify({"message": "Field requests is missing."}), 400

    # Validate that each request entry has a product 'id' field
    for i, r in enumerate(request.json["requests"]):
        if "id" not in r:
            return jsonify({"message": f"Product id is missing for request number {i}."}), 400

    # Validate that each request entry has a quantity field
    for i, r in enumerate(request.json["requests"]):
        if "quantity" not in r:
            return jsonify({"message": f"Product quantity is missing for request number {i}."}), 400

    # Validate that each product id is a positive number
    for i, r in enumerate(request.json["requests"]):
        if not isPositiveNumber(r['id']):
            return jsonify({"message": f"Invalid product id for request number {i}."}), 400

    # Validate that each quantity is a positive number
    for i, r in enumerate(request.json["requests"]):
        if not isPositiveNumber(r['quantity']):
            return jsonify({"message": f"Invalid product quantity for request number {i}."}), 400

    # Validate that each product exists in the database
    for i, r in enumerate(request.json["requests"]):
        if Product.query.filter(Product.productID == r["id"]).first() is None:
            return jsonify({"message": f"Invalid product for request number {i}."}), 400

    # Retrieve the status ID for the CREATED status
    created_status_id = Status.query.filter_by(name='CREATED').first().statusID
    user_email = get_jwt_identity()  # Get the user's email from JWT

    # Create a new order entry
    new_order = Order(
        statusID=created_status_id,
        timestamp=func.current_timestamp(),
        buyer=user_email,
    )
    database.session.add(new_order)
    database.session.commit()

    # Process each product in the order request
    for r in request.json["requests"]:
        id = r['id']
        quantity = r['quantity']
        # Calculate total price by summing up (quantity * price) for each product
        price += quantity * Product.query.filter_by(productID=id).first().price
        # Create an entry in ProductQuantity to associate the product and quantity with the order
        new_product_quantity = ProductQuantity(
            productID=id,
            quantity=quantity,
            order=new_order,
        )
        database.session.add(new_product_quantity)

    # Commit all ProductQuantity entries to the database
    database.session.commit()

    # Update the order with the calculated total price and save it
    new_order.price = price
    database.session.commit()

    # Return the order ID in the response
    return jsonify({"id": new_order.orderID}), 200

@application.route("/status", methods=["GET"])
@jwt_required()  # Ensure the user is authenticated
@role_check("customer")  # Ensure only users with the customer role can access this route
def status():
    user_email = get_jwt_identity()  # Get the user's email from JWT
    orders = Order.query.filter_by(buyer=user_email).all()  # Fetch all orders for the user
    order_array = []  # Initialize list to hold order details

    # Iterate over each order
    for order in orders:
        product_array = []  # Initialize list to hold product details for the order

        # Iterate over each product quantity in the order
        for p in order.productQuantities:
            prod = Product.query.filter_by(productID=p.productID).first()  # Fetch product details
            categories_array = []  # Initialize list to hold category names for the product

            # Collect all categories associated with the product
            for cat in prod.categories:
                categories_array.append(cat.name)

            # Gather details for each product
            name = prod.name
            price = prod.price
            quantity = p.quantity
            # Append product details to the product array
            product_array.append({
                "categories": categories_array,
                "name": name,
                "price": price,
                "quantity": quantity
            })

        # Gather details for the order
        price = order.price
        statusID = order.statusID
        statusName = Status.query.filter_by(statusID=statusID).first().name  # Fetch the status name
        timestamp = order.timestamp
        # Append order details to the order array
        order_array.append({
            "products": product_array,
            "price": price,
            "status": statusName,
            "timestamp": timestamp
        })

    # Return JSON response with the user's orders
    return jsonify({"orders": order_array}), 200

@application.route("/delivered", methods=["POST"])
@role_check("customer")  # Ensure only users with the customer role can access this route
def delivered():
    # Check if id field is present in the request JSON
    if 'id' not in request.json:
        return jsonify({"message": "Missing order id."}), 400

    # Retrieve the order ID from the request JSON
    id = request.json.get('id')

    # Validate if the order ID is a positive number
    if not isPositiveNumber(id):
        return jsonify({"message": "Invalid order id."}), 400

    # Fetch the order by ID
    order = Order.query.get(id)

    # Check if the order exists
    if not order:
        return jsonify({"message": "Invalid order id."}), 400

    # Retrieve the status ID for PENDING
    pending_status_id = Status.query.filter_by(name='PENDING').first().statusID

    # Check if the order status is PENDING
    if order.statusID != pending_status_id:
        return jsonify({"message": "Invalid order id."}), 400

    # Retrieve the status ID for COMPLETE
    delivered_status_id = Status.query.filter_by(name='COMPLETE').first().statusID

    # Update the order status to COMPLETE
    order.statusID = delivered_status_id
    database.session.commit()  # Commit the change to the database

    # Return an empty response with a 200 status code
    return ''

@application.route("/", methods=["GET"])
def index():
    return "Hello world from customer"  # Basic index route for testing

# Run the application on the specified host and port
if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5002)

