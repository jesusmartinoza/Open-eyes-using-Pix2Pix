from FacePatcher import FacePatcher
import os
import random

closed_eyes_files = os.listdir("closed_eyes_dataset/")
faces_files = os.listdir("regular_faces/")

for idx, f in enumerate(closed_eyes_files):
    if 'jpg' in f or 'png' in f:
        try:
            f = FacePatcher("closed_eyes_dataset/" + f,
                            "regular_faces/" + faces_files[random.randint(1,len(faces_files)-1)])

            f.save_result("generated_data/face_" + str(idx) + ".jpg")
        except ValueError as err:
            a = 2
        except:
            f = FacePatcher("closed_eyes_dataset/" + f,
                            "regular_faces/" + faces_files[random.randint(1,len(faces_files)-1)])

            f.save_result("generated_data/face_" + str(idx) + ".jpg")
