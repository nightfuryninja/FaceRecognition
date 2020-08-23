import face_recognition
import cv2
import numpy
import pickle
from PIL import Image

# 2D Array containing Face Encodings and Names
known_faces = []
known_face_names = []

# Load known faces from an image.
def Load_Known_Faces_Image(image):
    print("Loading known faces...")
    global known_faces
    image = face_recognition.load_image_file("C:/Users/night/Documents/Test.jpg")
    known_faces = Locate_Faces(image)
    print("Loaded {0} known face(s).".format(len(known_faces)))

# Load known faces from a file.
def Load_Known_Faces_File():
    print("Loading known faces...")
    global known_faces
    with open('known_faces.dat', 'rb') as f:
        known_faces = pickle.load(f)
    print("Loaded {0} known face(s).".format(len(known_faces)))
    global known_face_names
    known_face_names = ["Harry Ramsey"]

# Locates the faces in an image.    
def Locate_Faces(image):
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)
    return face_encodings

def Identify_Faces(face_encodings):
    print("Identifying faces...") 
    face_names = []
    for face_encoding in face_encodings:
        global knonw_faces
        matches = face_recognition.compare_faces(known_faces, face_encoding)
        name = "Unknown"
        face_distances = face_recognition.face_distance(known_faces, face_encoding)
        best_match_index = numpy.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        face_names.append(name)
    return face_names

# Draw labels and add names to detected faces.
def Draw_Face_Labels(face_locations, face_names):
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Draw a box around the face
        cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 5)

        # Draw a label with a name below the face
        cv2.rectangle(image, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(image, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 2)

def Save_Known_Faces():
    with open('known_faces.dat', 'wb') as f:
        pickle.dump(known_faces, f)

Load_Known_Faces_File()

# Load the image and process it for face locations.
print("Finding faces in image...")
image = face_recognition.load_image_file("C:/Users/night/Documents/Test2.jpg")
Identify_Faces(Locate_Faces(image))
print("Found {0} face(s).".format(len(face_encodings)))

print("Identifying faces...")
face_names = Identify_Faces(face_encodings)
print("Identified {0} face(s).".format(len(face_encodings)))

Draw_Face_Labels(face_locations, face_names)
image2 = cv2.resize(image, (1536, 864))
image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)
cv2.imshow("Facial Recognition", image2)
k = cv2.waitKey(0)