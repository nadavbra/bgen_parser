from __future__ import absolute_import, division, print_function

import os

import numpy as np

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

BGENIX_DIR_ENV_VARIABLE_NAME = 'BGENIX_DIR'

if BGENIX_DIR_ENV_VARIABLE_NAME in os.environ:
    bgenix_dir = os.path.expanduser(os.getenv(BGENIX_DIR_ENV_VARIABLE_NAME))
else:
    raise Exception('You must define an environment variable %s specifying where bgenix is installed.' % BGENIX_DIR_ENV_VARIABLE_NAME)
    
def readme():
    with open('README.rst', 'r') as f:
        return f.read()

setup(
    name = 'bgen_parser',
    version = '1.0',
    description = 'Basic parser for the BGEN format, based on the C++ library at https://bitbucket.org/gavinband/bgen',
    long_description = readme(),
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/nadavbra/bgen_parser',
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
        sources = [
            'bgen_parser/py_bgen_parser.pyx',
            'bgen_parser/BgenParser.cpp',
        ],
        include_dirs = [
            np.get_include(),
            os.path.join(bgenix_dir, 'genfile/include'),
            os.path.join(bgenix_dir, '3rd_party/zstd-1.1.0/lib'),
        ],
        extra_objects = [
            os.path.join(bgenix_dir, 'build/libbgen.a'),
            os.path.join(bgenix_dir, 'build/3rd_party/zstd-1.1.0/libzstd.a'), 
        ],
        extra_compile_args = ['-O3'],
    )],
)

