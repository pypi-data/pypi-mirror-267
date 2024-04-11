from setuptools import setup, find_packages

setup(
    name='LangList',
    version='1.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=3.1',
        'pandas>=1.0',
    ],
)
