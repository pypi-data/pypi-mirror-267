from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Lleva seguimiento del consumo de combustible'
LONG_DESCRIPTION = 'Un paquete que permite realizar un manejo mas conciente y eficiente del combustible para vehiculos.'

# Setting up

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="fuel_track",
    version=VERSION,
    author="Juan David Moreno",
    author_email="<jmorenoar@unal.edu.co>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=requirements,
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)