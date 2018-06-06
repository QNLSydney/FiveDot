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

exp_name = 'QDP_FIVEDOT'
sample_name = 'M08-10-16.2_0003_CHER_D6'

try:
    exp = load_experiment_by_name(exp_name, sample=sample_name)
    print('Experiment loaded. Last ID no:', exp.last_counter)
except ValueError:
    exp = new_experiment(exp_name, sample_name)
    print('Starting new experiment.')

scfg = StationConfigurator()

lockin = scfg.load_instrument('sr860')
ithaco = scfg.load_instrument('ithaco')
#qubit_source = scfg.load_instrument('qubit_source')
#lo_source = scfg.load_instrument('lo_source')
#dso = scfg.load_instrument('dso')
#midas = scfg.load_instrument('midas')
#atten = scfg.load_instrument('atten')
mdac = scfg.load_instrument('mdac')
yoko = scfg.load_instrument('yoko')
dmm = scfg.load_instrument('dmm')

# Biasing Gate Sets
OHMICS_BIAS_NUMS = (x-1 for x in (11, 6, 43, 39, 26, 38))
GATE_BIAS_NUMS = (x-1 for x in (47, 34, 36, 31, 24, 28, 10, 21, 8, 44, 7, 
                                30, 5, 42, 29, 17))
OHMICS_BIAS = qcm.make_channel_list(mdac, "Bias_Ohmics", OHMICS_BIAS_NUMS)
GATES_BIAS = qcm.make_channel_list(mdac, "Bias_Gates", GATE_BIAS_NUMS)
BIAS_BUS_CHAN = mdac.ch64

# Set up gate sets
OHMICS_1_NUMS = (x-1 for x in (41, 28, 15))
GATES_MDAC_1_NUMS = (x-1 for x in (12, 31, 45, 1, 39))
GATES_BB_1_NUMS = tuple(x-1 for x in range(48, 65))

OHMICS_2_NUMS = (x-1 for x in tuple())
GATES_MDAC_2_NUMS = (x-1 for x in tuple())
GATES_BB_2_NUMS = (x-1 for x in tuple())

SHORTS_NUMS = (x-1 for x in (37, 11, 33, 44, 20, 19, 4, 3, 14, 25, 43, 30))

SHORTS = qcm.make_channel_list(mdac, "Shorts", SHORTS_NUMS)

OHMICS_1 = qcm.make_channel_list(mdac, "Dev_1_Ohmics", OHMICS_1_NUMS)
GATES_MDAC_1 = qcm.make_channel_list(mdac, "Dev_1_Gates", GATES_MDAC_1_NUMS)
GATES_BB_1 = qcm.make_channel_list(mdac, "Dev_1_Gates", GATES_BB_1_NUMS)
GATES_1 = GATES_MDAC_1 + GATES_BB_1

OHMICS_2 = qcm.make_channel_list(mdac, "Dev_2_Ohmics", OHMICS_2_NUMS)
GATES_MDAC_2 = qcm.make_channel_list(mdac, "Dev_2_Gates", GATES_MDAC_2_NUMS)
GATES_BB_2 = qcm.make_channel_list(mdac, "Dev_2_Gates", GATES_BB_2_NUMS)
GATES_2 = GATES_MDAC_2 + GATES_BB_2

OHMICS = OHMICS_1 + OHMICS_2
GATES_MDAC = GATES_MDAC_1 + GATES_MDAC_2
GATES_BB = GATES_BB_1 + GATES_BB_2
GATES = GATES_1 + GATES_2

GATES.rate(0.05)

# Rasters
#LP2_5 = qcm.tools.mdac.ensure_channel(mdac.LP2_5)

# Raster Parameters
#dso.ch1.trace.prepare_curvedata()
#raster = RasterParam("Raster_LP2_5", mdac.LP2_5, midas.ch1.I)
#raster_cut = qcm.CutWrapper(raster, fromstart=70)
#raster_diff = qcm.DiffFilter(raster_cut)
