#Implement user sessions in a Flask app to store and display user-specific data.

from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

# Secret key is necessary for session management
app.secret_key = 'supersecretkey'

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Login route - display form and handle form submission
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        # Store the username in session
        session['username'] = username
        return redirect(url_for('profile'))
    return render_template('login.html')

# Profile route - accessible only if logged in
@app.route('/profile')
def profile():
    if 'username' in session:
        return render_template('profile.html')
    return redirect(url_for('login'))

# Logout route - clear the session
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
