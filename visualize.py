import sys
import json
import pandas as pd
import numpy as np
import sklearn.manifold
import sklearn.metrics.pairwise
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
with open('data/experiment_config.json', 'r') as file:
    config = json.load(file)

if len(sys.argv) == 1:
    VERSION=list(config.keys())[-1]
else:
    arg = sys.argv[1]
    if arg == '-h':
        print('Usage: visualize.py [version number]\nEx: visualize.py 2')
        exit()
    elif not arg.isdigit():
        print('Version needs to be a number!')
        exit()
    VERSION = f'exp{arg}'

try:
    config = config[VERSION]
except KeyError:
    print(f'Experiment \'{VERSION}\' does not exist')
    exit()

DATA_CSV = f'data/{config["dataset"]}'
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
        cmap=clothes_cm,
        s=10
    )

    axis.set_title(feature)

def plot_histograms():
    fig, (ax1, ax2) = plt.subplots(
        nrows=1,
        ncols=2,
        figsize=(10,6)
    )

    label_hist(ax1)
    time_hist(ax2)

    plt.savefig(f'visualizations/histograms_{VERSION}.png')
    plt.show()

def plot_scatters():
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(
        nrows=2,
        ncols=2,
        figsize=(12,7)
    )

    scatter(ax1, 'temp')
    scatter(ax2, 'humidity')
    scatter(ax3, 'uv')
    scatter(ax4, 'wind')

    legend_labels = ['coat', 'jacket-long', 'jacket-short', 'none']
    legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=list(COLORS.values())[i], markersize=10) for i in range(4)]
    fig.legend(legend_handles, legend_labels, title='Categories')
    
    fig.tight_layout()
    fig.subplots_adjust(right=0.87)
    plt.savefig(f'visualizations/scatters_{VERSION}.png')
    plt.show()

def plot_mds():
    data_norm = data.drop(columns=config['ignore']).select_dtypes(include=['number'])
    data_norm = (data_norm - data_norm.mean()) / data_norm.std()

    distMatrix = sklearn.metrics.pairwise.manhattan_distances(data_norm)
    distMatrix = pd.DataFrame(
        distMatrix,
        columns=data_norm.index,
        index=data_norm.index
    )
 
    mds = sklearn.manifold.MDS(
        n_components=2,
        dissimilarity='precomputed',
        n_init=100,
        max_iter=1000
    )

    data2D = mds.fit_transform(distMatrix)
    data2D = pd.DataFrame(
        data2D,
        columns=['x','y'],
        index=data_norm.index
    )

    print("Stress:", mds.stress_)

    data2D.plot.scatter(x='x', y='y')
    plt.show()

def plot_boxplots():
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(
        nrows=1,
        ncols=4,
        figsize=(12,4)
    )
    boxplot(ax1, 'temp')
    boxplot(ax2, 'uv')
    boxplot(ax3, 'humidity')
    boxplot(ax4, 'wind')

    fig.suptitle("Data Feature Distribution")
    fig.tight_layout()
    plt.savefig(f'visualizations/boxplots_{VERSION}.png')
    plt.show()

def boxplot(axis, col: str):
    data.boxplot(column=[col], ax=axis)

if __name__ == '__main__':
    init_data()
    plot_histograms()
    plot_scatters()
    plot_mds()
    plot_boxplots()
