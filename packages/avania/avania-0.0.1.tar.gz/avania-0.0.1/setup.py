from setuptools import setup, find_packages

setup(
    name='avania',
    version='0.0.1',
    description='An example Python project',
    author='Simon',
    packages=find_packages(),
    install_requires=[
        'requests',
        'numpy',
    ],
)
