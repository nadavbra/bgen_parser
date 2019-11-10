from __future__ import absolute_import, division, print_function

import cython
from libcpp.string cimport string

import numpy as np
cimport numpy as np

ctypedef unsigned int uint64_t

cdef extern from 'BgenParser.h':
    cdef cppclass BgenParser:
        BgenParser()
        void init(string bgenFilePath) except +
        void readVariantProbs(uint64_t variantFileStartPosition, float* probArray) except +
        size_t nSamples
        size_t nVariants
        
cdef class PyBgenParser:
    
    cdef BgenParser _bgenParser
    
    def init(self, str bgen_file_path):
        self._bgenParser.init(bgen_file_path.encode('UTF-8'))
    
    def get_shape(self):
        return (self._bgenParser.nVariants, self._bgenParser.nSamples)
    
    @cython.boundscheck(False)
    @cython.wraparound(False)
    def read_variant_probs(self, long variant_file_start_position, np.ndarray[float, ndim = 2, mode = 'c'] prob_array not None):
        self._bgenParser.readVariantProbs(variant_file_start_position, &prob_array[0, 0])
        
    @cython.boundscheck(False)
    @cython.wraparound(False)
    def read_multiple_variant_probs(self, np.ndarray[long, ndim = 1, mode = 'c'] variant_file_start_positions, \
            np.ndarray[float, ndim = 3, mode = 'c'] prob_array not None):
    
        cdef int i = 0
        cdef int n = len(variant_file_start_positions)
    
        while i < n:
            self._bgenParser.readVariantProbs(variant_file_start_positions[i], &prob_array[i, 0, 0])
            i += 1
