from setuptools import setup, find_packages

setup(
    name="icg",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "icg = cli.main:main",
        ]
    },
    install_requires=[
        "PyYAML",
    ],
)
