# remoteSensing-images-segmentation

## 1. Introduction
This project provide a workflow that trains a random forest/decision tree/SVM machine model upon given multispectral samples in xls format (which is a standard output of ArcGIS), and apply the model on a given image to output prediction result in Tiff.

## 2. Configuration
Required packages include GDAL, NumPy, sklearn, xlrd, pickle (only if you wish to save the model).

## 3. Samples
### 3.1 rape-wheat classification
<img width="429" alt="image" src="https://user-images.githubusercontent.com/52390858/144867346-d93ab795-e97a-449d-a4a7-55b82a2b958c.png">
<center style="font-size:14px;color:#C0C0C0">A Sentinel-2 image of Yancheng, Jiangsu, China shot on 08/04/2021</center>

The two crops are easily recognizable as the rape is flowering, showing a bright-green and yellow tone.
**Sampling:**<br>
<img width="568" alt="image" src="https://user-images.githubusercontent.com/52390858/144868473-d766b5d7-2459-49d4-b0c7-a8cab42a1bc7.png">
<center style="font-size:14px;color:#C0C0C0">Samples took in 4 classes: water, rape, wheat, and buildings/roads</center>

The NDVI (Normalized Difference Vegetation Index) was added into the spectral data to help the random forest model identify crops from water and buildings.

<img width="514" alt="image" src="https://user-images.githubusercontent.com/52390858/144870638-08aa9ead-3972-4794-85cf-25b8c0202b96.png">
<center style="font-size:14px;color:#C0C0C0"> The classification result</center>

### 3.2 
