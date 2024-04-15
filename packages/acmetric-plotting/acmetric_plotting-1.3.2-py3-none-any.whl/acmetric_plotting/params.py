'''
This module contains all parameters you need to build plots
'''

from matplotlib import rcParams
from matplotlib.colors import LinearSegmentedColormap
from seaborn import color_palette
from cycler import cycler

from . import colors
from . import fonts

__all__ = ['palette', 'cmap', 'fonts']

palette = color_palette(colors.color_dict.values(), desat=1)

cmap = LinearSegmentedColormap.from_list(
    'acmetric', [colors.sun, colors.coral], N=100)

rcParams['axes.edgecolor'] = colors.stone
rcParams['axes.labelcolor'] = colors.stone
rcParams['axes.spines.top'] = False
rcParams['axes.spines.right'] = False
rcParams['axes.titlecolor'] = colors.stone
rcParams['axes.titlesize'] = 16
rcParams['font.size'] = 12
rcParams['figure.figsize'] = (8, 5)
rcParams['figure.facecolor'] = colors.white
rcParams['legend.frameon'] = False
rcParams['legend.fontsize'] = 10
rcParams['legend.labelcolor'] = colors.stone
rcParams['lines.linewidth'] = 3
rcParams['lines.color'] = colors.sun
rcParams['patch.facecolor'] = colors.sun
rcParams['text.color'] = colors.stone
rcParams['xtick.color'] = colors.stone
rcParams['ytick.color'] = colors.stone
rcParams['xtick.bottom'] = False
rcParams['ytick.left'] = False
rcParams['xtick.labelsize'] = 12
rcParams['ytick.labelsize'] = 12
rcParams['axes.prop_cycle'] = cycler(color=palette)
rcParams['boxplot.boxprops.linewidth'] = 0
rcParams['boxplot.capprops.color'] = colors.stone
rcParams['boxplot.capprops.linewidth'] = 1
rcParams['boxplot.whiskerprops.color'] = colors.stone
rcParams['boxplot.whiskerprops.linewidth'] = 1
rcParams['boxplot.medianprops.color'] = colors.white
rcParams['boxplot.medianprops.linewidth'] = 2
rcParams['boxplot.patchartist'] = True
rcParams['boxplot.flierprops.markeredgecolor'] = colors.white
rcParams['boxplot.flierprops.markerfacecolor'] = colors.sun_60
rcParams['boxplot.flierprops.markeredgewidth'] = 0
rcParams['boxplot.flierprops.markersize'] = 5
rcParams['font.family'] = fonts.fe.name

def layout_color(color):
    '''
    Change axis and font color to black if needed.

    Parameters
    ----------
    color : str
        Name of the color to be used for axis and font. Choose one of the two options:
        'default' for ACMetric's Stone color, or 'black' for ACMetric's Charcoal color.
    '''
    if color == 'default':
        rcParams['axes.edgecolor'] = colors.stone
        rcParams['axes.labelcolor'] = colors.stone
        rcParams['axes.titlecolor'] = colors.stone
        rcParams['legend.labelcolor'] = colors.stone
        rcParams['text.color'] = colors.stone
        rcParams['xtick.color'] = colors.stone
        rcParams['ytick.color'] = colors.stone
    elif color == 'black':
        rcParams['axes.edgecolor'] = colors.charcoal
        rcParams['axes.labelcolor'] = colors.charcoal
        rcParams['axes.titlecolor'] = colors.charcoal
        rcParams['legend.labelcolor'] = colors.charcoal
        rcParams['text.color'] = colors.charcoal
        rcParams['xtick.color'] = colors.charcoal
        rcParams['ytick.color'] = colors.charcoal
    else:
        "Please, specify one of the two colors: 'default' (grey) or 'black'."