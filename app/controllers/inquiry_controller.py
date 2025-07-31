from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_401_UNAUTHORIZED,HTTP_400_BAD_REQUEST, HTTP_200_OK,HTTP_404_NOT_FOUND 
from app.models.inquiry import Inquiry
from app.models.customer import Customer
from flask_jwt_extended import jwt_required, get_jwt_identity 
from app.extensions import db

inquiry = Blueprint('inquiry', __name__, url_prefix='/inquiry')

# Creating a new inquiry
@inquiry.route('/create', methods=['POST'])
@jwt_required()
def create_inquiry():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "No input data provided"}), HTTP_400_BAD_REQUEST

        current_user_id = get_jwt_identity()
        current_customer = Customer.query.get(current_user_id) 
         
        if not current_customer:
            return jsonify({"message": "Unauthorized user"}), HTTP_401_UNAUTHORIZED
        
        inquiry = Inquiry(
            id=id,
            name=data.get('name'),
            email=data.get('email'),
            message=data.get('message'),
            timestamp=data.get('timestamp')

        )

        db.session.add(inquiry)
        db.session.commit()

        return jsonify({"message": "Inquiry created successfully", "inquiry_id": inquiry.id}), HTTP_200_OK
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Updating an inquiry  
@inquiry.route('/update/<int:inquiry_id>', methods=['PUT'])
@jwt_required()
def update_inquiry(inquiry_id):
    try:
        data = request.get_json()
        inquiry = Inquiry.query.get(inquiry_id)

        current_user_id = get_jwt_identity()
        current_customer = Customer.query.get(current_user_id)

        if not current_customer:
            return jsonify({"message": "Unauthorized user"}), HTTP_401_UNAUTHORIZED

        if not inquiry:
            return jsonify({"message": "Inquiry not found"}), HTTP_404_NOT_FOUND

        inquiry.name = data.get('name', inquiry.name)
        inquiry.email = data.get('email', inquiry.email)
        inquiry.message = data.get('message', inquiry.message)
        inquiry.timestamp = data.get('timestamp', inquiry.timestamp)

        db.session.commit()

        return jsonify({"message": "Inquiry updated successfully"}), HTTP_200_OK
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    

# Deleting an inquiry
@inquiry.route('/delete/<int:inquiry_id>', methods=['DELETE'])
@jwt_required()
def delete_inquiry(inquiry_id):
    try:
        inquiry = Inquiry.query.get(inquiry_id)
        if not inquiry:
            return jsonify({"message": "Inquiry not found"}), HTTP_404_NOT_FOUND

        db.session.delete(inquiry)
        db.session.commit()

        return jsonify({"message": "Inquiry deleted successfully"}), HTTP_200_OK
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR




    