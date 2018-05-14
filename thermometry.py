# -*- coding: utf-8 -*-
"""
Created on Tue May 15 08:39:43 2018

@author: Administrator
"""

import qcodes_measurements as qcm
import time

DEFAULT_EXCITATIONS = (50e-6, 40e-6, 30e-6, 25e-6, 20e-6, 15e-6, 10e-6,
                       9e-6, 8e-6, 7e-6, 6e-6, 5e-6, 4e-6, 3e-6, 2e-6, 1e-6)

def sweep_excitation(lockin, plungers, excitations=DEFAULT_EXCITATIONS, params=None):
    new_plot = True
    if params is None:
        params = (lockin.X_current,)
    for exc in excitations:
        lockin.amplitude(exc)
        plungers(-0.625)
        time.sleep(1)
        run_id, win = qcm.linear1d(plungers, -0.625, -0.685, 600, 0.2, *params, append=(not new_plot))
        print("Excitation: {:.1e}, id: {}".format(exc, run_id))
        new_plot = False
