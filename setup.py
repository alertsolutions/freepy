from setuptools import setup, find_packages

setup(
    name="freepy",
    version="0.9.8",
    packages=find_packages('lib'),
    package_dir = {'':'lib'},
    install_requires=['pykka >= 1.2.0', 'llist == 0.4', 'twisted >= 13.2.0'],
    include_package_data = True,
    author="Thomas Quintana",
    author_email="quintana.thomas@gmail.com",
    license="Apache License 2.0",
    url="https://github.com/thomasquintana/freepy",
    entry_points={
        'console_scripts': [
          'freepy-server = freepy.run:main',
        ]
    }
)

