from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_500_INTERNAL_SERVER_ERROR,HTTP_400_BAD_REQUEST, HTTP_200_OK,HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED,HTTP_409_CONFLICT 
from app.models.payment import Payment
from flask_jwt_extended import jwt_required, get_jwt_identity 
from app.extensions import db

# Blueprint
payment = Blueprint('payment', __name__, url_prefix='/payment')

# Creating payment
@payment.route('/create', methods=['POST'])
@jwt_required()
def create_payment():
    data = request.get_json()
    user_id = get_jwt_identity()
    amount = data.get('amount')
    payment_method = data.get('payment_method')

    # VALIDATIONS
    if amount is None or payment_method is None:
        return jsonify({'error': 'All fields are required'}), HTTP_400_BAD_REQUEST

    payment = Payment(user_id=user_id, amount=amount, payment_method=payment_method)
    db.session.add(payment)
    db.session.commit()

    return jsonify({'message': 'Payment created successfully'}), HTTP_200_OK

# Get all payments
@payment.route('/all', methods=['GET'])
@jwt_required()
def get_all_payments():
    try:
        all_payments = Payment.query.all()
        if not all_payments:
            return jsonify({'message': 'No payments found'}), HTTP_404_NOT_FOUND

        payment_list = []
        for payment in all_payments:
            payment_info = {
                'id': payment.id,
                'amount': payment.amount,
                'payment_method': payment.payment_method,
            }
            payment_list.append(payment_info)

        return jsonify({'payments': payment_list}), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Get payment by ID
@payment.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_payment_by_id(id):
    try:
        payment = Payment.query.get(id)
        if not payment:
            return jsonify({'message': 'Payment not found'}), HTTP_404_NOT_FOUND

        payment_info = {
            'id': payment.id,
            'amount': payment.amount,
            'payment_method': payment.payment_method,
        }

        return jsonify({'payment': payment_info}), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    
# Update payment
@payment.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_payment(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), HTTP_400_BAD_REQUEST

    payment = Payment.query.get(id)
    if not payment:
        return jsonify({'error': 'Payment not found'}), HTTP_404_NOT_FOUND

    payment.amount = data.get('amount', payment.amount)
    payment.payment_method = data.get('payment_method', payment.payment_method)

    db.session.commit()

    return jsonify({'message': 'Payment updated successfully'}), HTTP_200_OK

# Delete payment
@payment.route('/<int:id>', methods=['DELETE']) 
@jwt_required()
def delete_payment(id):
    try:
        payment = Payment.query.get(id)
        if not payment:
            return jsonify({'error': 'Payment not found'}), HTTP_404_NOT_FOUND

        db.session.delete(payment)
        db.session.commit()

        return jsonify({'message': 'Payment deleted successfully'}), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
