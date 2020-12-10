"""Minimal setup file for tasks project."""

from setuptools import setup, find_packages

setup(
    name='order_book',
    version='0.1.0',
    description='Project Order Book',

    author='Aleksei Agishev',
    author_email='leha_a-ev@mail.ru',

    packages=find_packages(where='src'),
    package_dir={'': 'src'},
)