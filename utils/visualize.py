import seaborn as sns
from matplotlib import pyplot as plt, ticker
import pandas as pd
import numpy as np
from matplotlib.patches import ConnectionPatch
from matplotlib.transforms import blended_transform_factory
from PIL import Image
from io import BytesIO
def set_ax_title(ax,title):
    ax.set_title(title)
def set_ax_xticks(ax):
    ax.tick_params(axis='x', which='major', direction='out', width=0.4, colors='gray',labelsize=6,labelrotation=75)
def set_ax_yticks(ax):
    ax.set_yticks(range(0, 2100, 100))
    ax.set_ylim(bottom=-20)
    ax.set_xmargin(0.01)
    ax.tick_params(axis='y', which='both', direction='out', length=5,width=0.4, colors='gray',labelsize=8)
def set_ax_border(ax):
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)
    ax.spines['top'].set_linewidth(0.4)
    ax.spines['top'].set_color('gray')
    ax.spines['right'].set_linewidth(0.4)
    ax.spines['right'].set_color('gray')
    ax.spines['bottom'].set_linewidth(0.4)
    ax.spines['bottom'].set_color('black')
    ax.spines['left'].set_linewidth(0.4)
    ax.spines['left'].set_color('black')





def visual_by_chr(data):

    '''
        生成每个染色体上的各种变异类型柱状图
        如果只有一条染色体,那么将会以每个变异类型一个柱的形式展示
        如果有多条染色体,那么将会以堆叠图的形式展示
        param data: VCF obejct
        return None
    '''

    # 判断染色体数目
    chr_num = len(data['CHR'].unique())
    
    if chr_num == 1:
        # 只有一条染色体，那么生成柱图,每个变异类型一个柱
        type_data = data.groupby('TYPE').size().reset_index(name='COUNT')
        x_data = type_data['TYPE']
        y_data = type_data['COUNT']
        fig,ax = plt.subplots(figsize=(8,6),dpi=500)
        bar_colors = ['#A5AEB7','#925EB0','#7E99F4','#CC7C71','#7AB656']
        ax.bar(x_data,y_data,color = bar_colors)
        set_ax_title(ax,'Numbers of Every Variant Type  in Chromosome '+ str(data['CHR'].unique()[0]))
        ax.set_ylabel('Counts')
        ax.set_xlabel('Variant Type')
        plt.savefig('test/pics/result.png')
    else:
        # 不止一条染色体,生成堆叠图
        count_data = data.groupby(['TYPE','CHR']).size().reset_index(name='COUNT')
        bar_labels = sorted(count_data['CHR'].unique())
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
            ax.bar(bar_labels,data,label=label,bottom=bottom,width=0.5,alpha=0.9)
            bottom += data
        set_ax_title(ax,'Numbers of Every Variant Type in Each Chromosome')
        ax.set_xticklabels(bar_labels,rotation=-75,fontsize=7)
        ax.set_ylabel('Counts')
        ax.set_xlabel('Chromosome')
        ax.legend()
        plt.savefig('test/pics/result_1.png')


def visual_by_var_len(data):
    '''
    以横轴为变异长度,纵轴为变异数量进行可视化,但是只针对结构变异,应在传参前确认是否为结构变异
    '''
    data_by_len = data['LEN']
    max_len = data_by_len.max()
    breakpoint()
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
    bins_main = np.arange(0, data_by_len.max() + 1, 0.1)    
    ax.hist(data_by_len, bins=bins_main, alpha=0.7,width=0.4)
    ax.set_xlim(-0.1, data_by_len.max())  

    ax.set_yscale('log')
    ax.set_xlabel(f"SV size ({x_tick_label})", fontsize=14)
    ax.set_ylabel("SV count", fontsize=14)
    ax.set_title("Distribution of Structural Variant Sizes", fontsize=16)
    plt.tight_layout()
    plt.savefig('test/pics/result_3.png')



def distribution_by_chr(data:pd.DataFrame):
    '''
        变异分布密度图
    '''
    fig, ax = plt.subplots(figsize=(12, 10), dpi=300)
    window_size = 1000000
    chrs = sorted(data['CHR'].unique())
    for i,chr in enumerate(chrs):
        data_by_chr = data[data['CHR'] == chr]
        max_position = data_by_chr['START'].max()
        win_locs = np.arange(0,max_position,window_size)
        counts, bin_edges = np.histogram(data_by_chr['START'], bins=win_locs)
        x = bin_edges[:-1] / window_size
        y = counts + i *10
        ax.bar(x,counts,width=window_size/1000000,align='edge',label=f'chr{chr}',alpha=0.5)
    ax.set_xlabel("Position (Mb)")
    ax.set_ylabel("Count")
    ax.set_title("Chromosome-based Variant Distribution")
    ax.legend(title="Chromosome")
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('test/pics/result_2.png')
