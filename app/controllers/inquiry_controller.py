from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_500_INTERNAL_SERVER_ERROR,HTTP_400_BAD_REQUEST, HTTP_200_OK,HTTP_404_NOT_FOUND 
from app.models.inquiry import Inquiry
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

        user_id = get_jwt_identity()
        inquiry = Inquiry(
            user_id=user_id,
            subject=data.get('subject'),
            description=data.get('description')
        )

        db.session.add(inquiry)
        db.session.commit()

        return jsonify({"message": "Inquiry created successfully", "inquiry_id": inquiry.id}), HTTP_200_OK
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Getting an inquiry by ID
@inquiry.route('/<int:inquiry_id>', methods=['GET'])
@jwt_required()
def get_inquiry_by_id(inquiry_id):
    try:
        inquiry = Inquiry.query.get(inquiry_id)
        if not inquiry:
            return jsonify({"message": "Inquiry not found"}), HTTP_404_NOT_FOUND

        return jsonify({
            "id": inquiry.id,
            "user_id": inquiry.user_id,
            "subject": inquiry.subject,
            "description": inquiry.description,
            "created_at": inquiry.created_at.isoformat()
        }), HTTP_200_OK
    except Exception as e:
        return jsonify({"message": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Getting all inquiries
@inquiry.route('/all', methods=['GET'])
@jwt_required()
def get_all_inquiries():
    try:
        user_id = get_jwt_identity()
        inquiries = Inquiry.query.filter_by(user_id=user_id).all()
        return jsonify([{
            "id": inquiry.id,
            "user_id": inquiry.user_id,
            "subject": inquiry.subject,
            "description": inquiry.description,
            "created_at": inquiry.created_at.isoformat()
        } for inquiry in inquiries]), HTTP_200_OK
    except Exception as e:
        return jsonify({"message": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    
# Deleting an inquiry
@inquiry.route('/<int:inquiry_id>', methods=['DELETE'])
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
    
@inquiry.route('/<int:inquiry_id>', methods=['PUT'])
@jwt_required()
def update_inquiry(inquiry_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "No input data provided"}), HTTP_400_BAD_REQUEST

        inquiry = Inquiry.query.get(inquiry_id)
        if not inquiry:
            return jsonify({"message": "Inquiry not found"}), HTTP_404_NOT_FOUND

        inquiry.subject = data.get('subject', inquiry.subject)
        inquiry.description = data.get('description', inquiry.description)

        db.session.commit()

        return jsonify({"message": "Inquiry updated successfully"}), HTTP_200_OK
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    

    