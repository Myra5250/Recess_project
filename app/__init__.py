from flask import Flask
from app.extensions import db, migrate, jwt,bcrypt
from app.controllers.customer_controller import customer
from app.controllers.auth_controller import auth


def create_app():  
    app = Flask(__name__)#It gets its value depending on how we execute the containing script
    app.config.from_object("config.Config") #configuration comes in first
    
    db.init_app(app) # then the db
    migrate.init_app(app, db) #then we migrate 
    jwt.init_app(app) 
    bcrypt.init_app(app)

    # Registering models
    from app.models.admin import Admin
    from app.models.cart_item import CartItem
    from app.models.cart import Cart
    from app.models.category import Category
    from app.models.customer import Customer
    from app.models.inquiry import Inquiry
    from app.models.order_item import OrderItem
    from app.models.order import Order
    from app.models.payment import Payment
    from app.models.product import Product
    from app.models.testimonial import Testimonial

    #registering blue prints
    app.register_blueprint(auth)

   #index route
    @app.route('/') 
    def index():
        return"Welcome to CAROLINE WAYS LTD backend design"

    return app