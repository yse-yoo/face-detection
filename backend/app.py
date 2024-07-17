from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.face_detection import detect_faces, register_face, recognize_face
import cv2
import base64
import os

app = Flask(__name__)
CORS(app)

@app.route('/detect', methods=['POST'])
def detect():
    file = request.files['image']
    img = file.read()

    result_img = detect_faces(img)

    _, buffer = cv2.imencode('.jpg', result_img)
    encoded_img = base64.b64encode(buffer).decode('utf-8')
    return jsonify({'image': encoded_img})

@app.route('/register', methods=['POST'])
def register():
    file = request.files['image']
    img = file.read()
    user_id = request.form['user_id']

    print(f"Received image for user ID: {user_id}")  # デバッグ表示
    print(f"Image size: {len(img)} bytes")  # 画像サイズを表示

    if register_face(user_id, img):
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'failure'})

@app.route('/recognize', methods=['POST'])
def recognize():
    file = request.files['image']
    img = file.read()

    recognized_user = recognize_face(img)

    if recognized_user:
        return jsonify({'status': 'success', 'user_id': recognized_user})
    else:
        return jsonify({'status': 'failure'})

if __name__ == '__main__':
    if not os.path.exists('static/registered_faces'):
        os.makedirs('static/registered_faces')
    app.run(host='0.0.0.0', port=5000)
