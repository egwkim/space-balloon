# Space balloon project

---

## Requirements

Install requirements

```
pip install cfgrib matplotlib xarray
```

Or

```
pip install -r requirements.txt
```

---

## Usage

### Downloading data

Downloads latest data from https://nomads.ncep.noaa.gov

```
python download_data.py
```

You can specify date and time

```
python download_data.py -d YYYYMMDD -t hh
```

Only 00, 06, 12, 18 are available for the time argument.

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