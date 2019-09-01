from FacePatcher import FacePatcher
import os
import random

closed_eyes_files = sorted(os.listdir("closed_eyes_dataset/"))
faces_files = os.listdir("regular_faces/")

# Standarize names
# for idx, f in enumerate(faces_files):
#      if 'jpg' in f or 'png' in f:
#          os.rename("regular_faces/"+f, "regular_faces/face_" + str(idx) + ".jpg")

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
