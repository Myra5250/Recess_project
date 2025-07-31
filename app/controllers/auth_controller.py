from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_200_OK,HTTP_500_INTERNAL_SERVER_ERROR, HTTP_409_CONFLICT,HTTP_201_CREATED
import validators
from flask_jwt_extended import create_access_token, create_refresh_token
from app.models.customer import Customer
from app.models.admin import Admin
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db, bcrypt

auth = Blueprint('auth', __name__, url_prefix='/auth')

# Creating admin
@auth.route('/admin/create', methods=['POST'])
def create_admin():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    is_admin = data.get('is_admin', True) # Default to True if not provided



    # VALIDATIONS
    if not name or not email or not password or is_admin is None:
        return jsonify({'error': 'All fields are required'}), HTTP_400_BAD_REQUEST
    
    if not validators.email(email):
        return jsonify({'error': 'Invalid email address'}), HTTP_400_BAD_REQUEST
    
    if Admin.query.filter_by(name=name).first():
        return jsonify({'error': 'name already exists'}), HTTP_409_CONFLICT

    if Admin.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), HTTP_409_CONFLICT
    
    if len(password) < 8:
        return jsonify({'error': 'Password is too short'}), HTTP_400_BAD_REQUEST

    # Check if admin already exists
    admin = Admin.query.filter_by(email=email, is_admin=True).first()
    if admin:
        return jsonify({'error': 'Admin already exists'}), HTTP_409_CONFLICT

    # Create new admin
    new_admin = Admin(name=name,
                      email=email,
                      is_admin=True,
                      password=bcrypt.generate_password_hash(password).decode('utf-8'))
    db.session.add(new_admin)
    db.session.commit()

    return jsonify({'message': 'Admin created successfully'}), HTTP_201_CREATED

#Admin login
@auth.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not email or not password or not name:
        return jsonify({'error':"Email, password, and name are required"}), HTTP_400_BAD_REQUEST

    admin = Admin.query.filter_by(email=email).first()
    if admin is None or not bcrypt.check_password_hash(admin.password, password):
        return jsonify({'error': 'Invalid email or password'}), HTTP_400_BAD_REQUEST

    access_token = create_access_token(identity=str(admin.id), additional_claims={"role": "admin"})
    refresh_token = create_refresh_token(identity=str(admin.id))

    return jsonify({
        'message': f"{admin.name} has successfully logged in",
        'access_token': access_token,
        'refresh_token': refresh_token,
        'admin': {
            'id': admin.id,
            'email': admin.email
        }
    }), HTTP_200_OK

@auth.route('/customer/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    phone_number = data.get('phone_number')
    password = data.get('password')


    if not name or not email or not phone_number or not password:
        return jsonify({'error':"All fields are required"}), HTTP_400_BAD_REQUEST

    if Customer.query.filter_by(email=email).first() is not None:
        return jsonify({'error': 'Email is already in use'}),  HTTP_409_CONFLICT
    
    if len(password) < 8:
        return jsonify({'error': "Password is too short"}), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({'error':"Email is not valid"}), HTTP_400_BAD_REQUEST
    
    if Customer.query.filter_by(phone_number=phone_number).first() is not None:
        return jsonify({'error': 'Phone number is already in use'}),  HTTP_409_CONFLICT

    try:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_customer = Customer(name=name,
                                email=email, 
                                phone_number=phone_number,
                                password=hashed_password,
                                is_admin=False)
        db.session.add(new_customer)
        db.session.commit()

        customer_name = new_customer.get_customer()

        return jsonify({
            'message':f"{customer_name} has successfully been created as a customer",
            'customer':{
                "id":new_customer.id,
                "name":new_customer.name,
                "email":new_customer.email,
                "phone_number":new_customer.phone_number
            }
    
        }), HTTP_201_CREATED
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),HTTP_500_INTERNAL_SERVER_ERROR


@auth.route('/customer/login', methods=['POST'])
def login_customer():
    
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({'error':"Email and password are required"}), HTTP_400_BAD_REQUEST

    customer = Customer.query.filter_by(email=email).first()

   # if customer is None:
      #  return jsonify({'error': 'Invalid email or password'}), HTTP_400_BAD_REQUEST

    if customer:
        correct_password = bcrypt.check_password_hash(customer.password, password)

        if  correct_password:
    
           access_token = create_access_token(identity=str(customer.id))
           refresh_token = create_refresh_token(identity=str(customer.id))

           return jsonify({
              'message': f"{customer.name} has successfully logged in",
               'customer': {
                   "id": customer.id,
                    "name": customer.name,
                    "email": customer.email,
                    "phone_number": customer.phone_number,
                    "access_token": access_token,
                   "refresh_token": refresh_token,
        }
    }), HTTP_200_OK
        

@auth.route("token/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, additional_claims={"role": "customer"})
    return jsonify({"access_token" : access_token})

# This code is part of a Flask application that handles user authentication.
# It provides endpoints for user registration and login, ensuring that user data is validated and securely stored
# and retrieved from a database. The code uses Flask's Blueprint for modularity and includes error handling for various scenarios such as missing fields,
# duplicate entries, and password validation.
# The registration endpoint checks for the presence of required fields, validates the email format, checks for existing users,
# and hashes the password before storing it in the database. The login endpoint verifies the user's credentials
# and returns user information upon successful login.






