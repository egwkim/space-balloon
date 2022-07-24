import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import os


def get_data_path(filename: str = None, date=None, time=None, n: int = None):
    if not filename:
        # Get filename from date, time, and n
        if None in (date, time):
            # Not enough arguments
            raise ValueError('Not enough arguments.')
        # Get file extension
        if n is None:
            ext = 'anl'
        else:
            ext = f'f{n:03d}'
        filename = f'{date}{time}.{ext}'

    filepath = os.path.join('data', filename)
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f'{filepath} is not found.')
    return filepath


def get_recent_data_path():
    # Get sorted list of files in data directory
    files = sorted(filter(os.path.isfile,
                          map(lambda x: os.path.join('data', x), os.listdir('data'))))
    if not files:
        raise FileNotFoundError('Data directory is empty.')
    filepath = files[-1]
    return filepath


def main():
    # Select data file
    filename = input('File name: ')
    try:
        filepath = get_data_path(filename)
    except ValueError:
        filepath = get_recent_data_path()
        print(f'Using {filepath} since {filename} is not found')

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
