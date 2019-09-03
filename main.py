from FacePatcher import FacePatcher
import os
import random
import cv2

closed_eyes_files = sorted(os.listdir("closed_eyes_dataset/"))
faces_files = os.listdir("regular_faces/")
generated_files = os.listdir("generated_data/")

for idx, f in enumerate(closed_eyes_files):
    if 'jpg' in f or 'png' in f:
        try:
            im = cv2.imread("closed_eyes_dataset/" + f)

            # Just medium size pictures
            if im.shape[0] > 220 or im.shape[1] > 220:
                print(im.shape)
                f = FacePatcher("closed_eyes_dataset/" + f,
                                "regular_faces/" + faces_files[random.randint(1,len(faces_files)-1)])

                file_name = "face_" + str(idx) + ".jpg"
                if file_name not in generated_files:
                    f.save_result("generated_data/" + file_name)
        except ValueError as err:
            a = 2
        except:
            f = FacePatcher("closed_eyes_dataset/" + f,
                            "regular_faces/" + faces_files[random.randint(1,len(faces_files)-1)])

            f.save_result("generated_data/face_" + str(idx) + ".jpg")

# Standarize names
# for idx, f in enumerate(faces_files):
#      if 'jpg' in f or 'png' in f:
#          os.rename("regular_faces/"+f, "regular_faces/face_" + str(idx) + ".jpg")

# Find original generated_fixed file
# generated_fix_files = os.listdir("generated_fixed/")
# for idx, f in enumerate(generated_fix_files):
#     print(f)
#     if f in generated_files:
#         os.system('cp generated_data/{} pruebas/{}'.format(f, f))