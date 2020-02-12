#!/usr/bin/env python
import io

from setuptools import setup, find_packages

test_requires = [
    # Required for running the tests
    'mock>=1.0.0',

    # For coverage and PEP8 linting
    'coverage>=3.7.0',
    'flake8>=2.2.0',

    # Required for matrix build on Travis
    'tox==3.9.0',
]

with io.open('README.md', encoding='utf-8') as readme_file:
    long_description = readme_file.read()

setup(
    name='wagtail_content_import',
    version="0.2.2",
    description='A module for Wagtail that provides functionality for importing page content from third-party sources.',
    author='Samir Shah, Jacob Topp-Mugglestone, Karl Hobley, Matthew Westcott',
    author_email='jacobtm@torchbox.com',
    url='https://github.com/torchbox/wagtail-content-import',
    packages=find_packages(),
    include_package_data=True,
    license='BSD',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Wagtail :: 2',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
    ],
    install_requires=[
        'wagtail>=2.2',
        'python-docx>=0.8.10'
    ],
    extras_require={
        'test': test_requires,
    },
    zip_safe=False,
)
