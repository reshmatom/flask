from flask import Flask, render_template

app = Flask(__name__)

# Sample route
@app.route('/')
def home():
    return "Welcome to the Flask app!"

# A route that triggers a 404 error
@app.route('/not-found')
def not_found_route():
    # This will intentionally raise a 404 error
    return "This route does not exist!", 404

# A route that triggers a 500 error
@app.route('/error')
def error_route():
    # This will intentionally raise a 500 error
    raise Exception("This is a sample exception for testing.")

# Custom error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
