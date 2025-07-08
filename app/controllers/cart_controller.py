from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_500_INTERNAL_SERVER_ERROR,HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_201_CREATED,HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED,HTTP_409_CONFLICT 
from app.models.cart import Cart
from flask_jwt_extended import jwt_required, get_jwt_identity 
from app.extensions import db, bcrypt  
from app.models.cart_item import CartItem

#Blueprint
cart = Blueprint('cart', __name__, url_prefix='/cart')

#Creating carts
@cart.route('/create', methods =['POST'])
@jwt_required()

def create_cart():
    data = request.get_json()
    id = get_jwt_identity()
    created_at = data.get('created_at')

    if Cart.query.filter_by(id=id).first() is not None:
         return jsonify({"error":"Cart id already exists"}),HTTP_409_CONFLICT

    try:
        #creating a new cart
        new_cart = cart(id=id, created_at=created_at) 
        db.session.add(new_cart)
        db.session.commit()

        return jsonify({
            'message': id + 'has been successfully created as a' + new_cart,
                'user': {
                'id' : new_cart.id,
                'created_at' : new_cart.created_at,
                }
        }),HTTP_201_CREATED
    
    except Exception as e:
        db.session.rollback()
        return jsonify ({'error':str(e)}),HTTP_500_INTERNAL_SERVER_ERROR
    
# Get all carts
@cart.route('/all', methods=['GET'])
@jwt_required()
def get_all_carts():
    try:
        carts = Cart.query.all()
        if not carts:
            return jsonify({'message': 'No carts found'}), HTTP_404_NOT_FOUND

        cart_list = []
        for cart in carts:
            cart_info = {
                'id': cart.id,
                'created_at': cart.created_at,
            }
            cart_list.append(cart_info)

        return jsonify({'carts': cart_list}), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Get cart by ID
@cart.route('/<int:cart_id>', methods=['GET'])
@jwt_required()
def get_cart_by_id(cart_id):
    try:
        cart = Cart.query.get(cart_id)
        if not cart:
            return jsonify({'message': 'Cart not found'}), HTTP_404_NOT_FOUND

        cart_info = {
            'id': cart.id,
            'created_at': cart.created_at,
        }

        return jsonify({'cart': cart_info}), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    
# Update cart
@cart.route('/update/<int:cart_id>', methods=['PUT'])
@jwt_required()
def update_cart(cart_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), HTTP_400_BAD_REQUEST

    cart = Cart.query.get(cart_id)
    if not cart:
        return jsonify({'error': 'Cart not found'}), HTTP_404_NOT_FOUND

    cart.created_at = data.get('created_at', cart.created_at)

    db.session.commit()

    return jsonify({'message': 'Cart updated successfully'}), HTTP_200_OK

# Delete cart
@cart.route('/delete/<int:cart_id>', methods=['DELETE'])
@jwt_required()
def delete_cart(cart_id):
    try:
        cart = Cart.query.get(cart_id)
        if not cart:
            return jsonify({'error': 'Cart not found'}), HTTP_404_NOT_FOUND

        db.session.delete(cart)
        db.session.commit()

        return jsonify({'message': 'Cart deleted successfully'}), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
