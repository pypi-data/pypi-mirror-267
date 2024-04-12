from setuptools import setup, find_packages

setup(
    name='fremake_canopy',
    version='0.1.5',
    description='Implementation of fremake',
    author='Thomas Robinson, Dana Singh',
    author_email='gfdl.climate.mode.info@noaa.gov',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pyyaml',
        'argparse',
        'jsonschema',
    ],
)
