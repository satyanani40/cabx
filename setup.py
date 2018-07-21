"""
soc-portal-api.

This a Flask application that handles the backend for the soc-portal.
"""

import re
import ast
import os
from setuptools import setup, find_packages


datadir = os.path.join('feqor','utils','configurations')
datafiles = [(d, [os.path.join(d,f) for f in files])
    for d, folders, files in os.walk(datadir)]

_version_re = re.compile(r'__version__\s+=\s+(.*)')


with open('feqor/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))


setup(
    name='CABX-API',
    version=version,
    url='https://github.com/satyanani40/cabx',
    license='',
    author='Vegesina Satyanarayana Raju',
    author_email='',
    description=__doc__,
    long_description=__doc__,
    packages=find_packages(),
    data_files=datafiles
)
