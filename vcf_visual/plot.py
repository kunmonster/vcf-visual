import math
from matplotlib import pyplot as plt
from natsort import natsorted
import numpy as np
import matplotlib.ticker as mticker
import matplotlib as mpl


def plot_stack_bar(bar_labels,bar_data):
    fig,ax = plt.subplots(figsize=(16,10),dpi=300)
    bottom = np.zeros(len(bar_labels))
    for label,data in bar_data.items():
        ax.bar(bar_labels,data,label=label,bottom=bottom,width=0.7,alpha=0.9)
        bottom += data
    ax.set_xticklabels(bar_labels,rotation=-75,fontsize=8)
    ax.set_xlim(left=-0.5)
    ax.set_ylim(bottom=-50)
    ax.legend()
    plt.savefig("./test.png")
    return None

def plot_bar(x_data,y_data):
    fig,ax = plt.subplots(figsize=(8,6),dpi=500)
    ax.bar(x_data,y_data)
    ax.set_xticklabels(x_data,rotation=-75,fontsize=8)
    ax.set_xlim(left=-0.5)
    plt.savefig('./test.png')
    
def plot_density(density,x,win_size):
    group_key = natsorted(density[x].unique())
    cols = 3
    rows = math.ceil(len(group_key) / cols)
    mpl.rcParams['axes.formatter.useoffset'] = False
    mpl.rcParams['axes.formatter.use_mathtext'] = False
    fig, ax = plt.subplots(rows, cols, figsize=(15, len(group_key)*0.5), sharex=True)
    ax = ax.flatten() 
    for i in range(len(ax)):
        if i < len(group_key):
            cur_key = group_key[i]
            cur_data = density[density[x] == cur_key]
            ax[i].bar(cur_data["BIN"], cur_data["COUNT"], width=win_size, color="skyblue", edgecolor="black",alpha=0.8)
            ax[i].set_title(f"{cur_key}", loc="right", fontsize=10)
            ax[i].set_xlim(left=-0.5)
            ax[i].tick_params(axis="both", labelsize=8)
            ax[i].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x // win_size} '))
        else:
            ax[i].axis("off") 
    fig.supxlabel("Position (Mb)", fontsize=14)
    fig.supylabel("Variant Count", fontsize=14)
    fig.suptitle("Structural Variant Distribution by Chromosome", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 1])
    fig.savefig('./test.png')