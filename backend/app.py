from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.face_detection import detect_faces
import cv2
import base64

app = Flask(__name__)
CORS(app)  # これでCORSが有効になります

@app.route('/detect', methods=['POST'])
def detect():
    file = request.files['image']
    img = file.read()

    result_img = detect_faces(img)

    _, buffer = cv2.imencode('.jpg', result_img)
    encoded_img = base64.b64encode(buffer).decode('utf-8')
    return jsonify({'image': encoded_img})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
