# -*- coding: utf-8 -*-
"""Installer script for Pywikibot 3.0 framework."""
#
# (C) Pywikibot team, 2009-2019
#
# Distributed under the terms of the MIT license.
#
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import os
import sys

from setuptools import find_packages, setup

PYTHON_VERSION = sys.version_info[:3]
PY2 = (PYTHON_VERSION[0] == 2)

versions_required_message = """
Pywikibot is not available on:
{version}

This version of Pywikibot only supports Python 2.7.4+ or 3.4+.
"""


def python_is_supported():
    """Check that Python is supported."""
    # Any change to this must be copied to pwb.py
    return PYTHON_VERSION >= (3, 4, 0) or PY2 and PYTHON_VERSION >= (2, 7, 4)


if not python_is_supported():
    raise RuntimeError(versions_required_message.format(version=sys.version))


def get_version():
    """Get a valid pywikibot module version string."""
    version = '3.0'
    try:
        import subprocess
        date = subprocess.check_output(
            ['git', 'log', '-1', '--format=%ci']).strip()
        date = date.decode().split(' ')[0].replace('-', '')
        version += '.' + date
        if 'sdist' not in sys.argv:
            version += '.dev0'
    except Exception as e:
        print(e)
        version += '.dev0'
    return version


def read_desc(filename):
    """Read long description.

    Combine included restructured text files which must be done before
    uploading because the source isn't available after creating the package.
    """
    desc = []
    with open(filename) as f:
        for line in f:
            if line.strip().startswith('.. include::'):
                include = os.path.relpath(line.rsplit('::')[1].strip())
                if os.path.exists(include):
                    with open(include) as g:
                        desc.append(g.read())
                else:
                    print('Cannot include {0}; file not found'.format(include))
            else:
                desc.append(line)
    return ''.join(desc)


name = 'pywikibot'
setup(
    name=name,
    version=get_version(),
    description='Python MediaWiki Bot Framework',
    long_description=read_desc('README.rst'),
    keywords=('API', 'bot', 'framework', 'mediawiki', 'pwb', 'python',
              'pywikibot', 'pywikipedia', 'pywikipediabot', 'wiki',
              'wikimedia', 'wikipedia'),
    maintainer='The Pywikibot team',
    maintainer_email='pywikibot@lists.wikimedia.org',
    license='MIT License',
    packages=[str(name)] + [package
                            for package in find_packages()
                            if package.startswith('pywikibot.')],
    python_requires='>=2.7.4, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    install_requires=[],
    extras_require={},
    url='https://www.mediawiki.org/wiki/Manual:Pywikibot',
    download_url='https://tools.wmflabs.org/pywikibot/',
    test_suite='tests.collector',
    tests_require=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Wiki',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    use_2to3=False
)
