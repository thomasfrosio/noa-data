from setuptools import setup, find_packages

setup(
    name='noa-data',
    version='0.1.0',
    url='https://github.com/ffyr2w/noa-data.git',
    author='Thomas Frosio',
    author_email='frosiot@gmail.com',
    description='Assets for the C++ noa library',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.21.2',
        'scipy>=1.7.1',
        'mrcfile>=1.3.0',
        'pyyaml',
        'eulerangles>=1.0.1'
    ]
)
