from typing import Union
import urllib.request
import urllib.error
import os
import datetime


def get_data(date: Union[int, str], time: Union[int, str], number: Union[int, None] = None, log: bool = False):
    """
    Get atmos data from https://nomads.ncep.noaa.gov
    """
    BUFFER_SIZE = 256*1024
    if number is not None:
        ext = f'f{number:03d}'
    else:
        ext = 'anl'
    url = fr'https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?file=gfs.t{time}z.pgrb2.0p25.{ext}&all_lev=on&all_var=on&subregion=&leftlon=124&rightlon=132&toplat=38&bottomlat=33&dir=%2Fgfs.{date}%2F{time}%2Fatmos'
    if log:
        print(f'Donwloading from: {url}')
    filename = f'{date}{time}.{ext}'
    filepath = os.path.join('data', filename)
    try:
        res = urllib.request.urlopen(url)
    except urllib.error.HTTPError:
        if log:
            print(f'{url} returned HTTP error')
        return
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


def get_latest_data(number: Union[int, None] = None, log: bool = False):
    """
    Get latest atmos data from https://nomads.ncep.noaa.gov
    """
    now = datetime.datetime.utcnow()
    date = now.strftime('%Y%m%d')
    time = (now.hour // 6) * 6
    url = fr'https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?dir=%2Fgfs.{date}%2F{time}%2Fatmos'
    for i in range(4):
        date = now.strftime('%Y%m%d')
        time = (now.hour // 6) * 6
        url = fr'https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?dir=%2Fgfs.{date}%2F{time}%2Fatmos'
        try:
            res = urllib.request.urlopen(url)
            break
        except urllib.error.HTTPError:
            now -= datetime.timedelta(hours=6)
    get_data(date, time, number, log)


if __name__ == '__main__':
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
    if args.date == None or args.time == None:
        get_latest_data(args.number, not args.quite)
    else:
        get_data(args.date, args.time, args.number, not args.quite)
