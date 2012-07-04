#!/usr/bin/env python
from distutils.core import setup
from roflcommits import __version__

setup(
    name='roflcommits',
    version=__version__,
    packages=['roflcommits'],
    package_data={'roflcommits': ['data/fonts/*.ttf']},
    #data_files=[('data', ['data/fonts/*.ttf'])],
    description='Save your commit faces for posterity',
    author='Sylvain Fankhauser',
    author_email='sylvain.fankhauser@liip.ch',
    scripts = ['bin/roflcommits'],
    url='http://github.com/sephii/roflcommits',
)
