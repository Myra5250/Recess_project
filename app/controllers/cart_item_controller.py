from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_500_INTERNAL_SERVER_ERROR,HTTP_400_BAD_REQUEST, HTTP_200_OK,HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED,HTTP_409_CONFLICT 
from app.models.cart_item import CartItem
from flask_jwt_extended import jwt_required, get_jwt_identity 
from app.extensions import db, bcrypt
from app.models.cart import Cart

#Blueprint
cart_item = Blueprint('cart_item', __name__, url_prefix='/cart_item')

#Creating cart_items
@cart_item.route('/create', methods =['POST'])
@jwt_required()

def create_cart_item():
    data = request.get_json()
    id = get_jwt_identity()
    quantity = data.get('quantity')
    cart_id = data.get('cart_id')
    product_id = data.get('product.id')

# VALIDATIONS
    if cart_id is None or product_id is None:
        return jsonify({'error': 'All fields are required'}), HTTP_400_BAD_REQUEST
    
    if CartItem.query.filter_by(cart_id=cart_id, product_id=product_id).first() is not None:
        return jsonify({'error': 'Item already exists in cart'}), HTTP_409_CONFLICT

    cart_item = CartItem(user_id=id, cart_id=cart_id, product_id=product_id, quantity=quantity)
    db.session.add(cart_item)
    db.session.commit()

    return jsonify({'message': 'Cart item created successfully'}), HTTP_200_OK

# Get all cart items
@cart_item.route('/all', methods=['GET'])
@jwt_required()
def get_all_cart_items():
    try:

        all_cart_items = CartItem.query.all()
        if not all_cart_items:
            return jsonify({'message': 'No cart items found'}), HTTP_404_NOT_FOUND  
        
        cart_item_request = []

        for cart_item in all_cart_items:
            cart_item_info ={
                'id': cart_item.id,
                'name': cart_item.name,
                'quantity': cart_item.quantity,
    }
        cart_item_request.append(cart_item_info) 

    except Exception as e:
        db.session.rollback()
        return jsonify ({'error':str(e)}),HTTP_500_INTERNAL_SERVER_ERROR
    return jsonify({'cart_items': cart_item_request}), HTTP_200_OK

# Get cart item by ID
@cart_item.route('/<int:cart_item_id>', methods=['GET'])    
@jwt_required()
def get_cart_item_by_id(cart_item_id):  
    try:
        cart_item = CartItem.query.get(cart_item_id)
        if not cart_item:
            return jsonify({'message': 'Cart item not found'}), HTTP_404_NOT_FOUND
        
        cart_item_info = {
            'id': cart_item.id,
            'name': cart_item.name,
            'quantity': cart_item.quantity,
        }
        
        return jsonify({'cart_item': cart_item_info}), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    
# Update cart item
@cart_item.route('/update/<int:cart_item_id>', methods=['PUT'])
@jwt_required()
def update_cart_item(cart_item_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No input data provided'}), HTTP_400_BAD_REQUEST

        cart_item = CartItem.query.get(cart_item_id)
        if not cart_item:
            return jsonify({'error': 'Cart item not found'}), HTTP_404_NOT_FOUND

        cart_item.name = data.get('name', cart_item.name)
        cart_item.quantity = data.get('quantity', cart_item.quantity)

        db.session.commit()

        return jsonify({'message': 'Cart item updated successfully'}), HTTP_200_OK
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

    
# Delete cart item
@cart_item.route('/delete/<int:cart_item_id>', methods=['DELETE'])
@jwt_required()
def delete_cart_item(cart_item_id):
    try:
        cart_item = CartItem.query.get(cart_item_id)
        if not cart_item:
            return jsonify({'error': 'Cart item not found'}), HTTP_404_NOT_FOUND

        db.session.delete(cart_item)
        db.session.commit()

        return jsonify({'message': 'Cart item deleted successfully'}), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    
