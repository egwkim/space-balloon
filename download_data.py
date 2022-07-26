from typing import Union
import urllib.request
import urllib.error
import errno
import os
import datetime

BUFFER_SIZE = 256*1024


def get_data(date: Union[int, str], time: Union[int, str], number: Union[int, None] = None, log: bool = False):
    """
    Get atmos data from https://nomads.ncep.noaa.gov
    Date format: YYYYMMDD
    Time format: HH (only 00, 06, 12, 18 are available)
    """

    if type(time) is int:
        time = f'{time:02d}'

    if number is not None:
        ext = f'f{number:03d}'
    else:
        ext = 'anl'

    filename = f'{date}{time}.{ext}'
    filepath = os.path.join('data', filename)
    if os.path.exists(filepath):
        raise FileExistsError(
            errno.ENOENT, os.strerror(errno.ENOENT), filepath)

    url = fr'https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?file=gfs.t{time}z.pgrb2.0p25.{ext}&lev_1000_mb=on&lev_100_mb=on&lev_10_m_above_ground=on&lev_10_mb=on&lev_150_mb=on&lev_15_mb=on&lev_1_mb=on&lev_200_mb=on&lev_20_mb=on&lev_250_mb=on&lev_2_mb=on&lev_300_mb=on&lev_30_mb=on&lev_350_mb=on&lev_3_mb=on&lev_400_mb=on&lev_40_mb=on&lev_450_mb=on&lev_500_mb=on&lev_50_mb=on&lev_550_mb=on&lev_5_mb=on&lev_600_mb=on&lev_650_mb=on&lev_700_mb=on&lev_70_mb=on&lev_750_mb=on&lev_7_mb=on&lev_800_mb=on&lev_850_mb=on&lev_900_mb=on&lev_925_mb=on&lev_950_mb=on&lev_975_mb=on&var_ABSV=on&var_DZDT=on&var_HGT=on&var_RH=on&var_SPFH=on&var_TMP=on&var_UGRD=on&var_VGRD=on&var_VVEL=on&subregion=&leftlon=124&rightlon=132&toplat=38&bottomlat=33&dir=%2Fgfs.{date}%2F{time}%2Fatmos'
    if log:
        print(f'Donwloading from: {url}')
    try:
        res = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        if log:
            print('HTTP Error occured. This might be caused by incorrect arguments.')
        raise e

    size = 0
    with open(filepath, 'wb') as f:
        while True:
            chunk = res.read(BUFFER_SIZE)
            if not chunk:
                break
            f.write(chunk)
            size += len(chunk)
            if log:
                print(f'{len(chunk)}, total {size}')
    if log:
        print(filename, size)

    return filepath


def get_latest_data(number: Union[int, None] = None, log: bool = False):
    """
    Get latest atmos data from https://nomads.ncep.noaa.gov
    """
    date, time = get_latest_data_time(log)
    return get_data(date, time, number, log)


def get_latest_data_time(log: bool = False):
    now = datetime.datetime.utcnow()
    for i in range(4):
        date = now.strftime('%Y%m%d')
        time = (now.hour // 6) * 6
        url = fr'https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?dir=%2Fgfs.{date}%2F{time:02d}%2Fatmos'
        if log:
            print(f'Trying {url}')
        try:
            res = urllib.request.urlopen(url)
            if b'No files or directories found' in res.read(BUFFER_SIZE):
                raise FileNotFoundError
            break
        except (urllib.error.HTTPError, FileNotFoundError) as e:
            now -= datetime.timedelta(hours=6)
    return date, time


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Download atmos data from https://nomads.ncep.noaa.gov and save it to data directory",
        epilog="If date or time is omitted, the most recent data will be downloaded")
    parser.add_argument('-d', '--date', default=None,
                        help="Date in YYYYMMDD format")
    parser.add_argument('-t', '--time', default=None,
                        help="Time, only 00, 06, 12, 18 are available")
    parser.add_argument('-n', '--number', default=None)
    parser.add_argument('-q', '--quite', action='store_true')
    args = parser.parse_args()
    if args.number != None:
        args.number = int(args.number)
    try:
        if args.date == None or args.time == None:
            get_latest_data(args.number, not args.quite)
        else:
            get_data(args.date, args.time, args.number, not args.quite)
    except FileExistsError as e:
        print(e)


if __name__ == '__main__':
    main()
