#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 19:41:08 2020

@author: vanilla
"""

import glob
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors as mcolors

def read_parameters():
    parameters = list(np.genfromtxt('parameters.csv', delimiter=','))
    for i in range(4):
        parameters[i] = int(parameters[i])
    return parameters

def read_refractive_index():
    epsilon_r = np.genfromtxt('./materials/epsilon_r.csv', delimiter=',')
    mu_r = np.genfromtxt('./materials/mu_r.csv', delimiter=',')
    return np.sqrt(epsilon_r*mu_r)

plt.close('all')
plt.ioff()
    
length, number_of_frames, steps_per_frame, ks, \
    c0, dz, tau, t0 = read_parameters()

n = read_refractive_index()
n_norm = (n-np.min(n))/(np.max(n)-np.min(n))

zH = (np.arange(length) + 0.5)*dz
zE = np.arange(length)*dz

fig, ax = plt.subplots()
ax.set_ylim(-1.5, 1.5)
ax.set_xlim(0, length)
# plt.minorticks_on()
# plt.grid(True, alpha=0.5, linewidth=0.8)
# plt.grid(True, 'minor', alpha=0.2, linewidth=0.6)
ax.axvline((ks-1)*dz, color='k', linestyle=':')

fig.patch.set_facecolor('darkgrey')

grey1 = mcolors.to_rgb('lightgrey')[0]
grey2 = mcolors.to_rgb('silver')[0]
greyvalues = grey1 + n_norm*(grey2-grey1)

for i in range(len(greyvalues)):
    color = (greyvalues[i], greyvalues[i], greyvalues[i])
    ax.axvspan(i*dz, (i+1)*dz, facecolor=color)

files = glob.glob('output/Hx*')
i = 0
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
