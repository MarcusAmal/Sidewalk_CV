"""
To obtain the labelData as the CSV
Run getFullLabelList.sql in the Sidewalk Database

This script will create a training set that is seperate from the dump of the pano_images
Update the Global Variables below and enter CROP_AMT, which is the amount of each crop type
you want.

The Data will be seperated into two folders, one with the panos and one with the crops


As of 9/30/2018 the script only creates a set with CurbRamp, NoCurbRamp, Obstacle, SurfaceProblem
"""
import csv
import json
import os
import logging
import operator

from PIL import Image, ImageDraw
import math
import shutil

import numpy as np

PATH_TO_LABEL_LIST = "/Users/marcus/Desktop/labeldata.csv"
GSV_PANO_PATH = "/Volumes/Extreme SSD/Sandbox Data/"
DESTINATION_DIR = "/Users/marcus/Desktop/Training_Data_SVM_Control/"
PANO_HEIGHT = 4096
PANO_WIDTH = 2048

# Enter how many of each crop you need
CROP_AMT = 500
TOTAL_CROP_AMT = CROP_AMT * 4


CROP_HEIGHT_WIDTH = 800 #in Pixels(Default value is: )
PIXEL_CROP_SIZE = int((CROP_HEIGHT_WIDTH/2)/3.25)


PANO_LIST = []
LABEL = {
    1 : "CurbRamp",
    2 : "NoCurbRamp",
    3 : "Obstacle",
    4 : "SurfaceProblem",
    5 : "Other",
    6 : "Occlusion",
    7 : "NoSidewalk"
}

def bulkExtractCrops(path_to_label_csv, GSV_PANO_PATH, DESTINATION_DIR):
    csv_file = open(path_to_label_csv)
    csv_f = csv.reader(csv_file)

    no_metadata_fail = 0
    no_pano_fail = 0
    counter = 0

    label_counts = [0,0,0,0] 

    pano_copy_dir = os.path.join(DESTINATION_DIR, "Pano_{0}_{1}".format(PANO_HEIGHT, PANO_WIDTH))
    crop_copy_dir = os.path.join(DESTINATION_DIR, "Crop_{0}_{1}".format(PANO_HEIGHT, PANO_WIDTH))
    if not os.path.exists(pano_copy_dir):
        os.makedirs(pano_copy_dir)
    if not os.path.exists(crop_copy_dir):
        os.makedirs(crop_copy_dir)

    for row in csv_f: 
        if(counter >= TOTAL_CROP_AMT):
            break

        pano_id = row[0]
        sv_image_x = float(row[1])
        sv_image_y = float(row[2])
        label_type = int(row[3])
        photographer_heading = float(row[4])
        label_id = int(row[7])

        print(LABEL[0+1], ":" , label_counts[0], LABEL[1+1], ":" , label_counts[1], LABEL[2+1], ":" , label_counts[2],LABEL[3+1], ":" , label_counts[3],end = '\r')
        
        pano_yaw_deg = 180 - photographer_heading
        x, y = getLabelCoordinates(sv_image_x, sv_image_y, pano_yaw_deg)
        pano_img_path = os.path.join(GSV_PANO_PATH, pano_id[:2], pano_id + ".jpg")
        
        if os.path.exists(pano_img_path):
            if not pano_img_path in PANO_LIST:
                pano = Image.open(pano_img_path)
                # Checks to see if the pano is blacked out or not
                if pano.getbbox() == None or label_type > 4:
                    continue
                count_index = label_type - 1

                if label_counts[count_index] < 501 :
                    label_counts[count_index] += 1
                    counter += 1
                else:
                    continue
                
                shutil.copy2(pano_img_path, pano_copy_dir)
                PANO_LIST.append(pano_img_path)
            
            label_folder = os.path.join(crop_copy_dir, LABEL[label_type])
            if not os.path.isdir(label_folder):
                os.makedirs(label_folder)
            destination_folder = os.path.join(label_folder, pano_id[:2])
            if not os.path.isdir(destination_folder):
                os.makedirs(destination_folder)
            crop_name = "{0}_._{1}_._{2}_._{3}_._".format(pano_id, LABEL[label_type], str(x), str(y))
            crop_destination = os.path.join(crop_copy_dir, LABEL[label_type], pano_id[:2], crop_name + ".jpg")
            json_destination = os.path.join(crop_copy_dir, LABEL[label_type], pano_id[:2], crop_name + ".json")
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

def createJsonFile(panoId, x, y, row, destination):
    #Adds the data into a dictionary
    data = {}
    data["Pano_Data"] = []
    data["Pano_Data"].append({
       'GSV_Pano_ID': panoId,
        'label_x': str(x),
        'label_y': str(y),
        'x1': str(x - PIXEL_CROP_SIZE),
        'y1': str(y - PIXEL_CROP_SIZE),
        'x2': str(x + PIXEL_CROP_SIZE),
        'y2': "{0}".format((y + PIXEL_CROP_SIZE)),
        'sv_image_x': row[1],
        'sv_image_y': row[2],
        'label_type': LABEL[int(row[3])],
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


def getLabelCoordinates(sv_image_x, sv_image_y, pano_yaw_deg):
    PANO_WIDTH = 13312
    PANO_HEIGHT = 6656


    x_label = ((float(pano_yaw_deg) / 360) * PANO_WIDTH + sv_image_x) % PANO_WIDTH
    y_label = PANO_HEIGHT / 2 - sv_image_y
    return x_label/3.25 , y_label/3.25

def fixedCropSinglePano(pano, x, y, crop_destination, label_id, tag = False):
    x = int(x)
    y = int(y)  
    croppedPano = pano.crop((x - PIXEL_CROP_SIZE, y - PIXEL_CROP_SIZE, x + PIXEL_CROP_SIZE, y + PIXEL_CROP_SIZE))
    # Saves cropped Pano without tag
    croppedPano.save(crop_destination)
    # Saves cropped Pano with tag
    if tag == True:
        tag = Image.open("./Tags/{0}.png".format(LABEL[label_id]))
        croppedPano.paste(tag, (int(croppedPano.height/2 - tag.height/2), int(croppedPano.width/2 - tag.width/2)))
        croppedPano.save(crop_destination[:-4] + "_tagged.jpg")
    


bulkExtractCrops(PATH_TO_LABEL_LIST, GSV_PANO_PATH, DESTINATION_DIR)
