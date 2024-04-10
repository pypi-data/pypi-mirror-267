from setuptools import setup, find_packages
setup(
name='ilovetea',
version='0.1.4',
author='Elonmute',
author_email='elonmute@gmail.com',
description='This is first project on Tea protocol',
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
install_requires=[
'requests',
],

python_requires='>=3.6',
)