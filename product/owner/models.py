from flask_sqlalchemy import SQLAlchemy

database=SQLAlchemy()
# class OrderProduct(database.Model):
#     __tablename__="orderProducts"
#     orderProductID=database.Column(database.Integer,primary_key=True)
#     productID=database.Column(database.Integer, database.ForeignKey("productQuantities.productID"),nullable=False)
#     orderID=database.Column(database.Integer, database.ForeignKey("orders.orderID"),nullable=False)

class ProductQuantity(database.Model):
    __tablename__="productQuantities"
    productQuantityID=database.Column(database.Integer, primary_key=True)
    productID=database.Column(database.Integer,database.ForeignKey("products.productID"),nullable=False)
    quantity=database.Column(database.Integer, nullable=False)
    # orders=database.relationship("OrderProduct",secondary=OrderProduct.__tablename__,back_populates="productQuantities")
    # order=database.Column(database.Integer, database.ForeignKey("orders.orderID"), nullable=False)
    # order=database.relationship("Order",back_populates="productQuantities")
    orderID = database.Column(database.Integer, database.ForeignKey("orders.orderID"), nullable=False)
    order = database.relationship("Order", back_populates="productQuantities", primaryjoin="ProductQuantity.orderID == Order.orderID")

class ProductCategory(database.Model):
    __tablename__="productCategories"
    productCategoryId=database.Column(database.Integer,primary_key=True)
    productID=database.Column(database.Integer, database.ForeignKey("products.productID"),nullable=False)
    categoryID=database.Column(database.Integer, database.ForeignKey("categories.categoryID"),nullable=False)

class Product(database.Model):
    __tablename__="products"
    productID=database.Column(database.Integer, primary_key=True)
    name=database.Column(database.String(256),nullable=False,unique=True)
    price=database.Column(database.Float,nullable=False)
    categories=database.relationship("Category",secondary=ProductCategory.__tablename__,back_populates="products")

class Status(database.Model):
    __tablename__="statuses"
    statusID=database.Column(database.Integer, primary_key=True)
    name=database.Column(database.String(256),unique=True,nullable=False)
    orders = database.relationship ( "Order", back_populates = "status")

class Order(database.Model):
    __tablename__="orders"
    orderID=database.Column(database.Integer, primary_key=True)
    # products=database.relationship("ProductQuantity",secondary=OrderProduct.__tablename__,back_populates="orders")
    # products=database.relationship("ProductQuantity",back_populates="orders")
    price=database.Column(database.Float, nullable=False,default=0.0)
    #status=database.Column(database.Integer,database.ForeignKey("statuses.statusID"),nullable=False)
    timestamp=database.Column(database.DateTime, nullable=False)
    productQuantities = database.relationship("ProductQuantity", back_populates="order")
    statusID=database.Column(database.Integer,database.ForeignKey("statuses.statusID"),nullable=False)
    status = database.relationship("Status", back_populates="orders", primaryjoin="Order.statusID == Status.statusID")
    buyer=database.Column(database.String(256),nullable=False)


class Category(database.Model):
    __tablename__="categories"
    categoryID=database.Column(database.Integer,primary_key=True)
    name=database.Column(database.String(256),nullable=False)
    products=database.relationship("Product",secondary=ProductCategory.__tablename__,back_populates="categories")






    

