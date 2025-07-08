from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_500_INTERNAL_SERVER_ERROR,HTTP_400_BAD_REQUEST, HTTP_200_OK,HTTP_404_NOT_FOUND 
from app.models.order_item import OrderItem
from flask_jwt_extended import jwt_required, get_jwt_identity 
from app.extensions import db

#Blueprint
order_item = Blueprint('order_item', __name__, url_prefix='/order_item')

#Creating order_items
@order_item.route('/create', methods =['POST'])
@jwt_required()
def create_order_item():
    data = request.get_json()
    user_id = get_jwt_identity()
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    # VALIDATIONS
    if product_id is None or quantity is None:
        return jsonify({'error': 'All fields are required'}), HTTP_400_BAD_REQUEST

    order_item = OrderItem(user_id=user_id, product_id=product_id, quantity=quantity)
    db.session.add(order_item)
    db.session.commit()

    return jsonify({'message': 'Order item created successfully'}), HTTP_200_OK

# Get all order items
@order_item.route('/all', methods=['GET'])
@jwt_required()
def get_all_order_items():
    try:
        all_order_items = OrderItem.query.all()
        if not all_order_items:
            return jsonify({'message': 'No order items found'}), HTTP_404_NOT_FOUND

        order_item_list = []
        for item in all_order_items:
            order_item_info = {
                'id': item.id,
                'name': item.name,
                'quantity': item.quantity,
            }
            order_item_list.append(order_item_info)

        return jsonify({'order_items': order_item_list}), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Get order item by ID
@order_item.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_order_item_by_id(id):
    try:
        order_item = OrderItem.query.get(id)
        if not order_item:
            return jsonify({'message': 'Order item not found'}), HTTP_404_NOT_FOUND

        order_item_info = {
            'id': order_item.id,
            'name': order_item.name,
            'quantity': order_item.quantity,
        }

        return jsonify({'order_item': order_item_info}), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    
# Update order item
@order_item.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_order_item(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), HTTP_400_BAD_REQUEST

    order_item = OrderItem.query.get(id)
    if not order_item:
        return jsonify({'error': 'Order item not found'}), HTTP_404_NOT_FOUND

    order_item.name = data.get('name', order_item.name)
    order_item.quantity = data.get('quantity', order_item.quantity)

    db.session.commit()

    return jsonify({'message': 'Order item updated successfully'}), HTTP_200_OK

# Delete order item
@order_item.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_order_item(id):
    try:
        order_item = OrderItem.query.get(id)
        if not order_item:
            return jsonify({'error': 'Order item not found'}), HTTP_404_NOT_FOUND

        db.session.delete(order_item)
        db.session.commit()

        return jsonify({'message': 'Order item deleted successfully'}), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

