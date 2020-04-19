#!/usr/bin/env python
from __future__ import print_function

import os
import sys

v = sys.version_info
# At least we're on the python version we need, move on.

from distutils.core import setup

pjoin = os.path.join
here = os.path.abspath(os.path.dirname(__file__))

# Get the current package version.
version_ns = {}
with open(pjoin(here, 'foxtrot', '_version.py')) as f:
    exec(f.read(), {}, version_ns)


setup_args = dict(
    name='pyfoxtrot',
    packages=['foxtrot'],
    version=version_ns['__version__'],
    description="""Python package to query foxtrot""",
    author="Shubham Sharma",
    author_email="shubham.sha12@gmail.com",
    url="https://github.com/gabber12/pyfoxtrot",
    download_url="https://github.com/gabber12/pyfoxtrot/archive/0.0.1.tar.gz",
    license="MIT",
    platforms="Linux, Mac OS X",
    keywords=['foxtrot'],
    classifiers=[
    ],
)

if 'bdist_wheel' in sys.argv:
    import setuptools

# setuptools requirements
if 'setuptools' in sys.modules:
    setup_args['install_requires'] = install_requires = []
    with open('requirements.txt') as f:
        for line in f.readlines():
            req = line.strip()
            if not req or req.startswith(('-e', '#')):
                continue
            install_requires.append(req)


def main():
    setup(**setup_args)

if __name__ == '__main__':
    main()
