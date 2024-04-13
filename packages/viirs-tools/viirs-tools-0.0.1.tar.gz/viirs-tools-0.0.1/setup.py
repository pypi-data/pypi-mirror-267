from setuptools import setup, find_packages

setup(
    name='viirs-tools',
    description='Python library for processing VIIRS data',
    author='Andrey Shuliak',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'xarray',
        'numpy'
    ],
    extras_require={
        'assimilator': ['netcdf4']
    }
)
