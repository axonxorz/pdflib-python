from setuptools import setup
from setuptools.dist import Distribution


class BinaryDistribution(Distribution):
    """Distribution which always forces a binary package with platform name.
    Used due to our precompiled extension"""
    def has_ext_modules(self):
        return True


setup(distclass=BinaryDistribution)
