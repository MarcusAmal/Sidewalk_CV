# Sidewalk_CV
In order for

## Template Matching Notebook

## training_set_generator.py

To obtain the labelData as the CSV
Run getFullLabelList.sql in the Sidewalk Database
This script will create a training set that is seperate from the dump of the pano_images
Update the Global Variables below and enter CROP_AMT, which is the amount of each crop type
you want.
The Data will be seperated into two folders, one with the panos and one with the crops
As of 9/30/2018 the script only creates a set with CurbRamp, NoCurbRamp, Obstacle, SurfaceProblem

## Potentially Useful Scripts

### ImageResizer.py
Resizes all images in GSV_PANO_PATH to 4096, 2048 a new DESTINATION_PATH, maintains the same directory structure and copies all the metadata to the from GSV_PANO_PATH to DESTINATION_PATH

### greyscale_converter.py
Input a directory of images as DIRECTORY, this script will convert all the images in the directory into grayscale.

### null_data_generator.py
Using the x,y coordinates of the labels in the pano, this script will generate crops that do not contain any labels. 

### pano_label_json_generator.py
Parses through the entire directory containing the crops and the respective metadata, and creates a new metadata file for each pano that contains all information regarding every single label it contains.

### training_set_generator.py
This script will create a training set that is seperate from the dump of the pano_images. By changing CROP_AMT you can alter the amount of each crop type you want. The Data will be seperated into two folders, one with a copy of the panos and one with the crops in the pano.
