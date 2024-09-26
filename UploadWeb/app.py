#Build a Flask app that allows users to upload files and display them on the website.

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__)

# Configuration for file uploads
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        return redirect(url_for('uploaded_file', filename=file.filename))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return render_template('uploaded_file.html', filename=filename)

@app.route('/display/<filename>')
def display_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
