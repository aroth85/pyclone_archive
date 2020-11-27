'''
Created on 2013-09-12

@author: andrew
'''
import matplotlib.cm as cm
import matplotlib.pyplot as plot
import numpy as np

from eppl.core import plot_wrapper 

@plot_wrapper
def heatmap(ax, 
            data, 
            alpha=0.8,
            color_bar_label=None,
            color_map='Blues', 
            edge_color='k', 
            nan_alpha=0.8, 
            nan_color='y',
            show_color_bar=True, 
            show_x_tick_labels=True, 
            show_y_tick_labels=True,
            value_range=None,
            line_width=1.0):
    
    xbin = np.linspace(0, data.shape[1], data.shape[1] + 1)
    
    ybin = np.linspace(0, data.shape[0], data.shape[0] + 1)
    
    if type(color_map) == str:
        cmap = cm.get_cmap(color_map)
    
    else:
        cmap = color_map
    
    cmap.set_bad(color=nan_color, alpha=nan_alpha)
        
    plot_data = np.ma.masked_invalid(data)
    
    if value_range is None:
        heatmap = ax.pcolormesh(xbin, ybin, plot_data, cmap=cmap, edgecolors=edge_color, vmin=0, lw=line_width)
    
    else:
        heatmap = ax.pcolormesh(xbin, ybin, plot_data, cmap=cmap, edgecolors=edge_color, vmin=0, vmax=0.5, alpha=0.8, lw=line_width)

    # ax.set_frame_on(False)
    
    # Put the major ticks at the middle of each cell
    ax.set_xticks(np.arange(data.shape[1]) + 0.5, minor=False)
    
    ax.set_yticks(np.arange(data.shape[0]) + 0.5, minor=False)
    
    ax.set_xlim(0, data.shape[1])
    
    ax.set_ylim(0, data.shape[0])
    
    # want a more natural, table-like display
    ax.invert_yaxis()
    
    # Set the labels
    if show_x_tick_labels:
        x_labels = data.columns
        
        ax.set_xticklabels(x_labels, minor=False, rotation=90)
    
    else:
        ax.set_xticklabels([], minor=False, rotation=90)
    
    if show_y_tick_labels:
        y_labels = data.index
    
        ax.set_yticklabels(y_labels, minor=False)
    
    else:
        ax.set_yticklabels([], minor=False)

    ax.grid(False)

    for t in ax.xaxis.get_major_ticks(): 
        t.tick1On = False 
        t.tick2On = False 

    for t in ax.yaxis.get_major_ticks(): 
        t.tick1On = False 
        t.tick2On = False
    
    #fig = plot.gcf()
    
    if show_color_bar is True:
        cbar = plot.colorbar(heatmap)
        
        if color_bar_label is not None:
            cbar.set_label(color_bar_label, rotation=90)

    return ax