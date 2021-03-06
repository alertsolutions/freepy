from setuptools import setup, find_packages

setup(
    name='freepy',
    version='0.10.5',
    packages=find_packages(),
    dependency_links=[
        'https://github.com/alertsolutions/pykka/tarball/master#egg=pykka-1.3.0',
    ],
    install_requires=['pykka', 'llist', 'twisted'],
    author='Thomas Quintana',
    author_email='quintana.thomas@gmail.com',
    license='Apache License 2.0',
    url='https://github.com/thomasquintana/freepy',
)
