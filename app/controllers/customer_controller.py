from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_500_INTERNAL_SERVER_ERROR,HTTP_400_BAD_REQUEST, HTTP_200_OK,HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED,HTTP_409_CONFLICT 
from app.models.customer import Customer
from app.models.admin import Admin
from flask_jwt_extended import jwt_required, get_jwt_identity 
from app.extensions import db, bcrypt  

customer =Blueprint('customer', __name__, url_prefix='/auth')

@customer.get('customer/get_all', endpoint='get_all_customers')
@jwt_required()
def get_all_customers():
    try:
        current_customer = get_jwt_identity()
        current_customer = Admin.query.get(current_customer)
        if not current_customer or not current_customer.is_admin:
            return jsonify({'error': 'Admins only'}), HTTP_401_UNAUTHORIZED
    
        all_customers = Customer.query.all()
        customers_data = []
        for customer in all_customers:
            customer_info = {
                'id': customer.id,
                'name': customer.name,
                'email': customer.email,
                'phone_number': customer.phone_number
                # Do NOT return password for security!
            }
            customers_data.append(customer_info)

        return jsonify({
            'message': 'All customers retrieved successfully',
            'customers': customers_data
        }), HTTP_200_OK
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR   
    
    
#get customer by id
@customer.get('/customer/<int:id>' ,  endpoint='get_customer_by_id')  
@jwt_required()
def get_customer_by_id(id):
    
    try:
        
            customer = Customer.query.filter_by(id = id).first() # Querying the database for the customer with the specified id
        
            if not customer:
                return jsonify({'message': 'customer does not exist'}), HTTP_404_NOT_FOUND
        
            return jsonify({
                'message':'Customer details retrieved successfully',
                'customer': {
                        'id' : customer.id,
                        'name' : customer.name,
                        'email' : customer.email,
                        'phone_number' : customer.phone_number
                    
            }
            }), HTTP_200_OK 

    except Exception as e:
        return jsonify({
            'error': str(e)
            }), HTTP_500_INTERNAL_SERVER_ERROR
    
#update customer details
@customer.put('/customer/<int:id>', endpoint='update_customer')
@jwt_required()
def update_customer(id):
    try:
        current_customer = get_jwt_identity()
        current_customer = Admin.query.get(current_customer)
        if not current_customer or not current_customer.is_admin:
            return jsonify({'error': 'Admins only'}), HTTP_401_UNAUTHORIZED

        customer = Customer.query.get(id)
        if not customer:
            return jsonify({'message': 'Customer does not exist'}), HTTP_404_NOT_FOUND

        data = request.get_json()
        customer.name = data.get('name', customer.name)
        customer.email = data.get('email', customer.email)
        customer.phone_number = data.get('phone_number', customer.phone_number)

        db.session.commit()

        return jsonify({
            'message': 'Customer details updated successfully',
            'customer': {
                'id': customer.id,
                'name': customer.name,
                'email': customer.email,
                'phone_number': customer.phone_number
            }
        }), HTTP_200_OK
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

#delete customer
@customer.delete('/customer/<int:id>', endpoint='delete_customer')
@jwt_required()
def delete_customer(id):
    try:
        current_customer = get_jwt_identity()
        current_customer = Admin.query.get(current_customer)
        if not current_customer or not current_customer.is_admin:
            return jsonify({'error': 'Admins only'}), HTTP_401_UNAUTHORIZED

        customer = Customer.query.get(id)
        if not customer:
            return jsonify({'message': 'Customer does not exist'}), HTTP_404_NOT_FOUND

        db.session.delete(customer)
        db.session.commit()

        return jsonify({
            'message': 'Customer deleted successfully'
        }), HTTP_200_OK
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

