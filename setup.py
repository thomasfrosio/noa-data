from setuptools import setup, find_packages

setup(
    name='noa-data',
    version='0.1.0',
    url='https://github.com/ffyr2w/noa-data.git',
    author='Thomas Frosio',
    author_email='frosiot@gmail.com',
    description='Assets for noa',
    packages=find_packages(),
    install_requires=['numpy', 'scipy', 'mrcfile', 'pyyaml']
)
