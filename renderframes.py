#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 19:41:08 2020

@author: vanilla
"""

import glob
import numpy as np
from matplotlib import pyplot as plt

def read_parameters():
    parameters = list(np.genfromtxt('parameters.csv', delimiter=','))
    for i in range(4):
        parameters[i] = int(parameters[i])
    return parameters

plt.close('all')
plt.ioff()
    
length, number_of_frames, steps_per_frame, ks, \
    c0, dz, tau, t0 = read_parameters()

zH = (np.arange(length) + 0.5)*dz
zE = np.arange(length)*dz

i = 0

fig, ax = plt.subplots()
ax.set_ylim(-1.5, 1.5)
ax.set_xlim(0, length)
# plt.minorticks_on()
# plt.grid(True, alpha=0.5, linewidth=0.8)
# plt.grid(True, 'minor', alpha=0.2, linewidth=0.6)
ax.axvline((ks-1)*dz, color='k', linestyle=':')

# ax.axvline(60*dz, color='darkgrey')
# ax.axvline(80*dz, color='darkgrey')

fig.patch.set_facecolor('darkgrey')
# ax.patch.set_facecolor('lightgrey')
ax.axvspan(0, 60, facecolor='lightgrey')
ax.axvspan(60, 80, facecolor='silver')
ax.axvspan(80, 120, facecolor='lightgrey')

files = glob.glob('output/Hx*')
for filename in files:
    Hx = np.genfromtxt(filename, delimiter=',')
    Ey = np.genfromtxt('output/Ey' + filename[-8:], delimiter=',')
    
    line1 = ax.plot(zH, Hx, 'b')
    line2 = ax.plot(zE, Ey, 'r')
    # plt.autoscale(enable=True, axis='x', tight=True)
    plt.title(filename[-8:-4])
    plt.savefig('frames/frame' + filename[-8:-4] + '.png')
    l1 = line1.pop(0); l1.remove(); del l1
    l2 = line2.pop(0); l2.remove(); del l2
    
    i+=1
    print('Rendered frame' + filename[-8:-4] + '\t', i, '/', len(files))

plt.ion()
