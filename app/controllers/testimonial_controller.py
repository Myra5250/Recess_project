from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_500_INTERNAL_SERVER_ERROR,HTTP_400_BAD_REQUEST, HTTP_200_OK,HTTP_404_NOT_FOUND
from app.models.testimonial import Testimonial
from flask_jwt_extended import jwt_required, get_jwt_identity 
from app.extensions import db

# Blueprint
testimonial = Blueprint('testimonial', __name__, url_prefix='/testimonial')

# Creating testimonial
@testimonial.route('/create', methods=['POST'])
@jwt_required()
def create_testimonial():
    data = request.get_json()
    user_id = get_jwt_identity()
    content = data.get('content')

    # VALIDATIONS
    if content is None:
        return jsonify({'error': 'Content is required'}), HTTP_400_BAD_REQUEST

    testimonial = Testimonial(user_id=user_id, content=content)
    db.session.add(testimonial)
    db.session.commit()

    return jsonify({'message': 'Testimonial created successfully'}), HTTP_200_OK

# Get all testimonials
@testimonial.route('/all', methods=['GET'])
@jwt_required()
def get_all_testimonials():
    try:
        all_testimonials = Testimonial.query.all()
        if not all_testimonials:
            return jsonify({'message': 'No testimonials found'}), HTTP_404_NOT_FOUND

        testimonial_list = []
        for testimonial in all_testimonials:
            testimonial_info = {
                'id': testimonial.id,
                'user_id': testimonial.user_id,
                'content': testimonial.content,
            }
            testimonial_list.append(testimonial_info)

        return jsonify({'testimonials': testimonial_list}), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    
# Get testimonial by ID
@testimonial.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_testimonial_by_id(id):
    try:
        testimonial = Testimonial.query.get(id)
        if not testimonial:
            return jsonify({'message': 'Testimonial not found'}), HTTP_404_NOT_FOUND

        testimonial_info = {
            'id': testimonial.id,
            'user_id': testimonial.user_id,
            'content': testimonial.content,
        }

        return jsonify({'testimonial': testimonial_info}), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    
# Update testimonial
@testimonial.route('/update/<int:id>', methods=['PUT'])
@jwt_required()
def update_testimonial(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), HTTP_400_BAD_REQUEST

    testimonial = Testimonial.query.get(id)
    if not testimonial:
        return jsonify({'error': 'Testimonial not found'}), HTTP_404_NOT_FOUND

    testimonial.content = data.get('content', testimonial.content)

    db.session.commit()

    return jsonify({'message': 'Testimonial updated successfully'}), HTTP_200_OK

# Delete testimonial
@testimonial.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_testimonial(id):
    try:
        testimonial = Testimonial.query.get(id)
        if not testimonial:
            return jsonify({'error': 'Testimonial not found'}), HTTP_404_NOT_FOUND

        db.session.delete(testimonial)
        db.session.commit()

        return jsonify({'message': 'Testimonial deleted successfully'}), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    

