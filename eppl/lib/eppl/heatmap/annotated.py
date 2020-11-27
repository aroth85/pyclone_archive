'''
Created on 2013-09-12

@author: Andrew Roth
'''
from eppl.heatmap import heatmap

import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plot
import numpy as np
import pandas as pd
import scipy.cluster.hierarchy as sch
import scipy.spatial.distance as dist

def annotated_heatmap(fig,
                      data,
                      col_annotations=None, 
                      row_annotations=None, 
                      col_distance_metric='euclidean',
                      row_distance_metric='euclidean',
                      col_linkage_method='complete',
                      row_linkage_method='complete',
                      plot_col_dendrogram=True,
                      plot_row_dendrogram=True,
                      color_map='Blues',
                      vmin=None,
                      vmax=None,
                      **kwargs):
    
    # Copy data to avoid mutating input
    data = data.copy()
    
    num_rows = data.shape[0]
    
    num_cols = data.shape[1]
    
    # Initialise grid
    num_grid_cols = 1 + plot_col_dendrogram + (col_annotations is None)
    
    num_grid_rows = 1 + plot_row_dendrogram + (row_annotations is None)

    grid = gridspec.GridSpec(num_grid_cols, 
                             num_grid_rows, 
                             width_ratios=[1, 1, num_cols], 
                             height_ratios=[1, 1, num_rows])

#     color_bar_w = 0.015
    
    if plot_row_dendrogram:
        ax = plot.subplot(grid[-1, 0])
        
        idx = plot_dendrogram(ax, data, row_linkage_method, row_distance_metric, 'right')
        
        data.reindex_axis(data.index[idx], axis=0)

    if plot_col_dendrogram:
        ax = plot.subplot(grid[0, -1])
        
        idx = plot_dendrogram(ax, data.T, col_linkage_method, col_distance_metric, 'top')
        
        data.reindex_axis(data.columns[idx], axis=1)

    # Plot distance matrix
    ax = plot.subplot(grid[-1, -1])
    
    heatmap(data, ax=ax, color_map=color_map, show_color_bar=False, **kwargs)
        
    return grid

    # Plot annotation track
#     if col_linkage_method != None:
#         cmap_c = mpl.colors.ListedColormap(['r', 'g', 'b', 'y', 'w', 'k', 'num_rows'])
#          
#         if col_annotations is not None:
#             dc = np.array(col_annotations)
#          
#         else:
#             dc = np.array(ind2, dtype=int)
#              
#             dc.shape = (1, len(ind2)) 
#          
#         im_c = axc.matshow(dc, aspect='auto', origin='lower', cmap=cmap_c)
#          
#         axc.set_xticks([])
#          
#         axc.set_yticks([])
     
#     # Plot rowside colors
#     # axr --> axes for row side colorbar
#     if row_linkage_method != None:
#         axr = fig.add_axes([axr_x, axr_y, axr_w, axr_h])  # axes for column side colorbar
#         
#         cmap_r = mpl.colors.ListedColormap(['r', 'g', 'b', 'y', 'w', 'k', 'num_rows'])
#         
#         if row_annotations is not None:
#             dr = np.array([row_annotations[data.index[idx1[i]]] for i in range(num_rows)])
#         
#         else:
#             dr = np.array(ind1, dtype=int)
#         
#         dr.shape = (len(ind1), 1)
# 
#         im_r = axr.matshow(dr, aspect='auto', origin='lower', cmap=cmap_r)
#         
#         axr.set_xticks([])
#         
#         axr.set_yticks([])

    # Plot color legend
#     axcb = fig.add_axes([axcb_x, axcb_y, axcb_w, axcb_h], frame_on=False)  # axes for colorbar
#     
#     cb = mpl.colorbar.ColorbarBase(axcb, cmap=cmap, norm=norm, orientation='horizontal')
#     
#     axcb.set_title("colorkey")
#     
#     show()

def plot_dendrogram(ax, data, method, metric, orientation):
    plot.sca(ax)
    
    d = dist.pdist(data)
        
    d = dist.squareform(d)

    Y = sch.linkage(d, method=method, metric=metric) ### gene-clustering metric - 'average', 'single', 'centroid', 'complete'
        
    Z = sch.dendrogram(Y, orientation=orientation, color_threshold=1.0)
     
    ax.set_xticks([])
        
    ax.set_yticks([])
    
    idx = Z['leaves']
    
    return idx

if __name__ == '__main__':
    data = pd.read_excel('/home/andrew/Desktop/SA501-X1.130708.xls', 'var_freq')

    fig = plot.figure()
    
    annotated_heatmap(fig, data, plot_col_dendrogram=True)
    
    fig.savefig('/home/andrew/Desktop/test.pdf', bbox_inches='tight')