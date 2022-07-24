import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import os

ds = xr.open_dataset('data/2022072306.anl',engine='cfgrib',backend_kwargs={'errors':'ignore'},filter_by_keys={'typeOfLevel': 'isobaricInhPa'})

ds = ds.sel(latitude=37, longitude=125.5)

plt.plot(ds['isobaricInhPa'], ds['t'])
plt.show()
