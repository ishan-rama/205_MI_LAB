import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns

from collections import OrderedDict

sns.set()

uoa_colours = OrderedDict([
    ('Dark blue', '#00467F'),
    ('Light blue', '#009AC7'),
    ('Silver', '#8D9091')
])
uoa_faculty_colours = OrderedDict([
    ('Arts', '#A71930'),
    ('Business', '#7D0063'),
    ('Creative Arts and Industries', '#D2492A'),
    ('Education and Social Work', '#55A51C'),
    ('Engineering', '#4F2D7F'),
    ('Auckland Law School', '#005B82'),
    ('Medical and Health Sciences', '#00877C'),
    ('Science', '#0039A6')
])


def faculty_color_palette(faculty='Engineering'):
    faculties = list(uoa_faculty_colours.keys())
    assert faculty in faculties
    faculties.insert(0, faculties.pop(faculties.index(faculty)))
    colors = uoa_colours.copy()
    for faculty in faculties:
        colors[faculty] = uoa_faculty_colours[faculty]
    return sns.color_palette([color for name, color in colors.items()])


engineering_colors = faculty_color_palette()

sns.set_palette(engineering_colors)


def distribution(series, log_transformed=False,
                 swarmplot=False,
                 bins='auto'):
    '''
    Visualize distribution of pandas.Series as combination of histogram and boxplot

    The code has been adapted from ENGSCI762 Data Science module

    :param series: pandas.Series
    :return: fig
    '''
    # ENGSCI762 Data Science module
    # http://stackoverflow.com/questions/40070093/gridspec-on-seaborn-subplots
    gridkw = dict(height_ratios=[5, 1])
    fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw=gridkw, sharex=True)
    if log_transformed:
        feature = pd.Series(np.log(series),
                            name='log({})'.format(series.name)
                            )
    else:
        feature = series
    sns.histplot(x=feature, ax=ax1, kde=False, bins=bins)  # array, top subplot
    sns.boxplot(x=feature, ax=ax2, width=.4)  # bottom subplot
    if swarmplot:
        sns.swarmplot(feature, ax=ax2,
                      size=2, color=".3", linewidth=0)

    ax1.set_xlabel('')
    ax1.text(1.05, 0.95,
             feature.describe().to_string(),
             transform=ax1.transAxes, fontsize=14,
             verticalalignment='top')
    #http://stackoverflow.com/questions/29813694/how-to-add-a-title-to-seaborn-facet-plot
    fig.subplots_adjust(top=0.9)
    fig.suptitle(feature.name, fontsize=16)
    return fig, (ax1, ax2)


def distributions(series, species, log_transformed=False,
                  both_series=False, bins='auto', colors=engineering_colors):
    '''
    Visualize distribution of pandas.Series as combination of histogram and boxplot

    The code has been adapted from ENGSCI762 Data Science module

    :param series: pandas.Series
    :return: fig
    '''
    # ENGSCI762 Data Science module
    # http://stackoverflow.com/questions/40070093/gridspec-on-seaborn-subplots
    gridkw = dict(height_ratios=[5, 1, 1])
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, gridspec_kw=gridkw, sharex=True)

    labels = np.unique(species)
    if log_transformed:
        feature = pd.Series(np.log(series),
                            name='log({})'.format(series.name)
                            )
    else:
        feature = series
    if not both_series:
        A = feature[species == labels[0]]
        B = feature[species == labels[1]]
        Alabel = labels[0]
        Blabel = labels[1]
    else:
        A = feature
        B = species
        Alabel = feature.name
        Blabel = species.name

    sns.histplot(x=A, ax=ax1,
                 kde=False,
                 label=Alabel,
                 color=colors[1],
                 bins=bins
                 )  # array, top subplot
    sns.histplot(x=B, ax=ax1,
                 kde=False,
                 label=Blabel,
                 color=colors[3],
                 bins=bins)  # array, top subplot
    ax1.legend()
    ax1.set_xlabel('')
    sns.boxplot(x=A, ax=ax2, width=.4,
                color=colors[1])  # middle subplot
    ax2.set_xlabel('')

    current_palette = colors
    sns.boxplot(x=B, ax=ax3, width=.4,
                color=colors[3]
                )  # bottom subplot
    return fig, (ax1, ax2, ax3)


def barplot(series):
    counts = series.value_counts()
    ax = counts.plot(kind='bar')
    plt.text(1.05, 0.95, str(counts),
             transform=ax.transAxes, fontsize=14,
             verticalalignment='top')


def savefig(filename, path='fig'):
    path_to_fig = os.path.join(path, filename)
    plt.savefig(path_to_fig, bbox_inches='tight')
    return path_to_fig


def saveorg(filename):
    output = "file:./{}".format(savefig(filename))
    return output


def stemplot(sequence, n_0=0):
    rcParams = plt.rcParams.copy()
    plt.rcdefaults()
    plt.rcParams.update({'font.size': 22})

    fig, ax = plt.subplots(figsize=(10, 10))
    # a defined in previous block
    x_n = np.pad(sequence, (1, 1), constant_values=(0, 0))
    n = np.arange(-n_0, x_n.shape[0] - n_0)  # a0 defined in previous block
    markerline, stemlines, baseline = ax.stem(n, x_n)
    plt.setp(stemlines, 'linewidth', 2)
    ax.grid(axis='both', which='both')

    # Adapted from https://stackoverflow.com/a/63539077
    # Set bottom and left spines as x and y axes of coordinate system
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')

    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Create 'x' and 'y' labels placed at the end of the axes
    ax.set_xlabel('$n$', labelpad=-24, x=1.03)
    ax.set_ylabel('$x[n]$', labelpad=-21, y=1.02, rotation=0)
    plt.rcParams.update(rcParams)
