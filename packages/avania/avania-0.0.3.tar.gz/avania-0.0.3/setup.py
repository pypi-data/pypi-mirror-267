from setuptools import setup, find_packages

setup(
    name='avania',
    version='0.0.3',
    description='Pays tribute to Laravel',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    author='Simon',
    packages=find_packages(),
    install_requires=[
        'requests',
        'numpy',
    ],
)
