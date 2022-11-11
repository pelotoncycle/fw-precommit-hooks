'''
pip package configuration for embedded c coding standard compliance
'''
import codecs
import os
from setuptools import setup

# pylint: disable-next=consider-using-with
reqs: list = open("requirements.txt", "r",encoding='utf-8').read().splitlines()

def read(rel_path):
    '''
    Supporting function to read the __init__.py file from the package
    to get attributes.  See get_version() below for more details.
    '''
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with codecs.open(os.path.join(here, rel_path), 'r') as file_pointer:
        return file_pointer.read()

def get_version(rel_path):
    '''
    Allows the version of the package to be fetched via the one
    stored in the __init__.py file.  This enables a single location
    to store this information (rather than having to pass it in
    with the metadata in the call to setup())

    See here:
    https://packaging.python.org/guides/single-sourcing-package-version/
    '''
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]

    raise RuntimeError("Unable to find version string.")

setup(name='pre_commit_hooks',
      description='C/C++ File formatting and cleanup per coding standards',
      url='https://github.com/delsauce/pre-commit-hooks',
      license='MIT',
      packages=['pre_commit_hooks'],
      zip_safe=False,
      version=get_version("hooks/__init__.py"),
      entry_points={
            'console_scripts': [
                'format-c-source=hooks.format_c_source:main',
            ],
        },

      python_requires='>=3.7',
      install_requires=reqs
)
