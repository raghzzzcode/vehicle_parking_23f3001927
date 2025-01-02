from flask import Flask, request, session
import secrets
from models import db, Service, Customer, Professional, Admin, ServiceRequest, Review
from flask_migrate import Migrate
from flask import jsonify
from werkzeug.security import check_password_hash
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from werkzeug.security import generate_password_hash
import os
from werkzeug.utils import secure_filename
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError



app = Flask(__name__)   
app.secret_key = secrets.token_hex(16)

# Configuration for the database
app.config['SQLALCHEMY_DATABASE_URI'] = r"sqlite:///C:/Users/hp/Desktop/household_services_final.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Directory where documents will be uploaded
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'jpg', 'jpeg', 'png'}

# Initialize the database
db.init_app(app)
m = Migrate(app,db)

CORS(app, resources={r"/*": {"origins": "http://localhost:8000"}})

# Create tables (Only needed on the first run)
# with app.app_context():
#     db.create_all()
#     print("Tables created successfully")
      
      

@app.route('/')
def home():
    return "Welcome to the Home Page!"


@app.route('/api/get_services', methods=['GET'])
def get_services():
    services = Service.query.all()
    return jsonify([{
        'id': service.service_id,
        'name': service.service_name,
        'basePrice': service.base_price
    } for service in services])


@app.route('/api/add_service', methods=['POST'])
def add_service():
    data = request.get_json()
    print(data)
    new_service = Service(
    service_name=data['service_name'],
    base_price=data['base_price'],
    description=data.get('description', ''),
    time_required=data['time_required']
    )
    db.session.add(new_service)
    db.session.commit()
    return jsonify({'message': 'Service added successfully'}), 201

@app.route('/api/delete_service/<int:id>', methods=['DELETE'])
def delete_service(id):
    service = Service.query.get(id)
    if service:
        db.session.delete(service)
        db.session.commit()
        return jsonify({'message': 'Service deleted successfully'}), 200
    return jsonify({'error': 'Service not found'}), 404

@app.route('/api/get_professionals', methods=['GET'])
def get_professionals():
    professionals = Professional.query.all()
    return jsonify([{
        'id': pro.professional_id,
        'name': pro.full_name,
        'experience': pro.experience,
        'serviceid': pro.service_id,
        'status': pro.status
    } for pro in professionals])

@app.route('/api/professionals/<int:id>/approve', methods=['POST'])
def approve_professional(id):
    professional = Professional.query.get(id)
    if professional:
        professional.status = 'approved'
        db.session.commit()
        return jsonify({'message': 'Professional approved'}), 200
    return jsonify({'error': 'Professional not found'}), 404

@app.route('/api/professionals/<int:id>/reject', methods=['POST'])
def reject_professional(id):
    professional = Professional.query.get(id)
    if professional:
        professional.status = 'rejected'
        db.session.commit()
        return jsonify({'message': 'Professional rejected'}), 200
    return jsonify({'error': 'Professional not found'}), 404

@app.route('/api/professionals/<int:id>/delete', methods=['DELETE'])
def delete_professional(id):
    professional = Professional.query.get(id)
    if professional:
        db.session.delete(professional)
        db.session.commit()
        return jsonify({'message': 'Professional deleted successfully'}), 200
    return jsonify({'error': 'Professional not found'}), 404

@app.route('/api/get_service_requests', methods=['GET'])
def get_service_requests():
    try:
        # Query all service requests and join with the related service and professional data
        service_requests = db.session.query(ServiceRequest, Service, Professional).\
            join(Service, ServiceRequest.service_id == Service.service_id).\
            outerjoin(Professional, ServiceRequest.professional_id == Professional.professional_id).\
            all()
        
        # Prepare a list of service requests with the necessary details
        service_requests_data = []
        for request, service, professional in service_requests:
            service_requests_data.append({
                'id': request.request_id,
                'serviceName': service.service_name,
                'professional': professional.full_name if professional else None,
                'status': request.service_status,
            })
        
        return jsonify(service_requests_data), 200
    except Exception as e:
        print(f"Error fetching service requests: {e}")
        return jsonify({"error": "Error fetching service requests"}), 500


@app.route('/api/get_service_basedon_id/<int:id>', methods=['GET', 'PUT'])
def get_service(id):
    service = Service.query.get(id)
    
    if request.method == 'GET':
        if service:
            return jsonify({
                'service_id': service.service_id,  # Mapping id to service_id
                'service_name': service.service_name,  # Mapping name to service_name
                'base_price': service.base_price,  # Mapping basePrice to base_price
                'description': service.description,  # Adding description
                'time_required': service.time_required  # Adding time_required
            })
        return jsonify({'error': 'Service not found'}), 404

    if request.method == 'PUT':
        if service:
            data = request.get_json()
            if 'name' in data:
                service.service_name = data['name']
            if 'basePrice' in data:
                service.base_price = data['basePrice']
            if 'description' in data:
                service.description = data['description']
            if 'timeRequired' in data:
                service.time_required = data['timeRequired']

            # Commit the changes to the database
            db.session.commit()

            return jsonify({
                'message': 'Service updated successfully',
                'service': {
                    'id': service.service_id,
                    'name': service.service_name,
                    'basePrice': service.base_price,
                    'description': service.description,
                    'timeRequired': service.time_required
                }
            })
        return jsonify({'error': 'Service not found'}), 404
    
@app.route('/update_service/<int:service_id>', methods=['PUT'])
def update_service(service_id):
    # Find the service by ID
    service = Service.query.get(service_id)

    if not service:
        return jsonify({"error": "Service not found"}), 404

    # Get the updated data from the request body
    data = request.get_json()
    
    # Update the service fields
    service.service_name = data.get('service_name', service.service_name)
    service.base_price = data.get('base_price', service.base_price)
    service.description = data.get('description', service.description)
    service.time_required = data.get('time_required', service.time_required)
    
    try:
        # Commit the changes to the database
        db.session.commit()
        return jsonify({"message": "Service updated successfully", "service": {
            "service_id": service.service_id,
            "service_name": service.service_name,
            "base_price": service.base_price,
            "description": service.description,
            "time_required": service.time_required
        }}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/api/admin_search", methods=["GET"])
def admin_search():
    search_by = request.args.get("by")
    search_text = request.args.get("text")
    results = []
    total_results = 0

    print(f"Searching by {search_by} for {search_text}")

    if search_by == "services":
        query = Service.query.filter(Service.service_name.ilike(f"%{search_text}%"))
        total_results = query.count()
        results = query.all()  # Get all results without pagination
        # Serialize only relevant fields for services
        serialized_results = [
            {
                "service_id": result.service_id,
                "service_name": result.service_name,
                "base_price": result.base_price,
                "status": result.description
            }
            for result in results
        ]

    elif search_by == "service_requests":
        # Explicitly join ServiceRequest with Service and Professional tables
        query = db.session.query(ServiceRequest, Service, Professional).join(
            Service, ServiceRequest.service_id == Service.service_id) \
            .join(Professional, ServiceRequest.professional_id == Professional.professional_id) \
            .filter(ServiceRequest.service_status.ilike(f"%{search_text}%"))
        
        total_results = query.count()
        results = query.all()  # Get all results without pagination
        
        # Serialize only relevant fields for service requests
        serialized_results = [
            {
                "service_id": result.Service.service_id ,
                "service_name": result.Service.service_name,
                "assigned_professional": result.Professional.full_name ,
                "requested_date": result.ServiceRequest.date_of_request,
                "status": result.ServiceRequest.service_status
            }
            for result in results
        ]
        
        

    elif search_by == "customers":
        query = Customer.query.filter(Customer.full_name.ilike(f"%{search_text}%"))
        total_results = query.count()
        results = query.all()  # Get all results without pagination
        # Serialize only relevant fields for customers
        serialized_results = [
            {
                "customer_name": result.full_name,
                "address": result.address,
                "pincode": result.pincode
            }
            for result in results
        ]

    elif search_by == "professionals":
        # Explicitly join Professional with Service table
        query = db.session.query(Professional, Service).join(
            Service, Professional.service_id == Service.service_id) \
            .filter(Professional.full_name.ilike(f"%{search_text}%"))
        
        total_results = query.count()
        results = query.all()  # Get all results without pagination
        # Serialize only relevant fields for professionals
        serialized_results = [
            {
                "professional_name": result.Professional.full_name,
                "experience": result.Professional.experience,
                "service_provided": result.Service.service_name,  # Accessing service_name from the joined Service table
                
            }
            for result in results
        ]

    return jsonify({
        "results": serialized_results,
        "total": total_results
    }), 200



@app.route('/api/ratings-summary', methods=['GET'])
def get_ratings_summary():
    ratings_summary = db.session.query(
        Review.rating,
        db.func.count(Review.rating).label('count')
    ).group_by(Review.rating).all()

    ratings_data = {rating: count for rating, count in ratings_summary}

    # Ensure all ratings (1-5) are represented
    for i in range(1, 6):
        ratings_data.setdefault(i, 0)

    return jsonify(ratings_data)

@app.route('/api/service-summary', methods=['GET'])
def get_service_requests_summary():
    # Query to fetch all service requests
    service_requests = ServiceRequest.query.all()

    # Create a dictionary to hold counts for all 4 statuses
    service_data = {
        'Requested': 0,
        'Assigned': 0,
        'Completed': 0,
        'Rejected': 0
    }

    # Iterate over each service request and increment the count based on its status
    for service_request in service_requests:
        if service_request.service_status == 'requested':
            service_data['Requested'] += 1
        elif service_request.service_status == 'assigned':
            service_data['Assigned'] += 1
        elif service_request.service_status == 'completed':
            service_data['Completed'] += 1
        elif service_request.service_status == 'rejected':
            service_data['Rejected'] += 1
    print(service_data)
    # Return the data as a JSON response
    return jsonify(service_data)



@app.route('/api/login', methods=['POST'])
def login():
    # Get login credentials from the request
    email = request.json.get('email')
    password = request.json.get('password')
    
    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password are required'}), 400

    # Check for the user in the Admin table
    admin = Admin.query.filter_by(email=email).first()
    if admin and check_password_hash(admin.password, password):
        return jsonify({'success': True, 'role': 'admin', 'message': 'Login successful!'}), 200

    # Check for the user in the Professional table
    professional = Professional.query.filter_by(email=email).first()
    if professional and check_password_hash(professional.password, password):
        return jsonify({'success': True, 'role': 'professional', 'message': 'Login successful!'}), 200

    # Check for the user in the Customer table
    customer = Customer.query.filter_by(email=email).first()
    if customer and check_password_hash(customer.password, password):
        return jsonify({'success': True, 'role': 'customer', 'message': 'Login successful!'}), 200

    # If no match is found
    return jsonify({'success': False, 'message': 'Invalid credentials. Please try again.'}), 401

# Customer routes

@app.route('/api/get_professional/<int:service_id>', methods=['GET'])
def get_professionals_byid(service_id):
    # Assuming Professional and Service are SQLAlchemy models
    professionals = db.session.query(
        Professional.professional_id,
        Professional.full_name.label("professional_name"),
        Professional.service_id,
        Professional.experience,
        Professional.address,
        Professional.pincode,
        Professional.email,
        Service.service_name
    ).join(Service, Professional.service_id == Service.service_id)\
     .filter(Professional.service_id == service_id)\
     .all()

    # Serialize the data into a JSON-compatible format
    return jsonify([{
        'professional_id': pro.professional_id,
        'professional_name': pro.professional_name,
        'service_id': pro.service_id,
        'service_name': pro.service_name,
        'experience': pro.experience,
        'address': pro.address,
        'pincode': pro.pincode,
        'email': pro.email
    } for pro in professionals])


@app.route('/api/book-service', methods=['POST'])
def book_service():
    data = request.get_json()
    print(data)

    # Check if 'service_id' is provided, else fetch the 'service_id' from the 'services' table
    if not data.get('service_id'):
        service_name = data.get('service_name')
        if service_name:
            # Query the 'services' table to find the service_id based on the service_name
            service = Service.query.filter_by(service_name=service_name).first()
            if service:
                data['service_id'] = service.service_id
            else:
                return jsonify({'message': 'Service name not found in the database'}), 400
        else:
            return jsonify({'message': 'Neither service_id nor service_name provided'}), 400

    # Now, 'service_id' is guaranteed to be in the data
    new_request = ServiceRequest(
        service_id=data['service_id'],
        customer_email=data['customer_email'],
        professional_id=data['professional_id'],
        date_of_request=datetime.now().date()
    )

    db.session.add(new_request)
    db.session.commit()

    return jsonify({'message': 'Service booking requested successfully'}), 200


@app.route('/api/close-service', methods=['POST'])
def close_service():
    data = request.get_json()
    
    # Extract professional_email and customer_email from request data
    professional_email = data['professional_email']
    customer_email = data['customer_email']


    # Fetch the professional and customer from their emails
    professional = Professional.query.filter_by(email=professional_email).first()
    customer = Customer.query.filter_by(email=customer_email).first()

    if not professional or not customer:
        return jsonify({'message': 'Professional or Customer not found'}), 404

    service = ServiceRequest.query.filter(
    ServiceRequest.professional_id == professional.professional_id, 
    ServiceRequest.customer_email == customer_email, 
    ServiceRequest.service_status.notin_(['completed'])
    ).first()

    if service:
        # Fetch the service name from the Service table using the service_id
        service_info = Service.query.filter_by(service_id=service.service_id).first()

        # Send request_id, customer_email, professional_email, professional's name, and service name in the response
        return jsonify({
            'message': 'Service close request initiated',
            'request_id': service.request_id,
            'customer_email': customer_email,
            'professional_email': professional_email,
            'professional_name': professional.full_name,
            'service_name': service_info.service_name
        }), 200

    return jsonify({'message': 'No matching service found or already completed'}), 404


@app.route('/api/insert_review', methods=['POST'])
def insert_review():
    data = request.get_json()
    request_id = data['request_id']
    rating = data['rating']
    comments = data.get('comments', '')

    # Fetch the service request by request_id
    service_request = ServiceRequest.query.filter_by(request_id=request_id).first()

    if not service_request:
        return jsonify({'message': 'Service request not found'}), 404

    # Create a new review entry
    new_review = Review(
        service_request_id=request_id,
        rating=rating,
        comments=comments
    )

    # Insert the review into the database
    db.session.add(new_review)
    db.session.commit()

    # Update service request status to completed
    service_request.service_status = 'completed'
    service_request.date_of_completion = datetime.now().date()
    db.session.commit()

    return jsonify({'message': 'Review inserted successfully'}), 200


@app.route('/api/get_service_history', methods=['GET'])
def get_service_history_for_cust():
    customer_email = request.args.get('customer_email')  # Get the customer email from query parameter

    # Perform a join query with ServiceRequest, Service, and Professional
    requests = db.session.query(ServiceRequest, Service, Professional, Customer).\
        join(Service, ServiceRequest.service_id == Service.service_id).\
        join(Professional, ServiceRequest.professional_id == Professional.professional_id, isouter=True).\
        join(Customer, ServiceRequest.customer_email == Customer.email).\
        filter(Customer.email == customer_email).all()
    
    # Return the results as a JSON response
    return jsonify([{
        'service_name': req[1].service_name,  # Accessing service_name from the joined Service table
        'professional_name': req[2].full_name if req[2] else None,  # Accessing full_name from the joined Professional table
        'email': req[3].email,  # Accessing email from the joined Customer table
        'status': req[0].service_status  # Accessing service_status from the ServiceRequest table
    } for req in requests])


# Route to get customer profile
@app.route('/api/customer/profile', methods=['GET'])
def get_customer_profile():
    customer_email = request.args.get('customer_email')  # Get email from query parameter

    customer = Customer.query.filter_by(email=customer_email).first()
    return jsonify({
        'email': customer.email,
        'full_name': customer.full_name,
        'address': customer.address,
        'pincode': customer.pincode
    })


# Route to logout
@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('customer_id', None)  # Clear the session
    return jsonify({'message': 'Logged out successfully'}), 200


@app.route('/api/customer_register', methods=['POST'])
def register_customer():
    data = request.get_json()
    # Validate incoming data
    required_fields = ['email', 'password', 'fullname', 'address', 'pincode']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing {field}"}), 400
    
    # Check if email already exists
    if Customer.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already registered"}), 400

    # Hash the password before storing
    hashed_password = generate_password_hash(data['password'])

    new_customer = Customer(
        email=data['email'],
        password=hashed_password,
        full_name=data['fullname'],
        address=data['address'],
        pincode=data['pincode']
    )

    try:
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({"message": "Registration successful!"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Error saving customer details. Please try again."}), 500

@app.route('/api/customer_search', methods=['GET'])
def customer_search():
    search_by = request.args.get('search_by', 'service_name')
    search_input = request.args.get('search_input', '')

    if search_by == 'service_name':
        # Join Professional with Service and filter by service_name
        results = (
            db.session.query(Professional, Service)
            .join(Service, Professional.service_id == Service.service_id)
            .filter(Service.service_name.ilike(f'%{search_input}%'))
            .all()
        )
    elif search_by == 'pin_code':
        results = (
            db.session.query(Professional, Service)
            .join(Service, Professional.service_id == Service.service_id)
            .filter(Professional.pincode.like(f'%{search_input}%'))
            .all()
        )
    elif search_by == 'location':
        results = (
            db.session.query(Professional, Service)
            .join(Service, Professional.service_id == Service.service_id)
            .filter(Professional.address.ilike(f'%{search_input}%'))
            .all()
        )
    else:
        return jsonify({'error': 'Invalid search filter'}), 400  # Bad Request

    if not results:
        return jsonify({'message': 'No results found'}), 404  # Not Found

    # Format results for the frontend
    search_results = []
    for professional, service in results:
        professional_info = {
            'professional_id': professional.professional_id,
            'full_name': professional.full_name,
            'service_name': service.service_name,  # From the joined Service model
            'experience': professional.experience,
            'address': professional.address,
            'pincode': professional.pincode
        }
        search_results.append(professional_info)

    return jsonify(search_results), 200  # OK


@app.route('/api/service-history/<customer_email>', methods=['GET'])
def get_service_history_cust_summ(customer_email):
    # Query the ServiceRequest table based on customer email
    service_history = db.session.query(
        ServiceRequest.service_status,
        db.func.count(ServiceRequest.service_status).label('status_count')
    ).join(Customer, ServiceRequest.customer_email == Customer.email) \
     .filter(Customer.email == customer_email) \
     .group_by(ServiceRequest.service_status).all()

    # Map the results to a dictionary
    service_history_data = {
        "Requested": 0,
        "Assigned": 0,
        "Closed": 0
    }

    for status, count in service_history:
        if status == 'requested':
            service_history_data["Requested"] = count
        elif status == 'assigned':
            service_history_data["Assigned"] = count
        elif status == 'completed':
            service_history_data["Closed"] = count
        elif status=='rejected':
            service_history_data["Rejected"] = count

    return jsonify(service_history_data)


# Get Professional Details
@app.route('/api/get_professional/<int:service_id>', methods=['GET'])
def get_professionals_by_id_prof(service_id):
    professionals = Professional.query.filter_by(service_id=service_id).all()
    return jsonify([{
        'professional_id': pro.professional_id,
        'professional_name': pro.full_name,
        'service_name': pro.service_name,
        'experience': pro.experience,
        'address': pro.address,
        'pincode': pro.pincode,
        'email': pro.email
    } for pro in professionals])    

@app.route('/api/service-history/<int:customer_id>', methods=['GET'])
def get_service_history(customer_id):
    # Fetch the service status counts for the specific customer
    requested_count = db.session.query(func.count(ServiceRequest.request_id)).filter(
        ServiceRequest.customer_id == customer_id,
        ServiceRequest.service_status == 'requested'
    ).scalar()

    assigned_count = db.session.query(func.count(ServiceRequest.request_id)).filter(
        ServiceRequest.customer_id == customer_id,
        ServiceRequest.service_status == 'assigned'
    ).scalar()

    closed_count = db.session.query(func.count(ServiceRequest.request_id)).filter(
        ServiceRequest.customer_id == customer_id,
        ServiceRequest.service_status == 'completed'
    ).scalar()

    # Return the service history data in a JSON format
    return jsonify({
        'Requested': requested_count,
        'Assigned': assigned_count,
        'Closed': closed_count
    })

# Professional Routes

@app.route('/api/professional_profile', methods=['GET'])
def get_profile():
    # Get the profile of the logged-in professional
    professional_id = request.args.get('professional_id')
    
    # Fetch the professional based on professional_id
    professional = Professional.query.filter_by(professional_id=professional_id).first()  # Adjust the column name if necessary
    
    if professional:
        # Fetch the service based on the service_id from the Professional table
        service = Service.query.filter_by(service_id=professional.service_id).first()  # Adjust service_id and id as needed

        # Prepare the response
        response = {
            'email': professional.email,
            'full_name': professional.full_name,
            'service_name': service.service_name if service else 'Unknown',  # Fetch service name or 'Unknown' if not found
            'experience': professional.experience,
            'address': professional.address,
            'pincode': professional.pincode,
            'status': professional.status,
        }
        return jsonify(response), 200
    
    return jsonify({'error': 'Profile not found'}), 404
@app.route('/api/professional/today-services', methods=['GET'])
def get_today_services():
    professional_email = request.args.get('professional_email')
    
    # Fetch the professional using email
    professional = Professional.query.filter_by(email=professional_email).first()
    
    if not professional:
        return jsonify({'error': 'Professional not found'}), 404

    # Fetch today's services for the professional (status 'requested' means pending)
    services = db.session.query(ServiceRequest).filter_by(professional_id=professional.professional_id, service_status='requested').all()

    if services:
        response = []
        for service in services:
            # Fetch customer details by customer email
            customer = Customer.query.filter_by(email=service.customer_email).first()
            if customer:
                customer_name = customer.full_name
                customer_address = customer.address  # Use customer address as location
            else:
                customer_name = 'Unknown'  # Default if customer is not found
                customer_address = 'Unknown'  # Default location if customer is not found
            
            # Prepare the response data for each service
            response.append({
                'id': service.request_id,
                'customer_name': customer_name,
                'email': service.customer_email,
                'location': customer_address,  # Using the address from the Customer table
                'status': service.service_status
            })
        
        return jsonify(response), 200

    return jsonify({'error': 'No services found for today.'}), 404


@app.route('/api/professional/accept-service', methods=['POST'])
def accept_service():
    professional_email = request.json.get('professional_email')
    professional_id=Professional.query.filter_by(email=professional_email).first().professional_id
    request_id = request.json.get('request_id')
    # Fetch the service request by ID
    service_request = ServiceRequest.query.filter_by(request_id=request_id).first()

    # Check if the service request exists and is still 'requested'
    if service_request and service_request.service_status == 'requested':
        # Update the service status and associate with the professional
        service_request.service_status = 'assigned'
        db.session.commit()

        return jsonify({'message': 'Service accepted successfully'}), 200
    
    # If service request is not found or already processed
    return jsonify({'error': 'Service request not found or already processed'}), 404


@app.route('/api/professional/reject-service', methods=['POST'])
def reject_service():
    # Reject a service request
    request_id = request.json.get('request_id')
    
    # Fetch the service request by ID
    service_request = ServiceRequest.query.filter_by(request_id=request_id).first()

    # Check if the service request exists and is still 'requested'
    if service_request and service_request.service_status == 'requested':
        # Update the service status to 'rejected'
        service_request.service_status = 'rejected'
        db.session.commit()

        return jsonify({'message': 'Service rejected successfully'}), 200
    
    # If service request is not found or already processed
    return jsonify({'error': 'Service request not found or already processed'}), 404



@app.route('/api/professional/closed-services', methods=['GET'])
def get_closed_services():
    professional_email = request.args.get('professional_email')
    
    # Fetch the professional using email
    professional = Professional.query.filter_by(email=professional_email).first()
    
    if not professional:
        return jsonify({'error': 'Professional not found'}), 404

    # Fetch completed services (status 'completed' means the service is done)
    services = db.session.query(ServiceRequest).filter_by(professional_id=professional.professional_id, service_status='completed').all()

    if services:
        response = []
        for service in services:
            # Fetch customer details by customer email
            customer = Customer.query.filter_by(email=service.customer_email).first()
            if customer:
                customer_name = customer.full_name
                customer_address = customer.address  # Use customer address as location
            else:
                customer_name = 'Unknown'  # Default if customer is not found
                customer_address = 'Unknown'  # Default location if customer is not found
            
            # Fetch the review for the service (if available)
            review = Review.query.filter_by(service_request_id=service.request_id).first()
            if review:
                rating = review.rating
            else:
                rating = 'Not closed'  # Default if no rating exists
            
            # Prepare the response data for each service
            response.append({
                'id': service.request_id,
                'customer_name': customer_name,
                'email': service.customer_email,
                'location': customer_address,  # Using the address from the Customer table
                'date': service.date_of_completion,  # Completion date from ServiceRequest table
                'rating': rating  # Rating from the Review table
            })
        
        return jsonify(response), 200

    return jsonify({'error': 'No closed services found for this professional.'}), 404


from datetime import datetime, timezone

from datetime import datetime, timezone

@app.route('/api/update_professional_profile', methods=['PUT'])
def update_professional_profile():
    # Fetch the professional email from the request parameters (passed from front-end)
    email = request.args.get('email')  # Using args instead of form
    print(f"Updating profile for email: {email}")

    # Query the Professional table based on email
    professional = Professional.query.filter_by(email=email).first()

    # Check if the professional exists
    if not professional:
        return jsonify({'message': 'Professional not found'}), 404

    data = request.args  # Using request.args instead of request.form
    
    # Handle updating non-document fields
    if 'email' in data:
        professional.email = data['email']
    if 'password' in data and data['password']:
        professional.password = generate_password_hash(data['password'])
    if 'full_name' in data:
        professional.full_name = data['full_name']
    
    # Fetch the Service in advance to handle service update properly
    service = None
    if 'service_name' in data:
        service = Service.query.filter_by(service_name=data['service_name']).first()
        if not service:
            return jsonify({'message': 'Service not found'}), 404
        professional.service_id = service.service_id
    
    if 'experience' in data:
        professional.experience = data['experience']
    if 'address' in data:
        professional.address = data['address']
    if 'pincode' in data:
        professional.pincode = data['pincode']
    
    # Optional: Handle document upload as base64 encoding or file upload if required.
    
    # Update date_updated for auditing purposes
    professional.date_updated = datetime.now(timezone.utc)

    try:
        db.session.commit()
        return jsonify({
            'message': 'Profile updated successfully!',
            'data': {
                'email': professional.email,
                'full_name': professional.full_name,
                'service_name': service.service_name if service else None,  # Ensure service exists
                'experience': professional.experience,
                'address': professional.address,
                'pincode': professional.pincode,
                'status': professional.status,
                'role': professional.role
            }
        }), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'message': 'Error updating profile', 'error': str(e)}), 500

    
    
@app.route('/api/professional_register', methods=['POST'])
def register_professional():
    # Extracting the form data from the request
    data = request.form
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('fullname')
    service_id = data.get('service_id')
    experience = data.get('experience')
    address = data.get('address')
    pincode = data.get('pincode')

    print(f"Registering professional with email: {email} and password: {password}")

    # Handling the document file
    document = request.files.get('documents')
    document_data = document.read() if document else None

    # Creating a new professional record
    new_professional = Professional(
        email=email,
        password=generate_password_hash(password),
        full_name=full_name,
        service_id=service_id,
        experience=experience,
        document=document_data,
        address=address,
        pincode=pincode,
        date_created=datetime.utcnow(),
        date_updated=datetime.utcnow()
    )

    try:
        db.session.add(new_professional)
        db.session.commit()
        return jsonify({"message": "Professional registered successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/get_services_for_prof_regis', methods=['GET'])
def get_services_for_prof_regis():
    services = Service.query.all()  # Assuming you have a Service model
    return jsonify({
        'services': [{'service_id': service.service_id, 'service_name': service.service_name} for service in services]
    })

@app.route('/api/professional_search', methods=['GET'])
def professional_search():
    # Get the authenticated professional's email (assuming you have a mechanism to get the logged-in professional)
    professional_email = request.args.get('professional_email')  # Replace with actual authenticated professional's email
    print(professional_email)
    if not professional_email:
        return jsonify({'error': 'Professional email is required.'}), 400

    # Fetch the professional by email
    professional = Professional.query.filter_by(email=professional_email).first()
    if not professional:
        return jsonify({'error': 'Professional not found.'}), 404

    # Get search parameters
    search_by = request.args.get('searchBy', 'date')  # Default is 'date'
    search_text = request.args.get('searchText', '').lower()

    # Begin constructing the query
    query = db.session.query(
        ServiceRequest, Customer, Professional, Review
    ).join(
        Customer, ServiceRequest.customer_email == Customer.email
    ).join(
        Service, ServiceRequest.service_id == Service.service_id
    ).join(
        Professional, ServiceRequest.professional_id == Professional.professional_id, isouter=True
    ).join(
        Review, ServiceRequest.request_id == Review.service_request_id, isouter=True
    ).filter(
        ServiceRequest.professional_id == professional.professional_id  # Ensure the professional is linked to the service request
    )

    # Filter the query based on search parameters
    if search_by == 'date':
        try:
            search_date = datetime.strptime(search_text, '%Y-%m-%d').date()
            query = query.filter(ServiceRequest.date_of_request == search_date)
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400
    elif search_by == 'location':
        query = query.filter(Customer.address.ilike(f'%{search_text}%'))
    elif search_by == 'pincode':
        query = query.filter(Customer.pincode.ilike(f'%{search_text}%'))
    elif search_by == 'customer':
        query = query.filter(Customer.full_name.ilike(f'%{search_text}%'))

    # Execute the query
    results = query.all()

    # Prepare the response results
    search_results = []
    for service_request, customer, professional, review in results:
        result = {
            'id': service_request.request_id,
            'customer_name': customer.full_name,
            'email': customer.email,
            'location': customer.address,
            'date': service_request.date_of_request.strftime('%Y-%m-%d'),
        }
        
        # Include the review information only if the service status is 'completed'
        if service_request.service_status == 'completed' and review:
            result['rating'] = review.rating
            result['comments'] = review.comments
        else:
            result['rating'] = None  # No review available if the service isn't completed

        search_results.append(result)

    return jsonify(search_results)


@app.route('/api/professional/reviews-ratings', methods=['GET'])
def get_reviews_ratings():
    try:
        # Get the professional's email from the request
        professional_email = request.args.get('email')
        # Get the professional from the database based on email
        professional = db.session.query(Professional).filter_by(email=professional_email).first()
        print(professional_email)
        print(professional)

        if not professional:
            return jsonify({'error': 'Professional not found'}), 404
        
        professional_id = professional.professional_id  # Referencing 'professional_id' based on the model
        
        # Query to get average ratings and count per rating level for the specific professional
        ratings = db.session.query(
            Review.rating,
            func.count(Review.rating).label('count')
        ).join(ServiceRequest, ServiceRequest.request_id == Review.service_request_id).filter(ServiceRequest.professional_id == professional_id).group_by(Review.rating).all()

        # Format ratings data to return
        ratings_data = {str(rating.rating): rating.count for rating in ratings}

        # Get the average rating for the current professional
        average_rating = db.session.query(
            func.avg(Review.rating).label('avg_rating')
        ).join(ServiceRequest, ServiceRequest.request_id == Review.service_request_id).filter(ServiceRequest.professional_id == professional_id).scalar()

        return jsonify({
            'ratingsData': ratings_data,
            'averageRating': average_rating if average_rating else 0
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/professional/service-requests', methods=['GET'])
def professional_get_service_requests():
    try:
        # Get the professional's email from the request
        professional_email = request.args.get('email')
        
        # Get the professional from the database based on email
        professional = db.session.query(Professional).filter_by(email=professional_email).first()
        
        if not professional:
            return jsonify({'error': 'Professional not found'}), 404
        
        professional_id = professional.professional_id  # Referencing 'professional_id' based on the model
        
        # Query to get service requests count by status for the specific professional
        service_requests = db.session.query(
            ServiceRequest.service_status,
            func.count(ServiceRequest.service_status).label('count')
        ).filter(ServiceRequest.professional_id == professional_id).group_by(ServiceRequest.service_status).all()

        # Format service requests data to return
        service_requests_data = {request.service_status: request.count for request in service_requests}

        # Calculate counts
        received = sum(service_requests_data.get(status, 0) for status in ['requested', 'assigned', 'completed', 'rejected'])
        rejected = service_requests_data.get('rejected', 0)
        closed = service_requests_data.get('completed', 0)
        requested = service_requests_data.get('requested', 0)
        assigned = service_requests_data.get('assigned', 0)

        # Prepare the response with all counts
        return jsonify({
            'serviceRequestsData': {
                'Received': received,
                'Rejected': rejected,
                'Closed': closed,
                'Requested': requested,
                'Assigned': assigned
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500



# View Professional Profile
@app.route('/api/view_professional', methods=['GET'])
def get_professional_for_profile():
    try:
        # Get the professional's email from the query parameters
        professional_email = request.args.get('email')
        print("professional_email:", professional_email)
        
        if not professional_email:
            return jsonify({'message': 'Email parameter is missing'}), 400

        # Query the Professional data with the provided email
        professional = db.session.query(Professional, Service).join(Service, Professional.service_id == Service.service_id).filter(Professional.email == professional_email).first()

        if not professional:
            return jsonify({'message': 'Professional not found'}), 404

        professional_data, service_data = professional
        print(professional_data)
        print(service_data)
        print(professional_data.full_name)
        print(service_data.service_name)
        # Construct the response data
        response_data = {
            'fullName': professional_data.full_name,
            'email': professional_data.email,
            'serviceName': service_data.service_name,
            'experience': professional_data.experience,
            'address': professional_data.address,
            'pincode': professional_data.pincode,
            'role': professional_data.role,
            'status': professional_data.status,
        }
        

        return jsonify(response_data), 200

    except Exception as e:
        print(f"Error fetching professional data: {str(e)}")
        return jsonify({'message': 'Error fetching professional data', 'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)