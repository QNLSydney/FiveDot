# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 14:42:53 2018

@author: Administrator
"""

import numpy.fft as fft
from scipy.signal import savgol_filter

start = 6116
stop = 6128

ffts = []
for i in range(start, stop+1):
    print(f"Analyzing {i}")
    data = get_shaped_data_by_runid(i)
    x = data[0][0]['data']
    y = data[0][1]['data']
    
    bins = fft.rfft(y, norm="ortho")
    freqs = fft.rfftfreq(x.size, x[1]-x[0])
    mean = np.mean(y)
    ffts.append({'id': i, 'freqs': freqs, 'bins': bins, 'mean': mean})
    
plt.figure()
for res in ffts:
    bins = savgol_filter(np.absolute(res['bins'][1:]),  7, 3)
    plt.loglog(res['freqs'][1:], bins, '.', 
               label=f"{res['id']}")
    plt.legend()
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude (A/sqrt(Hz))")
    
polys = []
means = []
plt.figure()
for res in ffts:
    x = res['freqs'][1:1801]
    y = np.absolute(res['bins'][1:1801])
    a, b = np.polyfit(np.log10(x), np.log10(y), 1)
    poly = np.frompyfunc(lambda x: 10**b * x**a, 1, 1)
    polys.append(10**b/res['mean'])
    means.append(res['mean'])
    plt.loglog(x, poly(x), label=f"{res['id']}")
    plt.legend()
    
fig, ax1 = plt.subplots()
plt.plot(polys, "b.")
plt.ylabel("Switching Magnitude (A.U.)")
plt.xlabel("Sweep Number")


ax2 = ax1.twinx()
plt.plot(means, "r.")
plt.ylabel("Mean Current (A)")

fig.tight_layout()