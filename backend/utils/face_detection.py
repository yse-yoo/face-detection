import cv2
import numpy as np
import os

def detect_faces(image_data):
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        print("Failed to decode image")
        return None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    if face_cascade.empty():
        print("Failed to load cascade classifier")
        return None

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    if len(faces) == 0:
        print("No faces detected")
        return None

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    return img

def register_face(user_id, image_data, timestamp):
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        print("Failed to decode image")
        return False

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    if face_cascade.empty():
        print("Failed to load cascade classifier")
        return False

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    if len(faces) == 0:
        print("No faces detected")
        return False

    x, y, w, h = faces[0]
    face_img = gray[y:y + h, x:x + w]

    user_dir = os.path.join('static/registered_faces', user_id)
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)

    face_path = os.path.join(user_dir, f'{timestamp}.jpg')
    cv2.imwrite(face_path, face_img)
    print(f"Saved face image for user ID: {user_id} at {face_path}")
    return True

def recognize_face(image_data):
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        print("Failed to decode image")
        return None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    if face_cascade.empty():
        print("Failed to load cascade classifier")
        return None

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    if len(faces) == 0:
        print("No faces detected")
        return None

    x, y, w, h = faces[0]
    face_img = gray[y:y + h, x:x + w]

    for user_id in os.listdir('static/registered_faces'):
        user_dir = os.path.join('static/registered_faces', user_id)
        if os.path.isdir(user_dir):
            for filename in os.listdir(user_dir):
                registered_face = cv2.imread(os.path.join(user_dir, filename), cv2.IMREAD_GRAYSCALE)
                if registered_face is None:
                    print(f"Failed to load registered face: {filename}")
                    continue

                res = cv2.matchTemplate(face_img, registered_face, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(res)
                if max_val > 0.7:
                    recognized_user = user_id
                    print(f"Recognized user ID: {recognized_user}")
                    return recognized_user

    print("No user recognized")
    return None
