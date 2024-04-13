from setuptools import setup, find_packages

setup(
    name='tiffx',
    version='0.1.1',
    description='A package for managing tiff-like whole slide image with annotation using HDF5',
    author='Zhi Huang',
    author_email='zhihuang.ai@gmail.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'Pillow',  # PIL fork for image handling
        'h5py',
        'tables'  # PyTables for pandas HDF5 support
        'openslide-python'  # This is the package for OpenSlide
    ],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],
)