from flask import Flask
from flask_cors import CORS
from app.extensions import db, migrate, jwt,bcrypt
from app.controllers.auth_controller import auth
from app.controllers.admin_controller import admin
from app.controllers.customer_controller import customer
from app.controllers.category_controller import category
from app.controllers.product_controller import product
from app.controllers.inquiry_controller import inquiry
from app.controllers.testimonial_controller import testimonial 

# This is the application factory function
# It creates and configures the Flask application instance
def create_app():  
    app = Flask(__name__)#It gets its value depending on how we execute the containing script
    app.config.from_object("config.Config") #configuration comes in first
    
    db.init_app(app) # then the db
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:3000", "http://127.0.0.1:5000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    }, supports_credentials=True)
    migrate.init_app(app, db) #then we migrate 
    jwt.init_app(app) 
    bcrypt.init_app(app)

    # Registering models
    from app.models.admin import Admin
    from app.models.customer import Customer
    from app.models.category import Category
    from app.models.product import Product
    from app.models.inquiry import Inquiry
    from app.models.testimonial import Testimonial

    #registering blue prints
    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(customer)
    app.register_blueprint(category)
    app.register_blueprint(product)
    app.register_blueprint(inquiry)
    app.register_blueprint(testimonial)

   #index route
    @app.route('/') 
    def index():
        return"Welcome to CAROLINE WAYS LTD backend design"

    return app