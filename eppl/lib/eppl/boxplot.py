'''
Created on 2013-05-10

@author: Andrew Roth
'''
from core import plot_wrapper

import matplotlib.pyplot as plot

@plot_wrapper
def boxplot(ax, data, value_column, class_column, labels=None, notch=True, box_color='blue', median_color='red', 
            whisker_color='black', outlier_color='black'):
    if labels is None:
        labels = sorted(set(data[class_column])) 
    
    plot_data = []
    
    for l in labels:
        plot_data.append(data[data[class_column] == l][value_column])
    
    bp = ax.boxplot(plot_data, notch=notch, patch_artist=True)
    
    if box_color is not None:
        plot.setp(bp['boxes'], facecolor=box_color, color=box_color)
    
    plot.setp(bp['medians'], color=median_color)
    
    plot.setp(bp['whiskers'], color=whisker_color)
    
    plot.setp(bp['fliers'], color=outlier_color)
    
    ax.set_xticklabels(labels)
    
    return ax
