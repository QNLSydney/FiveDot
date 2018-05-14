# -*- coding: utf-8 -*-
"""
Created on Wed May  9 10:28:38 2018

@author: Administrator
"""

import qcodes as qc
from qcodes.dataset.measurements import Measurement
from qcodes.dataset.plotting import plot_by_id
from qcodes.dataset.data_set import load_by_id, load_by_counter
from qcodes.dataset.experiment_container import load_experiment_by_name

import qcodes_measurements as qcm

import numpy as np

exp_name = 'QDP_FIVEDOT'
sample_name = 'M08-10-16.2_0003_CHER'

exp = load_experiment_by_name(exp_name, sample=sample_name)
print('Experiment loaded. Last ID no:', exp.last_counter)