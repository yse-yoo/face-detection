import cv2
import numpy as np
import os

def detect_faces(image_data):
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    if len(faces) == 0:
        print("No faces detected")  # デバッグ表示

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    return img

def register_face(user_id, image_data):
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    if len(faces) == 0:
        print("No faces detected")  # デバッグ表示

    if len(faces) == 1:
        x, y, w, h = faces[0]
        face_img = gray[y:y + h, x:x + w]
        cv2.imwrite(f'static/registered_faces/{user_id}.jpg', face_img)
        return True
    else:
        return False

def recognize_face(image_data):
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    if len(faces) == 1:
        x, y, w, h = faces[0]
        face_img = gray[y:y + h, x:x + w]

        for filename in os.listdir('static/registered_faces'):
            registered_face = cv2.imread(f'static/registered_faces/{filename}', cv2.IMREAD_GRAYSCALE)
            res = cv2.matchTemplate(face_img, registered_face, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(res)
            if max_val > 0.7:
                return filename.split('.')[0]

    return None
