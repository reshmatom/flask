from flask import Flask, render_template, request

app = Flask(__name__)

# Route for displaying the form
@app.route('/')
def form():
    return render_template('form.html')

# Route to handle the form submission
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    age = request.form['age']
    return render_template('result.html', name=name, age=age)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
