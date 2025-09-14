from setuptools import setup, find_packages

setup(
    name="riemann",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "mpmath",
        "matplotlib",
        # weitere Abhängigkeiten
    ],
    entry_points={
        "console_scripts": [
            "riemann=cli:main",
        ],
    },
)
