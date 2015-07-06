#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import (
    setup,
    find_packages,
    )

base_dir = os.path.dirname(os.path.abspath(__file__))


def here(path):
    return os.path.join(base_dir, path)


def load_requirements(path):
    with open(path, 'rt') as fp:
        for line in fp:
            line = line.strip()
            if line:
                yield line

src = 'src'
install_requires = list(load_requirements('requirements/install.txt'))
test_require = list(load_requirements('requirements/test.txt'))
requires = install_requires + test_require
packages = find_packages(src)
package_dir = {'': src}
package_data = {}


setup(
    name='sandstorm',
    version='0.1.4',
    url='https://github.com/TakesxiSximada/sandstorm',
    download_url='https://github.com/TakesxiSximada/sandstorm',
    license='See http://www.python.org/3.4/license.html',
    author='TakesxiSximada',
    author_email='takesxi.sximada@gmail.com',
    description="sandstorm",
    long_description="sandstorm",
    zip_safe=False,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.4',
        ],
    platforms='any',
    packages=packages,
    package_dir=package_dir,
    package_data=package_data,
    include_package_data=True,
    requires=requires,
    install_requires=install_requires,
    test_require=test_require,
    entry_points='''
    [console_scripts]
    sandstorm.server = sandstorm.server:main
    '''
    )
