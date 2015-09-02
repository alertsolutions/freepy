from setuptools import setup, find_packages

setup(
    name='freepy',
    version='0.9.9',
    packages=find_packages(),
    install_requires=[
        'pykka>=1.2.0',
        'llist==0.4',
        'twisted>=13.2.0'
    ],
    author='Thomas Quintana',
    author_email='quintana.thomas@gmail.com',
    license='Apache License 2.0',
    url='https://github.com/thomasquintana/freepy',
)
