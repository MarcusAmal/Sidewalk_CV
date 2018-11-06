# Converts the images to Grey Scale
#
# This file changes all the images in the Directory to GreyScale,
# to use just update the DIRECTORY variable 


import os
from PIL import Image

DIRECTORY = "/Users/marcus/Desktop/Training_Data_SVM/"

for dir_name, sub_dir_list, file_list in os.walk(DIRECTORY):
    for file_name in file_list:
        if file_name[-4:] == ".jpg" and len(file_name) > 5:
            image_path = os.path.join(dir_name, file_name)
            img = Image.open(image_path)
            img = img.convert('L')
            
            img.save(image_path)

