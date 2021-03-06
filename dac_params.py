# -*- coding: utf-8 -*-
"""
Created on Mon May 14 16:42:27 2018

@author: Administrator
"""
from qcodes import ChannelList, Parameter, ArrayParameter
from qcodes.instrument_drivers.Keysight.Infiniium import InfiniiumChannel
import numpy as np
import time
import qcodes_measurements as qcm
from scipy import signal

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
                
class RasterParam(ArrayParameter):
    def __init__(self, name, gate_source, readout_source, amplitude_override=None,
                 label=None, unit=None):
        
        # Set sources
        self.gate_source = qcm.ensure_channel(gate_source)
        self.readout_source = readout_source
        
        if label is None:
            label = readout_source.label
        if unit is None:
            unit = readout_source.unit
        
        # Initialize parameter
        super().__init__(name,
                       instrument=gate_source,
                       shape=(1,), # Note we'll overwrite this below
                       unit=unit,
                       label=label,
                       setpoint_names=(gate_source.name,),
                       setpoint_units=(gate_source.unit,),
                       setpoint_labels=(gate_source.label,))
        
        self.amplitude = amplitude_override
        
        self.refresh()
    
    def refresh(self, cut=None):
        gate_source = self.gate_source
        readout_source = self.readout_source
        # Calculate setpoints
        if self.amplitude is None:
            if gate_source.waveform() != 'saw':
                raise ValueError("No sawtooth on gate")
            amplitude = gate_source.amplitude()
            offset = gate_source.offset()
        else:
            amplitude = self.amplitude
            offset = gate_source.voltage()
            
        start = offset - amplitude/2
        stop = offset + amplitude/2
        
        # Figure out the number of points in the raster
        if isinstance(readout_source._instrument, InfiniiumChannel):
            readout_source.prepare_curvedata()
            self.prepare_curvedata = readout_source.prepare_curvedata
        npts = readout_source.shape[0]
        
        # Set our setpoints and shape
        self.setpoints = (np.linspace(start, stop, npts),)
        self.shape = (npts,)
    
    def get_raw(self):
        return self.readout_source.get()

class Time(Parameter):
    def __init__(self):
        super().__init__("Time",
             unit="s",
             label="Time")
        self.init = time.process_time()
        
    def set_raw(self, val):
        pass
    
    def get_raw(self):
        return time.process_time() - self.init