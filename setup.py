'''
Plagiarised this from
https://github.com/navdeep-G/samplemod/blob/master/setup.py
'''

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('LICENSE') as license_file:
    license = license_file.read()

setup (
    name = 'socketwithoutpowers',
    version = '25.07.1',
    description = 'Wrapper class and random bits of code around sockets.',
    long_description = readme,
    author = 'Austin Rudkin',
    author_email = 'nunya@nope.na',
    url = 'https://github.com/AustinWithoutPowers/SocketWithoutPowers',
    license = license,
    packages = find_packages(exclude=('tests', 'docs'))
)