from __future__ import absolute_import, division, print_function

import numpy as np
import pandas as pd

import sqlite3

from cython_bgen_parser import PyBgenParser as CythonBgenParser

class BgenParser(object):
    
    def __init__(self, bgen_file_path, bgi_file_path, sample_file_path):
        self._cython_bgen_parser = CythonBgenParser()
        self._cython_bgen_parser.init(bgen_file_path)
        self.n_variants, self.n_samples = self._cython_bgen_parser.get_shape()
        self._load_bgi(bgi_file_path)
        self._load_samples(sample_file_path)
        
    def read_variant_probs(self, variant_index_or_indices):
        
        try:
            iter(variant_index_or_indices)
            read_function = self._read_multiple_variants_probs
        except TypeError:
            read_function = self._read_single_variant_probs
            
        return read_function(variant_index_or_indices)
        
    def _load_bgi(self, bgi_file_path):
        with sqlite3.connect(bgi_file_path) as bgi_connection:
            self.variants = pd.read_sql_query(_SELECT_VARIANTS_SQL, bgi_connection)
            assert len(self.variants) == self.n_variants
    
    def _load_samples(self, sample_file_path):
        self.sample_ids = pd.read_csv(sample_file_path, sep = ' ', skiprows = [1])['ID_1'].rename('eid')
        assert len(self.sample_ids) == self.n_samples
        
    def _read_single_variant_probs(self, variant_index):
        variant_probs = np.empty((self.n_samples, _N_PROBS_PER_SAMPLE), dtype = np.float32)
        self._cython_bgen_parser.read_variant_probs(self.variants.loc[variant_index, 'file_start_position'], variant_probs)
        return variant_probs
        
    def _read_multiple_variants_probs(self, variant_indices):
        variant_probs = np.empty((len(variant_indices), self.n_samples, _N_PROBS_PER_SAMPLE), dtype = np.float32)
        self._cython_bgen_parser.read_multiple_variant_probs(self.variants.loc[variant_indices, 'file_start_position'].values, variant_probs)
        return variant_probs
            
_SELECT_VARIANTS_SQL = 'SELECT * FROM Variant'

_N_PROBS_PER_SAMPLE = 3
