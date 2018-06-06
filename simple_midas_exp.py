# -*- coding: utf-8 -*-
"""
Created on Fri May 18 16:03:11 2018

@author: Administrator
"""

import qcodes_measurements as qcm
from qcodes_measurements import pyplot
from qcodes_measurements.plot import plot_tools
from scipy import signal

midas.raster_points(2048)
midas.sw_mode(0)
midas.raster_rate(8)
midas.num_sweeps_2d(1)

midas.ch1.frequency(370.5e6)

for param in ("magnitude", "phase", "I", "Q"):
    param = getattr(midas.ch1, param)
    param.shape=(2048,)
    param.setpoint_names=("Voltage",)
    param.setpoints=(np.linspace(0, 1, 2048),)
    param.setpoint_labels = ("Voltage", )
    param.setpoint_units = ("V", )

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
    ateach.append(midas.averaged_1d_trace())
    
    # Do the sweep
    res = qcm.linear1d(param_set, start, stop, num_points, delay, *param_meas,
                       atstart=atstart, ateach=ateach, atend=atend, **kwargs)
    
    # Return the result
    return res