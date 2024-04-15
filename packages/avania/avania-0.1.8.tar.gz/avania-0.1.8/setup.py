from setuptools import setup, find_packages

setup(
    name='avania',
    version='0.1.8',
    description='Pays tribute to Laravel',
    long_description_content_type='text/markdown',
    long_description=open('CONTRIBUTING.md').read(),
    author='Simon',
    packages=find_packages(),
    install_requires=[
        'mysql-connector-python',
        'flask'
    ],
)
