from setuptools import setup

setup(
    name='spotify-backup',
    packages=['spotify'],
    include_package_data=True,
    install_requires=[
        'flask', 'requests', 'dotenv', 'sqlalchemy'
    ],
)