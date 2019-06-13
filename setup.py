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

# ============
# Dependencies
# ============
# It is good practise to install packages using the system
# package manager if it has a packaged version. If you are unsure,
# please use pip.
#
# To get a list of potential matches, on some Linux distributions
# you can use:
#
# $ awk -F '[#>=]' '{print $1}' setup.py | xargs yum search
#     or
# $ awk -F '[#>=]' '{print $1}' setup.py | xargs apt-cache search
#
# Some dependencies can be found also in tox.ini.
test_deps = ['bz2file', 'mock']

# Mandatory dependencies
# ======================
# requests is mandatory; see README.conversion.txt
dependencies = ['requests>=2.20.0']


# Extra dependencies
# ==================
# Core library dependencies.
#
# Extra dependencies can be installed using
# $ pip install .[extras]
pydocstyle = 'pydocstyle<=3.0.0' if PY2 else 'pydocstyle>=2.5.0'
if PY2:
    pillow = 'Pillow<7.0.0'
elif PYTHON_VERSION < (3, 5):
    pillow = 'Pillow<6.0.0'
else:
    pillow = 'Pillow'

extra_deps = {
    # Core library dependencies
    'flake8': [  # Due to incompatibilities between packages the order matters.
        'flake8>=3.7.5',
        pydocstyle,
        'hacking',
        'flake8-coding',
        'flake8-comprehensions',
        'flake8-docstrings>=1.1.0',
        'flake8-future-import',
        'flake8-mock>=0.3',
        'flake8-print>=2.0.1',
        'flake8-quotes>=2.0.1',
        'flake8-string-format',
        'flake8-tuple>=0.2.8',
        'flake8-no-u-prefixed-strings>=0.2',
        'pep8-naming>=0.7',
        'pyflakes>=2.1.0',
    ],
    # pagegenerators.py
    'eventstreams': ['sseclient>=0.0.18,!=0.0.23,!=0.0.24'],
    'Google': ['google>=1.7'],
    # interwiki_graph.py
    'Graphviz': ['pydot>=1.2'],
    # core HTML comparison parser in diff module
    'html': ['BeautifulSoup4'],
    # comms/http.py
    'http': ['fake_useragent'],
    # cosmetic_changes.py
    'isbn': ['python-stdnum'],
    # OAuth support
    # mwoauth 0.2.4 is needed because it supports getting identity
    # information about the user
    'mwoauth': ['mwoauth>=0.2.4,!=0.3.1'],
    # textlib.py
    'mwparserfromhell': ['mwparserfromhell>=0.3.3'],
    # The mysql generator in pagegenerators.py depends on
    # either PyMySQL or MySQLdb. Pywikibot prefers
    # PyMySQL over MySQLdb (Python 2 only).
    'mysql': ['PyMySQL'],
    # requests security extra
    'security': ['requests[security]', 'pycparser!=2.14'],
    # GUI
    'Tkinter': [pillow]
}

if PY2:
    # Additional wikistats.py dependency which is only available
    # on Python 2
    extra_deps.update({
        'csv': ['unicodecsv']
    })

script_deps = {
    'flickrripper.py': ['flickrapi', pillow],
    'isbn.py': ['python-stdnum'],
    'patrol.py': ['mwparserfromhell>=0.3.3'],
    'states_redirect.py': ['pycountry'],
    'weblinkchecker.py': ['memento_client>=0.5.1,!=0.6.0']
}


if PY2:
    # tools.ip does not have a hard dependency on an IP address module,
    # as it falls back to using regexes if one is not available.
    # The functional backport of py3 ipaddress is acceptable:
    # https://pypi.org/project/ipaddress
    # However the Debian package python-ipaddr is also supported:
    # https://pypi.org/project/ipaddr
    # Other backports are likely broken.
    # ipaddr 2.1.10+ is distributed with Debian and Fedora. See T105443.
    dependencies.append('ipaddr>=2.1.10')

    # version.package_version() uses pathlib which is a python 3 library.
    # pathlib2 is required for python 2.7
    dependencies.append('pathlib2')

    if (2, 7, 6) < PYTHON_VERSION < (2, 7, 9):
        # Python versions before 2.7.9 will cause urllib3 to trigger
        # InsecurePlatformWarning warnings for all HTTPS requests. By
        # installing with security extras, requests will automatically set
        # them up and the warnings will stop. See
        # <https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning>
        # for more details.
        # There is no secure version of cryptography for Python 2.7.6 or older.
        dependencies += extra_deps['security']

    script_deps['data_ingestion.py'] = extra_deps['csv']

# tools/__init__.py
# Pywikibot prefers using the inbuilt bz2 module if Python was compiled
# with bz2 support. But if it wasn't, bz2file is used instead.
try:
    import bz2
except ImportError:
    # Use bz2file if the python is not compiled with bz2 support.
    dependencies.append('bz2file')
else:
    _unused = bz2


# Some of the ui_tests depend on accessing the console window's menu
# to set the console font and copy and paste, achieved using pywinauto
# which depends on pywin32.
# These tests may be disabled because pywin32 depends on VC++, is time
# consuming to build, and the console window can't be accessed during appveyor
# builds.
# Microsoft makes available a compiler for Python 2.7
# http://www.microsoft.com/en-au/download/details.aspx?id=44266
if os.name == 'nt' and os.environ.get('PYSETUP_TEST_NO_UI', '0') != '1':
    if PYTHON_VERSION >= (3, 5, 0) or PY2:
        pywinauto = 'pywinauto>0.6.4'
        pywin32 = 'pywin32>220'
    else:  # Python 3.4
        pywinauto = 'pywinauto<=0.6.4'
        pywin32 = 'pywin32<=220'
    test_deps += [pywin32, pywinauto]

extra_deps.update(script_deps)

# Add all dependencies as test dependencies,
# so all scripts can be compiled for script_tests, etc.
if 'PYSETUP_TEST_EXTRAS' in os.environ:
    test_deps += [i for k, v in extra_deps.items() if k != 'flake8' for i in v]

    if 'requests[security]' in test_deps:
        # Bug T105767 on Python 2.7 release 9+
        if PY2 and PYTHON_VERSION[2] >= 9:
            test_deps.remove('requests[security]')

# Extras category containing all extras
extra_deps.update({'extras': [i for k, v in extra_deps.items() for i in v]})

# These extra dependencies are needed other unittest fails to load tests.
if PY2:
    test_deps += extra_deps['csv']
else:
    test_deps += ['six']


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
    install_requires=dependencies,
    extras_require=extra_deps,
    url='https://www.mediawiki.org/wiki/Manual:Pywikibot',
    download_url='https://tools.wmflabs.org/pywikibot/',
    test_suite='tests.collector',
    tests_require=test_deps,
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
