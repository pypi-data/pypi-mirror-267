
from setuptools import setup, find_packages

setup(
    name='coglib',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['requests', 'pandas'],  # Add any dependencies
    author='Kannan M',
    author_email='kannan.m@cogencis.com',
    description='Simple interface to quickly to consume the Cogencis Data API in python environment. This package provides several functions for accessing historical market data and reference data',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://cogencis.com',
    license='MIT',
)