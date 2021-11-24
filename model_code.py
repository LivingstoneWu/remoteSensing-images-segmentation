import xlrd
import sklearn
from sklearn import tree
import pickle
import osgeo
from osgeo import gdal
import numpy as np

# paths
savePath = "../../data/model.pickle"
image_path = "../../data/408data.tif"
image_save_path = "../../data/result.tif"
workbook_path = "../../data/newSamples.xls"

# read data from the table
workbook = xlrd.open_workbook(workbook_path)
table = workbook.sheets()[0]
dataset = []
data_size = table.nrows
for i in range(1, data_size):
    dataset.append(table.row_values(i))

# set data and label
samples_data = []
samples_label = []

for i in range(len(dataset)):
    samples_data.append(dataset[i][3:10])  # set the data columns
    samples_label.append(dataset[i][1])  # set the label column
X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(samples_data, samples_label, random_state=0)
classifier = tree.DecisionTreeClassifier(criterion='gini', max_depth=3, min_samples_leaf=30)
classifier = classifier.fit(X_train, y_train)

# print model's score on training set and testing set
print("on training set: ", classifier.score(X_train, y_train))
print("on testing set: ", classifier.score(X_test, y_test))


file=open(savePath,"wb")
pickle.dump(classifier,file)
file.close()

feature_name=["B","G","R","B5","B6","B7","B8"]
import graphviz
dot_data=tree.export_graphviz(classifier,
                              feature_names=feature_name,
                              class_names=["小麦", "油菜","水体","建筑等"],
                              filled=True,
                              rounded=True,
                              out_file=None)
graph=graphviz.Source(dot_data)
print(graph.source)

# read image data
image = gdal.Open(image_path)
image_width = image.RasterXSize
image_height = image.RasterYSize
image_proj = image.GetProjection()
image_dataset = image.ReadAsArray(0, 0, image_width, image_height)
image_geotransform = image.GetGeoTransform()

# # load model
# file=open(savePath, "rb")
# trained_model=pickle.load(file)
# file.close()

# adjust dataset to feed into model
data = np.zeros((image_dataset.shape[0], image_dataset.shape[1] * image_dataset.shape[2]))
for i in range(image_dataset.shape[0]):
    data[i] = image_dataset[i].flatten()
data = data.swapaxes(0, 1)

pred = classifier.predict(data)

pred = np.reshape(pred,(image_dataset.shape[1],image_dataset.shape[2]))
pred = pred.astype(np.uint8)


def writeTiff(im_data, im_geotrans, im_proj, path):
    if 'int8' in im_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in im_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32
    if len(im_data.shape) == 3:
        im_bands, im_height, im_width = im_data.shape
    elif len(im_data.shape) == 2:
        im_data = np.array([im_data])
        im_bands, im_height, im_width = im_data.shape

    # Create the result file
    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(path, int(im_width), int(im_height), int(im_bands), datatype)
    if (dataset != None):
        dataset.SetGeoTransform(im_geotrans)  # Write geotransformation
        dataset.SetProjection(im_proj)  # set Projection
    for i in range(im_bands):
        dataset.GetRasterBand(i + 1).WriteArray(im_data[i])
    del dataset


writeTiff(pred, image_geotransform, image_proj, image_save_path)
