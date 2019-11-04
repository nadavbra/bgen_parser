from __future__ import absolute_import, division, print_function

import os

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

import numpy as np

'''
Installation:
>> cd /tmp
>> wget http://bitbucket.org/gavinband/bgen/get/master.tar.gz
>> tar xvfz master.tar.gz
>> mv gavinband-bgen-456f4fcbc75c ~/third_party/bgenix
>> cd ~/third_party/bgenix
>> ./waf-1.8.13 configure
>> ./waf-1.8.13

See: https://bitbucket.org/gavinband/bgen
'''
BGENIX_DIR = '/cs/phd/nadavb/third_party/bgenix'

setup(
    name = 'bgen_parser',
    version = '1.0',
    description = 'Basic parser for the BGEN format, based on the C++ library: https://bitbucket.org/gavinband/bgen',
    author = 'Nadav Brandes',
    author_email  ='nadav.brandes@mail.huji.ac.il',
    license = 'MIT',
    packages = ['bgen_parser'],
    install_requires = [
        'cython',
        'numpy',
        'pandas',
    ],
    cmdclass = {'build_ext': build_ext},
    ext_modules = [Extension(
        'cython_bgen_parser',
        language = 'c++',
        sources = ['bgen_parser/py_bgen_parser.pyx', 'bgen_parser/BgenParser.cpp'],
        include_dirs = [
            np.get_include(),
            os.path.join(BGENIX_DIR, 'genfile/include'),
            os.path.join(BGENIX_DIR, '3rd_party/zstd-1.1.0/lib'),
        ],
        extra_objects = [
            os.path.join(BGENIX_DIR, 'build/libbgen.a'),
            os.path.join(BGENIX_DIR, 'build/3rd_party/zstd-1.1.0/libzstd.a'), 
        ],
        extra_compile_args = ['-O3'],
    )],
)

