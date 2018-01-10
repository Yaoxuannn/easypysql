# coding: utf-8

from setuptools import setup

setup(
    name='easypysql',
    version='0.1.1',
    author='Justin13',
    author_email='justin13wyx@gmail.com',
    url='https://github.com/Justin13wyx/easypysql',
    description='A simple and small python ORM framework',
    # long_description=open("README.md", encoding="utf-8").read(),
    packages=['easypysql'],
    install_requires=["pymysql"],

)