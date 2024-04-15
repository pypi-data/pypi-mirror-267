'''
This module lets you build ACMetric brand plots
'''

from matplotlib.patches import Rectangle, Patch
import matplotlib.pyplot as plt
from numpy import atleast_2d, linspace, mean, arange
from scipy.stats import sem, t

from . import colors
from . import params

__all__ = ['display_colors', 'bar', 'scatter', 'pie', 'box']


def display_colors():
    '''
    Display all the colors available in the palette.
    '''
    _, ax = plt.subplots(figsize=(4, 6))
    plt.axis('off')
    for i, v in enumerate(params.palette):
        ax.add_patch(Rectangle(
            (i % 2*0.5, i//2*0.15), 0.5, 0.15, color=v))
        if i == 4:
            ax.text(i % 2*0.5+0.25,
                    i//2*0.15+0.075,
                    list(colors.color_dict.keys())[i],
                    ha='center',
                    va='center',
                    color=colors.charcoal,
                    fontsize=14)
        elif i == 11:
            ax.text(i % 2*0.5+0.25,
                    i//2*0.15+0.075,
                    list(colors.color_dict.keys())[i],
                    ha='center',
                    va='center',
                    color=colors.sky,
                    fontsize=14)
        elif i == 9:
            ax.text(i % 2*0.5+0.25,
                    i//2*0.15+0.075,
                    list(colors.color_dict.keys())[i],
                    ha='center',
                    va='center',
                    color=colors.coral_60,
                    fontsize=14)
        else:
            ax.text(i % 2*0.5+0.25,
                    i//2*0.15+0.075,
                    list(colors.color_dict.keys())[i],
                    ha='center',
                    va='center',
                    color='w',
                    fontsize=14)
        ax.text(0.5, 0.95, 'ACMetric colors',
                ha='center', va='center', fontsize=16)


def bar(
    x, y, data, hue=None, display_values=False, value_size=12, value_fmt='%.1f',
    title=None, gradient=False, vert=True, agg='mean', display_ci=False, ci=.95
):
    '''
    Build an ACMetric branded bar chart.

    Use `hue` parameter to slice the bars by some additional category.
    Display the value of the bars with `display_values`.
    Change the format of the values with `value_fmt`.
    The bars can also be gradient if `gradient=True` is specified.
    If you want the bars to be horizontal, set `vert` to False.
    Set `display_ci` to display confidence intervals for each bar mean.
    Change the aggregating function `agg` to display median
    or any other metric within each category.

    Parameters
    ----------
    x : array-like
        Name of the column to divide to the bars.

    y : array-like
        Name of the column to determine the height of the bars.

    data : pd.DataFrame
        Dataset which the function should extract the data for the bar chart from.

    hue : array-like, optional
        Name of the column to slice the data by.
        If None, will display unsliced data.

    display_values : bool, default: False
        Whether to display the value above each bar.

    value_size : int, default: 12
        Size of the values upon the bars in pixels.

    value_fmt : str, default: '%.1f'
        Format of the bar values.
        Use '%.0f%%' to display percentages.

    title : str, optional
        Title of the bar chart.

    gradient : bool, default: False
        Whether to make bars gradient.

    vert : bool, default: True
        If False, bars will be horizontal.

    agg : str or func, default: 'mean'
        Name of function to aggregate y.
        List of possible func names:
            'mean' — calculate mean y for each x,
            'sum' — calculate sum of y for each x,
            'count' — calculate amount of y in each x,
            'nunique' — calculate amount of unique y for each x
        agg can also be a func, e.g. numpy.mean, numpy.log, etc.

    display_ci : bool, default: False
        Whether to display confidence intervals.

    ci : float, default: 0.95
        A range for the confidence interval from 0 to 1
    '''
    if display_ci and (display_values or gradient or agg != 'mean'):
        print("ERROR: ci is not available with 'display_values'", end=' ')
        print("or 'gradient' or when agg is not 'mean'.")
        return
    plt.title(title)
    plt.xlabel(x.capitalize().replace('_', ' '), fontsize=14)
    plt.ylabel(y.capitalize().replace('_', ' '), fontsize=14)
    if vert:
        if hue is None:
            data_grouped = data.groupby(x).agg({y: agg}).reset_index().dropna()
            bars = plt.bar(x=x, height=y, data=data_grouped,
                           color=params.palette)
            if display_ci:
                for i, x_value in enumerate(data_grouped[x]):
                    x_array = data[data[x] == x_value][y].dropna()
                    interval = t.interval(
                        ci, len(x_array)-1, loc=mean(x_array), scale=sem(x_array))
                    plt.vlines(x=i,
                               ymin=interval[0],
                               ymax=interval[1],
                               color=colors.stone,
                               lw=5
                               )
            if display_values:
                plt.yticks([])
                gap = data_grouped[y].mean() * 0.01
                for i, v in enumerate(data_grouped[y]):
                    plt.text(i, v + gap, str(round(v, 2)),
                             ha='center', va='bottom', fontsize=value_size)

            if gradient:
                grad = atleast_2d(linspace(0, 1, 256)).T
                ax = bars[0].axes
                lim = ax.get_xlim()+ax.get_ylim()
                for bar in bars:
                    bar.set_zorder(1)
                    bar.set_facecolor("none")
                    x, y = bar.get_xy()
                    w, h = bar.get_width(), bar.get_height()
                    ax.imshow(X=grad, cmap=params.cmap, extent=[
                              x, x+w, y, y+h], aspect="auto", zorder=0)
                ax.axis(lim)

        else:
            if gradient:
                print('Error: gradient and hue are not supported at the same time.')
                return
            pivot_table = data.pivot_table(
                index=x, columns=hue, values=y, aggfunc=agg)
            labels = pivot_table.index
            columns = pivot_table.columns
            labels_array = arange(len(labels))
            columns_array = arange(len(columns))
            width = 1 / (len(columns) + 1)
            for i, v in enumerate(columns):
                values = pivot_table[v]
                bars = plt.bar(
                    labels_array - (mean(columns_array) * width) + (i * width),
                    values,
                    width,
                    label=v)
                if display_ci:
                    for idx in labels_array:
                        x_array = data[(data[hue] == v) & (
                            data[x] == labels[idx])][y].dropna()
                        interval = t.interval(
                            ci, len(x_array)-1, loc=mean(x_array), scale=sem(x_array))
                        plt.vlines(x=idx - (mean(columns_array) * width) + (i * width),
                                   ymin=interval[0],
                                   ymax=interval[1],
                                   color=colors.stone,
                                   lw=5
                                   )
                if display_values:
                    plt.yticks([])
                    plt.bar_label(bars, padding=3,
                                  fontsize=value_size, fmt=value_fmt)
            plt.legend(title=hue.capitalize().replace('_', ' '))
            plt.xticks(labels_array, labels)

    else:
        if hue is None:
            data_grouped = data.groupby(y).agg({x: agg}).reset_index().dropna()
            bars = plt.barh(y=y, width=x, data=data_grouped,
                            color=params.palette)
            if display_ci:
                for i, y_value in enumerate(data_grouped[y]):
                    y_array = data[data[y] == y_value][x].dropna()
                    interval = t.interval(
                        ci, len(y_array)-1, loc=mean(y_array), scale=sem(y_array))
                    plt.hlines(y=i,
                               xmin=interval[0],
                               xmax=interval[1],
                               color=colors.stone,
                               lw=5
                               )
            if display_values:
                plt.xticks([])
                gap = data_grouped[x].mean() * 0.01
                for i, v in enumerate(data_grouped[x]):
                    plt.text(v - gap, i, str(round(v, 2)), ha='right',
                             va='center', fontsize=value_size, color='w')

            if gradient:
                grad = atleast_2d(linspace(1, 0, 256))
                ax = bars[0].axes
                lim = ax.get_xlim()+ax.get_ylim()
                for bar in bars:
                    bar.set_zorder(1)
                    bar.set_facecolor("none")
                    x, y = bar.get_xy()
                    w, h = bar.get_width(), bar.get_height()
                    ax.imshow(X=grad, cmap=params.cmap, extent=[
                              x, x+w, y, y+h], aspect="auto", zorder=0)
                ax.axis(lim)
        else:
            if gradient:
                print('Error: gradient and hue are not supported at the same time.')
            pivot_table = data.pivot_table(
                index=y, columns=hue, values=x, aggfunc=agg)
            labels = pivot_table.index
            columns = pivot_table.columns
            labels_array = arange(len(labels))
            columns_array = arange(len(columns))
            width = 1 / (len(columns) + 1)
            for i, v in enumerate(columns):
                values = pivot_table[v]
                bars = plt.barh(
                    labels_array - (mean(columns_array) * width) + (i * width),
                    values,
                    width,
                    label=v)
                if display_ci:
                    for idx in labels_array:
                        y_array = data[(data[hue] == v) & (
                            data[y] == labels[idx])][x].dropna()
                        interval = t.interval(
                            ci, len(y_array)-1, loc=mean(y_array), scale=sem(y_array))
                        plt.hlines(y=idx - (mean(columns_array) * width) + (i * width),
                                   xmin=interval[0],
                                   xmax=interval[1],
                                   color=colors.stone,
                                   lw=5
                                   )
                if display_values:
                    plt.xticks([])
                    plt.bar_label(bars, padding=3,
                                  fontsize=value_size, fmt=value_fmt)
            plt.legend(title=hue.capitalize().replace('_', ' '))
            plt.yticks(labels_array, labels)


def scatter(x, y, data, hue=None, marker_size=20, title=None):
    '''
    Making ACMetric branded scatter plot.

    Slice the data by some category with `hue` parameter.
    Adjust the marker size with `marker_size`.
    Set the title of the plot with `title`.

    Parameters
    ----------
    x : array-like
        Name of the column to build X axis.

    y : array-like
        Name of the column to build Y axis.

    data : DataFrame
        Dataset which the function should extract data for the scatter plot from.

    hue : array-like, optional
        Name of the column to slice the data by.
        If None, will display unsliced data and the scatter plot will be of one colour.

    marker_size : int, default: 20
        Size of the markers in pixels.

    title : str, optional
        Title of the scatter plot.
    '''
    if hue is not None:
        hue_values = sorted(data[hue].unique())
        for hue_value in hue_values:
            plt.scatter(
                x=x, y=y, data=data[data[hue] == hue_value], s=marker_size)
        plt.legend(
            hue_values,
            title=hue.capitalize().replace('_', ' '))
    else:
        plt.scatter(x=x, y=y, data=data, s=marker_size)
    plt.title(title)
    plt.xlabel(x.capitalize().replace('_', ' '), fontsize=14)
    plt.ylabel(y.capitalize().replace('_', ' '), fontsize=14)


def pie(x, data, labels=True, title=None, pct=False):
    '''
    Making ACMetric branded pie chart.

    Display or not the label of each group next to the wedges with `labels`.
    Show the share of each group in percents using `pct=True`.
    Add a title using `title`.

    Parameters
    ----------
    x : array-like
        Name of the column to determine the share of each wedge.

    data : pd.DataFrame
        Dataset which the function should extract data for the pie chart from.

    labels : bool, default: True
        If True, display labels next to each wedge.
        If False, display legend.

    title: str, optional
        Title of the pie chart.

    pct : bool, default: False
        Whether or not to display percentages of each wedge.
    '''
    plt.title(title)
    data = data.groupby(x).agg({x: 'count'}).rename(
        columns={x: 'count'}).reset_index()
    if pct:
        big_chart = plt.pie(
            x='count',
            data=data,
            colors=params.palette,
            startangle=90,
            counterclock=False,
            autopct='%1.1f%%',
            pctdistance=1.2
        )
        plt.legend(
            labels=data[x].unique(),
            loc=(0, .85),
            title=x.capitalize().replace('_', ' '))
    else:
        if labels:
            big_chart = plt.pie(
                x='count',
                data=data,
                labels=x,
                colors=params.palette,
                startangle=90,
                counterclock=False
            )
        else:
            big_chart = plt.pie(
                x='count',
                data=data,
                colors=params.palette,
                startangle=90,
                counterclock=False
            )
            plt.legend(
                labels=data[x].unique(),
                loc=(0, .85),
                title=x.capitalize().replace('_', ' '))

    small_circle = plt.Circle((0, 0), 0.25, color=colors.white)
    big_circle = plt.Circle((0, 0), 0.75, color=colors.white)
    p = plt.gcf()
    p.gca().add_artist(big_circle)
    small_chart = plt.pie(
        x='count',
        data=data,
        radius=0.5,
        colors=params.palette,
        startangle=90,
        counterclock=False
    )
    p.gca().add_artist(small_circle)


def box(x=None, y=None, data=None, hue=None, vert=True):
    '''
    Making ACMetric branded box plot.

    Use one or more than one column as X.
    Slice the data by some category using `hue`.
    Make the boxes horizontal with `vert=False`.

    Parameters
    ----------
    x : array-like, optional
        Name of the column(s) to build the box plot(s) on.
        Note: x MUST be a string if `hue` is not None!

    y : array-like, optional
        Name of the column to build Y axis.

    data : pd.DataFrame, optional
        Dataset which the function should extract data for the box plot from.

    hue : array-like, optional
        Name of the column to slice the data by.
        If None, will display unsliced data.
        If hue is not None, x must be a string.

    vert : bool, default: True)
        If False, boxes will be horizontal.
    '''
    if y is None:
        if isinstance(x, list):
            if hue is not None:
                print(
                    'Error: x cannot be a list if hue is used. \
                        Please, choose either multiple x or hue to slice x.')
            else:
                plt.boxplot(x=[data[i].dropna() for i in x], vert=vert)
                if vert:
                    plt.xticks(ticks=range(1, len(x)+1), labels=x)
                else:
                    plt.yticks(ticks=range(1, len(x)+1), labels=x)

        else:
            if hue is None:
                plt.boxplot(x=data[x].dropna(), vert=vert)
                if vert:
                    plt.xticks(ticks=[1], labels=[x])
                else:
                    plt.yticks(ticks=[1], labels=[x])
            else:
                hue_values = sorted(data[hue].unique())
                plt.boxplot(x=[data[data[hue] == i][x].dropna()
                            for i in hue_values], vert=vert)
                if vert:
                    plt.xticks(ticks=range(1, len(hue_values)+1),
                               labels=hue_values)
                    plt.ylabel(x.capitalize().replace('_', ' '), fontsize=14)
                else:
                    plt.yticks(ticks=range(1, len(hue_values)+1),
                               labels=hue_values)
                    plt.xlabel(x.capitalize().replace('_', ' '), fontsize=14)

    else:
        if isinstance(x, list):
            print('If y is specified, x cannot be a list')
        else:
            if hue is None:
                x_values = sorted(data[x].unique())

                for i, x_value in enumerate(x_values):
                    plt.boxplot(
                        data[data[x] == x_value][y].dropna(),
                        positions=[i],
                        vert=vert
                    )
                if vert:
                    plt.xticks(ticks=[i for i in range(len(x_values))],
                               labels=x_values)
                    plt.xlabel(x.capitalize().replace('_', ' '), fontsize=14)
                    plt.ylabel(y.capitalize().replace('_', ' '), fontsize=14)
                else:
                    plt.yticks(ticks=[i for i in range(len(x_values))],
                               labels=x_values)
                    plt.ylabel(x.capitalize().replace('_', ' '), fontsize=14)
                    plt.xlabel(y.capitalize().replace('_', ' '), fontsize=14)

            else:
                x_values = sorted(data[x].unique())
                hue_values = sorted(data[hue].unique())
                handles = [Patch(color=params.palette[i], label=v) for i, v in enumerate(hue_values)]

                for i, x_value in enumerate(x_values):
                    for j, hue_value in enumerate(hue_values):
                        plt.boxplot(
                            data[(data[x] == x_value) & (
                                data[hue] == hue_value)][y].dropna(),
                            positions=[i*len(hue_values)*0.25 + j*.18],
                            boxprops={'facecolor': params.palette[j]},
                            vert=vert
                        )
                for j, hue_value in enumerate(hue_values):
                    plt.plot([], color=params.palette[j], label=hue_value)
                if vert:
                    plt.xticks(ticks=[i*0.25*len(hue_values) + .18*mean(arange(len(hue_values)))
                                      for i in range(len(x_values))],
                               labels=x_values)
                    plt.xlabel(x.capitalize().replace('_', ' '), fontsize=14)
                    plt.ylabel(y.capitalize().replace('_', ' '), fontsize=14)
                else:
                    plt.yticks(ticks=[i*0.25*len(hue_values) + .18*mean(arange(len(hue_values)))
                                      for i in range(len(x_values))],
                               labels=x_values)
                    plt.ylabel(x.capitalize().replace('_', ' '), fontsize=14)
                    plt.xlabel(y.capitalize().replace('_', ' '), fontsize=14)
                plt.legend(handles=handles, title=hue.capitalize().replace('_', ' '))
