import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = ''
CHANGES = ''

requires = []

setup(name='PDFlib',
      version='9.0',
      description='Modified OO wrapper around PDFlib',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[],
      author='',
      author_email='',
      url='',
      keywords='',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires = requires,
      entry_points = ''
      )

