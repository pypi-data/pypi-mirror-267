from distutils.core import setup

import setuptools


def readme() -> str:
    with open(r"README.md") as f:
        README = f.read()
    return README


with open("requirements.txt", "r") as f:
    reqs = [line.strip() for line in f]


setup(
    name="pyBAv",
    packages=setuptools.find_packages(),
    version="5.4.1",
    license="MIT",
    description="BAv2 is simple personalised  chatbot for every user and developer",
    author="Srinadhch07",
    author_email="srinadhc07@gmail.com",
    url="https://github.com/Srinadhch07/Personal-Projects-.git",
    download_url="https://github.com/Srinadhch07/Personal-Projects-.git",
    keywords=["chatbot", "info", "personalai", "search"],
    install_requires=reqs,
    package_data={"pyBAv": ["data.txt"]},
    include_package_data=False,
    long_description="BAv2 is simple personalised chatbot made for developers",
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
