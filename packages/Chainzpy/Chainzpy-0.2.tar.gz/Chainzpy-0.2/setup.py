from setuptools import setup, find_packages

setup(
    name="Chainzpy",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        "requests",
        "bs4"
    ],
    description="API wrapper for https://chainz.cryptoid.info/"
)