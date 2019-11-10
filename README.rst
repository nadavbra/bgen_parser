What is bgen_parser
===============

bgen_parser is a simple, lightweight and (hopefully) efficient Python parser for the `BGEN format <https://www.well.ox.ac.uk/~gav/bgen_format/>`_. It is nothing more than a Python wrapper to the `bgenix C++ library of 
Gavin Band <https://bitbucket.org/gavinband/bgen>`_.

The main motivation for developing this package was that, at the time, I couldn't find a decent BGEN parser that would parse the `imputed genotypes of the UK Biobank <https://www.ukbiobank.ac.uk/scientists-3/genetic-data/>`_ in a reasonable time (it took them too long to initially load the data). I needed a parser that would work in real time.

Usage
===============

For example, to parse the imputed genotypes of the UK Biobank on chromosome 14:

.. code-block:: python

    import os
    from bgen_parser import BgenParser
    
    UKBB_IMPUTATION_V3_DIR = '/path/to/uk_biobank/EGAD00010001474'
    chrom = '14'
    
    bgen_file_path = os.path.join(UKBB_IMPUTATION_V3_DIR, 'ukb_imp_chr%s_v3.bgen' % chrom)
    bgi_file_path = os.path.join(UKBB_IMPUTATION_V3_DIR, 'ukb_imp_chr%s_v3.bgen.bgi' % chrom)
    sample_file_path = os.path.join(UKBB_IMPUTATION_V3_DIR, 'ukb26664_imp_chr%s_v3.sample' % chrom)
    
    chrom_imputation_data = BgenParser(bgen_file_path, bgi_file_path, sample_file_path)
    
    chrom_imputation_data.sample_ids # A series with the sample IDs
    chrom_imputation_data.variants # A dataframe of all the variants
    chrom_imputation_data.read_variant_probs(4) # Will read the genotyping of the fifth variant, returning a numpy array of shape (n_samples, 3)

Installation
===============

Step 1: Install bgenix
-----------------

The following instructions worked at the time they were written, but it could very well be that bgenix has since changed. If it doesn't work for you, please refer to their `website <https://bitbucket.org/gavinband/bgen>`_ for instructions.

To install bgenix at ~/third_party/bgenix, do the following:

.. code-block:: cshell

    cd /tmp
    wget http://bitbucket.org/gavinband/bgen/get/master.tar.gz
    tar xvfz master.tar.gz
    mv gavinband-bgen-456f4fcbc75c ~/third_party/bgenix
    cd ~/third_party/bgenix
    ./waf-1.8.13 configure
    ./waf-1.8.13
    
Step 2: Install bgen_parser
-----------------

1. Set the BGENIX_DIR environment variable to whatever directory you have installed bgenix at. For example, in cshell it would look like:

.. code-block:: cshell

  setenv BGENIX_DIR /cs/phd/nadavb/third_party/bgenix
  
2. Run:

.. code-block:: cshell

  pyhton setup.py install
