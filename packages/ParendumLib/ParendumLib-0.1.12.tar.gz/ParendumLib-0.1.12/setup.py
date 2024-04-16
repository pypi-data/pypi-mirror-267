from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='ParendumLib',
    version='0.1.12',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['requirements.txt']
    },
    install_requires=requirements,
    author='Parendum',
    author_email='info@parendum.com',
    description='Parendum Official Library',
    keywords='logger',
)
