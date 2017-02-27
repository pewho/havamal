#!/usr/bin/env python3

from setuptools import setup, find_packages
import havamal

setup(
    name='havamal',
    version=havamal.__version__,
    packages=find_packages(),
    author=havamal.__author__,
    author_email="mathias.bazire@sylpheo.com",
    description="LDIF to CSV formater",
    long_description=open('README.md').read(),
    install_requires=["pyldap"] ,
    include_package_data=True,
    url='http://github.com/pewho/havamal',
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Tool",
    ],
    entry_points = {
        'console_scripts': [
            'havamal = havamal.cmd:handle_cmd',
            'havamal_generate_default_mapper = havamal.cmd:generate_default_mapping'
        ],
    },
    license="MIT"
)
