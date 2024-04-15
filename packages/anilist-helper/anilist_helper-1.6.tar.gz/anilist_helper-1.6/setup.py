from setuptools import setup, find_packages
setup(
    name='anilist-helper',
    version='1.06',
    description='A Python library to fetch data from Anilist',
    author='Dominik Procházka',
    packages=find_packages(),
    install_requires=['flask', 'gevent', 'requests']
)