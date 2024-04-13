from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.1.0'
DESCRIPTION = 'basic hello pkg'

# Setting up
setup(
    name="adscode",
    version=VERSION,
    author="Mathew Patil",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)