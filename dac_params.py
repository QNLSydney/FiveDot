# -*- coding: utf-8 -*-
"""
Created on Mon May 14 16:42:27 2018

@author: Administrator
"""
from qcodes import ChannelList, Parameter
import numpy as np
import time
class CombinedVoltage(Parameter):
    def __init__(self, name, label, *gates):
        unit = gates[0].unit
        self.gates = []
        for gate in gates:
            self.gates.append(gate._instrument)
        
        super().__init__(name, label=label,
                         unit=unit,
                         get_cmd=self.get_raw,
                         set_cmd=self.set_raw)
    
    def get_raw(self):
        return self.gates[0].voltage()
    def set_raw(self, val):
        for gate in self.gates:
            gate.ramp(val)
        for gate in self.gates:
            while not np.isclose(val, gate.voltage(), 1e-3):
                time.sleep(0.05)