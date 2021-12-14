#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 19:41:08 2020

@author: vanilla
"""

import numpy as np
from renderframes import Parameters


def sigmoid(n,s):
    x = np.linspace(-1, 1, num=n)
    return 1/(1+np.exp(-s*x))

def gaussian(n,s):
    x = np.linspace(-1, 1, num=n)
    return np.exp(-(x/s)**2)

def rescale(y, y1, y2):
    y -= np.min(y)
    y /= np.max(y)
    y *= y2-y1
    y += y1
    # return y

    
# Read necessary parameters from .csv file
parameters = Parameters()
parameters.read('parameters.csv')

# length,_,_,ks,_,dz,_,_ = read_parameters()

# Declare arrays of material properties and set them to 1
epsilon_r = np.ones(parameters.length)
mu_r = np.ones(parameters.length)


# Change properties to model some material

# # CONSTANT
# x1=58; x2=82
# epsilon_r[x1:x2] = 3

# # STEP
# x1=58; x2=70; x3=82
# epsilon_r[x1:x2] = 1.8
# epsilon_r[x2:x3] = 4.2

# # DOUBLE STEP
# x1=58; x2=64; x3=76; x4=82
# epsilon_r[x1:x2] = 4.2
# epsilon_r[x2:x3] = 1.8
# epsilon_r[x3:x4] = 4.2

# # LINEAR
# x1=58; x2=82
# epsilon_r[x1:x2] = np.linspace(1.8, 4.2, num=x2-x1)

# # SIGMOID
# x1=58; x2=82
# epsilon_r[x1:x2] = sigmoid(x2-x1, 8)
# rescale(epsilon_r[x1:x2], 1.8, 4.2)

# DOUBLE SIGMOID
x1=58; x2=70; x3=82
epsilon_r[x1:x2] = 1 - sigmoid(x2-x1, 5)
epsilon_r[x2:x3] = sigmoid(x3-x2, 5)
rescale(epsilon_r[x1:x3], 1.8, 4.2)

# # GAUSSIAN
# x1=58; x2=82
# epsilon_r[x1:x2] = gaussian(x2-x1, 0.5)
# rescale(epsilon_r[x1:x2], 1.8, 4.2)

# # INVERTED GAUSSIAN
# x1=58; x2=82
# epsilon_r[x1:x2] = gaussian(x2-x1, 0.5)
# rescale(epsilon_r[x1:x2], 4.2, 1.8)


# Save material properties to .csv file
np.savetxt('./materials/epsilon_r.csv', [epsilon_r], delimiter=',',fmt='%g')
np.savetxt('./materials/mu_r.csv', [mu_r], delimiter=',',fmt='%g')




# # PLOTS OF MATERIAL PROPERTIES AND FIGURE PREVIEW

# # Calculate refractive index
# n = np.sqrt(epsilon_r*mu_r)

# from matplotlib import pyplot as plt
# from renderframes import draw_figure

# plt.close('all')

# # Material properties
# plt.figure()
# plt.plot(mu_r)
# plt.plot(epsilon_r)
# plt.plot(n)
# plt.minorticks_on()
# plt.grid(True, alpha=0.5, linewidth=0.8)
# plt.grid(True, 'minor', alpha=0.2, linewidth=0.6)

# # Figure preview
# draw_figure(parameters.length, parameters.ks, parameters.dz, n)


