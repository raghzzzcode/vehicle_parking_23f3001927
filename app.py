from flask import Flask, render_template, request, redirect, url_for, flash, session
import secrets
from models import db, Migrate

app = Flask(__name__)   
app.secret_key = secrets.token_hex(16)

# Configuration for the database
app.config['SQLALCHEMY_DATABASE_URI'] = r"sqlite:////tmp/household_services_database_2.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)
m = Migrate(app,db)

# Create the tables (Only needed on the first run)
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("common/base.html")

