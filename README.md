# Space balloon project

---

## Requirements

Install requirements

This project needs following python packages:  
`ecmwflibs eccodes cfgrib matplotlib xarray`

Install packages

```
pip install ecmwflibs eccodes cfgrib matplotlib xarray
```

You can use requirements.txt

```
pip install -r requirements.txt
```

Optional: Install jupyter to run ipynb files.

```
pip install jupyter
```

---

## Usage

### Downloading data

Create data directory

```
mkdir data
```

Download the latest data from https://nomads.ncep.noaa.gov

```
python download_data.py
```

You can specify date and time

```
python download_data.py -d YYYYMMDD -t hh
```

Only 00, 06, 12, 18 are available for the time argument.

Use `python download_data.py -h` for more information.

### Reading data file

```
python read_data.py
```

This python script reads data from selected data file and plot pressure-temperature graph. You can specify latitude and longitude.

---

## Errors

### SSL: UNSAFE_LEGACY_RENEGOTIATION_DISABLED

Error message

```
urllib.error.URLError: <urlopen error [SSL: UNSAFE_LEGACY_RENEGOTIATION_DISABLED] unsafe legacy renegotiation disabled (_ssl.c:997)>
```

Solution [(source)](https://stackoverflow.com/a/72245418)

```
export OPENSSL_CONF=<Repository directory>/openssl.conf
```

Or just

```
source ./openssl_conf.sh
```
