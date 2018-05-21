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
from qcodes import Station
from qcodes.dataset.experiment_container import load_experiment_by_name
from qcodes.instrument_drivers.Keysight.N5245A import N5245A

from qdev_wrappers.station_configurator import StationConfigurator

import qcodes_measurements as qcm
from qcodes_measurements.plot.plot_tools import *

import time
import numpy as np

from dac_params import *

# Close any instruments that may already be open
instruments = list(qc.Instrument._all_instruments.keys())
for instrument in instruments:
    instr = qc.Instrument._all_instruments.pop(instrument)
    instr = instr()
    instr.close()

exp_name = 'QDP_FIVEDOT'
sample_name = 'M08-10-16.2_0003_CHER'

exp = load_experiment_by_name(exp_name, sample=sample_name)
print('Experiment loaded. Last ID no:', exp.last_counter)

scfg = StationConfigurator()

mdac = scfg.load_instrument('mdac')
lockin = scfg.load_instrument('sr860')
ithaco = scfg.load_instrument('ithaco')

# Set up gate sets from Bottom
#OHMICS_1_NUMS = (x-1 for x in tuple())
#GATES_1_NUMS = (x-1 for x in tuple())
#OHMICS_2_NUMS = (x-1 for x in (36, 29, 20, 27))
#GATES_2_NUMS = (x-1 for x in (47, 42, 41, 31, 11, 37, 45, 28, 34, 24, 39, 
#                              7, 19, 18, 30, 5))
#SHORTS_NUMS = (x-1 for x in (15, 13, 40, 3, 48, 10, 1, 12, 14, 2))

# Set up gate sets
OHMICS_1_NUMS = (x-1 for x in (37, 48, 24, 11, 19, 7))
GATES_1_NUMS = (x-1 for x in (9, 32, 34, 31, 23, 46, 47, 42, 28, 38, 36, 21, 45, 10, 
                       22, 44, 35, 30, 18, 29, 17, 5))
OHMICS_2_NUMS = (x-1 for x in (14, 15))
GATES_2_NUMS = (x-1 for x in (49, 50, 51, 52, 53, 26, 57, 58, 59, 60, 61, 16, 41, 3, 
                              2, 40, 56, 55, 54, 62, 63, 64))
SHORTS_NUMS = (x-1 for x in (1, 25, 8, 20, 13, 12))

SHORTS = qcm.make_channel_list(mdac, "Shorts", SHORTS_NUMS)
OHMICS_1 = qcm.make_channel_list(mdac, "Dev_1_Ohmics", OHMICS_1_NUMS)
GATES_1 = qcm.make_channel_list(mdac, "Dev_1_Gates", GATES_1_NUMS)
OHMICS_2 = qcm.make_channel_list(mdac, "Dev_2_Ohmics", OHMICS_2_NUMS)
GATES_2 = qcm.make_channel_list(mdac, "Dev_2_Gates", GATES_2_NUMS)
OHMICS = OHMICS_1 + OHMICS_2
GATES = GATES_1 + GATES_2

GATES.rate(0.05)