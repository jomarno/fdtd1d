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


def draw_figure(length, ks, dz, n):
    
    # Create figure and axes
    fig, ax = plt.subplots()

    # Set axis limits
    ax.set_ylim(-1.5, 1.5)
    ax.set_xlim(0, length)

    # # Draw gridlines
    # plt.minorticks_on()
    # plt.grid(True, alpha=0.5, linewidth=0.8)
    # plt.grid(True, 'minor', alpha=0.2, linewidth=0.6)

    # Draw vertical line to mark the source
    ax.axvline((ks-1)*dz, color='k', linestyle=':')

    # Set color of margins
    fig.patch.set_facecolor('darkgrey')

    # Get color values for refractive index
    grey1 = mcolors.to_rgb('lightgrey')[0] # For highest refractive index
    grey2 = mcolors.to_rgb('silver')[0] # For lowest refractive index
    greyvalues = grey1 + (n-np.min(n))/(np.max(n)-np.min(n))*(grey2-grey1)

    # Draw background with color corresponding to refractive index
    for i in range(len(greyvalues)):
        color = (greyvalues[i], greyvalues[i], greyvalues[i])
        ax.axvspan(i*dz, (i+1)*dz, facecolor=color)
    
    return ax


def main():
    
    # Read simulation parameters from .csv file
    length, number_of_frames, steps_per_frame, ks, \
        c0, dz, tau, t0 = read_parameters()

    # Read material properties to draw background
    epsilon_r = np.genfromtxt('./materials/epsilon_r.csv', delimiter=',')
    mu_r = np.genfromtxt('./materials/mu_r.csv', delimiter=',')
    n = np.sqrt(epsilon_r*mu_r) # Calculate refractive index

    # Generate z-coordinates corresponding to H- and E-fields
    zH = (np.arange(length) + 0.5)*dz
    zE = np.arange(length)*dz


    # DRAW FRAMES

    plt.close('all')
    plt.ioff() # Turn off interactive mode for increased speed
    
    # Draw figure and axes before loop
    ax = draw_figure(length, ks, dz, n)

    # Get list of all .csv files with H-field data
    filenames = sorted(glob.glob('output/Hx*'))

    for filename in filenames:
        
        # For each H-field file, read it and the corresponding E-field
        Hx = np.genfromtxt(filename, delimiter=',')
        Ey = np.genfromtxt('output/Ey' + filename[-8:], delimiter=',')
        
        # Plot the data
        line1 = ax.plot(zH, Hx, 'b')
        line2 = ax.plot(zE, Ey, 'r')
        
        # Set frame number as title
        plt.title(filename[-8:-4])
        
        # Save figure as .png image
        plt.savefig('frames/frame' + filename[-8:-4] + '.png')
        
        # Erase plot lines from figure
        l1 = line1.pop(0); l1.remove(); del l1
        l2 = line2.pop(0); l2.remove(); del l2
        
        # Show progress
        print('Rendered frame'+filename[-8:-4])


# If renderframes.py is the main program, run the main() function
if __name__ == "__main__": main()