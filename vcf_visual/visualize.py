from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import math
from natsort import natsorted
from PIL import Image
from io import BytesIO
import matplotlib.ticker as mticker
import matplotlib as mpl

def visual_by_chr(data:pd.DataFrame):
    """generate bar chart of variant type in each chromosome\n

    Args:
        data (pd.DataFrame): VCF info
    Returns:
        None
    """
    chr_num = len(data['CHR'].unique())
    
    if chr_num == 1:
        type_data = data.groupby('TYPE').size().reset_index(name='COUNT')
        x_data = type_data['TYPE']
        y_data = type_data['COUNT']
        fig,ax = plt.subplots(figsize=(8,6),dpi=500)
        bar_colors = ['#A5AEB7','#925EB0','#7E99F4','#CC7C71','#7AB656']
        ax.bar(x_data,y_data,color = bar_colors)
        ax.set_xlim(left=-0.5)
        ax.set_title('Numbers of Every Variant Type  in Chromosome '+ str(data['CHR'].unique()[0]))
        ax.set_ylabel('Counts')
        ax.set_xlabel('Variant Type')
        plt.savefig('test/pics/result.png')
    else:
        # more than one chromosome, then generate stacked bar chart
        count_data = data.groupby(['TYPE','CHR']).size().reset_index(name='COUNT')
        bar_labels = natsorted(count_data['CHR'].unique())
        var_type = sorted(count_data['TYPE'].unique())
        bar_data = {}
        for every_type in var_type:
            bar_data[every_type] = []
            for every_chr in bar_labels:
                count = count_data[(count_data['CHR'] == every_chr) & (count_data['TYPE'] == every_type)]['COUNT'].values[0]
                if count is None:
                    count = 0
                bar_data[every_type].append(count)

        # 对种类进行排序
        bar_data = dict(sorted(bar_data.items(),key=lambda item:sum(item[1])/len(item[1]),reverse=True))
        fig,ax = plt.subplots(figsize=(16,10),dpi=300)
        bottom = np.zeros(len(bar_labels))
        for label,data in bar_data.items():
            ax.bar(bar_labels,data,label=label,bottom=bottom,width=0.7,alpha=0.9)
            bottom += data
        ax.set_xticklabels(bar_labels,rotation=-75,fontsize=7)
        ax.set_xlim(left=-0.5)
        ax.set_ylim(bottom=-50)
        ax.set_title('Numbers of Every Variant Type in Each Chromosome')
        ax.set_ylabel('Counts')
        ax.set_xlabel('Chromosome')
        ax.legend()
        plt.savefig('test/pics/visual_by_chr.png')


def visual_by_var_len(data:pd.DataFrame):
    """ generate histogram of variant length\n

    Args:
        data (pd.DataFrame): VCF info
    Returns:
        None
    """
    data_by_len = data['LEN']
    max_len = data_by_len.max()
    x_tick_label = "bp"
    scale_factor = 1
    if max_len > 1000000:
        scale_factor = 1000000
        x_tick_label = "Mb"
    elif max_len < 1000000 and max_len > 1000:
        scale_factor = 1000
        x_tick_label = "kb"
    else:
        pass 
    data_by_len = data_by_len / scale_factor
    fig, ax = plt.subplots(figsize=(12, 10), dpi=300)
    step_size =  (1 if scale_factor == 1 else 0.1)
    bins_main = np.arange(0, data_by_len.max(),step_size)    
    ax.hist(data_by_len, bins=bins_main, alpha=0.7,width=0.4)
    ax.set_xlim(left=-0.5)
    ax.set_yscale('log')
    ax.set_xlabel(f"SV size ({x_tick_label})", fontsize=14)
    ax.set_ylabel("SV count", fontsize=14)
    ax.set_title("Distribution of Structural Variant Sizes", fontsize=16)
    plt.tight_layout()
    plt.savefig('test/pics/visual_by_var_len.png')


def distribution_by_chr(data:pd.DataFrame):
    """ generate histogram of variant distribution by chromosome\n
    Args:
        data (pd.DataFrame): VCF info
    Returns:
        None
    """
    mpl.use('Agg')
    bin_size = 1_000_000
    # data["BIN"] = data["START"] // bin_size * bin_size
    data["BIN"] = pd.cut(data["START"], bins=range(0, data["START"].max() + bin_size, bin_size), right=False, labels=range(0, data["START"].max(), bin_size))
    density = data.groupby(["CHR", "BIN"]).size().reset_index(name="COUNT")
    # breakpoint()

    chrs = natsorted(density["CHR"].unique())

    cols = 3
    rows = math.ceil(len(chrs) / cols)
    mpl.rcParams['axes.formatter.useoffset'] = False
    mpl.rcParams['axes.formatter.use_mathtext'] = False
    fig, ax = plt.subplots(rows, cols, figsize=(15, len(chrs)*0.5), sharex=True)
    ax = ax.flatten() 
    for i in range(len(ax)):
        if i < len(chrs):
            chrom = chrs[i]
            chrom_data = density[density["CHR"] == chrom]
            ax[i].bar(chrom_data["BIN"], chrom_data["COUNT"], width=bin_size, color="skyblue", edgecolor="black",alpha=0.8)
            ax[i].set_title(f"{chrom}", loc="right", fontsize=10)
            ax[i].set_xlim(left=-0.5)
            ax[i].tick_params(axis="both", labelsize=8)
            ax[i].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x // 1_000_000} '))
        else:
            ax[i].axis("off") 
    fig.supxlabel("Position (Mb)", fontsize=14)
    fig.supylabel("Variant Count", fontsize=14)
    fig.suptitle("Structural Variant Distribution by Chromosome", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 1])
    fig.savefig('test/pics/distribution_by_chr.png')

# TODO:MAF histogram
def visual_maf(data:pd.DataFrame):
    """ generate histogram of variant MAF\n
    Args:
        data (pd.DataFrame): VCF info
    Returns:
        None
    """
    return None

# TODO:AF histogram
def visual_af(data:pd.DataFrame):
    """ generate histogram of variant AF\n
    Args:
        data (pd.DataFrame): VCF info
    Returns:
        None
    """


# TODO:Annotation pie chart
def visual_annotation_pie(data):
    return None