#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
$ python setup.py register sdist upload

First Time register project on pypi
https://pypi.org/manage/projects/


Pypi Release
$ pip3 install twine

$ python3 setup.py sdist
$ twine upload dist/kerify-0.0.1.tar.gz

Create release git:
$ git tag -a v0.4.2 -m "bump version"
$ git push --tags
$ git checkout -b release_0.4.2
$ git push --set-upstream origin release_0.4.2
$ git checkout main

Best practices for setup.py and requirements.txt
https://caremad.io/posts/2013/07/setup-vs-requirement/
"""

from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import find_packages, setup
setup(
    name='kerify',
    version='0.0.2',  # also change in src/kerify/__init__.py
    license='Apache Software License 2.0',
    description='Kerify',
    long_description="KERI Verification Service",
    author='Philip S. Feairheller',
    author_email='phil@healthkeri.com',
    url='https://github.com/WebOfTrust/kerify',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Utilities',
    ],
    project_urls={
        'Documentation': 'https://kerify.readthedocs.io/',
        'Changelog': 'https://kerify.readthedocs.io/en/latest/changelog.html',
        'Issue Tracker': 'https://github.com/WebOfTrust/kerify/issues',
    },
    keywords=[
        # eg: 'keyword1', 'keyword2', 'keyword3',
    ],
    python_requires='>=3.12.2',
    install_requires=[
        'keri>=1.2.0-dev0',
        'multicommand>=1.0.0',
        'http_sfv>=0.9.8',
        'msgpack>=1.0.4',
        'cbor2>=5.4.3'
    ],
    extras_require={
    },
    tests_require=[
        'coverage>=6.5.0',
        'pytest==7.2.0',
        'mockito==1.4.0'
    ],
    setup_requires=[
    ],
    entry_points={
        'console_scripts': [
            'kerify = kerify.app.cli.kerify:main',
        ]
    },
)

