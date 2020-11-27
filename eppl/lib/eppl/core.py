'''
Created on 2013-05-10

@author: Andrew Roth
'''
import matplotlib.pyplot as plot

def plot_wrapper(f):
    def annotate_axes(*args, **kwargs):
        ax = kwargs.get('ax', None)
        
        if ax is None:
            fig = plot.figure()
            
            ax = fig.add_subplot(1, 1, 1)            
        else:
            ax = kwargs['ax']
            
            del kwargs['ax']
        
        args = tuple([ax, ] + list(args))
        
        _format_text(ax, kwargs)
        
        _format_ticks(ax, kwargs)
        
        _format_axes_labels(ax, kwargs, 'title', 'title')
        
        _format_axes_labels(ax, kwargs, 'x_label', 'xlabel')
        
        _format_axes_labels(ax, kwargs, 'y_label', 'ylabel')

        return f(*args, **kwargs) 
    
    return annotate_axes

def _format_text(ax, kwargs):
    text_decoration_methods = {
                               'x_label' : 'set_xlabel', 
                               'y_label' : 'set_ylabel', 
                               'title' : 'set_title'
                               }
    
    for arg_name, method in text_decoration_methods.items():
        if arg_name in kwargs:
            _annotate_axes(ax, kwargs, arg_name, method, multialignment = 'center')

def _format_ticks(ax, kwargs):
    tick_methods = {
                    'tick_label_rotation' : 'set_rotation',
                    'tick_font_size' : 'set_fontsize'
                    }
    
    for x in ['x', 'y']:
        for arg_name, tick_method in tick_methods.items():
            ax_method = 'get_{0}ticklabels'.format(x)
            
            arg_name = '_'.join((x, arg_name))
            
            if arg_name in kwargs:
                _set_tick_property(ax, kwargs, arg_name, ax_method, tick_method)
                
def _format_axes_labels(ax, kwargs, eppl_name, matplotlib_name):
    font_properties = {
                       'font_size' : 'fontsize',
                       'font' : 'fontname',
                       'horizontal_alignment' : 'horizontalalignment',
                       'multi_line_alignment' : 'multialignment',
                       'vertical_alignment' : 'verticalalignment'                  
                       }
    
    font_dict = {}
    
    for arg_name, property in font_properties.items():
        arg_name = '_'.join((eppl_name, arg_name))
        
        if arg_name in kwargs:
            font_dict[property] = kwargs[arg_name]
            
            del kwargs[arg_name]
    
    if len(font_dict) > 0:
        matplotlib_getter = 'get_{0}'.format(matplotlib_name)
                
        value = getattr(ax, matplotlib_getter)()
        
        matplotlib_setter = 'set_{0}'.format(matplotlib_name)
        
        getattr(ax, matplotlib_setter)(value, fontdict=font_dict)
       
def _annotate_axes(ax, args_dict, arg_name, ax_method, **kwargs):
    getattr(ax, ax_method)(args_dict[arg_name], **kwargs)
    
    del args_dict[arg_name]

def _set_tick_property(ax, args_dict, arg_name, ax_method, tick_method, **kwargs):
    for t in getattr(ax, ax_method)():
        getattr(t, tick_method)(args_dict[arg_name], **kwargs)
    
    del args_dict[arg_name]     
    