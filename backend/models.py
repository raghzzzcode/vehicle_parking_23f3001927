from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum

# Initializing the database
db = SQLAlchemy()

# Customer Table
class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text, nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    role = db.Column(Enum('customer', name='role'), default='customer')

# Professional Table
class Professional(db.Model):
    professional_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    service_name = db.Column(db.String(255), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    document = db.Column(db.LargeBinary)  # To store profile documents (e.g., PDF)
    address = db.Column(db.Text, nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    status = db.Column(Enum('pending', 'approved', 'blocked', name='status'), default='pending')
    role = db.Column(Enum('professional', name='role'), default='professional')
    date_created = db.Column(db.DateTime, nullable=False)
    date_updated = db.Column(db.DateTime, nullable=False)

# Admin Table
class Admin(db.Model):
    admin_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

# Services Table
class Service(db.Model):
    service_id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(256), nullable=False)
    base_price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    time_required = db.Column(db.Integer, nullable=False)

# ServiceRequest Table 
class ServiceRequest(db.Model):
    request_id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.service_id'), nullable=False)  # Foreign key to Service
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False)  # Foreign key to Customer
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.professional_id'), nullable=True)  # Foreign key to Professional
    date_of_request = db.Column(db.Date, nullable=False)
    date_of_completion = db.Column(db.Date, nullable=True)
    service_status = db.Column(Enum('requested', 'assigned', 'completed', name='service_status'), default='requested')
    remarks = db.Column(db.Text, nullable=True)

# Review Table 
class Review(db.Model):
    review_id = db.Column(db.Integer, primary_key=True)
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_request.request_id'), nullable=False)  # Foreign key to ServiceRequest
    rating = db.Column(db.Integer, nullable=False)  # Add validation in the application
    comments = db.Column(db.Text, nullable=True)
    __table_args__ = (db.UniqueConstraint('service_request_id', name='unique_service_review'),)
