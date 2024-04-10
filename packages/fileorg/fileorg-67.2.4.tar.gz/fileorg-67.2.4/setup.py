from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

VERSION = '67.2.4' 
DESCRIPTION = 'An Advcanced File Organizer'

setup(
    name="fileorg", 
    version=VERSION,
    author="Zack",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),  # Make sure this correctly locates all your packages
    keywords=['python', 'File Organizer'],
    license="MIT",  # Verify that this license matches your project
    install_requires=["setuptools>=61.0"],
)
