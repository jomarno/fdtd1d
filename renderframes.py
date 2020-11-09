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

for filename in glob.glob('output/Hx*'):
    print(filename)
    Hx = np.genfromtxt(filename, delimiter=',')
    # Ey = np.genfromtxt('output/Ey' + filename[-8:], delimiter=',')
    
    
    plt.plot(Hx)
    plt.ylim(-1,1)
    plt.title(filename[-8:-4])
    plt.savefig('frames/frame' + filename[-8:-4] + '.png')
    plt.close('all')