# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 12:21:38 2018

@author: Administrator
"""

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
from qcodes_measurements.device import *

import time
import numpy as np
import scipy

from dac_params import *

import matplotlib.pyplot as plt

# Log all output
from IPython import get_ipython
ip = get_ipython()
ip.magic("logstop")
ip.magic("logstart -o -t iPython_Logs\\fivedot_log.py rotate")

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
# dso = scfg.load_instrument('dso')
midas = scfg.load_instrument('midas')
atten = scfg.load_instrument('atten')
mdac = scfg.load_instrument('mdac')
yoko = scfg.load_instrument('yoko')
dmm = scfg.load_instrument('dmm')
bb1 = scfg.load_instrument('bb1')
bb2 = scfg.load_instrument('bb2')

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

# Cold Gate Nums
OHMICS_NUMS = tuple(x-1 for x in (2, 4, 10, 12, 20, 21, 24, 31, 38, 39, 47))
GATE_NUMS   = tuple(x-1 for x in (1, 3, 5, 6, 7, 8, 9, 11, 13, 14, 15, 16, 17,
                                  18, 19, 22, 23, 25, 26, 27, 28, 29, 30, 32,
                                  33, 34, 35, 36, 37, 40, 41, 42, 43, 44, 45,
                                  46, 48))

# Device 5 Definition
dev5 = Device("Device_5")

dev5.add_gate("LW1", bb2.ch03.connect_dac(mdac.ch49))
dev5.add_gate("LP1", bb1.ch07.connect_dac(mdac.ch50))
dev5.add_gate("C1",  bb1.ch19.connect_dac(mdac.ch51))
dev5.add_gate("RP1", bb1.ch04.connect_dac(mdac.ch52))
dev5.add_gate("RW1", bb1.ch14.connect_dac(mdac.ch53))
dev5.add_gate("N1",  bb2.ch05.connect_dac(mdac.ch54))
dev5.add_gate("LSDC",bb1.ch17.connect_dac(mdac.ch55))

dev5.add_gate("LW2", bb2.ch15.connect_dac(mdac.ch57))
dev5.add_gate("LP2", bb1.ch18.connect_dac(mdac.ch58))
dev5.add_gate("C2",  bb1.ch05.connect_dac(mdac.ch59))
dev5.add_gate("RP2", bb1.ch16.connect_dac(mdac.ch60))
dev5.add_gate("RW2", bb1.ch01.connect_dac(mdac.ch61))
dev5.add_gate("N2",  mdac.ch44)
dev5.add_gate("RSDC",mdac.ch08)

dev5.add_ohmic("O1", bb2.ch16)
dev5.add_ohmic("O2", bb1.ch02)
dev5.add_ohmic("O3", bb2.ch17)
dev5.add_ohmic("O4", mdac.ch20)
dev5.add_ohmic("O5", bb1.ch03)
dev5.add_ohmic("O6", bb2.ch02)

qc.Station.default.add_component(dev5, "Dev5")
qc.Monitor(*(qc.Monitor.running._parameters + tuple(dev5.parameters.values())[1:]))

# Raster Parameters
#dso.ch1.trace.prepare_curvedata()

#raster = RasterParam("Raster_LW2", mdac.ch57.voltage, midas.ch1.I)
#raster_phase = RasterParam("Raster_LW2_Ph", mdac.ch57.voltage, midas.ch1.phase)
#
#raster_cut = qcm.CutWrapper(raster, fromstart=40)
#raster_diff = qcm.DiffFilter(raster_cut)
