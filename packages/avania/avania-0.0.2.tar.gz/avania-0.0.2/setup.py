from setuptools import setup, find_packages

setup(
    name='avania',
    version='0.0.2',
    description='Pays tribute to Laravel',
    author='Simon',
    packages=find_packages(),
    install_requires=[
        'requests',
        'numpy',
    ],
)
