from setuptools import setup, find_packages
setup(
name='removable_package',
version='1.0.0',
author='andreyp',
author_email='andrepy@jfrog.com',
description='Removable package',
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
)
