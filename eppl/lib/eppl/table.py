from matplotlib.table import Table

import numpy as np

def plot_table(ax, data, float_format='{:.2f}', columns=None, bbox=None, cell_font_size=6):
    if columns is not None:
        if type(columns) is dict:
            data = data[columns.keys()]
            
            data = data.rename(columns)
        
        else:
            data = data[columns]
    
    if bbox is None:
        bbox = [0, 0, 1, 1]
    
    ax.set_axis_off()
    
    table = Table(ax, bbox=bbox)

    num_rows, num_cols = data.shape
    
    width = 1.0 / num_cols
    
    #height = 1.0 / num_rows 
    height = table._approx_text_height()

    # Add cells
    for (i,j), val in np.ndenumerate(data):
        val = float_format.format(val)
        
        table.add_cell(i, j, width, height, text=val, loc='center')
    
    cells = table.get_celld()
    
    for index, val in np.ndenumerate(data):
        cells[index].set_fontsize(cell_font_size)

    # Row Labels...
    for i, label in enumerate(data.index):
        table.add_cell(i, -1, width, height, text=label, loc='right', edgecolor='none', facecolor='none')
    
    # Column Labels...
    for j, label in enumerate(data.columns):
        table.add_cell(-1, j, width, height/2, text=label, loc='center', edgecolor='none', facecolor='none')
    
    ax.add_table(table)
    
    table.set_fontsize(cell_font_size)
    
    return ax