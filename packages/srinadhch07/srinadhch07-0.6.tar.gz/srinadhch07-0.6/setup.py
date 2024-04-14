from setuptools import setup, find_packages
import codecs
import os

def readme() -> str:
    with open(r"README.md") as f:
        README = f.read()
    return README
with open("requirements.txt", "r") as f:
    reqs = [line.strip() for line in f]

VERSION = '0.6'
DESCRIPTION = 'BAv2G'
long_description = 'Updated verision of BAv2'

# Setting up
setup(
    name="srinadhch07",
    version=VERSION,
    author="srinadhch07",
    license="MIT",
    author_email="<srinadhc07@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=readme(),
    packages=find_packages(),
    install_requires=reqs,
    keywords=['python', 'video', 'chat', 'video stream', 'camera stream', 'sockets'],
    url="https://github.com/Srinadhch07/BAv2.git",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ]
)