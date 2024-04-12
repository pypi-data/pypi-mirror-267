from setuptools import setup, find_packages

setup(
    name='PicKit',
    version='1.0.0',
    author='Sumukh M G',
    author_email='sumukhmg45@gmail.com',
    description='A simple library for processing images.',
    packages=find_packages(),
    install_requires=[
        'Pillow',
    ],
)
