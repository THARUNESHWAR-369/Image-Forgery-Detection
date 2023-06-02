from flask import Flask, render_template, request
import cv2
import hashlib
import numpy as np
import base64

app = Flask(__name__)

def calculate_md5(image_data):
    md5_hash = hashlib.md5(image_data).hexdigest()
    return md5_hash

def detect_forgery(original_image_data, modified_image_data):
    original_hash = calculate_md5(original_image_data)
    modified_hash = calculate_md5(modified_image_data)

    if original_hash == modified_hash:
        result = "The images are identical."
        modified_image_encoded = None
    else:
        result = "The images are different. Forgery detected!"
        modified_image = cv2.imdecode(np.frombuffer(modified_image_data, np.uint8), cv2.IMREAD_COLOR)
        _, modified_image_encoded = cv2.imencode('.jpg', modified_image)
        modified_image_encoded = base64.b64encode(modified_image_encoded).decode('utf-8')

    return result, modified_image_encoded

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    # Handle login functionality here
    username = request.form['username']
    password = request.form['password']
    return render_template('admin.html')

@app.route('/admin', methods=['POST'])
def admin():
    original_image = request.files['original_image']
    modified_image = request.files['modified_image']

    original_image_data = original_image.read()
    modified_image_data = modified_image.read()

    result, modified_image_encoded = detect_forgery(original_image_data, modified_image_data)

    return render_template('admin.html', result=result, modified_image_encoded=modified_image_encoded)

if __name__ == '__main__':
    app.run(debug=True)
