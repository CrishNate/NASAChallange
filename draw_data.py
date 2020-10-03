import numpy as np
from PIL import Image, ImageDraw
import netCDF4  as nc
import filter as fc

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
    if v.max() > 0:
        images.append(v * 255. / v.max())

a = np.stack(images)
ims = [Image.fromarray(images) for images in a]
ims[0].save("out_test.gif", save_all=True, append_images=ims[1:])