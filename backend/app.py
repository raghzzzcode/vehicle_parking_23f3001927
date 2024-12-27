from flask import Flask, render_template, request, redirect, url_for, flash, session
import secrets
from backend.models import db, Migrate
from backend.models import Service, Customer, Professional, Admin, ServiceRequest, Review
from flask import jsonify
from werkzeug.security import check_password_hash
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from werkzeug.security import generate_password_hash
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)   
app.secret_key = secrets.token_hex(16)

# Configuration for the database
app.config['SQLALCHEMY_DATABASE_URI'] = r"sqlite:////tmp/household_services_database_2.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Directory where documents will be uploaded
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'jpg', 'jpeg', 'png'}

# Initialize the database
db.init_app(app)
m = Migrate(app,db)

# Create the tables (Only needed on the first run)
with app.app_context():
    db.create_all()

app.route('/api/services', methods=['GET'])
def get_services():
    services = Service.query.all()
    return jsonify([{
        'id': service.service_id,
        'name': service.service_name,
        'basePrice': service.base_price
    } for service in services])

@app.route('/api/services/<int:id>', methods=['GET'])
def get_service(id):
    service = Service.query.get(id)
    if service:
        return jsonify({
            'id': service.service_id,
            'name': service.service_name,
            'basePrice': service.base_price
        })
    return jsonify({'error': 'Service not found'}), 404

@app.route('/api/services', methods=['POST'])
def add_service():
    data = request.get_json()
    new_service = Service(
        service_name=data['name'],
        base_price=data['basePrice'],
        description=data.get('description', ''),
        time_required=data['timeRequired']
    )
    db.session.add(new_service)
    db.session.commit()
    return jsonify({'message': 'Service added successfully'}), 201

@app.route('/api/services/<int:id>', methods=['DELETE'])
def delete_service(id):
    service = Service.query.get(id)
    if service:
        db.session.delete(service)
        db.session.commit()
        return jsonify({'message': 'Service deleted successfully'}), 200
    return jsonify({'error': 'Service not found'}), 404

@app.route('/api/professionals', methods=['GET'])
def get_professionals():
    professionals = Professional.query.all()
    return jsonify([{
        'id': pro.professional_id,
        'name': pro.full_name,
        'experience': pro.experience,
        'serviceName': pro.service_name,
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

@app.route('/api/professionals/<int:id>', methods=['DELETE'])
def delete_professional(id):
    professional = Professional.query.get(id)
    if professional:
        db.session.delete(professional)
        db.session.commit()
        return jsonify({'message': 'Professional deleted successfully'}), 200
    return jsonify({'error': 'Professional not found'}), 404

@app.route('/api/service_requests', methods=['GET'])
def get_service_requests():
    service_requests = ServiceRequest.query.join(Service, ServiceRequest.service_id == Service.service_id).join(Professional, ServiceRequest.professional_id == Professional.professional_id).all()
    return jsonify([{
        'id': request.request_id,
        'serviceName': request.service_name,
        'professional': request.professional.full_name if request.professional else 'N/A',
        'status': request.service_status
    } for request in service_requests])

@app.route('/api/service_requests/<int:id>', methods=['GET'])
def get_service_request(id):
    service_request = ServiceRequest.query.join(Service, ServiceRequest.service_id == Service.service_id).join(Professional, ServiceRequest.professional_id == Professional.professional_id).filter(ServiceRequest.request_id == id).first()
    if service_request:
        return jsonify({
            'id': service_request.request_id,
            'serviceName': service_request.service_name,
            'professional': service_request.professional.full_name if service_request.professional else 'N/A',
            'status': service_request.service_status
        })
    return jsonify({'error': 'Service request not found'}), 404

@app.route('/api/service_requests/assign', methods=['POST'])
def assign_professional_to_request():
    data = request.get_json()
    service_request = ServiceRequest.query.get(data['requestId'])
    professional = Professional.query.get(data['professionalId'])
    if service_request and professional:
        service_request.professional_id = professional.professional_id
        service_request.service_status = 'assigned'
        db.session.commit()
        return jsonify({'message': 'Professional assigned to request successfully'}), 200
    return jsonify({'error': 'Service request or professional not found'}), 404

@app.route('/api/service_requests/<int:id>/update_status', methods=['POST'])
def update_service_request_status(id):
    data = request.get_json()
    service_request = ServiceRequest.query.get(id)
    if service_request:
        service_request.service_status = data['status']
        service_request.date_of_completion = datetime.now() if data['status'] == 'completed' else None
        db.session.commit()
        return jsonify({'message': 'Service request status updated successfully'}), 200
    return jsonify({'error': 'Service request not found'}), 404


@app.route("/search", methods=["GET"])
def search():
    search_by = request.args.get("by")
    search_text = request.args.get("text")
    results = []

    if search_by == "services":
        results = Service.query.filter(Service.service_name.ilike(f"%{search_text}%")).all()
    elif search_by == "service_requests":
        results = ServiceRequest.query.filter(ServiceRequest.service_status.ilike(f"%{search_text}%")).all()
    elif search_by == "customers":
        results = Customer.query.filter(Customer.full_name.ilike(f"%{search_text}%")).all()
    elif search_by == "professionals":
        results = Professional.query.filter(Professional.full_name.ilike(f"%{search_text}%")).all()

    return jsonify({"results": [result.to_dict() for result in results]}), 200

# API Route to fetch ratings data
@app.route('/api/ratings', methods=['GET'])
def get_ratings():
    ratings = db.session.query(Review.rating, db.func.count(Review.rating)).group_by(Review.rating).all()
    ratings_data = {str(rating): count for rating, count in ratings}
    return jsonify(ratings_data)

# API Route to fetch service requests data
@app.route('/api/service-requests', methods=['GET'])
def get_service_requests():
    statuses = db.session.query(
        ServiceRequest.service_status,
        db.func.count(ServiceRequest.service_status)
    ).group_by(ServiceRequest.service_status).all()
    request_data = {status: count for status, count in statuses}
    return jsonify(request_data)

@app.route('/api/services/<int:id>', methods=['DELETE'])
def delete_service(id):
    # Find the service by ID
    service = Service.query.get(id)
    
    if service:
        try:
            db.session.delete(service)  # Delete the service from the database
            db.session.commit()
            return jsonify({'message': 'Service deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()  # Rollback in case of any error
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Service not found'}), 404

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Check if the user exists in the Customer table
    customer = Customer.query.filter_by(email=email).first()
    if customer and check_password_hash(customer.password, password):
        return jsonify({"success": True, "role": "customer"}), 200

    # Check if the user exists in the Professional table
    professional = Professional.query.filter_by(email=email).first()
    if professional and check_password_hash(professional.password, password):
        return jsonify({"success": True, "role": "professional"}), 200

    # Check if the user exists in the Admin table
    admin = Admin.query.filter_by(email=email).first()
    if admin and check_password_hash(admin.password, password):
        return jsonify({"success": True, "role": "admin"}), 200

    # If no user is found or password is incorrect
    return jsonify({"success": False, "message": "Invalid credentials"}), 401

# Route to fetch all services
@app.route('/api/services', methods=['GET'])
def get_services():
    services = Service.query.all()
    return jsonify([service.as_dict() for service in services])

# Route to fetch professionals based on service id
@app.route('/api/professionals/<int:service_id>', methods=['GET'])
def get_professionals(service_id):
    professionals = Professional.query.filter_by(service_name=service_id).all()
    return jsonify([professional.as_dict() for professional in professionals])

# Route to fetch service history of a customer
@app.route('/api/service-history', methods=['GET'])
def get_service_history():
    customer_id = request.args.get('customer_id')  # You can get customer_id from the session or request
    service_history = ServiceRequest.query.filter_by(customer_id=customer_id).all()
    return jsonify([service.as_dict() for service in service_history])

# Route to book a service (create a service request)
@app.route('/api/book-service', methods=['POST'])
def book_service():
    data = request.get_json()
    new_request = ServiceRequest(
        service_id=data['service_id'],
        professional_id=data['professional_id'],
        customer_id=1,  # This should come from the logged-in user
        date_of_request=datetime.utcnow(),
    )
    db.session.add(new_request)
    db.session.commit()
    return jsonify({"message": "Service booked successfully"}), 201

# Route to close a service request
@app.route('/api/close-service', methods=['POST'])
def close_service():
    data = request.get_json()
    service_request = ServiceRequest.query.filter_by(service_id=data['service_id']).first()
    if service_request:
        service_request.service_status = 'completed'
        db.session.commit()
        return jsonify({"message": "Service closed successfully"})
    return jsonify({"error": "Service not found"}), 404


# Route to get customer profile
@app.route('/api/customer/profile', methods=['GET'])
def get_customer_profile():
    customer_id = session.get('customer_id')
    if not customer_id:
        return jsonify({'error': 'Not logged in'}), 401
    
    customer = Customer.query.filter_by(customer_id=customer_id).first()
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
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

# Route to update customer information (example for updating address)
@app.route('/api/customer/update', methods=['PUT'])
def update_customer():
    customer_id = session.get('customer_id')
    if not customer_id:
        return jsonify({'error': 'Not logged in'}), 401
    
    customer = Customer.query.filter_by(customer_id=customer_id).first()
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    data = request.json
    if 'address' in data:
        customer.address = data['address']
    
    db.session.commit()
    return jsonify({'message': 'Profile updated successfully'}), 200

# Route to get all service requests for a customer (joins customer and service tables)
@app.route('/api/customer/requests', methods=['GET'])
def get_service_requests():
    customer_id = session.get('customer_id')
    if not customer_id:
        return jsonify({'error': 'Not logged in'}), 401
    
    requests = db.session.query(ServiceRequest, Service).join(Service, ServiceRequest.service_id == Service.service_id) \
        .filter(ServiceRequest.customer_id == customer_id).all()
    
    response_data = []
    for request, service in requests:
        response_data.append({
            'service_name': service.service_name,
            'date_of_request': request.date_of_request,
            'service_status': request.service_status
        })
    
    return jsonify(response_data), 200

@app.route('/api/register', methods=['POST'])
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
    hashed_password = generate_password_hash(data['password'], method='sha256')

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

# Customer Login Route
@app.route('/api/login', methods=['POST'])
def login_customer():
    data = request.get_json()

    if 'email' not in data or 'password' not in data:
        return jsonify({"error": "Email and password are required."}), 400

    customer = Customer.query.filter_by(email=data['email']).first()

    if not customer or not check_password_hash(customer.password, data['password']):
        return jsonify({"error": "Invalid email or password."}), 401

    return jsonify({"message": "Login successful!"}), 200

# Service Request Route (for registered customers to request services)
@app.route('/api/request-service', methods=['POST'])
def request_service():
    data = request.get_json()

    # Validate incoming data
    if 'customer_id' not in data or 'service_id' not in data:
        return jsonify({"error": "Missing customer_id or service_id"}), 400

    customer = Customer.query.get(data['customer_id'])
    if not customer:
        return jsonify({"error": "Customer not found."}), 404

    service = Service.query.get(data['service_id'])
    if not service:
        return jsonify({"error": "Service not found."}), 404

    service_request = ServiceRequest(
        service_id=service.service_id,
        customer_id=customer.customer_id,
        date_of_request=datetime.now().date()
    )

    try:
        db.session.add(service_request)
        db.session.commit()
        return jsonify({"message": "Service request submitted successfully!"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Error submitting service request."}), 500

@app.route('/api/service/<int:service_id>', methods=['GET'])
def get_service(service_id):
    service = db.session.query(Service).filter(Service.service_id == service_id).first()
    if service:
        # Get service details along with related professional info
        service_details = db.session.query(Service, Professional).join(Professional, Professional.service_name == Service.service_name).filter(Service.service_id == service_id).first()

        if service_details:
            service_data = {
                'service_id': service_details.Service.service_id,
                'service_name': service_details.Service.service_name,
                'professional_name': service_details.Professional.full_name,
                'base_price': service_details.Service.base_price,
                'description': service_details.Service.description,
                'time_required': service_details.Service.time_required
            }
            return jsonify(service_data)
        return jsonify({'message': 'Professional not found for this service'}), 404
    return jsonify({'message': 'Service not found'}), 404

@app.route('/api/service/remarks', methods=['POST'])
def submit_remarks():
    data = request.json
    service_id = data.get('service_id')
    customer_id = data.get('customer_id')
    rating = data.get('rating')
    remarks = data.get('remarks')

    # Check if the service and customer exist
    service = Service.query.get(service_id)
    customer = Customer.query.get(customer_id)
    
    if not service or not customer:
        return jsonify({'message': 'Service or customer not found'}), 404

    # Create a new service request or update existing one
    service_request = ServiceRequest.query.filter_by(service_id=service_id, customer_id=customer_id, service_status='completed').first()
    
    if not service_request:
        service_request = ServiceRequest(
            service_id=service_id,
            customer_id=customer_id,
            date_of_request=datetime.now(),
            service_status='completed'
        )
        db.session.add(service_request)
        db.session.commit()

    # Create or update the review
    review = Review.query.filter_by(service_request_id=service_request.request_id).first()

    if not review:
        review = Review(
            service_request_id=service_request.request_id,
            rating=rating,
            comments=remarks
        )
        db.session.add(review)
    else:
        review.rating = rating
        review.comments = remarks

    db.session.commit()

    return jsonify({'message': 'Remarks submitted successfully'}), 200

@app.route('/search', methods=['GET'])
def search():
    search_by = request.args.get('search_by', 'service_name')
    search_input = request.args.get('search_input', '')
    
    if search_by == 'service_name':
        results = db.session.query(Professional).join(Service).filter(Service.service_name.ilike(f'%{search_input}%')).all()
    elif search_by == 'pin_code':
        results = db.session.query(Professional).filter(Professional.pincode.like(f'%{search_input}%')).all()
    elif search_by == 'location':
        results = db.session.query(Professional).filter(Professional.address.ilike(f'%{search_input}%')).all()
    else:
        return jsonify({'error': 'Invalid search filter'}), 400

    if not results:
        return jsonify({'message': 'No results found'}), 404

    # Return relevant details for frontend
    search_results = []
    for result in results:
        professional_info = {
            'professional_id': result.professional_id,
            'full_name': result.full_name,
            'service_name': result.service_name,
            'experience': result.experience,
            'address': result.address,
            'pincode': result.pincode
        }
        search_results.append(professional_info)

    return jsonify(search_results)

# Booking Route
@app.route('/book', methods=['POST'])
def book_service():
    data = request.get_json()
    professional_id = data.get('professional_id')
    service_name = data.get('service_name')
    professional_name = data.get('professional_name')
    customer_id = data.get('customer_id')  # You might need to get the customer ID from the session or token

    # Create a new service request
    service = Service.query.filter_by(service_name=service_name).first()
    customer = Customer.query.filter_by(customer_id=customer_id).first()

    if not service or not customer:
        return jsonify({'error': 'Service or customer not found'}), 404

    new_request = ServiceRequest(
        service_id=service.service_id,
        customer_id=customer.customer_id,
        professional_id=professional_id,
        date_of_request=func.now()
    )

    db.session.add(new_request)
    db.session.commit()

    return jsonify({'message': f'Service request for {professional_name} booked successfully'}), 201

# Get Professional Details
@app.route('/professional/<int:professional_id>', methods=['GET'])
def get_professional_details(professional_id):
    professional = Professional.query.filter_by(professional_id=professional_id).first()

    if not professional:
        return jsonify({'error': 'Professional not found'}), 404

    # Return the professional details
    professional_details = {
        'full_name': professional.full_name,
        'service_name': professional.service_name,
        'experience': professional.experience,
        'address': professional.address,
        'pincode': professional.pincode,
        'email': professional.email
    }

    return jsonify(professional_details)

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

@app.route('/api/profile', methods=['GET'])
def get_profile():
    # Get the profile of the logged-in professional
    professional_id = request.args.get('professional_id')
    professional = Professional.query.filter_by(professional_id=professional_id).first()
    
    if professional:
        return jsonify({
            'email': professional.email,
            'full_name': professional.full_name,
            'service_name': professional.service_name,
            'experience': professional.experience,
            'address': professional.address,
            'pincode': professional.pincode,
            'status': professional.status,
        }), 200
    return jsonify({'error': 'Profile not found'}), 404

@app.route('/api/profile', methods=['PUT'])
def edit_profile():
    # Edit the profile of the logged-in professional
    professional_id = request.json.get('professional_id')
    professional = Professional.query.filter_by(professional_id=professional_id).first()

    if professional:
        professional.full_name = request.json.get('full_name', professional.full_name)
        professional.service_name = request.json.get('service_name', professional.service_name)
        professional.experience = request.json.get('experience', professional.experience)
        professional.address = request.json.get('address', professional.address)
        professional.pincode = request.json.get('pincode', professional.pincode)
        professional.status = request.json.get('status', professional.status)
        professional.date_updated = datetime.utcnow()

        db.session.commit()

        return jsonify({'message': 'Profile updated successfully'}), 200
    return jsonify({'error': 'Profile not found'}), 404

@app.route('/api/today-services', methods=['GET'])
def get_today_services():
    # Get services for today with customer and professional info (if any)
    today = datetime.utcnow().date()
    today_services = db.session.query(ServiceRequest, Customer, Professional).join(
        Customer, ServiceRequest.customer_id == Customer.customer_id
    ).join(
        Professional, ServiceRequest.professional_id == Professional.professional_id, isouter=True
    ).filter(
        ServiceRequest.date_of_request == today,
        ServiceRequest.service_status == 'requested'
    ).all()

    services_data = []
    for service_request, customer, professional in today_services:
        services_data.append({
            'id': service_request.request_id,
            'customer_name': customer.full_name,
            'email': customer.email,
            'location': customer.address,
            'professional_name': professional.full_name if professional else None,
        })
    
    return jsonify(services_data), 200

@app.route('/api/accept-service', methods=['POST'])
def accept_service():
    # Accept a service request
    request_id = request.json.get('request_id')
    service_request = ServiceRequest.query.filter_by(request_id=request_id).first()

    if service_request and service_request.service_status == 'requested':
        service_request.service_status = 'assigned'
        service_request.professional_id = request.json.get('professional_id')
        db.session.commit()

        return jsonify({'message': 'Service accepted successfully'}), 200
    return jsonify({'error': 'Service request not found or already accepted'}), 404

@app.route('/api/reject-service', methods=['POST'])
def reject_service():
    # Reject a service request
    request_id = request.json.get('request_id')
    service_request = ServiceRequest.query.filter_by(request_id=request_id).first()

    if service_request and service_request.service_status == 'requested':
        service_request.service_status = 'rejected'
        db.session.commit()

        return jsonify({'message': 'Service rejected successfully'}), 200
    return jsonify({'error': 'Service request not found or already processed'}), 404

@app.route('/api/closed-services', methods=['GET'])
def get_closed_services():
    # Get closed services with customer and professional info (if any)
    closed_services = db.session.query(ServiceRequest, Customer, Professional, Review).join(
        Customer, ServiceRequest.customer_id == Customer.customer_id
    ).join(
        Professional, ServiceRequest.professional_id == Professional.professional_id, isouter=True
    ).join(
        Review, ServiceRequest.request_id == Review.service_request_id, isouter=True
    ).filter(
        ServiceRequest.service_status == 'completed'
    ).all()

    services_data = []
    for service_request, customer, professional, review in closed_services:
        services_data.append({
            'id': service_request.request_id,
            'customer_name': customer.full_name,
            'email': customer.email,
            'location': customer.address,
            'date': service_request.date_of_completion,
            'rating': review.rating if review else 'No rating',
        })
    
    return jsonify(services_data), 200

@app.route('/api/professional/<int:professional_id>', methods=['PUT'])
def update_professional_profile(professional_id):
    """
    Route to update professional profile data.
    """
    # Get the logged-in user (In this example, it's assumed you use session or JWT for authentication)
    # This should be checked with proper authentication and authorization
    logged_in_professional_id = session.get('professional_id')  # Or from JWT
    if logged_in_professional_id != professional_id:
        return jsonify({"message": "Unauthorized"}), 403

    # Fetch the professional data from the database
    professional = Professional.query.get(professional_id)
    if not professional:
        return jsonify({"message": "Professional not found"}), 404

    # Get data from the request
    data = request.json
    if 'full_name' in data:
        professional.full_name = data['full_name']
    if 'service_name' in data:
        professional.service_name = data['service_name']
    if 'experience' in data:
        professional.experience = data['experience']
    if 'address' in data:
        professional.address = data['address']
    if 'pincode' in data:
        professional.pincode = data['pincode']
    
    # Handle document upload (optional, if the file is uploaded)
    document = data.get('document')
    if document:
        professional.document = document  # Save document (make sure it's properly handled as a file)

    # Set the date_updated field to the current time
    professional.date_updated = datetime.utcnow()

    # Commit the changes to the database
    try:
        db.session.commit()
        return jsonify({"message": "Profile updated successfully!"}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Error updating profile, please try again."}), 500
    
# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/update_profile/<int:professional_id>', methods=['PUT'])
def update_professional_profile(professional_id):
    professional = Professional.query.get_or_404(professional_id)

    data = request.form
    # Handle updating non-document fields
    if 'email' in data:
        professional.email = data['email']
    if 'password' in data:
        professional.password = data['password']  # You can hash the password here if needed
    if 'full_name' in data:
        professional.full_name = data['full_name']
    if 'service_name' in data:
        professional.service_name = data['service_name']
    if 'experience' in data:
        professional.experience = int(data['experience'])
    if 'address' in data:
        professional.address = data['address']
    if 'pincode' in data:
        professional.pincode = data['pincode']
    
    # Handle file upload (document)
    if 'document' in request.files:
        file = request.files['document']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Store the file path or binary data in the database
            with open(filepath, 'rb') as f:
                professional.document = f.read()
    
    # Update the date_updated field to the current time
    professional.date_updated = datetime.utcnow()

    try:
        db.session.commit()
        return jsonify({
            'message': 'Profile updated successfully!',
            'data': {
                'email': professional.email,
                'full_name': professional.full_name,
                'service_name': professional.service_name,
                'experience': professional.experience,
                'address': professional.address,
                'pincode': professional.pincode,
                'status': professional.status.name,
                'role': professional.role.name
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating profile', 'error': str(e)}), 500
    
@app.route('/api/register-professional', methods=['POST'])
def register_professional():
    # Extracting the form data from the request
    data = request.form
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('fullname')
    service_name = data.get('service_name')
    experience = int(data.get('experience'))
    address = data.get('address')
    pincode = data.get('pincode')

    # Handling the document file
    document = request.files.get('documents')
    if document and allowed_file(document.filename):
        filename = secure_filename(document.filename)
        document_data = document.read()  # Reading the file content as binary data
    else:
        return jsonify({"error": "Invalid file format or no file uploaded"}), 400

    # Creating a new professional record
    new_professional = Professional(
        email=email,
        password=password,  # Remember to hash the password in a real-world scenario
        full_name=full_name,
        service_name=service_name,
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

# Route to handle user login (for demonstration purposes)
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Check if professional exists with the provided email and password
    professional = Professional.query.filter_by(email=email, password=password).first()
    if professional:
        return jsonify({"message": "Login successful", "professional_id": professional.professional_id}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/professional_search', methods=['GET'])
def professional_search():
    search_by = request.args.get('searchBy', 'date')  # Default is 'date'
    search_text = request.args.get('searchText', '').lower()

    query = db.session.query(ServiceRequest, Customer, Professional, Review).join(
        Customer, ServiceRequest.customer_id == Customer.customer_id
    ).join(
        Service, ServiceRequest.service_id == Service.service_id
    ).join(
        Professional, ServiceRequest.professional_id == Professional.professional_id, isouter=True
    ).join(
        Review, ServiceRequest.request_id == Review.service_request_id, isouter=True
    )

    # Filtering based on the 'searchBy' and 'searchText'
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

    # Execute the query and return the results
    results = query.all()

    # Prepare the results for the response
    search_results = []
    for service_request, customer, professional, review in results:
        result = {
            'id': service_request.request_id,
            'customer_name': customer.full_name,
            'email': customer.email,
            'location': customer.address,
            'date': service_request.date_of_request.strftime('%Y-%m-%d'),
            'rating': review.rating if review else None,
        }
        search_results.append(result)

    return jsonify(search_results)

@app.route('/api/reviews-ratings', methods=['GET'])
def get_reviews_ratings():
    try:
        # Query to get average ratings and count per rating level
        ratings = db.session.query(
            Review.rating,
            func.count(Review.rating).label('count')
        ).join(ServiceRequest).group_by(Review.rating).all()

        # Format ratings data to return
        ratings_data = {str(rating.rating): rating.count for rating in ratings}

        # Get average rating (if needed)
        average_rating = db.session.query(
            func.avg(Review.rating).label('avg_rating')
        ).scalar()

        return jsonify({
            'ratingsData': ratings_data,
            'averageRating': average_rating if average_rating else 0
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/service-requests', methods=['GET'])
def get_service_requests():
    try:
        # Query to get service requests count by status
        service_requests = db.session.query(
            ServiceRequest.service_status,
            func.count(ServiceRequest.service_status).label('count')
        ).group_by(ServiceRequest.service_status).all()

        # Format service requests data to return
        service_requests_data = {request.service_status: request.count for request in service_requests}

        return jsonify({
            'serviceRequestsData': service_requests_data
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/professional/<int:professional_id>', methods=['GET'])
def get_professional(professional_id):
    try:
        # Query the Professional data with the provided ID
        professional = db.session.query(Professional).filter_by(professional_id=professional_id).first()

        if not professional:
            return jsonify({'message': 'Professional not found'}), 404
        
        # You can also join other tables if needed (like ServiceRequest)
        # Example: joinedload(ServiceRequest)
        response_data = {
            'fullName': professional.full_name,
            'email': professional.email,
            'serviceName': professional.service_name,
            'experience': professional.experience,
            'address': professional.address,
            'pincode': professional.pincode,
            'role': professional.role,
            'status': professional.status,
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({'message': 'Error fetching professional data', 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)