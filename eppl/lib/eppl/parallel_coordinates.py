from __future__ import division

from math import ceil

import brewer2mpl
import numpy as np

from eppl.core import plot_wrapper

@plot_wrapper
def parallel_coordinates_plot(ax, data, class_column, cols=None, colors=None, xticks=None, line_width=None,
                              line_width_scale=1.0, alpha=0.8, show_class_size=False, line_style=None, show_lines=True, 
                              legend_font_size=6):
    class_col = data[class_column]

    if cols is None:
        df = data.drop(class_column, axis=1)
    else:
        df = data[cols]

    num_cols = len(df.columns)

    xticks = np.arange(1, num_cols + 1)
    
    legend_handles = []
    
    labels = class_col.unique()

    if colors is None:
        if len(labels) > 12:
            raise Exception('''parallel_coordinates_plot cannot work with a default color scheme when more than 12
            groups are present. To avoid this error pass the kwarg colors.''')
        
        bmap = brewer2mpl.get_map('Set3', 'qualitative', len(labels))
        
        colors = dict(zip(labels, bmap.mpl_colors))
    
    if line_style is None:
        line_style = dict(zip(labels, ['-' for _ in labels]))
    
    if line_width is None:
        line_width = dict(zip(labels, [1 for _ in labels]))
    
    for l in labels:
        y = df[class_col == l].values
        
        x = np.tile(xticks, (len(y), 1))
        
        lw = line_width[l] * line_width_scale
        
        if show_lines:
            p = ax.plot(x.T, y.T, c=colors[l], label=str(l), lw=lw, alpha=alpha, ls=line_style[l])
        
            legend_handles.append(p[0])
        
        else:
            p = ax.scatter(x.T, y.T, c=colors[l], label=str(l), alpha=alpha)
            
            legend_handles.append(p)

    ax.set_xticks(xticks)
    
    ax.set_xticklabels(df.columns)
    
    ax.set_xlim(xticks[0], xticks[-1])
    
    box = ax.get_position()
    
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    
    if show_class_size:
        n = data.groupby(class_column).size()
        
        legend_text = ['{0}  (n={1})'.format(l, n.values[i]) for i, l in enumerate(labels)]
    else:    
        legend_text = [str(l) for l in labels]
    
    if show_lines:
        legend = ax.legend(legend_handles, legend_text, loc='center left', bbox_to_anchor=(1.1, 0.5), prop={'size': legend_font_size})
        
        for l in legend.get_lines():
            l.set_linewidth(1.0)
    
    else:
        ax.legend(legend_handles, legend_text, loc='center left', bbox_to_anchor=(1.1, 0.5), prop={'size': legend_font_size}, scatterpoints=1)
    
    ax.grid()

    return ax

@plot_wrapper
def aggregated_parallel_coordinates_plot(ax, data, class_column, aggregation_method='mean', show_class_size=False,
                                         line_width_scale=None, **kwargs):
    df = data.groupby(class_column, sort=False).aggregate(aggregation_method)
    
    df[class_column] = df.index
    
    n = data.groupby(class_column).size()

    if line_width_scale is None:
        line_width = n.copy()
        
        line_width[:] = 1.0
    
    else:
        line_width = n * line_width_scale
    
    parallel_coordinates_plot(df, class_column, ax=ax, line_width=line_width, show_class_size=False, **kwargs)
    
    if show_class_size:    
        for i, t in enumerate(ax.legend_.get_texts()):
            old_text = t.get_text()
            
            new_text = '{0}  (n={1})'.format(old_text, n.values[i])
        
            t.set_text(new_text)
