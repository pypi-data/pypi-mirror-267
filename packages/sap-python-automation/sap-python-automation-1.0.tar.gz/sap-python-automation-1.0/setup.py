from setuptools import setup, find_packages
from pathlib import Path

setup(
    name='sap-python-automation',
    version=1.0,
    description='Pacote usado para automações no SAP GUI',
    long_description=Path('README.md').read_text(),
    author='Ygor Seiji',
    packages=find_packages()
)