import cv2
import numpy as np
import dlib
import imutils
from color_transfer import color_transfer
from math import atan2,degrees
from PIL import Image

class FacePatcher:
    """
    This file receive picture_input and target_face.
    The goal is to extract eyes of target_face and patch them in picture_input

    @author: Jesús Alberto Martínez Mendoza
    """
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    def __init__(self, picture_input = None, target_face = None, is_test = False):
        """
        Read images from paths and init patching.

        First transfer picture style using
        https://github.com/jrosebr1/color_transfer
        """
        self.is_test = is_test

        if picture_input is not None:
            self.picture_input = cv2.imread(picture_input)
            self.target_face = cv2.imread(target_face)

            if not self.is_greyscale(picture_input) and not self.is_greyscale(target_face):
                self.target_face = color_transfer(self.picture_input, self.target_face)
            self.initPatching()

    def load_from_files(self, picture_input, target_face):
        npimg = np.fromfile(picture_input, np.uint8)
        self.picture_input = cv2.imdecode(npimg, cv2.COLOR_BGR2RGB)

        npimg = np.fromfile(target_face, np.uint8)
        self.target_face = cv2.imdecode(npimg, cv2.COLOR_BGR2RGB)

        #if not self.is_greyscale(picture_input) and not self.is_greyscale(target_face):
        #    self.target_face = color_transfer(self.picture_input, self.target_face)

        self.initPatching()

    def is_greyscale(self, img_path):
        """
        https://stackoverflow.com/questions/23660929/how-to-check-whether-a-jpeg-image-is-color-or-gray-scale-using-only-python-stdli
        """
        img = Image.open(img_path).convert('RGB')
        w,h = img.size
        for i in range(w):
            for j in range(h):
                r,g,b = img.getpixel((i,j))
                if r != g != b: return False
        return True

    def overlay_image_alpha(self, picture, img_overlay, pos, alpha_mask):
        """
        Overlay img_overlay on top of img at the position specified by
        pos and blend using alpha_mask.

        Alpha mask must contain values within the range [0, 1] and be the
        same size as img_overlay.
        """
        img = picture
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

        self.result = img

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

    def crop_face(self, image, face):
        offset = int(image.shape[1] / 6)
        x, y = face.left(), face.top()
        x1, y1 = face.right(), face.bottom()

        cropped = image[y - offset:y1 + offset, x - offset:x1 + offset].copy()

        return cropped

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

        if len(eye) == 0:
            raise AttributeError('No left eye detected')

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

        if len(eye) == 0:
            raise AttributeError('No right eye detected')

        return cv2.cvtColor(eye, cv2.COLOR_RGB2RGBA).copy(), w, h, padding

    def save_result(self, name):
        """
        Store image in disk
        """
        #cv2.imwrite(name, self.picture_input)
        h1, w1 = self.picture_input.shape[:2]
        h2, w2 = img2.shape[:2]
        vis = np.zeros((max(h1, h2), w1+w2), np.uint8)
        vis[:h1, :w1] = img1
        vis[:h2, w1:w1+w2] = img2
        vis = cv2.cvtColor(vis, cv2.COLOR_GRAY2BGR)
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

        # Crop closed eyes face from picture_input
        extracted_face = self.crop_face(self.picture_input, faces[face_to_change])
        face_gray = cv2.cvtColor(extracted_face, cv2.COLOR_BGR2GRAY)
        faces = FacePatcher.detector(face_gray)
        
        if len(faces) == 0:
            raise ValueError('Not detected face in input image')

        landmarks = FacePatcher.predictor(face_gray, faces[0])
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
        self.overlay_image_alpha(extracted_face,
                                left_eye[:, :, 0:3],
                                (l_eye_x - le_p, l_eye_y - left_eye.shape[0] + le_p),
                                left_eye[:, :, 3] / 255.0)

        self.overlay_image_alpha(extracted_face,
                                right_eye[:, :, 0:3],
                                (r_eye_x - re_p, r_eye_y - right_eye.shape[0] + re_p),
                                right_eye[:, :, 3] / 255.0)

        if self.is_test: # Draw eye landmarks
            for n in range(0, 68):
                x = landmarks.part(n).x
                y = landmarks.part(n).y

                cv2.circle(self.result, (x, y), 4, (255, 0, 255), -1)

                # Left eye
                if n in range(36, 42):
                    cv2.circle(self.result, (x, y), 4, (255, 0, 0), -1)

                # Right eye
                if n in range(42, 48):
                   cv2.circle(self.result, (x, y), 4, (255, 0, 0), -1)