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

def bulk_extract_crops():
    csv_f = open(LABEL_LIST_PATH)
    csv_file = csv.reader(csv_f)

    sorted_csv = sorted(csv_file, key = operator.itemgetter(0))
    print(len(sorted_csv))

bulk_extract_crops()
