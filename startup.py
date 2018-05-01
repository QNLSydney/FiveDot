# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 12:21:38 2018

@author: Administrator
"""

import qcodes as qc

from qcodes import ChannelList

from qcodes.dataset.measurements import Measurement
from qcodes.dataset.plotting import plot_by_id
from qcodes import Station
from qcodes.dataset.experiment_container import load_experiment_by_name

from qdev_wrappers.station_configurator import StationConfigurator

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

CONFIG_FILE = 'system1.yaml'
scfg = StationConfigurator(CONFIG_FILE)

mdac = scfg.load_instrument('mdac')
lockin = scfg.load_instrument('sr860')

OHMICS_NUMS = (x-1 for x in (37, 48, 24, 11, 19, 7))
GATES_NUMS = (x-1 for x in (9, 32, 34, 31, 23, 46, 47, 42, 28, 38, 36, 21, 45, 10, 
                       22, 44, 35, 30, 18, 29, 17, 5))
SHORTS_NUMS = (x-1 for x in (1, 25, 8, 20, 13, 12))

OHMICS = ChannelList(mdac, "Ohmics_Channels", mdac.ch01.__class__)
for i in OHMICS_NUMS:
    OHMICS.append(mdac.channels[i])
OHMICS.lock()

GATES = ChannelList(mdac, "Gates_Channels", mdac.ch01.__class__)
for i in GATES_NUMS:
    GATES.append(mdac.channels[i])
GATES.lock()

SHORTS = ChannelList(mdac, "Shorts_Channels", mdac.ch01.__class__)
for i in SHORTS_NUMS:
    SHORTS.append(mdac.channels[i])
SHORTS.lock()