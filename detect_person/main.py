import cv2
import numpy as np

def find_face_locations(image):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
    return faces

def find_face_encodings(image, faces):
    face_encodings = []
    for (x, y, w, h) in faces:
        face_encodings.append(image[y:y+h, x:x+w])
    return face_encodings

def compare_faces(known_face, unknown_faces):
    known_face_gray = cv2.cvtColor(known_face, cv2.COLOR_BGR2GRAY)
    for face in unknown_faces:
        face_gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(face_gray, known_face_gray, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)
        if max_val > 0.6:  # Threshold value, can be adjusted
            return True
    return False

# Load a reference image and detect the face
reference_image = cv2.imread('reference_person.jpg')
reference_faces = find_face_locations(reference_image)
reference_encodings = find_face_encodings(reference_image, reference_faces)

# Start the webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    faces = find_face_locations(frame)
    face_encodings = find_face_encodings(frame, faces)

    if compare_faces(reference_encodings[0], face_encodings):
        print("Person detected!")

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()