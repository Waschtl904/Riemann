# setup.py
from setuptools import setup

setup(
    name="riemann",
    version="0.1.0",
    py_modules=["zeta", "utils"],  # einzelne Module statt Pakete
    package_dir={"": "src"},
)
