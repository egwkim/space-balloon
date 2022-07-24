import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import os
import sys


def main():
    # Select data file
    filename = input('File name: ')
    filepath = os.path.join('data', filename)
    if not os.path.isfile(filepath):
        try:
            # If file is not found, use the latest data in the data directory
            filepath = os.path.join('data', sorted(os.listdir('data'))[-1])
            print(f'Using {filepath} since {filename} is not found')
        except IndexError:
            # Data directory is empty
            print('No data file found')
            sys.exit(1)

    ds = xr.open_dataset(filepath, engine='cfgrib',
                         backend_kwargs={'errors': 'ignore', 'indexpath': ''},
                         filter_by_keys={'typeOfLevel': 'isobaricInhPa'})

    # Select latitude
    latitude = 37.25
    try:
        print(ds['latitude'].__array__())
        latitude = float(input(f'Select latitude (default: {latitude}): '))
    except ValueError:
        pass

    # Select longitude
    longitude = 126.5
    try:
        print(ds['longitude'].__array__())
        longitude = float(input(f'Select longitude (default: {longitude}): '))
    except ValueError:
        pass

    # Get dataset from selected latitude and longitude
    ds = ds.sel(latitude=latitude, longitude=longitude)

    # Plot pressure - temperature graph
    plt.plot(ds['isobaricInhPa'], ds['t'])
    plt.show()


if __name__ == '__main__':
    main()
