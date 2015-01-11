from setuptools import setup

setup(
    name='alfred-cli',
    description='Tools for building Alfred Packages',
    author='Paul Traylor',
    url='https://github.com/kfdm/alfred-cli',
    version='0.0.1',
    packages=['alfredcli'],
    install_requires=['click==3.3'],
    entry_points={
        'console_scripts': [
            'alfred = alfredcli.cli:main'
        ],
    }
)
