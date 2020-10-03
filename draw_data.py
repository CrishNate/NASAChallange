import numpy as np
from PIL import Image
import netCDF4  as nc

fn = 'C:/Users/someonelse/Downloads/dataset-cems-fire-historical-37ed8d86-5a3b-4817-9d06-db8d0494adde/ECMWF_FWI_DANGER_RISK_20200101_1200_hr_v3.1_con.nc'
ds = nc.Dataset(fn)
a = ds.variables["danger_risk"][0].filled(fill_value=0)
v = np.array(a);
max = v.max()
v = v * 255. / max

img = Image.fromarray( v )       # Create a PIL image
img.show()                      # View in default viewer