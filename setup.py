from setuptools import setup

setup(
    name="riemann",
    version="0.1",
    py_modules=[
        "zeta",
        "utils",
        "prime_connection",
        "explicit_formula",
        "zeros",
        "data_pipeline",  # NEU
    ],
    package_dir={"": "src"},
    install_requires=[
        "mpmath",
        "matplotlib",
    ],
)
