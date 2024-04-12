"""
Setup script for the Leelavati library.
"""
import setuptools

with open('README.md', 'r',encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='lilavati',
    version='1.0.0',
    packages=setuptools.find_packages(),
    install_requires=[],
    author='Vedic Pythonist',
    author_email='projectleelavati@gmail.com',
    description='This library aims at discoving the hidden gems of lilavati, a vedic mathematics book. written by Bhaskaracharya.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/Project-Leelavati/Leelavati.git',
)
