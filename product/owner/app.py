from flask import Flask, request,jsonify
from models import database
from configuration import Configuration
from flask_migrate import Migrate
from models import Product, ProductCategory, Category, Order, Status, ProductQuantity
import io;
import csv;
from sqlalchemy import func
from functools import wraps
from flask_jwt_extended import get_jwt, jwt_required, decode_token, JWTManager
from sqlalchemy import or_, case
def role_check ( role ):
    def decorator ( function ):
        @jwt_required ( )
        @wraps ( function )
        def wrapper ( *args, **kwargs ):
            if 'Authorization' not in request.headers:
                return jsonify({"msg": "Missing Authorization Header"}),401
            claims = get_jwt ( )
            try:
                decode_token(request.headers.get('Authorization').split('Bearer ')[1])
            except Exception as e:
                return jsonify({"msg": "Missing Authorization Header"}),401
                # return jsonify({"msg": "Nije dobro dekodiran"}),401
            if ( role in claims["roles"] ):
                return function ( *args, **kwargs )
            else:
                return jsonify({"msg": "Missing Authorization Header"}),401
                # return jsonify({"msg": "Nije dobra uloga"}),401
        return wrapper
    return decorator



application=Flask(__name__)
application.config.from_object(Configuration)
database.init_app(application)
jwt = JWTManager ( application )

migrate = Migrate ( application, database )
def is_real_positive_number(x):
    try:
        broj = float(x)
        return broj > 0
    except Exception as e:
        return False

@application.route("/update",methods=["POST"])
@role_check("owner")
def update():
    if 'file' not in request.files:
         return jsonify({"message":"Field file is missing."}),400
    print("Usli smo u funkciju")
    content = request.files["file"].stream.read ( ).decode ( "cp1250" )
    stream = io.StringIO ( content )
    reader = csv.reader ( stream )
    stream.seek(0)
    i=0
    for row in reader:
        if(len(row)!=3):
            return jsonify({"message":f"Incorrect number of values on line {i}."}),400
        i+=1
    stream.seek(0)
    i=0
    for row in reader:
        if(not is_real_positive_number(row[2])):
            return jsonify({"message":f"Incorrect price on line {i}."}),400
        i+=1
    stream.seek(0)
    reader = csv.reader(stream)

    for row in reader:
        name=row[1]
        product=Product.query.filter_by(name=name).first()
        if product is not None:
            return jsonify({"message":f"Product {name} already exists."}),400
    stream.seek(0)
    reader = csv.reader(stream)
    for row in reader:
        categories=[]
        categories = row[0].split("|")
        new_product=Product(
            name=row[1],
            price=row[2]
        )
        database.session.add(new_product)
        database.session.commit()
        for t in categories:
            cat=Category.query.filter_by(name=t).first()
            if cat is None:
                cat=Category(
                    name=t
                )
                database.session.add(cat)
                database.session.commit()
            id=cat.categoryID
            new_product_category=ProductCategory(
                productID=new_product.productID,
                categoryID=id
            )
            database.session.add(new_product_category)
            database.session.commit()
    return ''

@application.route("/product_statistics",methods=["GET"])
@role_check("owner")
def product_statistics():
    ret=[]
    # created = database.session.query(Product.name, database.func.sum(ProductQuantity.quantity).label('created_count')) \
    #                  .outerjoin(ProductQuantity).outerjoin(Order).outerjoin(Status) \
    #                  .filter(Status.name != 'COMPLETE') \
    #                  .group_by(Product.name).all()
    # complete = database.session.query(Product.name, database.func.sum(ProductQuantity.quantity).label('complete_count')) \
    #                  .outerjoin(ProductQuantity).outerjoin(Order).outerjoin(Status) \
    #                  .filter(Status.name == 'COMPLETE') \
    #                  .group_by(Product.name).all()
    query = database.session.query(
    Product.name,
    func.sum(case((Status.name != 'COMPLETE', ProductQuantity.quantity), else_=0)).label('created_count') \
     ,func.sum(case((Status.name == 'COMPLETE', ProductQuantity.quantity), else_=0)).label('complete_count') \
     )\
    .outerjoin(ProductQuantity) \
    .outerjoin(Order) \
    .outerjoin(Status) \
    .group_by(Product.name) 
    result=query.all()
    print(str(query))
    # query1 = database.session.query(
    # Product.name,
    # func.sum(ProductQuantity.quantity).label('all_count'))\
    # .join(ProductQuantity) \
    # .join(Order) \
    # .join(Status) \
    # .group_by(Product.name).all()
    # query2 = database.session.query(
    # Product.name,func.sum(ProductQuantity.quantity).label('complete_count')) \
    # .join(ProductQuantity) \
    # .join(Order) \
    # .join(Status) \
    # .filter(Status.name=="COMPLETE")\
    # .group_by(Product.name).all()
    # dict={}
    # for q in query1:
    #     dict[q.name]=q.all_count
    for r in result:
        if r.complete_count>0 or r.created_count>0:
            ret.append(({"name":r.name,"sold":int(r.complete_count),"waiting":int(r.created_count)}))
    return jsonify({"statistics": ret}),200

@application.route("/category_statistics",methods=["GET"])
@role_check("owner")
def category_statistics():
    ret=[]
    # results=database.session.query(Category.name,(database.func.sum(ProductQuantity.quantity)).label('complete_count')).join \
    #                 .join(ProductCategory, categoryID=ProductCategory.categoryID).join(Product).join(ProductQuantity).join(Order).join(Status).filter(Status.name=='complete').group_by(Category.name).order_by \
    #                 (database.func.count(Order.orderID).desc(),Category.name.asc()).all()
    query = database.session.query(
        Category.name,
        func.sum(ProductQuantity.quantity).label('sold_count')
    )\
    .join(ProductCategory)\
    .join(Product)\
    .join(ProductQuantity)\
    .join(Order)\
    .join(Status)\
    .filter(or_(Status.name == 'COMPLETE', Status.name == None))\
    .group_by(Category.name)\
    .order_by(func.sum(ProductQuantity.quantity).desc(), Category.name.asc())
    results=query.all()
    query2=Category.query.order_by(Category.name.asc()).all()
    for result in results:
        ret.append(result.name)
    for r in query2:
        if r.name not in ret:
            ret.append(r.name)
    return jsonify({"statistics":ret}),200

@application.route ( "/", methods = ["GET"] )
def index():
    return "Hello world from owner"

if ( __name__ == '__main__' ):
    application.run(host='0.0.0.0', port=5001, debug=True)
