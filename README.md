# configjy

> Loads variables from a .json, .yaml or .yml file

[![PyPI version][pypi-image]][pypi-url]
[![Build status][build-image]][build-url]
[![GitHub stars][stars-image]][stars-url]
[![Support Python versions][versions-image]][versions-url]



## Getting started

You can [get `configjy` from PyPI](https://pypi.org/project/configjy),
which means it's easily installable with `pip`:

```bash
python -m pip install configjy
```


## Example usage

```python

from configjy import ConfigFile

# given this file:
"""
{
    "key1": 10,
    "key2": {
        "key3": 20
    },
    "key4": "{{key1}}"
}
"""

        
fvar = ConfigFile(config_file_path)
key1 = fvar.get('key1')
print(key1) # 10

key2 = fvar.get('key2')
print(key2) # {"key3": 20}

key3 = fvar.get('key2.key3')
print(key3) # 20

key4 = fvar.get('key4')
print(key4) # str(key1) = "10"

key5 = fvar.get('key5', default=1, print_when_not_exists=False)
print(key5) # 1

try:
    key6 = fvar.get('key6', raise_when_not_exists=True) # raises key error
except KeyError:
    pass

key6 = fvar.get('key6') # print a warning abou non existent key
print(key6) # None


```



## Changelog

Refer to the [CHANGELOG.md](https://github.com/henriquelino/configjy/blob/main/CHANGELOG.md) file.



<!-- Badges -->

[pypi-image]: https://img.shields.io/pypi/v/configjy
[pypi-url]: https://pypi.org/project/configjy/

[build-image]: https://github.com/henriquelino/configjy/actions/workflows/build.yaml/badge.svg
[build-url]: https://github.com/henriquelino/configjy/actions/workflows/build.yaml

[stars-image]: https://img.shields.io/github/stars/henriquelino/configjy
[stars-url]: https://github.com/henriquelino/configjy

[versions-image]: https://img.shields.io/pypi/pyversions/configjy
[versions-url]: https://pypi.org/project/configjy/

