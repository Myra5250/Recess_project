from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_500_INTERNAL_SERVER_ERROR,HTTP_400_BAD_REQUEST, HTTP_200_OK,HTTP_404_NOT_FOUND 
from app.models.product import Product
from flask_jwt_extended import jwt_required, get_jwt_identity 
from app.extensions import db

# Blueprint
product = Blueprint('product', __name__, url_prefix='/product')

# Creating product
@product.route('/create', methods=['POST'])
@jwt_required()
def create_product():
    data = request.get_json()
    user_id = get_jwt_identity()
    name = data.get('name')
    price = data.get('price')

    # VALIDATIONS
    if name is None or price is None:
        return jsonify({'error': 'All fields are required'}), HTTP_400_BAD_REQUEST

    product = Product(user_id=user_id, name=name, price=price)
    db.session.add(product)
    db.session.commit()

    return jsonify({'message': 'Product created successfully'}), HTTP_200_OK

# Get all products
@product.route('/all', methods=['GET'])
@jwt_required()
def get_all_products():
    try:
        all_products = Product.query.all()
        if not all_products:
            return jsonify({'message': 'No products found'}), HTTP_404_NOT_FOUND

        product_list = []
        for product in all_products:
            product_info = {
                'id': product.id,
                'name': product.name,
                'price': product.price,
            }
            product_list.append(product_info)

        return jsonify({'products': product_list}), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    
# Get product by ID
@product.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_product_by_id(id):
    try:
        product = Product.query.get(id)
        if not product:
            return jsonify({'message': 'Product not found'}), HTTP_404_NOT_FOUND

        product_info = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
        }

        return jsonify({'product': product_info}), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    
# Update product
@product.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), HTTP_400_BAD_REQUEST

    product = Product.query.get(id)
    if not product:
        return jsonify({'error': 'Product not found'}), HTTP_404_NOT_FOUND

    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)

    db.session.commit()

    return jsonify({'message': 'Product updated successfully'}), HTTP_200_OK

# Delete product
@product.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    try:
        product = Product.query.get(id)
        if not product:
            return jsonify({'error': 'Product not found'}), HTTP_404_NOT_FOUND

        db.session.delete(product)
        db.session.commit()

        return jsonify({'message': 'Product deleted successfully'}), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    

