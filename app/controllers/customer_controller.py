from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK,HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED,HTTP_409_CONFLICT 
from app.models.customer import Customer
from flask_jwt_extended import jwt_required, get_jwt_identity 
from app.extensions import db, bcrypt  

customer =Blueprint('customer', __name__, url_prefix='/auth')

@customer.get('/get_all', endpoint='get_all_customers')
@jwt_required()
def get_all_customers():
    try:
        all_customers = Customer.query.all()
        customers_data = []

        for customer in all_customers:
                customer_info ={
                'customer_id' : customer.customer_id,
                'name' : customer.name,
                'email' : customer.email,
                'phone_number' : customer.phone_number,
                'password': customer.password
            }
        customers_data.append(customer_info)

        return jsonify({
            'message':'All customers retrieved successfully',
            'customers':customers_data
        }), HTTP_200_OK
    
    except Exception as e:
         print('Error:', e)
         return jsonify({
              'error': str(e)
         }), HTTP_500_INTERNAL_SERVER_ERROR
    
#get customer by id
@customer.get('/customer/<int:customer_id>' ,  endpoint='get_customer_by_id')  
@jwt_required()
def get_customer_by_id(customer_id):
    
    try:
        
            customer = Customer.query.filter_by(customer_id = customer_id).first() # Querying the database for the customer with the specified id
        
            if not customer:
                return jsonify({'message': 'customer does not exist'}), HTTP_404_NOT_FOUND
        
            return jsonify({
                'message':'Customer details retrieved successfully',
                'customer': {
                        'customer_id' : customer.customer_id,
                        'name' : customer.name,
                        'email' : customer.email,
                        'phone_number' : customer.phone_number,
                        'password': customer.password
                    
            }
            }), HTTP_200_OK 

    except Exception as e:
        return jsonify({
            'error': str(e)
            }), HTTP_500_INTERNAL_SERVER_ERROR
    
 #Updating a customer   
@customer.route('/update/<int:customer_id>', methods=['PUT', 'PATCH'] ,  endpoint='update_customer') # Defining a route for editing an customer  
@jwt_required()
def update_customer_details(customer_id):
    
    try:
        
        current_customer = get_jwt_identity() # returns the current customer's id
        logged_in_customer = Customer.query.filter_by(customer_id=current_customer).first() # Querying the database for the customer with the specified id
        
        
        customer = customer.query.get(customer_id) # Querying the database for the customer with the specified id
    
        
        if not customer:
            return jsonify({'message': 'customer does not exist'}), HTTP_404_NOT_FOUND
        
        elif logged_in_customer.customer_id != customer.customer_id:
            return jsonify({'message': 'You are not authorized to edit this customer'}), HTTP_401_UNAUTHORIZED
        
        else:
            data = request.get_json()
            name = data.get('name', customer.name)
            email = data.get('email', customer.email)
            phone_number = data.get('phone_number', customer.phone_number)

            if "password" in request.json:
                password = request.json.get('password')
                hashed_password = bcrypt.generate_password_hash(password)
                customer.password = hashed_password

                if email != customer.email and Customer.query.filter_by(email=email).first():
                  return jsonify({"Error":"Email is already in use."}),HTTP_409_CONFLICT
    
                if phone_number != customer.phone_number and Customer.query.filter_by(phone_number=phone_number).first():
                  return jsonify({"Error":"Phone number is already in use."}),HTTP_409_CONFLICT
                
                customer.name = name
                customer.email = email
                customer.phone_number = phone_number
                customer.password = password

                db.session.commit() # Committing the changes to the database

                customer_name = customer.get_customer()
                return jsonify({
                    'message': customer_name + 'has been updated successfully',
                    'customer':{
                        'name' : customer.name,
                        'email' : customer.email,
                        'phone_number' : customer.phone_number,
                        'updated_at' : customer.updated_at 
                    }
                }), HTTP_200_OK
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    
#delete customer
@customer.route('/delete/<int:customer_id>', methods=['DELETE'] ,  endpoint='delete_author') # Defining a route for deleting an customer  
@jwt_required()
def delete_customer(customer_id):
    
    try:
        
        current_customer = get_jwt_identity() # returns the current customer's id
        logged_in_customer = Customer.query.filter_by(customer_id=current_customer).first() # Querying the database for the customer with the specified id
        
        customer = Customer.query.get(customer_id) 
        if not customer:
            return jsonify({'message': 'Customer does not exist'}), HTTP_404_NOT_FOUND
        
        elif logged_in_customer.customer_id != customer.customer_id:
            return jsonify({'message': 'You are not authorized to delete this customer'}), HTTP_401_UNAUTHORIZED
        
        db.session.delete(customer)
        db.session.commit()

        return jsonify({
                'message': 'Customer has been deleted successfully'
                }) , HTTP_200_OK
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    
#search for an customer
@customer.get('/search', endpoint='search_customer') 
@jwt_required 
def search_customer():
     
     try:
          
          search_query = request.args.get('query', '')

          customers = Customer.query.filter(
                                       (Customer.first_name.ilike(f"%{search_query}%")) |
                                       (Customer.last_name.ilike(f"%{search_query}%"))
                                       ).all()
          
          if len(customers) == 0:
               return jsonify({
                'message': 'No results found.'
                }), HTTP_404_NOT_FOUND
          else:
              
              all_customers = Customer.query.all()
              customers_data = []

          for customer in all_customers:
                    customer_info ={
                    'customer_id' : customer.customer_id,
                    'name' : customer.name,
                    'email' : customer.email,
                    'phone_number' : customer.phone_number,
                    'password': customer.password
                }
          customers_data.append(customer_info)
          return jsonify({
                            'message': f'Customer with name {search_query} retrieved successfully',
                            'search_results': customers_data
                            }) , HTTP_200_OK 

     except Exception as e:
        return jsonify({
            'error': str(e)
            }), HTTP_500_INTERNAL_SERVER_ERROR
