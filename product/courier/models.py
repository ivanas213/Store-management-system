from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy instance for database operations
database = SQLAlchemy()

# ProductQuantity model represents the quantity of each product in an order
class ProductQuantity(database.Model):
    __tablename__ = "productQuantities"
    productQuantityID = database.Column(database.Integer, primary_key=True)  # Primary key
    productID = database.Column(database.Integer, database.ForeignKey("products.productID"), nullable=False)  # Foreign key to products
    quantity = database.Column(database.Integer, nullable=False)  # Quantity of the product
    orderID = database.Column(database.Integer, database.ForeignKey("orders.orderID"), nullable=False)  # Foreign key to orders
    # Relationship to the Order model
    order = database.relationship("Order", back_populates="productQuantities", primaryjoin="ProductQuantity.orderID == Order.orderID")

# ProductCategory model links products to categories
class ProductCategory(database.Model):
    __tablename__ = "productCategories"
    productCategoryId = database.Column(database.Integer, primary_key=True)  # Primary key
    productID = database.Column(database.Integer, database.ForeignKey("products.productID"), nullable=False)  # Foreign key to products
    categoryID = database.Column(database.Integer, database.ForeignKey("categories.categoryID"), nullable=False)  # Foreign key to categories

# Product model represents products with attributes like name and price
class Product(database.Model):
    __tablename__ = "products"
    productID = database.Column(database.Integer, primary_key=True)  # Primary key
    name = database.Column(database.String(256), nullable=False, unique=True)  # Product name
    price = database.Column(database.Float, nullable=False)  # Product price
    # Relationship to Category through ProductCategory association table
    categories = database.relationship("Category", secondary=ProductCategory.__tablename__, back_populates="products")

# Status model represents the status of an order (e.g., 'CREATED', 'PENDING')
class Status(database.Model):
    __tablename__ = "statuses"
    statusID = database.Column(database.Integer, primary_key=True)  # Primary key
    name = database.Column(database.String(256), unique=True, nullable=False)  # Status name
    # Relationship to Order model
    orders = database.relationship("Order", back_populates="status")

# Order model represents an order with details such as price, timestamp, and buyer
class Order(database.Model):
    __tablename__ = "orders"
    orderID = database.Column(database.Integer, primary_key=True)  # Primary key
    price = database.Column(database.Float, nullable=False, default=0.0)  # Total order price
    timestamp = database.Column(database.DateTime, nullable=False)  # Timestamp for the order
    # Relationship to ProductQuantity to track quantities of each product in the order
    productQuantities = database.relationship("ProductQuantity", back_populates="order")
    statusID = database.Column(database.Integer, database.ForeignKey("statuses.statusID"), nullable=False)  # Foreign key to statuses
    # Relationship to Status model
    status = database.relationship("Status", back_populates="orders", primaryjoin="Order.statusID == Status.statusID")
    buyer = database.Column(database.String(256), nullable=False)  # Buyer email or name

# Category model represents categories that group products
class Category(database.Model):
    __tablename__ = "categories"
    categoryID = database.Column(database.Integer, primary_key=True)  # Primary key
    name = database.Column(database.String(256), nullable=False)  # Category name
    # Relationship to Product through ProductCategory association table
    products = database.relationship("Product", secondary=ProductCategory.__tablename__, back_populates="categories")
