from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.status_codes import HTTP_200_OK, HTTP_201_CREATED,HTTP_400_BAD_REQUEST,HTTP_401_UNAUTHORIZED
from app.models.category import Category
from app.models.admin import Admin

category = Blueprint('category', __name__, url_prefix='/categories')

#creating category
@category.route('/create', methods=['POST'])
@jwt_required()
def create_category():
    data = request.get_json()

    if not data:
        return jsonify({'message': 'Invalid input'}), HTTP_400_BAD_REQUEST

    admin = Admin.query.filter_by(id=get_jwt_identity()).first()
    
    if admin.role != 'admin':
        return jsonify({'message': 'Only admins can create categories'}), HTTP_401_UNAUTHORIZED

    try:
        category = Category(
            name=data.get('name'),
            description=data.get('description')
        )
        db.session.add(category)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error creating category', 'error': str(e)}), HTTP_400_BAD_REQUEST
    return jsonify({'message': 'Category created', 'id': category.id}), HTTP_201_CREATED


#getting categories
@category.route('/all', methods=['GET'])
@jwt_required()
def get_all_categories():
    try:
        categories = Category.query.all()
        if not categories:
            return jsonify({'message': 'No categories found'}), HTTP_200_OK
        
        current_user_id = get_jwt_identity()
        current_admin = Admin.query.get(current_user_id)

        if not current_admin or not current_admin.is_admin:
            return jsonify({'error': 'Admins only'}), HTTP_401_UNAUTHORIZED

        category_list = []
        for category in categories:
            category_info = {
                'id': category.id,
                'name': category.name,
                'description': category.description
            }
            category_list.append(category_info)

        return jsonify({'categories': category_list}), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_400_BAD_REQUEST


#updating category
@category.route('/update/<int:id>', methods=['PUT'])
@jwt_required()
def update_category(id):
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Invalid input'}), HTTP_400_BAD_REQUEST
    
    current_user_id = get_jwt_identity()
    current_admin = Admin.query.get(current_user_id)

    if not current_admin or not current_admin.is_admin:
        return jsonify({'message': 'Only admins can update categories'}), HTTP_401_UNAUTHORIZED

    category = Category.query.get_or_404(id)

    if 'name' in data:
        category.name = data['name']
    if 'description' in data:
        category.description = data['description']

    try:
        db.session.commit()
        return jsonify({'message': 'Category updated successfully', 'category': {
            'id': category.id,
            'name': category.name,
            'description': category.description
        }}), HTTP_200_OK
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating category', 'error': str(e)}), HTTP_400_BAD_REQUEST

#deleting category
@category.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_category(id):
    current_user_id = get_jwt_identity()
    current_admin = Admin.query.get(current_user_id)

    if not current_admin or not current_admin.is_admin:
        return jsonify({'message': 'Only admins can delete categories'}), HTTP_401_UNAUTHORIZED

    category = Category.query.get_or_404(id)

    try:
        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': 'Category deleted successfully'}), HTTP_200_OK
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error deleting category', 'error': str(e)}), HTTP_400_BAD_REQUEST
