from flask import Blueprint, request, jsonify
from app.models.customer import Customer
from app.models.admin import Admin
from app.status_codes import HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR,HTTP_400_BAD_REQUEST, HTTP_200_OK,HTTP_404_NOT_FOUND 
from app.models.product import Product
from flask_jwt_extended import jwt_required, get_jwt_identity 
from app.extensions import db

# Blueprint
product = Blueprint('product', __name__, url_prefix='/product')

# Creating product
@product.route('/create', methods=['POST'])
@jwt_required()
def create_product():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"message": "No input data provided"}), HTTP_400_BAD_REQUEST
        
        current_user_id = get_jwt_identity()
        current_admin = Admin.query.get(current_user_id)

        if not current_admin:
            return jsonify({"message": "Unauthorized user"}), HTTP_401_UNAUTHORIZED

        product = Product(
            name=data.get('name'),
            description=data.get('description', ''),
            stock=data.get('stock', 0)
        )

        db.session.add(product)
        db.session.commit()

        return jsonify({"message": "Product created successfully", "product_id": product.id}), HTTP_200_OK
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Get all products
@product.route('/get/all', methods=['GET'])
@jwt_required()
def get_all_products():
    try:
        all_products = Product.query.all()
        current_user_id = get_jwt_identity()
        current_customer = Customer.query.get(current_user_id)

        if not current_customer:
            return jsonify({'message': 'Unauthorized user'}), HTTP_401_UNAUTHORIZED
        
        if not all_products:
            return jsonify({'message': 'No products found'}), HTTP_404_NOT_FOUND
        
        product_list = []
        for product in all_products:
            product_info = {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'stock': product.stock,
            }
            product_list.append(product_info)

        return jsonify({'products': product_list}), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    

# Update product
@product.route('/update/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    data = request.get_json()
    current_user_id = get_jwt_identity()
    current_admin = Admin.query.get(current_user_id)

    if not current_admin or not current_admin.is_admin:
        return jsonify({'error': 'Admins only'}), HTTP_401_UNAUTHORIZED
    
    if not data:
        return jsonify({'error': 'No input data provided'}), HTTP_400_BAD_REQUEST

    product = Product.query.get(id)
    if not product:
        return jsonify({'error': 'Product not found'}), HTTP_404_NOT_FOUND

    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.stock = data.get('stock', product.stock)

    db.session.commit()

    return jsonify({'message': 'Product updated successfully'}), HTTP_200_OK

# Delete product
@product.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    current_user_id = get_jwt_identity()
    current_admin = Admin.query.get(current_user_id)

    if not current_admin or not current_admin.is_admin:
        return jsonify({'error': 'Admins only'}), HTTP_401_UNAUTHORIZED

    product = Product.query.get(id)
    if not product:
        return jsonify({'error': 'Product not found'}), HTTP_404_NOT_FOUND

    db.session.delete(product)
    db.session.commit()

    return jsonify({'message': 'Product deleted successfully'}), HTTP_200_OK
    

