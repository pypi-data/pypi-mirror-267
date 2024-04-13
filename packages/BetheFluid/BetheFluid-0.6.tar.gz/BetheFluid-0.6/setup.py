from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="BetheFluid",
    version="0.6",
    description='Python package for solving GHD equations',
    author='Antoni Lis, Milosz Panfil',
    packages=find_packages(),
    install_requires=requirements,
    zip_safe=False
)