# Sidewalk_CV


## Notebooks

### Crop Classifier.ipynb 
A Random Forest Classifier was used to classify between the different crops. The features used to train were the raw pixels, from the crop, the SIFT histograms are available for training as well.

### HOG Notebook.ipynb
In this notebook, SIFT features were extracted from the crops, and each crop was assigned a histogram of SIFT features. 
Currently the features used to train were the raw pixels, but can easily be changed to use sift_features. Another random forest classifier was used, but can easily be changed to use a SVM. 

Contains a cell which has a slider method, that can be used for object detection. There are couple tests (not that good), using the model to predict the what the crop was based on the given crop from pano slider mechanism.

### Playground.ipynb
Practice creating SVMs and HOG feature extraction.

### Sift.ipynb
Practice extracting SIFT features from crops and matching them to their respective panos.

### Stanford Tutorial.ipynb
Practice using a rainforest classifier, going through the number detection example.

### SVM.ipynb
Practice training a SVM classifier, that was trained on the raw pixel data from each crop;

### Template Matching Sidewalk.ipynb
Selecting one Template for each label, and detecting them on a pano

### Template Matching.ipynb
Template Matching approach for the label detection, complete with data analysis

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
