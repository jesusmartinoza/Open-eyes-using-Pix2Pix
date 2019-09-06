from FacePatcher import FacePatcher
import os
import random
import cv2
import numpy as np

faces_files = os.listdir("regular_faces/")
generated_files = os.listdir("generated_data/")
closed_eyes_files = sorted(os.listdir("closed_eyes_dataset/"))
generated_fix_files = os.listdir("generated_fixed/")

# for idx, f in enumerate(closed_eyes_files):
#     if 'jpg' in f or 'png' in f:
#         try:
#             im = cv2.imread("closed_eyes_dataset/" + f)
#
#             # Just medium size pictures
#             if im.shape[0] > 220 or im.shape[1] > 220:
#                 print(im.shape)
#                 f = FacePatcher("closed_eyes_dataset/" + f,
#                                 "regular_faces/" + faces_files[random.randint(1,len(faces_files)-1)])
#
#                 file_name = "face_" + str(idx) + ".jpg"
#                 if file_name not in generated_files:
#                     f.save_result("generated_data/" + file_name)
#         except ValueError as err:
#             a = 2
#         except:
#             f = FacePatcher("closed_eyes_dataset/" + f,
#                             "regular_faces/" + faces_files[random.randint(1,len(faces_files)-1)])
#
#             f.save_result("generated_data/face_" + str(idx) + ".jpg")

# Standarize names
# for idx, f in enumerate(faces_files):
#      if 'jpg' in f or 'png' in f:
#          os.rename("regular_faces/"+f, "regular_faces/face_" + str(idx) + ".jpg")

# Join generated_image with fixed image
for idx, f in enumerate(generated_fix_files):
    if f in generated_files:
        print(f)
        fix_image = cv2.imread("generated_fixed/" + f)
        print('Fixed image: {}'.format(fix_image.shape))
        gen_image = cv2.imread("generated_data/" + f)
        print('Fixed image: {}'.format(gen_image.shape))
        vis = np.concatenate((fix_image, gen_image), axis=1)
        cv2.imwrite('dataset/' + f, vis)