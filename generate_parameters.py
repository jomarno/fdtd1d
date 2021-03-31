#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 19:41:08 2020

@author: vanilla
"""

import numpy as np

# length, number_of_frames, steps_per_frame, ks, c0, dz, tau, t0 = 120,144,4,9,1,1,9,27

length = 120
number_of_frames = 144
steps_per_frame = 4
ks = 9
c0 = 1
dz = 1
tau = 9
t0 = 27

parameters = np.array([length, number_of_frames, steps_per_frame, ks, c0, dz, tau, t0])

np.savetxt('parameters.csv', [parameters], delimiter=',',fmt='%g')


