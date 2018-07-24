# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 17:24:28 2018

@author: Administrator
"""
from qcodes.dataset.data_set import load_by_id, load_by_counter
import numpy as np
import si_prefix

def leakage_sweep(voltage_out, dmm, to=1e-3, nump=101, wt=0.1, ithaco_impedance=20):
    id, plot = qcm.linear1d(voltage_out.voltage, 0, to, nump, wt, dmm.ithaco_current, setback=True)
    data = load_by_id(id)
    plot.close()
    
    yoko_param = voltage_out.voltage.full_name
    dmm_param = dmm.ithaco_current.full_name
    
    setpoints = np.array(data.get_data(yoko_param)).T[0]
    values = np.array(data.get_data(dmm_param)).T[0]
    fit, res, _, _, _ = np.polyfit(values, setpoints, 1, full=True)
    print("Resistance was: {}Ohms".format(
            si_prefix.si_format(fit[0] - ithaco_impedance, precision=3)))
    print("Residuals were: {}".format(res))
    
    return fit, res

def test_all(output, to=1e-3, force_gate=None, start=0, stop=48):
    """
    force_gate to test one gate only, note: indexed from 1 to correspond
    to labels on front of mdac
    """
    global mdac, yoko, dmm
    
    ithaco_impedance = 20
    
    if force_gate is not None:
        start=force_gate-1
        stop=force_gate
    
    with open(output, "a") as f:
        for i in range(start, stop):
            print (f"Testing Channel {i+1}")
            ch = mdac.channels[i]
            
            d = ch.dac_output()
            ch.dac_output('open')
            ch.bus('close'); ch.gnd('open')
            
            try:
                fit, res = leakage_sweep(yoko, dmm, to=to, wt=0.05)
                calc_res = fit[0] - ithaco_impedance
                valid = "X" if res > 5e-7 else calc_res
                f.write(f"{i+1},{calc_res},{res},{valid}\n")
                f.flush()
            finally:
                ch.gnd('close'); ch.bus('open')
                ch.dac_output(d)
            
        