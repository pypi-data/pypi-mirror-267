import os
from setuptools import find_packages, setup

extras_require = open('requirements.txt').read().splitlines()

setup(
    name='slth-package',
    version='0.0.1',
    packages=find_packages(exclude=('xxx', 'xxx.*')),
    install_requires=[],
    extras_require={
        'dev': extras_require
    },
    include_package_data=True,
    license='BSD License',
    description='API generator based on yml file',
    long_description='',
    url='https://github.com/brenokcc',
    author='Breno Silva',
    author_email='brenokcc@yahoo.com.br',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
