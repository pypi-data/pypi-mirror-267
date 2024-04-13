# tiff.anno

An extension of `tiff` image.


## Installation

```bash
pip install .
```

Or use PyPI:
```bash
pip install tiffx
```


## Usage

```python
import tiffx

data = tiffx.TiffX("example.tiffx")
np_array = data.load_nparray()
metadata = data.load_metadata()
image = data.load_image()
df = data.load_df()
```


## For Zhi Huang's note
### Distribute to PyPI

1. Navigate to the directory containing `setup.py`.
2. Run `python setup.py sdist bdist_wheel` to generate distribution archives.
3. Use `twine upload dist/*` to upload the package to PyPI (ensure you have a PyPI account and are logged in via Twine).
