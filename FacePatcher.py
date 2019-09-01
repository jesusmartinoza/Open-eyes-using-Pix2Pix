import cv2
import numpy as np
import dlib
import imutils
from math import atan2,degrees

class FacePatcher:
    """
    This file receive picture_input and target_face.
    The goal is to extract eyes of target_face and patch them in picture_input

    @author: Jesús Alberto Martínez Mendoza
    """
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    def __init__(self, picture_input, target_face, test = False):
        """
        Read images from paths and init patching
        """
        self.picture_input = cv2.imread(picture_input)
        self.target_face = cv2.imread(target_face)
        self.test = test
        self.initPatching()

    def overlay_image_alpha(self, img_overlay, pos, alpha_mask):
        """
        Overlay img_overlay on top of img at the position specified by
        pos and blend using alpha_mask.

        Alpha mask must contain values within the range [0, 1] and be the
        same size as img_overlay.
        """
        img = self.picture_input
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

    def calculate_eyes_angle(self, landmarks):
        """
        SOHCAHTOA
        """
        l_delta_X = landmarks.part(39).x - landmarks.part(36).x
        l_delta_Y = landmarks.part(39).y - landmarks.part(36).y
        l_angle = degrees(atan2(l_delta_Y, l_delta_X))

        r_delta_X = landmarks.part(45).x - landmarks.part(42).x
        r_delta_Y = landmarks.part(45).y - landmarks.part(42).y
        r_angle = degrees(atan2(r_delta_Y, r_delta_X))

        return (l_angle, r_angle)

    def extract_left_eye(self, face, landmarks):
        x = landmarks.part(36).x
        y = landmarks.part(37).y
        w = landmarks.part(39).x - x
        h = landmarks.part(40).y - y

        padding = int(w / 5)
        x -= padding
        y -= padding
        w += padding * 2
        h += padding * 2

        # Crop [y:y+h, x:x+w]
        eye = face[y:y+h, x:x+w].copy()

        return cv2.cvtColor(eye, cv2.COLOR_RGB2RGBA).copy(), w, h, padding

    def extract_right_eye(self, face, landmarks):
        x = landmarks.part(42).x
        y = landmarks.part(43).y
        w = landmarks.part(45).x - x
        h = landmarks.part(46).y - y

        padding = int(w / 5)
        x -= padding
        y -= padding
        w += padding * 2
        h += padding * 2

        # Crop [y:y+h, x:x+w]
        eye = face[y:y+h, x:x+w].copy()

        return cv2.cvtColor(eye, cv2.COLOR_RGB2RGBA).copy(), w, h, padding

    def save_result(self, name):
        """
        Store image in disk
        """
        cv2.imwrite(name, self.picture_input)
        print("Image saved with name:" + name)

    def show_result(self):
        """
        Show patching result using cv2
        """
        cv2.imshow('Result of patch',self.picture_input)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def initPatching(self):
        """
        Main function of FacePatcher.
        It extracts eyes from target_face and patch them in picture_input.

        Landmarks for eyes
        - Left eye points: 36, 37, 38, 39, 40, 41
        - Right eye points: 42, 43, 44, 45, 46, 47

        For a detailed image please visit:
        https://pysource.com/wp-content/uploads/2019/06/landmarks_points_eyes.png

        DISCLAIMER: This function is a little messy 😅 Eventually I will clean it
        since I don't have time because #RetoDotCSV2080Super deadline is in 2 weeks!
        TODO: Clean this function
        """
        print("Init patching...")
        # Make pictures gray
        picture_gray = cv2.cvtColor(self.picture_input, cv2.COLOR_BGR2GRAY)
        target_face_gray = cv2.cvtColor(self.target_face, cv2.COLOR_BGR2GRAY)

        # Get first detected face of target_face
        faces = FacePatcher.detector(target_face_gray)
        if len(faces) == 0:
            raise ValueError('Not detected face in target image')

        landmarks = FacePatcher.predictor(target_face_gray, faces[0])
        # *_eye, *_eye_width, *_eye_height, *_eye_padding
        left_eye, le_w, le_h, le_p = self.extract_left_eye(self.target_face, landmarks)
        right_eye, ri_w, ri_h, re_p = self.extract_right_eye(self.target_face, landmarks)

        # Get faces of the self.picture_input
        faces = FacePatcher.detector(picture_gray)
        if len(faces) == 0:
            raise ValueError('Not detected face in input image')

        # Iterate in picture to find the face with the closest eyes
        prev_eye_height = float("inf") # A very opened eye
        face_to_change = 0

        for idx, face in enumerate(faces):
            landmarks = FacePatcher.predictor(picture_gray, face)
            eye_height = landmarks.part(41).y - landmarks.part(37).y

            if eye_height < prev_eye_height:
                face_to_change = idx

        landmarks = FacePatcher.predictor(picture_gray, faces[face_to_change])
        l_eye_x = landmarks.part(36).x
        l_eye_w = landmarks.part(39).x - l_eye_x
        l_eye_y = landmarks.part(41).y

        r_eye_x = landmarks.part(42).x
        r_eye_w = landmarks.part(45).x - r_eye_x
        r_eye_y = landmarks.part(47).y

        w_ratio = l_eye_w / (le_w - le_p * 2)
        left_eye = cv2.resize(left_eye, None, fx = w_ratio, fy = w_ratio)
        right_eye = cv2.resize(right_eye, None, fx = w_ratio, fy = w_ratio)

        # Rotate eyes to correct angle
        l_angle, r_angle = self.calculate_eyes_angle(landmarks)
        left_eye = imutils.rotate_bound(left_eye, l_angle)
        right_eye = imutils.rotate_bound(right_eye, r_angle)

        # Overlay eyes
        self.overlay_image_alpha(left_eye[:, :, 0:3],
                           (l_eye_x - le_p, l_eye_y - left_eye.shape[0] + le_p),
                           left_eye[:, :, 3] / 255.0)

        self.overlay_image_alpha(right_eye[:, :, 0:3],
                          (r_eye_x - re_p, r_eye_y - right_eye.shape[0] + re_p),
                          right_eye[:, :, 3] / 255.0)

        if self.test: # Draw eye landmarks
            for n in range(0, 68):
                x = landmarks.part(n).x
                y = landmarks.part(n).y

                # Left eye
                if n in range(36, 42):
                    cv2.circle(self.picture_input, (x, y), 4, (255, 0, 0), -1)

                # Right eye
                if n in range(42, 48):
                   cv2.circle(self.picture_input, (x, y), 4, (255, 0, 0), -1)