import numpy as np
from PIL import Image, ImageDraw
import netCDF4  as nc
import filter as fc
import cv2
import detect

# longitude
# latitude

fn = 'C:/Users/someonelse/Downloads/ua_data_FossilFuelCarbonOnly.nc'

ds = nc.Dataset(fn)

data = ds.variables["ecff_conc"][:]
data_leng = len(data)

# init data set
layer_data = np.array(data[0][0].filled(fill_value=0))

leng_y = len(layer_data)
leng_x = len(layer_data[0])
data_lines = [[[0] * data_leng for i in range(leng_x)] for j in range(leng_y)]

# init data
for i in range(0, data_leng):
    v = np.array(data[i][0].filled(fill_value=0)) # one layer
    for j in range(0, leng_y):
        for k in range(0, leng_x):
            data_lines[j][k][i] = v[j][k]

max = 0
# filtering
for i in range(0, leng_y):
    for j in range(0, leng_x):
        data_lines[i][j] = fc.filter(data_lines[i][j])

        if data_lines[i][j].max() > max:
            max = data_lines[i][j].max()

# output image sequence
images = []
for i in range(0, data_leng):
    result = []
    for j in range(0, leng_y):
        result_line = []
        for k in range(0, leng_x):
            result_line.append(data_lines[j][k][i])
        result.append(result_line)

    v = np.array(result)
    if v.max() > 0:
        img = Image.fromarray(v * 255. / v.max())

        cv_img = np.array(img.convert('RGB'))
        cv_img = cv_img[:, :, ::-1].copy()

        temp = cv_img.copy()
        a = detect.detect_blob(cv_img)

        width = int(temp.shape[1] * 4)
        height = int(temp.shape[0] * 4)
        dsize = (width, height)
        temp = cv2.resize(temp, dsize)
        cv2.imshow("aaa", temp)
        cv2.waitKey()

        width = int(cv_img.shape[1] * 4)
        height = int(cv_img.shape[0] * 4)
        dsize = (width, height)
        cv_img = cv2.resize(cv_img, dsize)
        cv2.imshow("aaa", cv_img)
        cv2.waitKey()

        # cv2.imwrite("out_test1.png", cv_img)

        images.append(img)

images[0].save("out_test.gif", save_all=True, append_images=images[1:])