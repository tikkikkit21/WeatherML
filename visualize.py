import sys
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.axes
from matplotlib.colors import ListedColormap
from util import time_to_int

COLORS = {
    'coat': '#4A86E8',
    'jacket-long': '#00FF00',
    'jacket-short': '#FFFF00',
    'none': '#FF0000'
}

# check for provided version in cline args
with open('data/version_info.json', 'r') as file:
    config = json.load(file)

if len(sys.argv) == 1:
    VERSION=list(config.keys())[-1]
else:
    arg = sys.argv[1]
    if arg == '-h':
        print('Usage: visualize.py [version number]')
        exit()
    elif not arg.isdigit():
        print('Version needs to be a number!')

    VERSION = f'v{arg}'

try:
    config = config[VERSION]
except KeyError:
    print(f'Dataset {VERSION} does not exist')
    exit()

DATA_CSV = f'data/weather_data_{VERSION}.csv'
data = None

def init_data():
    global data
    
    data = pd.read_csv(DATA_CSV, names=config['labels'], skiprows=1)
    data['time'] = data['time'].apply(lambda d: time_to_int(d))
    data['humidity'] = data['humidity'].apply(lambda h: float(h.strip('%'))/100)

def label_hist(axis: matplotlib.axes.Axes):
    output = data[config['output']].value_counts().sort_index()
    output.plot.bar(
        x='Label',
        y='# Occurences',
        ax=axis,
        color=list(COLORS.values())
    )
    axis.set_title('Label Distribution')
    axis.set_xlabel('Clothing Type')
    axis.set_ylabel('# Records')
    axis.tick_params(axis='x', labelrotation=0)

def time_hist(axis: matplotlib.axes.Axes):
    data['time'].plot.hist(bins=24, ax=axis)
    axis.set_title('Time Distribution')
    axis.set_xlabel('Time')
    axis.set_ylabel('# Records')

def scatter(axis: matplotlib.axes.Axes, feature='temp'):
    clothes_cm = ListedColormap(COLORS.values())
    
    axis.scatter(
        x=data.index,
        y=data[feature],
        c=data[config['output']].astype('category').cat.codes,
        cmap=clothes_cm
    )

    legend_labels = ['coat', 'jacket-long', 'jacket-short', 'none']
    legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=list(COLORS.values())[i], markersize=10) for i in range(4)]
    axis.legend(legend_handles, legend_labels, title='Categories')
    axis.set_title(feature)

def plot_histograms():
    fig, (ax1, ax2) = plt.subplots(
        nrows=1,
        ncols=2,
        figsize=(10,6)
    )

    label_hist(ax1)
    time_hist(ax2)
    plt.show()

def plot_scatters():
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(
        nrows=2,
        ncols=2,
        figsize=(8,8)
    )

    scatter(ax1, 'temp')
    scatter(ax2, 'humidity')
    scatter(ax3, 'uv')
    scatter(ax4, 'wind')

    plt.show()

if __name__ == '__main__':
    init_data()
    plot_histograms()
    plot_scatters()
