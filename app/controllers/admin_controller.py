from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_200_OK, HTTP_404_NOT_FOUND,HTTP_409_CONFLICT,HTTP_201_CREATED
import validators
from app.models.customer import Customer
from app.extensions import db, bcrypt

# Blueprint
admin = Blueprint('admin', __name__, url_prefix='/admin')  

# Creating admin
@admin.route('/create', methods=['POST'])
def create_admin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # VALIDATIONS
    if email is None or password is None:
        return jsonify({'error': 'All fields are required'}), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({'error': 'Invalid email address'}), HTTP_400_BAD_REQUEST

    # Check if admin already exists
    existing_admin = Customer.query.filter_by(email=email).first()
    if existing_admin:
        return jsonify({'error': 'Admin already exists'}), HTTP_409_CONFLICT

    # Create new admin
    new_admin = Customer(email=email, password=bcrypt.generate_password_hash(password).decode('utf-8'))
    db.session.add(new_admin)
    db.session.commit()

    return jsonify({'message': 'Admin created successfully'}), HTTP_201_CREATED

# Get all admins
@admin.route('/all', methods=['GET'])
def get_all_admins():
    try:
        all_admins = Customer.query.all()
        if not all_admins:
            return jsonify({'message': 'No admins found'}), HTTP_404_NOT_FOUND

        admin_list = []
        for admin in all_admins:
            admin_info = {
                'id': admin.id,
                'email': admin.email,
            }
            admin_list.append(admin_info)

        return jsonify({'admins': admin_list}), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    
# Get admin by ID
@admin.route('/<int:id>', methods=['GET'])
def get_admin_by_id(id):
    try:
        admin = Customer.query.get(id)
        if not admin:
            return jsonify({'message': 'Admin not found'}), HTTP_404_NOT_FOUND

        admin_info = {
            'id': admin.id,
            'email': admin.email,
        }

        return jsonify({'admin': admin_info}), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Update admin
@admin.route('/<int:id>', methods=['PUT'])
def update_admin(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), HTTP_400_BAD_REQUEST

    admin = Customer.query.get(id)
    if not admin:
        return jsonify({'error': 'Admin not found'}), HTTP_404_NOT_FOUND

    admin.email = data.get('email', admin.email)
    admin.password = bcrypt.generate_password_hash(data.get('password', admin.password)).decode('utf-8')

    db.session.commit()

    return jsonify({'message': 'Admin updated successfully'}), HTTP_200_OK

# Delete admin
@admin.route('/<int:id>', methods=['DELETE'])
def delete_admin(id):
    try:
        admin = Customer.query.get(id)
        if not admin:
            return jsonify({'error': 'Admin not found'}), HTTP_404_NOT_FOUND

        db.session.delete(admin)
        db.session.commit()

        return jsonify({'message': 'Admin deleted successfully'}), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    
