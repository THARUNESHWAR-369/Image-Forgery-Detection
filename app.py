from flask import Flask, render_template, request, redirect, url_for
import cv2
import hashlib
from io import BytesIO

app = Flask(__name__)

def calculate_md5(image_data):
    md5_hash = hashlib.md5(image_data).hexdigest()
    return md5_hash

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    # Handle login functionality here
    username = request.form['username']
    password = request.form['password']
    print(username, password)
    if username == password:
        return redirect(url_for('admin'))
    return redirect(url_for("home"))

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/detect_forgery', methods=['POST'])
def detect_forgery():
    original_image = request.files['original_image']
    modified_image = request.files['modified_image']

    original_image_data = original_image.read()
    modified_image_data = modified_image.read()

    original_hash = calculate_md5(original_image_data)
    modified_hash = calculate_md5(modified_image_data)

    if original_hash == modified_hash:
        result = "The images are identical."
    else:
        result = "The images are different. Forgery detected!"

    return render_template('admin.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
