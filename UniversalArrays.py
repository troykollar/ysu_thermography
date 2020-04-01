#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 19:42:24 2020

@author: rjyarwood

This is an ndarray library for Python that supports standard numpy as well as
CUDA optimzed functions. The goal of this library is for teams to be able to
work on Python scripts together while still being able to see the improved
performance boost from CUDA optimized arrays. This means that the same code
can be used by those with CUDA accelerated setups without the need for these
to be set up on everyone's computer. This can make these scripts more universal
while also not sacrificing performance.
"""


''' Imports: '''

import numpy as np
try:
    import cupy as cp
except ImportError:
    print("CuPy not installed, will run all arrays as numpy")
    hasCuPy = False
else:
    print("CuPy is installed and can be utilized")
    hasCuPy = True


''' End of Imports '''



class UniversalArrays:

    def asNumpy(array):
        try:
            z = cp.asnumpy(array)
        except:
            z = array.copy()
        finally:
            return z

    def amax(a, axis=None, out=None, keepdims=None, initial=None, where=None):
        '''Try first to run as CuPy array, if not run as numpy'''
        try:
            z = cp.amax(a, axis, out, keepdims)
        except:
            z = np.amax(a, axis, out, keepdims, initial, where)


        '''Synchronize all GPU cores as preventative measure against race condition'''
        cp.cuda.Stream.null.synchronize()

        if out is not None:
            return out

        return z
    


    def load(file, mmap_mode=None, allow_pickle=False, fix_imports=True, encoding='ASCII'):
        '''Try first to run as CuPy array, if not run as numpy'''
        try:
            z = cp.load(file, mmap_mode, allow_pickle)
        except:
            z = np.load(file, mmap_mode, allow_pickle, fix_imports, encoding)


        '''Synchronize all GPU cores as preventative measure against race condition'''
        cp.cuda.Stream.null.synchronize()

        return z


    def where(condition, x = None, y = None):
        '''Try first to run as CuPy array, if not run as numpy'''
        try:
            z = cp.where(condition, x, y)
        except:
            z = np.where(condition, x, y)


        '''Synchronize all GPU cores as preventative measure against race condition'''
        cp.cuda.Stream.null.synchronize()

        return z

    def zeros(shape, dtype='float', order = 'C'):
        '''Try first to run as CuPy array, if not run as numpy'''
        try:
            z = cp.zeros(shape, dtype, order)
        except:
            z = np.zeros(shape, dtype, order)

        '''Synchronize all GPU cores as preventative measure against race condition'''
        cp.cuda.Stream.null.synchronize()

        return z

