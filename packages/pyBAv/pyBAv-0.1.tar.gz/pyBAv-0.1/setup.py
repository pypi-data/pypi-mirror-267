from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.1'
DESCRIPTION = 'BAv2 is simple personalised  chatbot for every user and developer'
long_description = 'BAv2 is simple personalised chatbot made for developers and users'

# Setting up
setup(
    name="pyBAv",
    version=VERSION,
    author="srinadhch07",
    author_email="<srinadhc07@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['chatbot','ai','python','pyBAv'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ]
)