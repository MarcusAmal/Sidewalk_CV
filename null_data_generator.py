"""
To obtain the labelData as the CSV
Run getFullLabelList.sql in the Sidewalk Database

"""

# This script generates null_data, that shouldnt have any features in it
import csv
import json
import os
import logging
import operator

from PIL import Image, ImageDraw
import math
import shutil
import random
import numpy as np

PATH_TO_LABEL_LIST = "/Users/marcus/Desktop/labeldata.csv"
GSV_PANO_PATH = "/Volumes/Extreme SSD/Sandbox Data/"
CROP_DESTINATION_PATH = "/Users/marcus/Desktop/Training_Data_SVM_null/"
PANO_HEIGHT = 4096
PANO_WIDTH = 2048


# Enter desired crop sidelength here, default value is 
CROP_HEIGHT_WIDTH = 246 #in Pixels(Default value is: )
PIXEL_CROP_SIZE = int(crop_height_width/2)

label = {
    1 : "CurbRamp",
    2 : "NoCurbRamp",
    3 : "Obstacle",
    4 : "SurfaceProblem",
    5 : "Other",
    6 : "Occlusion",
    7 : "NoSidewalk"
}


def bulkExtractCrops(path_to_label_csv, GSV_PANO_PATH, CROP_DESTINATION_PATH):
    csv_file = open(path_to_label_csv)
    csv_f = csv.reader(csv_file)

    pano_list = []

    no_metadata_fail = 0
    no_pano_fail = 0
    counter = 0

    label_counts = [0,0,0,0]
    something = 0 

    for row in csv_f:
        something += 1
        if(counter >= 2000):
            break
        pano_id = row[0]
        sv_image_x = float(row[1])
        sv_image_y = float(row[2])
        label_type = int(row[3])
        photographer_heading = float(row[4])
        label_id = int(row[7])

        print("Status: [" + "#" * int(counter/20) + " " * (100 - int(counter/20)) + "]" + "  {}/2000    ".format(counter) + str(something) + " " + str(label_counts), end = '\r')
        pano_yaw_deg = 180 - photographer_heading
        x, y = getLabelCoordinates(sv_image_x, sv_image_y, pano_yaw_deg)
        pano_img_path = os.path.join(GSV_PANO_PATH, pano_id[:2], pano_id + ".jpg")
    
        if os.path.exists(pano_img_path):
            if not pano_img_path in pano_list:
                pano = Image.open(pano_img_path)
                # Checks to see if the pano is blacked out, if so it skips it.
                if pano.getbbox() == None or label_type > 4:
                    continue
                count_index = label_type - 1

                if label_counts[count_index] < 501 :
                    label_counts[count_index] += 1
                    counter += 1
                else:
                    continue
            
            label_folder = os.path.join(CROP_DESTINATION_PATH, label[label_type])
            if not os.path.isdir(label_folder):
                os.makedirs(label_folder)
            destination_folder = os.path.join(label_folder, pano_id[:2])
            if not os.path.isdir(destination_folder):
                os.makedirs(destination_folder)
            crop_name = "{0}_._{1}_._{2}_._{3}_._".format(pano_id, label[label_type], str(x), str(y))
            crop_destination = os.path.join(CROP_DESTINATION_PATH, label[label_type], pano_id[:2], crop_name + ".jpg")
            json_destination = os.path.join(CROP_DESTINATION_PATH, label[label_type], pano_id[:2], crop_name + ".json")
            if not os.path.exists(crop_destination):
                fixedCropSinglePano(pano_img_path, x, y, crop_destination, label_type)
                createJsonFile(pano_id, x, y, row, json_destination)
                logging.info(crop_name + ".jpg" + " " + pano_id + " " + str(sv_image_x)
                             + " " + str(sv_image_y) + " " + str(pano_yaw_deg) + " " + str(label_id))
                logging.info("---------------------------------------------------")
        else:
            no_pano_fail += 1

    print("Finished.")
    print(str(no_pano_fail) + " extractions failed because panorama image was not found.")
    print(str(no_metadata_fail) + " extractions failed because metadata was not found.")


#Creates and Exports JSON File
def createJsonFile(panoId, x, y, row, destination):
    #Adds the data into a dictionary
    data = {}
    data["Pano_Data"] = []
    data["Pano_Data"].append({
       'GSV_Pano_ID': panoId,
        'label_x': str(x),
        'label_y': str(y),
        'x1': str(x - PIXEL_CROP_SIZE
    ),
        'y1': str(y - PIXEL_CROP_SIZE
    ),
        'x2': str(x + PIXEL_CROP_SIZE
    ),
        'y2': "{0}".format((y + PIXEL_CROP_SIZE
    )),
        'sv_image_x': row[1],
        'sv_image_y': row[2],
        'label_type': label[int(row[3])],
        'label_type_id': row[3],
        'pano_yaw-deg' : 180 - float(row[4]),
        'photographer_heading': row[4],
        'heading': row[5],
        'pitch': row[6],
        'label_id': row[7]
        
    })
    #Exports the json file to destination folder
    with open(destination, 'w') as outfile:
        json.dump(data, outfile)

#Gets the X, Y coordinates from the the variables below
def getLabelCoordinates(sv_image_x, sv_image_y, pano_yaw_deg):
    PANO_WIDTH = 13312
    PANO_HEIGHT = 6656


    x_label = ((float(pano_yaw_deg) / 360) * PANO_WIDTH + sv_image_x) % PANO_WIDTH
    y_label = PANO_HEIGHT / 2 - sv_image_y
    return x_label/3.25 , y_label/3.25

def fixedCropSinglePano(pano_img_path, x, y, crop_destination, label_id, tag = False):
    pano = Image.open(pano_img_path)
    tag = Image.open("./Tags/{0}.png".format(label[label_id]))
    
    randx = [-PIXEL_CROP_SIZE
, 0, PIXEL_CROP_SIZE
][random.randint(0,2)]
    randy = [-PIXEL_CROP_SIZE
, 0, PIXEL_CROP_SIZE
][random.randint(0,2)]
    
    


    x = int(x) + randx
    y = int(y) + randy
    croppedPano = pano.crop((x - PIXEL_CROP_SIZE
, y - PIXEL_CROP_SIZE
, x + PIXEL_CROP_SIZE
, y + PIXEL_CROP_SIZE
))
    # Saves cropped Pano without tag
    croppedPano.save(crop_destination)
    # Saves cropped Pano with tag
    if tag:
        croppedPano.paste(tag, (int(croppedPano.height/2 - tag.height/2), int(croppedPano.width/2 - tag.width/2)))
        croppedPano.save(crop_destination[:-4] + "_tagged.jpg")
    


bulkExtractCrops(PATH_TO_LABEL_LIST, GSV_PANO_PATH, CROP_DESTINATION_PATH)
