#!/usr/bin/env python

from setuptools import setup

setup(
    name='harvey',
    version='0.0.1',
    description='Simple crawler for Tor hidden services',
    author='Alberto Granzotto',
    author_email='agranzot@gmail.com',
    packages=['harvey'],
    test_suite='harvey.test',
    entry_points = {
        'console_scripts': ['harvey=harvey.command_line:main'],
    }
)

