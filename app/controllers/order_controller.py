from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_500_INTERNAL_SERVER_ERROR,HTTP_400_BAD_REQUEST, HTTP_200_OK,HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED,HTTP_409_CONFLICT 
from app.models.order import Order
from flask_jwt_extended import jwt_required, get_jwt_identity 
from app.extensions import db, bcrypt

order = Blueprint('order', __name__, url_prefix='/order')
@order.route('/create', methods=['POST'])
@jwt_required()

def create_order():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "No input data provided"}), HTTP_400_BAD_REQUEST
        
        user_id = get_jwt_identity()
        order = Order(
            user_id=user_id,
            total_amount=data.get('total_amount'),
            status=data.get('status', 'pending')
        )
        
        db.session.add(order)
        db.session.commit()
        
        return jsonify({"message": "Order created successfully", "order_id": order.id}), HTTP_200_OK
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
