from setuptools import find_packages, setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='base58random',
    version='0.0.2',
    description='Random base58 generator',
    author='Viacheslav Alekseev',
    author_email='alexeev.corp@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_dir = { '': 'src' },
    packages = find_packages(where='src')
)
