import csv 
import json
import os
import logging
import operator

from PIL import Image, ImageDraw
import math
import shutil

import numpy as np

LABEL_LIST_PATH = "/Users/marcus/Desktop/labeldata.csv"
PANO_DUMP_PATH = ""

DESTINATION_PATH = ""

PANO_HEIGHT = 4096
PANO_WIDTH = 2048

LABEL = {
    1 : "CurbRamp",
    2 : "NoCurbRamp",
    3 : "Obstacle",
    4 : "SurfaceProblem",
    5 : "Other",
    6 : "Occlusion",
    7 : "NoSidewalk"
}
def get_csv_file():
    csv_f = open(LABEL_LIST_PATH)
    csv_file = csv.reader(csv_f)
    sorted_csv = sorted(csv_file, key = operator.itemgetter(0))
    return sorted_csv

def bulk_extract_crops():
    csv_file = get_csv_file()

    old_pano = ""
    pano = None
    for row in csv_file:
        pano_id = row[0]
        sv_image_x = float(row[1])
        sv_image_y = float(row[2])
        label_type = int(row[3])
        photographer_heading = float(row[4])
        label_id = int(row[7])

        


    

bulk_extract_crops()
