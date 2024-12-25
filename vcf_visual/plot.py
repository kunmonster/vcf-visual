import math
from matplotlib import pyplot as plt
from natsort import natsorted
from sklearn.neighbors import KernelDensity
import numpy as np
import matplotlib.ticker as mticker
import matplotlib as mpl
from vcf_visual.utils import get_unit


def plot_scatter(x_data,y_data):
    fig,ax = plt.subplots(figsize=(8,6),dpi=500)
    ax.scatter(x_data,y_data)
    return fig


         
def plot_boxplot(labels,data):
    fig,ax = plt.subplots(figsize=(10,6),dpi=500)
    ax.boxplot(data,labels=labels,patch_artist=True,showfliers=False,showmeans=True)
    ax.set_xticklabels(labels,rotation=-75,fontsize=8)
    fig.tight_layout()
    return fig


def plot_stack_bar(bar_labels,bar_data):
    fig,ax = plt.subplots(figsize=(16,10),dpi=300)
    bottom = np.zeros(len(bar_labels))
    sum_val_array = np.zeros(len(bar_labels))
    for label,data in bar_data.items():
        sum_val_array += np.array(data)
        ax.bar(bar_labels,data,label=label,bottom=bottom,width=0.8,alpha=0.9)
        bottom += data
    sum_val = max(sum_val_array)
    ax.set_ylim(-0.03*sum_val,sum_val+0.1*sum_val)
    ax.set_xticklabels(bar_labels,rotation=-75,fontsize=8)
    ax.set_xlim(-0.5,len(bar_labels)-0.2)
    ax.legend()
    return fig

def plot_bar(x_data,y_data):
    fig,ax = plt.subplots(figsize=(16,10),dpi=500)
    ax.bar(x_data,y_data,width=0.8,alpha=0.9)
    max_y = max(y_data)
    ax.set_ylim(-0.03*max_y,max_y+0.1*max_y)
    ax.set_xlim(-0.5,len(x_data)-0.2)
    ax.set_xticklabels(x_data,rotation=-75,fontsize=8)
    fig.tight_layout()
    return fig
    
    
def plot_density(data,**kwargs):
    if isinstance(data,list):
       # single ax
        kde = KernelDensity(kernel='gaussian', bandwidth=50).fit(data)
        x_axis = np.linspace(data.min(), data.max(), 1000).reshape(-1, 1)
        # 计算 log 密度
        log_density = kde.score_samples(x_axis)
        fig ,ax = plt.subplots(figsize=(8,6),dpi=500)
        ax.plot(x_axis, np.exp(log_density), color="skyblue", lw=2)
        ax.set_xlabel("Value")
        ax.set_ylabel("Density")
        return fig
    else:
       # multi ax
        axis = kwargs.get("axis")
        group_keys = data.index.tolist()
        num_groups = len(group_keys)

         # 动态计算行数和列数（尽量接近正方形布局）
        cols = math.ceil(math.sqrt(num_groups))
        rows = math.ceil(num_groups / cols)

        # 创建子图网格
        fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows), sharex=True, sharey=True)
        axes = np.array(axes).flatten()  # 展平为一维数组，便于迭代处理

        # 设置统一的 x 轴范围
        
        min_value = np.array(data["DENSITY"].min()).min()
        max_value = np.array(data["DENSITY"].max()).max()
        X_plot = np.linspace(min_value, max_value, 1000).reshape(-1, 1)

        # 绘制每个分组的密度图
        for idx, row in data.iterrows():
            group = row[axis.x]
            values = row["DENSITY"]
            kde = KernelDensity(kernel="gaussian", bandwidth=100).fit(np.array(values).reshape(-1, 1))
            log_density = kde.score_samples(X_plot)

            axes[idx].plot(X_plot, np.exp(log_density), label=f"{group}")
            axes[idx].set_title(f"{group}")
            axes[idx].legend()
            axes[idx].grid(False)

            # 移除未使用的子图
        for ax in axes[num_groups:]:
            ax.axis("off")
            # 设置共享轴标签
        fig.text(0.5, 0.04, axis.y, ha='center', va='center')
        fig.text(0.06, 0.5, 'Density', ha='center', va='center', rotation='vertical')
        return fig

def plot_histogram(density,x,win_size):
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
            ax[i].tick_params(axis="both", labelsize=8)
            ax[i].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x // win_size} '))
        else:
            ax[i].axis("off") 
    unit_label  = get_unit(win_size)
    fig.supxlabel(f'Position ({unit_label})', fontsize=14)
    fig.supylabel("Variant Count", fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 1])
    return fig