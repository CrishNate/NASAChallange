import numpy as np
from scipy import signal
from astropy.convolution import convolve
from scipy.signal import convolve as scipy_convolve

FILTER_TAP_NUM = 37

filter_taps = np.array([
  0.007670476360046427,
  0.02692545378341951,
  0.03757124982400134,
  0.04187076304402351,
  0.02617972086533838,
  -0.0006363927258988782,
  -0.024382469969212024,
  -0.02751624313409613,
  -0.006411717758155898,
  0.02418314173865777,
  0.038423621861006396,
  0.01901955148361517,
  -0.02597779341323415,
  -0.0625539020012281,
  -0.050605553145569394,
  0.02743572322702793,
  0.14923134612290068,
  0.26046916330229924,
  0.30536576946063515,
  0.26046916330229924,
  0.14923134612290068,
  0.02743572322702793,
  -0.050605553145569394,
  -0.0625539020012281,
  -0.02597779341323415,
  0.01901955148361517,
  0.038423621861006396,
  0.02418314173865777,
  -0.006411717758155898,
  -0.02751624313409613,
  -0.024382469969212024,
  -0.0006363927258988782,
  0.02617972086533838,
  0.04187076304402351,
  0.03757124982400134,
  0.02692545378341951,
  0.007670476360046427
])


def filter_lowpass(signal):
  return scipy_convolve(signal, filter_taps, mode='same', method='direct')
