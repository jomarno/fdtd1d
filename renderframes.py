#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 19:41:08 2020

@author: vanilla
"""

import glob
import numpy as np
from matplotlib import pyplot as plt

plt.close('all')
plt.ioff()

i = 0

files = glob.glob('output/Hx*')
for filename in files:
    Hx = np.genfromtxt(filename, delimiter=',')
    Ey = np.genfromtxt('output/Ey' + filename[-8:], delimiter=',')
    
    plt.plot(Hx,'b')
    plt.plot(Ey,'r')
    plt.ylim(-1.1,1.1)
    plt.autoscale(enable=True, axis='x', tight=True)
    # plt.grid(b=True,which='major')
    # plt.minorticks_on()
    # plt.grid(b=True,which='minor',alpha=0.5)
    plt.title(filename[-8:-4])
    plt.savefig('frames/frame' + filename[-8:-4] + '.png')
    plt.close('all')
    
    i+=1
    print('Rendered frame' + filename[-8:-4] + '\t', i, '/', len(files))

plt.ion()
