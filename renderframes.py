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

k = np.arange(length)+1
i = 0
fig, ax = plt.subplots()
files = glob.glob('output/Hx*')
for filename in files:
    Hx = np.genfromtxt(filename, delimiter=',')
    Ey = np.genfromtxt('output/Ey' + filename[-8:], delimiter=',')
    
    ax.axvline(ks, color='k', linestyle=':')
    ax.plot(k,Hx,'b')
    ax.plot(k,Ey,'r')
    ax.set_ylim(-1.1,1.1)
    ax.set_xlim(0,length)
    # plt.autoscale(enable=True, axis='x', tight=True)
    plt.title(filename[-8:-4])
    plt.savefig('frames/frame' + filename[-8:-4] + '.png')
    plt.cla()
    
    # plt.plot(Hx,'b')
    # plt.plot(Ey,'r')
    # plt.ylim(-1.1,1.1)
    # plt.autoscale(enable=True, axis='x', tight=True)
    # # plt.grid(b=True,which='major')
    # # plt.minorticks_on()
    # # plt.grid(b=True,which='minor',alpha=0.5)
    # plt.title(filename[-8:-4])
    # plt.savefig('frames/frame' + filename[-8:-4] + '.png')
    # plt.close('all')
    
    i+=1
    print('Rendered frame' + filename[-8:-4] + '\t', i, '/', len(files))

plt.ion()
