#!/usr/bin/python3

from setuptools import setup,  find_packages

setup(
    name='toxix_bitbucket_cli',

    version='0.1',

    description='',
    long_description='',

    author='Toxix',
    author_email='kontakt@zenoo.de',

    license='All rights reserved',

    zip_safe=False,
    packages=find_packages(),
    
    install_requires=[
         'stdiomask',
         'argparse',
         'configobj', 
         'keyring', 
         'gitpython', 
      ],
      
      entry_points={
         'console_scripts': [
             'toxix-bitbucket-cli=toxix_bitbucket_cli.ToxixBitbucketCli:main'
        ]
      }
)
