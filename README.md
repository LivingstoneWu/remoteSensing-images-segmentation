# remoteSensing-images-segmentation

##Introduction
This project provide a workflow that trains a random forest/decision tree/SVM machine model upon given multispectral samples in xls format (which is a standard output of ArcGIS), and apply the model on a given image to output prediction result in Tiff.

##Configuration
Required packages include GDAL, NumPy, sklearn, xlrd, pickle (only if you wish to save the model).
