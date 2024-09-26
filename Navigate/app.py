from flask import Flask, render_template

app = Flask(__name__)

# Route for home page
@app.route('/')
def home():
    return render_template('home.html')

# Route for about page
@app.route('/about')
def about():
    return render_template('about.html')

# Route for contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
