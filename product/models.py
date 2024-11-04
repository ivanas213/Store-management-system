from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy instance
database = SQLAlchemy()

# Model for product quantities in an order
class ProductQuantity(database.Model):
    __tablename__ = "productQuantities"
    productQuantityID = database.Column(database.Integer, primary_key=True)  # Primary key for each product quantity entry
    productID = database.Column(database.Integer, database.ForeignKey("products.productID"), nullable=False)  # Foreign key to the product
    quantity = database.Column(database.Integer, nullable=False)  # Quantity of the product in the order
    orderID = database.Column(database.Integer, database.ForeignKey("orders.orderID"), nullable=False)  # Foreign key to the order
    order = database.relationship("Order", back_populates="productQuantities", primaryjoin="ProductQuantity.orderID == Order.orderID")  # Relationship to the Order model

# Model for associating products with categories
class ProductCategory(database.Model):
    __tablename__ = "productCategories"
    productCategoryId = database.Column(database.Integer, primary_key=True)  # Primary key for each product-category association
    productID = database.Column(database.Integer, database.ForeignKey("products.productID"), nullable=False)  # Foreign key to the product
    categoryID = database.Column(database.Integer, database.ForeignKey("categories.categoryID"), nullable=False)  # Foreign key to the category

# Model representing a product
class Product(database.Model):
    __tablename__ = "products"
    productID = database.Column(database.Integer, primary_key=True)  # Primary key for each product
    name = database.Column(database.String(256), nullable=False, unique=True)  # Unique product name
    price = database.Column(database.Float, nullable=False)  # Price of the product
    categories = database.relationship("Category", secondary=ProductCategory.__tablename__, back_populates="products")  # Many-to-many relationship with categories

# Model representing an order status
class Status(database.Model):
    __tablename__ = "statuses"
    statusID = database.Column(database.Integer, primary_key=True)  # Primary key for each status
    name = database.Column(database.String(256), unique=True, nullable=False)  # Unique status name (e.g., "Pending", "Shipped")
    orders = database.relationship("Order", back_populates="status")  # Relationship to the Order model

# Model representing an order
class Order(database.Model):
    __tablename__ = "orders"
    orderID = database.Column(database.Integer, primary_key=True)  # Primary key for each order
    price = database.Column(database.Float, nullable=False, default=0.0)  # Total price of the order
    timestamp = database.Column(database.DateTime, nullable=False)  # Timestamp for when the order was created
    productQuantities = database.relationship("ProductQuantity", back_populates="order")  # Relationship to ProductQuantity model
    statusID = database.Column(database.Integer, database.ForeignKey("statuses.statusID"), nullable=False)  # Foreign key to the status
    status = database.relationship("Status", back_populates="orders", primaryjoin="Order.statusID == Status.statusID")  # Relationship to the Status model
    buyer = database.Column(database.String(256), nullable=False)  # Information about the buyer

# Model representing a product category
class Category(database.Model):
    __tablename__ = "categories"
    categoryID = database.Column(database.Integer, primary_key=True)  # Primary key for each category
    name = database.Column(database.String(256), nullable=False)  # Name of the category
    products = database.relationship("Product", secondary=ProductCategory.__tablename__, back_populates="categories")  # Many-to-many relationship with products
