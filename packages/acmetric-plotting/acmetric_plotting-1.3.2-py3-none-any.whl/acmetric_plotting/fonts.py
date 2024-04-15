'''
ACMetric default font for plots, Oswald Regular
'''
from matplotlib import font_manager
from pkg_resources import resource_filename

font_path = resource_filename('acmetric_plotting', 'Oswald-Regular.ttf')

fe = font_manager.FontEntry(
    fname=font_path,
    name='Oswald Regular'
)
font_manager.fontManager.ttflist.insert(0, fe)
