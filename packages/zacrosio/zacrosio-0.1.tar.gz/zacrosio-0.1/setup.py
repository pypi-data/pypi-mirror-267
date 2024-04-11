from setuptools import setup, find_packages

setup(
    name='zacrosio',
    version='0.1',
    url='https://github.com/hprats/ZacrosIO',
    download_url='https://github.com/hprats/ZacrosIO/archive/refs/tags/v_01.tar.gz',
    author='Hector Prats Garcia',
    author_email='hpratsgarcia@gmail.com',
    description='A collective of tools for the preparation of input files for ZACROS',
    packages=find_packages(),
    keywords=['KMC', 'ZACROS'],
    install_requires=['pandas'],
)
