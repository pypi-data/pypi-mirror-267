from setuptools import setup, find_packages

setup(
name='biftest',
version='0.0.2',
packages=find_packages(),
    install_requires=[
        'pandas>=1.0',
        'matplotlib>=3.1',
        'seaborn>=0.10'
    ]
)