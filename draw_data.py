import numpy as np
from PIL import Image, ImageDraw
import netCDF4  as nc
import filter as fc
import cv2
from datetime import datetime, timedelta

import detect

# longitude
# latitude

fn = 'C:/Users/someonelse/Downloads/ua_data_FossilFuelCarbonOnly.nc'

# gathering data
ds = nc.Dataset(fn)

data = ds.variables["ecff_conc"][:]
data_leng = len(data)
split = ds.variables["time"].long_name.split()
longitude = ds.variables["longitude"][:]
latitude = ds.variables["latitude"][:]
time_stamp_data = split[-1]
time_stamp = datetime(year=int(time_stamp_data[0:4]), month=int(time_stamp_data[4:6]), day=int(time_stamp_data[6:8]))

# init data set
layer_data = np.array(data[0][0].filled(fill_value=0))

leng_y = len(layer_data)
leng_x = len(layer_data[0])
data_lines = [[[0] * data_leng for i in range(leng_x)] for j in range(leng_y)]

def analyze(coord, time):
    coors_lang = (longitude[coord[0]], latitude[coord[1]])
    print(coors_lang, time)

# init data
for i in range(0, data_leng):
    v = np.array(data[i][0].filled(fill_value=0)) # one layer
    for j in range(0, leng_y):
        for k in range(0, leng_x):
            data_lines[j][k][i] = v[j][k]

# filtering
for i in range(0, leng_y):
    for j in range(0, leng_x):
        data_lines[i][j] = fc.filter(data_lines[i][j])


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
    img = Image.fromarray(v * 255. / (v.max() + 2.220446049250313e-16))

    cv_img = np.array(img.convert('RGB'))
    cv_img = cv_img[:, :, ::-1].copy()

    images.append(img)

    coords = detect.detect_blob(cv_img)
    time = time_stamp + timedelta(hours=int(ds.variables["time"][i]))

    for coord in coords:
        analyze(coord, time)

images[0].save("out_test.gif", save_all=True, append_images=images[1:])