import numpy as np
from PIL import Image, ImageDraw
import netCDF4  as nc
import filter as fc

# longitude
# latitude

fn = 'C:/Users/someonelse/Downloads/ua_data_FossilFuelCarbonOnly.nc'
analyze_range = 10

ds = nc.Dataset(fn)

data = ds.variables["ecff_conc"][:50]
data_leng = len(data)
images = [] * data_leng

# init data set
layer_data = np.array(data[0][0].filled(fill_value=0))

leng_y = len(layer_data)
leng_x = len(layer_data[0])
data_lines = [[[0] * analyze_range for i in range(leng_x)] for j in range(leng_y)]

for x in range(0, data_leng):
    start_x = max(min(x - analyze_range, data_leng), 0)
    end_x = max(min(x + 1, data_leng), 0)

    result = []
    for i in range(0, end_x - start_x):
        v = np.array(data[start_x + i][0].filled(fill_value=0)) # one layer

        for j in range(0, leng_y):
            for k in range(0, leng_x):
                data_lines[j][k][0] = v[j][k]

    for data_horizontal_line in data_lines:
        result_line = []

        for data_line in data_horizontal_line:
            if data_line[0] > 6.923174e-11:
                data_line[0] = 0
            #data_line = fc.filter_lowpass(data_line)
            result_line.append(data_line[0])

        result.append(result_line)

    result = np.array(result)
    result = result * 255. / result.max()
    images[x] = result
    print(x)

a = np.stack(images)
ims = [Image.fromarray(images) for images in a]
ims[0].save("out1.gif", save_all=True, append_images=ims[1:])