import cv2
import numpy as np

def find_face_locations(image):
    """
    Detects faces within an image using OpenCV's Haar feature-based cascade classifiers.

    Parameters:
    image (numpy.ndarray): The image in which to detect faces, in BGR format.

    Returns:
    numpy.ndarray: An array of rectangles, where each rectangle contains the (x, y, width, height) of a detected face.
    """
    # Load the pre-trained Haar cascade for frontal face detection from OpenCV's data directory
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # Convert the image to grayscale as Haar cascades require gray images
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Detect faces in the image. Adjust the parameters for different use cases.
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
    return faces

def find_face_encodings(image, faces):
    """
    Extracts face encodings (regions) from an image based on detected face locations.

    Parameters:
    image (numpy.ndarray): The original image from which faces are to be extracted.
    faces (numpy.ndarray): An array of rectangles, where each rectangle contains the (x, y, width, height) of a detected face.

    Returns:
    list: A list of numpy.ndarray, each representing a cropped image of a detected face.
    """
    face_encodings = []
    for (x, y, w, h) in faces:
        # Crop the face region from the original image using the coordinates and dimensions of each face
        face_encodings.append(image[y:y+h, x:x+w])
    return face_encodings

def compare_faces(known_face, unknown_faces):
    """
    Compares a known face with a list of unknown faces to find a match based on template matching.

    This function converts both the known face and each of the unknown faces to grayscale,
    then uses OpenCV's matchTemplate function to compare the known face against each unknown face.
    A match is found if the highest template matching score exceeds a predefined threshold.

    Parameters:
    known_face (numpy.ndarray): The image of the known face in BGR format.
    unknown_faces (list of numpy.ndarray): A list of images of unknown faces, each in BGR format.

    Returns:
    bool: True if a match is found (i.e., at least one unknown face matches the known face above the threshold); otherwise, False.
    """
    known_face_gray = cv2.cvtColor(known_face, cv2.COLOR_BGR2GRAY)  # Convert the known face to grayscale
    for face in unknown_faces:
        face_gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)  # Convert each unknown face to grayscale
        res = cv2.matchTemplate(face_gray, known_face_gray, cv2.TM_CCOEFF_NORMED)  # Compare the known face against each unknown face
        _, max_val, _, _ = cv2.minMaxLoc(res)  # Find the highest matching score
        if max_val > 0.6:  # If the highest score exceeds the threshold, a match is found
            return True
    return False  # If no matches are found above the threshold, return False

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