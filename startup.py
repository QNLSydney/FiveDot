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
ip.magic("logstart -o -t iPython_Logs\\fivedot_log.py rotate")
ip.magic("load_ext autoreload")
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
OHMICS_NUMS = tuple(x-1 for x in (1, 5, 12, 17, 38, 39))
GATE_NUMS   = tuple(x-1 for x in (13, 28, 2, 41, 27, 3, 14, 37, 42, 24, 25,
                                  6, 19, 20, 18, 44, 26, 29, 4, 16, 8, 40))

# Device 5 Definition
dev1 = Device("Device_1")

dev1.add_gate("LW1", mdac.ch13)
dev1.add_gate("LP1", mdac.ch28)
dev1.add_gate("C1",  mdac.ch02)
dev1.add_gate("RP1", mdac.ch41)
dev1.add_gate("RW1", mdac.ch27)
dev1.add_gate("N1",  mdac.ch04)
dev1.add_gate("LSDT",mdac.ch16)
dev1.add_gate("LSDC",mdac.ch08)
dev1.add_gate("LSDB",mdac.ch40)

dev1.add_gate("LW2", mdac.ch14)
dev1.add_gate("LP2", mdac.ch37)
dev1.add_gate("C2",  mdac.ch42)
dev1.add_gate("RP2", mdac.ch24)
dev1.add_gate("RW2", mdac.ch25)
dev1.add_gate("N2",  mdac.ch18)
dev1.add_gate("RSDT",mdac.ch20)
dev1.add_gate("RSDC",mdac.ch19)
dev1.add_gate("RSDB",mdac.ch06)

dev1.add_gate("JBL",mdac.ch29)
dev1.add_gate("JBT",mdac.ch26)
dev1.add_gate("JBR",mdac.ch44)
dev1.add_gate("JBB",mdac.ch03)

dev1.add_ohmic("O1", mdac.ch12)
dev1.add_ohmic("O2", mdac.ch39)
dev1.add_ohmic("O3", mdac.ch17)
dev1.add_ohmic("O4", mdac.ch05)
dev1.add_ohmic("O5", mdac.ch38)
dev1.add_ohmic("O6", mdac.ch01)

qc.Station.default.add_component(dev1, "Dev1")

qc.Monitor(*(qc.Monitor.running._parameters +
             tuple(dev1.parameters.values())[1:]))


def conv_r(current, voltage=50e-6, ithaco_imp=200, filtering=13400):
    r = voltage/current
    r -= ithaco_imp
    r -= filtering
    return r


def conv_g(resistance):
    cc = scipy.constants.value("conductance quantum")
    g = 1/(cc*resistance)
    return g



# Raster Parameters
# dso.ch1.trace.prepare_curvedata()

# raster = RasterParam("Raster_LW2", dev5.LW2.source.dac_source.voltage, dso.ch1.trace)
# raster_phase = RasterParam("Raster_LW2_Ph", mdac.ch57.voltage, midas.ch1.phase)
#
# raster_cut = qcm.CutWrapper(raster, fromstart=40, fromend=40)
# raster_diff = qcm.DiffFilter(raster)
# raster_diff._unit = "dV<sub>rf</sub>/dV<sub>G</sub>"
