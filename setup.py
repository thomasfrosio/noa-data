from setuptools import find_packages, setup

setup(
    name="noa-data",
    version="0.1.0",
    url="https://github.com/thomasfrosio/noa-data.git",
    author="Thomas Frosio",
    description="Assets for the C++ noa library",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scipy",
        "mrcfile",
        "pyyaml",
        "eulerangles",
    ],
)
