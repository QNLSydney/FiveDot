# -*- coding: utf-8 -*-
"""
Created on Fri May 18 16:03:11 2018

@author: Administrator
"""

import qcodes_measurements as qcm
from qcodes_measurements import pyplot
from qcodes_measurements.plot import plot_tools
from scipy import signal
import math

midas.sw_mode('distributed')
midas.filter_mode('5k')
midas.raster_rate(8)
midas.num_sweeps_2d(4)

midas.ch1.frequency(532e6)

def _ensure_list(item):
    if any(isinstance(item, x) for x in (list, tuple)):
        return item
    return [item]



def linear1d_midas(midas, param_set, start, stop, num_points, delay, *param_meas, 
             **kwargs):
    """
    """

    # Add the midas sync params
    atstart = _ensure_list(kwargs.pop("atstart", []))
    ateach = _ensure_list(kwargs.pop("ateach", []))
    atend = _ensure_list(kwargs.pop("atend", []))
    ateach.append(midas.averaged_1d_trace)
    
    try:
        # Do the sweep
        res = qcm.linear1d(param_set, start, stop, num_points, delay, *param_meas,
                           atstart=atstart, ateach=ateach, atend=atend, **kwargs)
    finally:
        midas.visa_handle.clear()
    
    # Return the result
    return res