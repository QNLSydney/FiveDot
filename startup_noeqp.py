# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 12:21:38 2018

@author: Administrator
"""

import time
import numpy as np
import scipy, scipy.constants
import matplotlib.pyplot as plt

import qcodes as qc
from qcodes import ChannelList, Parameter
from qcodes.dataset.measurements import Measurement
from qcodes.dataset.plotting import plot_by_id
from qcodes.dataset.database import initialise_database
from qcodes.dataset.data_set import load_by_id, load_by_counter
from qcodes.dataset.experiment_container import load_or_create_experiment

from qdev_wrappers.station_configurator import StationConfigurator

import qcodes_measurements as qcm
from qcodes_measurements.plot.plot_tools import *
from qcodes_measurements.device import *

from dac_params import *

# Log all output
from IPython import get_ipython
ip = get_ipython()
ip.magic("logstop")
ip.magic("logstart -o -t iPython_Logs\\fivedot_analysis_log.py rotate")
ip.magic("autoreload 0")

# Close any instruments that may already be open
instruments = list(qc.Instrument._all_instruments.keys())
for instrument in instruments:
    instr = qc.Instrument._all_instruments.pop(instrument)
    instr = instr()
    instr.close()
del instruments

exp_name = 'QDP_FIVEDOT'
sample_name = 'DARLINGTON_D1'

initialise_database()
exp = load_or_create_experiment(exp_name, sample_name)
print('Experiment loaded. Last ID no:', exp.last_counter)
