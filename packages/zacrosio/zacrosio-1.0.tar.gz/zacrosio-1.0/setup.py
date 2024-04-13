from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='zacrosio',
    version='1.0',
    description='A collective of tools for the preparation of input files for ZACROS',
    long_description=long_description,
    packages=find_packages(),
    url='https://github.com/hprats/ZacrosIO',
    download_url='https://github.com/hprats/ZacrosIO/archive/refs/tags/v1.0.tar.gz',
    author='Hector Prats Garcia',
    author_email='hpratsgarcia@gmail.com',
    keywords=['python', 'chemistry', 'KMC', 'ZACROS'],
    install_requires=['pandas', 'scipy']
)
