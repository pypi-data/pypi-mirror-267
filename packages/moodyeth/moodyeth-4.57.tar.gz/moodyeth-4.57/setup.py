#!/usr/bin/env python
# --------------------------------------------------------------------
# Copyright (c) TokenChain. All rights reserved.
# Licensed under the MIT License.
# See License.txt in the project root for license information.
#
#
#     :copyright: © 2021 by the TokenChain.
#     :license: MIT License
# --------------------------------------------------------------------

import codecs
import os
import platform

import pypandoc
from setuptools import (
    find_packages,
    setup,
)

_dir = os.path.dirname(__file__)
py_version = platform.python_version()


def find_version() -> str:
    f = codecs.open('version', 'r', 'utf-8-sig')
    new_ver = f.readline().strip().replace("\n", "")
    f.close()
    edit_at_line(new_ver)
    return new_ver


def edit_at_line(version: str):
    file = 'moody/__init__.py'
    lines = []
    with open(file, "r") as f:
        lines = f.readlines()
        f.close()
        o = 0
        for h in lines:
            if "__version__" in h:
                lines[o] = f"__version__ = '{version}'"
                break
            o += 1
    if len(lines) > 0:
        with open(file, "w") as f:
            f.write("".join(lines))
            f.close()


_dir = os.path.dirname(__file__)
py_version = platform.python_version()

EXTRAS_REQUIRE = {
    "tester": [
        "coverage",
        "pep8",
        "pyflakes",
        "pylint",
        "pytest-cov"
    ],

    "docs": [
        "mock",
        "sphinx-better-theme>=0.1.4",
        "click>=5.1",
        "configparser==3.5.0",
        "contextlib2>=0.5.4",
        "py-solc>=0.4.0",
        "pytest>=2.7.2",
        "sphinx",
        "pdoc3",
        "sphinx_rtd_theme>=0.1.9",
        "toposort>=1.4",
        "urllib3",
        "wheel >= 0.31.0"
    ],

    "dev": [
        "bumpversion",
        "flaky>=3.3.0",
        "hypothesis>=3.31.2",
        "pytest>=3.5.0,<4",
        "pytest-mock==1.*",
        "pytest-pythonpath>=0.3",
        "pytest-watch==4.*",
        "pytest-xdist==1.*",
        "setuptools>=38.6.0",
        "tox>=1.8.0",
        "twine >= 1.11.0",
        "tqdm",
        "pyinstall",
        "when-changed"
    ]

}

EXTRAS_REQUIRE['dev'] = (
        EXTRAS_REQUIRE['tester'] +
        EXTRAS_REQUIRE['docs'] +
        EXTRAS_REQUIRE['dev']
)

install_requires = [
    "mypy-extensions==0.4.3",
    "web3>=5.20.0",
    "eth-utils==1.10.0",
    "eth-uniswap==0.0.2"
]


def convert_rst():
    output = pypandoc.convert_file(os.path.join('README.md'), 'rst', format='md', outputfile='README.rst')
    io = open('README.rst', 'r')
    package_description = io.read()
    return 'README.rst'


setup(
    name='moodyeth',
    version=find_version(),
    description='A Python API for interacting with Ethereum based networks',
    long_description=convert_rst(),
    long_description_content_type='text/x-rst',
    keywords='ethereum eth-api eth-api-python eth-base cli sdk pentest',
    url='https://github.com/tokenchain/moodyeth',
    author='Heskemo',
    author_email='topdog@onekexx.com',
    license='MIT License',
    zip_safe=False,
    python_requires='>=3.8,<4',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    packages=find_packages(exclude=['examples', 'lab', 'test']),
    include_package_data=True,
    install_requires=install_requires,
    tests_require=EXTRAS_REQUIRE['tester'],
    extras_require=EXTRAS_REQUIRE,
)
