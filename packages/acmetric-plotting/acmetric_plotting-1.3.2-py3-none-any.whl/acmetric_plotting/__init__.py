'''
ACMetric package helps you build plots without hours of tuning.

ac.display_colors() will show you a table with all the colors available and their names.

ac.colors module contains ACMetric colors, you can access them by writing
ac.colors.coral, ac.colors.sky_60, etc.

ac.palette is a matplotlib color palette. You can call it and choose a color you like
by index, e.g. ac.palette[3].

ac.cmap is a gradient colormap that can be used in seaborn heatmap and other plots.

Now 4 kinds of plots are available in the package: bar chart, pie chart, scatter plot
and box plot. You can make them using ac.bar, ac.pie, ac.scatter and ac.box.
All the possible parameters can be found in the docstring.

Note: it doesn't mean you can't build other kinds of plots. Just import matplotlib
or seaborn, and all the plots you create will also be ACMetric branded!

You can find code examples here:
https://github.com/ACMetric/acmetric_package/blob/master/notebooks/acmetric_package_intro.ipynb
'''

from . import colors
from .params import *
from .plots import *

__version__ = '1.2.2'
