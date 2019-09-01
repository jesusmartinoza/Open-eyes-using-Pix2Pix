import cv2
import numpy as np
import dlib

"""
This file receive picture_1 and target_face.
The goal is to extract eyes of target_face and patch them in picture_1
"""
def overlay_image_alpha(img, img_overlay, pos, alpha_mask):
    """
    Overlay img_overlay on top of img at the position specified by
    pos and blend using alpha_mask.

    Alpha mask must contain values within the range [0, 1] and be the
    same size as img_overlay.
    """

    x, y = pos

    # Image ranges
    y1, y2 = max(0, y), min(img.shape[0], y + img_overlay.shape[0])
    x1, x2 = max(0, x), min(img.shape[1], x + img_overlay.shape[1])

    # Overlay ranges
    y1o, y2o = max(0, -y), min(img_overlay.shape[0], img.shape[0] - y)
    x1o, x2o = max(0, -x), min(img_overlay.shape[1], img.shape[1] - x)

    # Exit if nothing to do
    if y1 >= y2 or x1 >= x2 or y1o >= y2o or x1o >= x2o:
        return

    channels = img.shape[2]

    alpha = alpha_mask[y1o:y2o, x1o:x2o]
    alpha_inv = 1.0 - alpha

    for c in range(channels):
        img[y1:y2, x1:x2, c] = (alpha * img_overlay[y1o:y2o, x1o:x2o, c] +
                                alpha_inv * img[y1:y2, x1:x2, c])

def midpoint(p1 ,p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

def extract_left_eye(face, landmarks):
    left_point = (landmarks.part(36).x, landmarks.part(36).y)
    right_point = (landmarks.part(39).x, landmarks.part(39).y)
    center_top = midpoint(landmarks.part(37), landmarks.part(38))
    center_bottom = midpoint(landmarks.part(41), landmarks.part(40))

    # Crop [x:w, y:h]
    # crop_img = img[y:y+h, x:x+w]
    print(left_point, right_point, center_top , center_bottom)
    x = landmarks.part(36).x
    y = landmarks.part(37).y
    w = landmarks.part(39).x - x
    h = landmarks.part(40).y - y

    offset = int(w / 5)
    x -= offset
    y -= offset
    w += offset * 2
    h += offset * 2

    eye = face[y:y+h, x:x+w].copy()

    return cv2.cvtColor(eye, cv2.COLOR_RGB2RGBA).copy(), w, h

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

picture_1 = cv2.imread('people1.jpg')
target_face = cv2.imread('people2.jpg')
#target_face = cv2.cvtColor(target_face, cv2.COLOR_RGB2RGBA).copy()

# Make pictures gray
picture_gray = cv2.cvtColor(picture_1, cv2.COLOR_BGR2GRAY)
target_face_gray = cv2.cvtColor(target_face, cv2.COLOR_BGR2GRAY)

# Get faces of the picture_1
faces = detector(target_face_gray)

for face in faces:
    x1 = face.left()
    y1 = face.top()
    x2 = face.right()
    y2 = face.bottom()
    #cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

    landmarks = predictor(target_face_gray, face)
    left_eye, le_w, le_h = extract_left_eye(target_face, landmarks)

    # Landmarks for eyes
    # - Left eye points: 36, 37, 38, 39, 40, 41
    # - Right eye points: 42, 43, 44, 45, 46, 47
    # Reference: https://pysource.com/wp-content/uploads/2019/06/landmarks_points_eyes.png
    for n in range(0, 68):
        x = landmarks.part(n).x
        y = landmarks.part(n).y

        # Left eye
        if n in range(36, 42):
            cv2.circle(target_face, (x, y), 4, (255, 0, 0), -1)

        # Right eye
        if n in range(42, 48):
           cv2.circle(target_face, (x, y), 4, (255, 0, 0), -1)


# Get faces of the picture_1
faces = detector(picture_gray)

for face in faces:
    x1 = face.left()
    y1 = face.top()
    x2 = face.right()
    y2 = face.bottom()
    #cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

    landmarks = predictor(picture_gray, face)
    eye_x = landmarks.part(36).x
    eye_y = landmarks.part(37).y
    eye_w = landmarks.part(39).x - eye_x
    eye_h = landmarks.part(40).y - eye_y
    offset = int(eye_w / 6)

    print('extracted_w: ' + str(le_w) + ' target_w: ' + str(eye_w))
    print('extracted_h: ' + str(le_h) + ' target_h: ' + str(eye_h))
    w_ratio = le_w / eye_w
    h_ratio = le_h / eye_h
    left_eye = cv2.resize(left_eye, None, fx = w_ratio * 1.1, fy = w_ratio * 1.1)

    overlay_image_alpha(picture_1,
                       left_eye[:, :, 0:3],
                       (eye_x - offset, eye_y - offset * 2),
                       left_eye[:, :, 3] / 255.0)

    for n in range(0, 68):
        x = landmarks.part(n).x
        y = landmarks.part(n).y

        # Left eye
        if n in range(36, 42):
            cv2.circle(picture_1, (x, y), 4, (255, 0, 0), -1)

        # Right eye
        if n in range(42, 48):
           cv2.circle(picture_1, (x, y), 4, (255, 0, 0), -1)

cv2.imshow('my image',picture_1)
cv2.waitKey(0)
cv2.destroyAllWindows()