#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 19:41:08 2020

@author: vanilla
"""

from renderframes import Parameters

parameters = Parameters()

parameters.length = 120
parameters.number_of_frames = 144
parameters.steps_per_frame = 4
parameters.ks = 9
parameters.c0 = 1
parameters.dz = 1
parameters.tau = 9
parameters.t0 = 27

parameters.write('parameters.csv')

