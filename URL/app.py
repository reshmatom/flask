from flask import Flask, render_template

app = Flask(__name__)

# Route with dynamic URL parameters
@app.route('/index/<name>/<int:age>')
def greet(name, age):
    return render_template('index.html', name=name, age=age)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
