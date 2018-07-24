# -*- coding: utf-8 -*-
"""
Created on Wed May  9 10:28:38 2018

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