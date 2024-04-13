from setuptools import setup, find_packages

setup(
    name='pymysqls',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'PyMySQL',
    ],
    include_package_data=True,
)
