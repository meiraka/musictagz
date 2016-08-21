"""Setup script for MusicTagz."""


from os import path
from setuptools import setup, find_packages
import musictagz
import musictagz.console

pwd = path.abspath(path.dirname(__file__))

with open(path.join(pwd, 'README.rst')) as f:
    long_description = f.read()


setup(
    name='musictagz',
    version=musictagz.__version__,
    description=long_description.splitlines()[4],
    author='mei raka',
    license='GPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2.7',
    ],
    packages=find_packages(exclude=['tests']),
    # install_requires=['python-yaml'],
    install_requires=['PyYAML'],
    entry_points={
        'console_scripts': [
            'musictagz = musictagz.console:main'
        ]
    },
)
