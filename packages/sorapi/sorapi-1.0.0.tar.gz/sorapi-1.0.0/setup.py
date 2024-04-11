#      __ _  _  _  _ ___    |     _           _  _  _
#     (_ / \|_)|_||_) |     |    |_) _     | |_)| \|_|    _  _ __
#     __)\_/| \| ||  _|_    |    | \(_||_| | | \|_/| | o (_ (_)|||

from setuptools import setup, find_packages

setup(
    name = 'sorapi',
    version = '1.0.0',
    packages = find_packages(),
    license = 'MIT',
    description = 'This module provides a convenient way to interact with all endpoints of some-random-api(.com).',
    long_description = open('README.md').read(),
    install_requires = ['requests'],
    url = 'http://github.com/RaulRDA/sorapi/wiki',
    author = 'RaulRDA',
    author_email = 'hey@raulrda.com'
)