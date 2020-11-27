'''
Routines for plotting segment files from array or WGSS data.

Created on 2013-05-17

@author: Andrew Roth
'''
from collections import OrderedDict

import csv
import matplotlib as mpl
import os

from eppl import get_data
from eppl.core import plot_wrapper 

@plot_wrapper
def genome_points_plot(ax, data, column, genome, alpha=1.0, color='r', marker_size=2):
    '''
    Args:
        ax : Axes object to plot figure on
        
        data : DataFrame object
        
        column : (str) Column to plot.
        
        genome: Either a Genome object or a string. If a string is passed the function will attempt to load the genome from the database of known genomes.
    
    Kwargs:
        alpha: Alpha value.
        
        color: Color of points.
            
        marker_size : Size of point to plot.       
        '''
    if not isinstance(genome, Genome):
        genome = load_genome(genome)
        
    x_min = 0
    
    x_max = 0
    
    chroms = data.chrom.unique()

    for chrom in chroms:
        chrom_data = data[data.chrom == chrom]
        
        x = genome.get_linear_coordinate(chrom, chrom_data.coord)
        
        y = chrom_data[column]
        
        ax.scatter(x, y, s=marker_size, c=color, alpha=alpha)
        
        if x.max() > x_max:
            x_max = x.max()
        
    y_min = data[column].min()
    
    y_max = data[column].max()
        
    ax.set_xlim(x_min, x_max)
    
    ax.set_ylim(y_min, y_max)
    
    # Set ticks so labels appear between ticks
    major_ticks = [0, ] + [genome.get_linear_coordinate(chrom.name, chrom.length) for chrom in genome.chromosomes]
    
    minor_ticks = [(x + y) / 2 for x, y in zip(major_ticks[:-1], major_ticks[1:])]
    
    minor_labels = [chrom.name for chrom in genome.chromosomes]
    
    ax.xaxis.set_major_locator(mpl.ticker.FixedLocator(major_ticks))
    
    ax.xaxis.set_major_formatter(mpl.ticker.NullFormatter())
    
    ax.xaxis.set_minor_locator(mpl.ticker.FixedLocator(minor_ticks))
    
    ax.xaxis.set_minor_formatter(mpl.ticker.FixedFormatter(minor_labels))
    
    ax.xaxis.grid(True, which='major')
    
    ax.xaxis.grid(False, which='minor')      

@plot_wrapper
def genome_segments_plot(ax, data, genome, alpha=1.0, cols=None, colors=None, line_widths=None, offsets=None):
    '''
    Args:
        ax : Axes object to plot figure on
        
        data : DataFrame object
        
        genome: Either a Genome object or a string. If a string is passed the function will attempt to load the genome from the database of known genomes.
    
    Kwargs:
        alpha: Alpha value.
        
        cols: Iterable of columns to plot. If None all columns except 'chrom', 'beg', and 'end' will be plotted.
        
        colors: Dictionary of colors to plot each column with. If None all columns will be red.
        
        line_widths: Dictionary of line widths for each column to be plotted. If not set a line width of 1 will used.
        
        offsets : How much segments for each colum will be offset from true value. If not set no offsets will used.       
        '''
    if not isinstance(genome, Genome):
        genome = load_genome(genome)
    
    if cols is None:
        cols = data.columns
        
        cols = cols.drop(['chrom', 'beg', 'end'])
    
    if colors is None:
        colors = {}
        
        for col in cols:
            colors[col] = 'r'
    
    if line_widths is None:
        line_widths = {}
        
        for col in cols:
            line_widths[col] = 1
    
    if offsets is None:
        offsets = {}
        
        for col in cols:
            offsets[col] = 0
    
    segments = _load_segments(data, cols)
    
    y_min = -1
    
    y_max = 0
    
    x_min = 0
    
    x_max = 0

    for seg in segments:
        beg = genome.get_linear_coordinate(seg.chrom, seg.beg)
        
        end = genome.get_linear_coordinate(seg.chrom, seg.end)
        
        x = [beg, end]
        
        for col in cols:
            y = [getattr(seg, col) + offsets[col], ] * 2
            
            ax.plot(x, y, c=colors[col], alpha=alpha, lw=line_widths[col])
        
        if seg.total_cn > y_max:
            y_max = seg.total_cn
        
        if end > x_max:
            x_max = end
    
    y_max += 1
    
    ax.set_xlim(x_min, x_max)
    
    ax.set_ylim(y_min, y_max)    
    
    # Set ticks so labels appear between ticks
    major_ticks = [0, ] + [genome.get_linear_coordinate(chrom.name, chrom.length) for chrom in genome.chromosomes]
    
    minor_ticks = [(x + y) / 2 for x, y in zip(major_ticks[:-1], major_ticks[1:])]
    
    minor_labels = [chrom.name for chrom in genome.chromosomes]
    
    ax.xaxis.set_major_locator(mpl.ticker.FixedLocator(major_ticks))
    
    ax.xaxis.set_major_formatter(mpl.ticker.NullFormatter())
    
    ax.xaxis.set_minor_locator(mpl.ticker.FixedLocator(minor_ticks))
    
    ax.xaxis.set_minor_formatter(mpl.ticker.FixedFormatter(minor_labels))
    
    ax.xaxis.grid(True, which='major')
    
    ax.xaxis.grid(False, which='minor')
    
    # Legend
    patch_artists = OrderedDict()
    
    for col in cols:
        patch_artists[col] = mpl.patches.Rectangle((0, 0), 1, 0.5, fc=colors[col])
        
    ax.legend(patch_artists.values(), patch_artists.keys(), fontsize=6)    

def load_genome(name):
    file_name = os.path.join('genome', '{0}.chromosomes.tsv'.format(name))
    
    file_name = get_data(file_name)
    
    reader = csv.DictReader(open(file_name), delimiter='\t')
    
    chromosomes = []
    
    for row in reader:
        chromosomes.append(Chromosome(row['name'], int(row['length'])))
    
    return Genome(chromosomes)

#=======================================================================================================================
# Helper functions
#=======================================================================================================================
def _load_segments(data, cols):
    segments = []
    
    for _, row in data.iterrows():
        chrom = row['chrom']
        
        beg = row['beg']
        
        end = row['end']
        
        seg = Segment(chrom, beg, end)
        
        for col in cols:
            setattr(seg, col, row[col])
        
        segments.append(seg)
    
    return segments          

#=======================================================================================================================
# Helper classes
#=======================================================================================================================
class Chromosome(object):
    def __init__(self, name, length):
        '''
        Args:
            name : (str) Name of chromosome.
                
            length: (int) Length of chromosome in relevant units, commonly bases.
        '''
        self.name = name
        
        self.length = length

class Genome(object):
    def __init__(self, chromosomes):
        '''
        Args:
            chromsomes: (list) List of chromosomes in genome. The order of the list defines the linear order in the genome.
        '''
        self.chromosomes = chromosomes
        
        self._init_chromosome_offsets()
    
    def get_linear_coordinate(self, chrom, coord):
        return self.chromosome_offsets[chrom] + coord 
    
    def _init_chromosome_offsets(self):
        self.chromosome_offsets = OrderedDict()
    
        self.chromosome_offsets[self.chromosomes[0].name] = 0
        
        for i, chrom in enumerate(self.chromosomes):
            if chrom.name in self.chromosome_offsets:
                continue
            
            prev_chrom = self.chromosomes[i-1]
            
            self.chromosome_offsets[chrom.name] = prev_chrom.length + self.chromosome_offsets[prev_chrom.name]

class Segment(object):
    def __init__(self, chrom, beg, end):
        self.chrom = chrom
        
        self.beg = beg
        
        self.end = end
    
    def __len__(self):
        return self.end - self.beg
