#Implement user authentication and registration in a Flask app using Flask-Login.
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize the Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisismysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and login manager
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User model for the database
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Create the database table
with app.app_context():
    db.create_all()

# Load the user by their ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')

        # Check if passwords match
        if password != password_confirm:
            flash('Passwords do not match!')
            return redirect(url_for('register'))

        # Check if the user already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists!')
            return redirect(url_for('register'))

        # Generate hashed password using PBKDF2 SHA256
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful, please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Fetch the user from the database
        user = User.query.filter_by(email=email).first()

        # Check if user exists and if the password matches
        if not user or not check_password_hash(user.password, password):
            flash('Invalid login credentials')
            return redirect(url_for('login'))

        # Log in the user
        login_user(user)
        return redirect(url_for('dashboard'))

    return render_template('login.html')

# Dashboard (Protected Route)
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.email)

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
