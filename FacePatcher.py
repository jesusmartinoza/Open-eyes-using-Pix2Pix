import cv2
import numpy as np
import dlib

# This file receive picture_1 and target_face.
# The goal is to extract eyes of target_face and patch them in picture_1

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

picture_1 = cv2.imread('people1.jpg')
target_face = cv2.imread('people2.jpg')

#make pictures gray
picture_gray = cv2.cvtColor(picture_1, cv2.COLOR_BGR2GRAY)
target_face_gray = cv2.cvtColor(target_face, cv2.COLOR_BGR2GRAY)

# Get faces of the picture_1
faces = detector(picture_gray)

for face in faces:
    x1 = face.left()
    y1 = face.top()
    x2 = face.right()
    y2 = face.bottom()
    #cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

    landmarks = predictor(picture_gray, face)

    for n in range(0, 68):
        x = landmarks.part(n).x
        y = landmarks.part(n).y
        cv2.circle(picture_1, (x, y), 4, (255, 0, 0), -1)

    # Landmarks for eyes
    # - Left eye points: 36, 37, 38, 39, 40, 41
    # - Right eye points: 42, 43, 44, 45, 46, 47

cv2.imshow('my image',target_face)
cv2.waitKey(0)
cv2.destroyAllWindows()