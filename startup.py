# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 12:21:38 2018

@author: Administrator
"""

# Log all output
from IPython import get_ipython
ip = get_ipython()
ip.magic("logstop")
ip.magic("logstart -o -t iPython_Logs\\fivedot_log.py rotate")

import qcodes as qc
from qcodes import ChannelList, Parameter
from qcodes.dataset.measurements import Measurement
from qcodes.dataset.plotting import plot_by_id
from qcodes.dataset.data_set import load_by_id, load_by_counter
from qcodes.dataset.experiment_container import new_experiment, load_experiment_by_name
from qcodes.instrument_drivers.Keysight.N5245A import N5245A

from qdev_wrappers.station_configurator import StationConfigurator

import qcodes_measurements as qcm
from qcodes_measurements.plot.plot_tools import *

import time
import numpy as np
import scipy

from dac_params import *

import matplotlib.pyplot as plt

# Close any instruments that may already be open
instruments = list(qc.Instrument._all_instruments.keys())
for instrument in instruments:
    instr = qc.Instrument._all_instruments.pop(instrument)
    instr = instr()
    instr.close()
del instruments

exp_name = 'QDP_FIVEDOT'
sample_name = 'M02_24_17.1_0003_MARIAH_D2345'

try:
    exp = load_experiment_by_name(exp_name, sample=sample_name)
    print('Experiment loaded. Last ID no:', exp.last_counter)
except ValueError:
    exp = new_experiment(exp_name, sample_name)
    print('Starting new experiment.')

scfg = StationConfigurator()

lockin = scfg.load_instrument('sr860')
ithaco = scfg.load_instrument('ithaco')
qubit_source = scfg.load_instrument('qubit_source')
lo_source = scfg.load_instrument('lo_source')
dso = scfg.load_instrument('dso')
#midas = scfg.load_instrument('midas')
#atten = scfg.load_instrument('atten')
mdac = scfg.load_instrument('mdac')
yoko = scfg.load_instrument('yoko')
dmm = scfg.load_instrument('dmm')

# Biasing Gate Sets
OHMICS_BIAS_NUMS = tuple(x-1 for x in (2, 4, 9, 10, 12, 20, 24, 38, 39, 47, 48))
GATES_BIAS_NUMS =  tuple(x-1 for x in (1, 3, 5, 6, 7, 8, 11, 13, 14, 15, 16, 
                                       17, 18, 19, 21, 22, 23, 25, 26, 27, 28, 
                                       29, 30, 31, 32, 33, 34, 35, 36, 37, 40, 
                                       41, 42, 43, 44, 45, 46))
OHMICS_BIAS = qcm.make_channel_list(mdac, "Bias_Ohmics", OHMICS_BIAS_NUMS)
GATES_BIAS = qcm.make_channel_list(mdac, "Bias_Gates", GATES_BIAS_NUMS)
BIAS_BUS_CHAN = mdac.ch64

SHORTS_NUMS = (x-1 for x in tuple())
SHORTS = qcm.make_channel_list(mdac, "Shorts", SHORTS_NUMS)

# OHMICS
OHMICS_NUMS = tuple(x-1 for x in (2, 4, 10, 12, 20, 21, 24, 31, 38, 39, 47))
GATE_NUMS   = tuple(x-1 for x in (1, 3, 5, 6, 7, 8, 9, 11, 13, 14, 15, 16, 17, 
                                  18, 19, 22, 23, 25, 26, 27, 28, 29, 30, 32, 
                                  33, 34, 35, 36, 37, 40, 41, 42, 43, 44, 45,
                                  46, 48))
OHMICS_SET = set(OHMICS_NUMS)
GATE_SET = set(GATE_NUMS)
assert(len(OHMICS_SET.intersection(GATE_SET)) == 0)
assert(len(OHMICS_SET.union(GATE_SET)) == 48)
OHMICS = qcm.make_channel_list(mdac, "Ohmics", OHMICS_NUMS)
GATES = qcm.make_channel_list(mdac, "Gates", GATE_NUMS)

OHMICS_4_NUMS = tuple(x-1 for x in (2, 4, 12, 38, 39))
OHMICS_4 = qcm.make_channel_list(mdac, "Ohmics_Dev_4", OHMICS_4_NUMS)

OHMICS_5_NUMS = tuple(x-1 for x in (20,))
OHMICS_5 = qcm.make_channel_list(mdac, "Ohmics_Dev_5", OHMICS_5_NUMS)

GATES.rate(0.05)

# Raster Parameters
#dso.ch1.trace.prepare_curvedata()

#raster = RasterParam("Raster_RW1", mdac.RW1, dso.ch1.trace)

#raster_cut = qcm.CutWrapper(raster, fromstart=70)
#raster_diff = qcm.DiffFilter(raster)
