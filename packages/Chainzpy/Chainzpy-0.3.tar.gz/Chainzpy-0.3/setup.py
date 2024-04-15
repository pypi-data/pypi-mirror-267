from setuptools import setup, find_packages

setup(
    name="Chainzpy",
    version="0.3",
    packages=find_packages(),
    install_requires=[
        "requests",
        "bs4"
    ],
    description="API wrapper for https://chainz.cryptoid.info/",
    long_description="This API wrapper allows you to gather information about peoples crypto wallets and their transactions"
)