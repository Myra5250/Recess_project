from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_500_INTERNAL_SERVER_ERROR, HTTP_409_CONFLICT,HTTP_201_CREATED
import validators
from app.models.customer import Customer
from app.extensions import db, bcrypt

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    phone_number = data.get('phone_number')
    password = data.get('password')


    if not name or not email or not phone_number:
        return jsonify({'error':"All feilds are required"}), HTTP_400_BAD_REQUEST

    if Customer.query.filter_by(email=email).first() is not None:
        return jsonify({'message': 'email is already in use'}),  HTTP_409_CONFLICT
    
    if len(password) < 8:
        return jsonify({"error":"Password is too short"}), HTTP_400_BAD_REQUEST
    
    if not validators.email(email):
        return jsonify({"error":"Email is not valid"})
    
    if Customer.query.filter_by(phone_number=phone_number).first() is not None:
        return jsonify({'message': 'phone_number is already in use'}),  HTTP_409_CONFLICT
    
    try:
        hashed_password = bcrypt.generate_password_hash(password)

        new_customer = Customer(name=name, email=email, phone_number=phone_number, password=hashed_password)
        db.session.add(new_customer)
        db.session.commit()

        customer_name = new_customer.get_customer()

        return jsonify({
            'message':customer_name + "has successfully been created as a " + new_customer,
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



