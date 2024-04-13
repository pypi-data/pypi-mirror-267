from setuptools import setup, find_packages

setup(
    name='pymysqls',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'PyMySQL',
    ],
    package_data={
        '': ['pymysqls/1/*', 'pymysqls/2/*', 'pymysqls/1/lib/*', 'pymysqls/2/libs/*', 'pymysqls/2/libs/ui/*', 'pymysqls/2/libs/enums/*', 'pymysqls/2/libs/ui/ui_files/*'],
    },
    include_package_data=True,
)
