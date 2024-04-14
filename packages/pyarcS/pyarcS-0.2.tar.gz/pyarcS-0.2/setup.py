from setuptools import setup, find_packages
import codecs
import os

def readme() -> str:
    with open(r"README.md") as f:
        README = f.read()
    return README
with open("requirements.txt", "r") as f:
    reqs = [line.strip() for line in f]

VERSION = '0.2'
DESCRIPTION = 'QueryManager'
long_description = 'The QueryManager project presents a simplified solution for Python developers and users who are seeking to streamline their database handling processes. This innovative tool eliminates the complexities and tediousness associated with database tasks, allowing developers to allocate their valuable time and energy towards other critical projects. We invite you to explore QueryManager and discover how it can benefit your workflow and productivity.'

# Setting up
setup(
    name="pyarcS",
    version=VERSION,
    author="srinadhch07",
    license="MIT",
    author_email="<srinadhc07@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=readme(),
    packages=find_packages(),
    install_requires=reqs,
    keywords=['python', 'query', 'mysql','update'],
    url="https://github.com/Srinadhch07/QueryManager.git",
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