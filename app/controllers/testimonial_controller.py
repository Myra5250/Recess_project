from flask import Blueprint, request, jsonify
from app.models.admin import Admin
from app.status_codes import HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR,HTTP_400_BAD_REQUEST, HTTP_200_OK,HTTP_404_NOT_FOUND
from app.models.testimonial import Testimonial
from flask_jwt_extended import jwt_required, get_jwt_identity 
from app.extensions import db

# Blueprint
testimonial = Blueprint('testimonial', __name__, url_prefix='/testimonial')

# Creating testimonial
@testimonial.route('/create', methods=['POST'])
@jwt_required()

def create_testimonial():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"message": "No input data provided"}), HTTP_400_BAD_REQUEST
        
        current_user_id = get_jwt_identity()
        testimonial = Testimonial(
            id=current_user_id,
            customer_name=data.get('customer_name'),
            content=data.get('content', '')
        
        )

        db.session.add(testimonial)
        db.session.commit()

        return jsonify({"message": "Testimonial created successfully", "testimonial_id": testimonial.id}), HTTP_200_OK
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


# Delete testimonial
@testimonial.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_testimonial(id):
    try:
        testimonial = Testimonial.query.get(id)
        current_user_id = get_jwt_identity()
        current_admin = Admin.query.get(current_user_id)

        if not current_admin:
            return jsonify({'message': 'Admins only'}), HTTP_401_UNAUTHORIZED

        if not testimonial:
            return jsonify({'message': 'Testimonial not found'}), HTTP_404_NOT_FOUND
        
        db.session.delete(testimonial)
        db.session.commit()

        return jsonify({'message': 'Testimonial deleted successfully'}), HTTP_200_OK
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    

