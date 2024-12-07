import seaborn as sns
from matplotlib import pyplot as plt, ticker
import pandas as pd
import numpy as np
from matplotlib.patches import ConnectionPatch
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
        plt.savefig('result.png')
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
        bar_colors = ['#925EB0','#A5AEB7','#CC7C71','#7E99F4']
        bottom = np.zeros(len(bar_labels))
        for label,data in bar_data.items():
            ax.bar(bar_labels,data,label=label,bottom=bottom,color=bar_colors.pop(),width=0.5,alpha=0.9)
            bottom += data
        set_ax_title(ax,'Numbers of Every Variant Type in Each Chromosome')
        ax.set_xticklabels(bar_labels,rotation=-75,fontsize=7)
        ax.set_ylabel('Counts')
        ax.set_xlabel('Chromosome')
        ax.legend()
        plt.savefig('result_1.png')

def visual_by_var_len(data):
    '''
    @TODO:以横轴为变异长度,纵轴为变异数量进行可视化,但是只针对结构变异,应在传参前确认是否为结构变异
    '''
    data_by_len = data.groupby('LEN').size().reset_index(name='COUNT')
    sorted_data = data_by_len.sort_values(by='LEN',ascending=True)
    print(sorted_data)





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

    # 显示图形
    plt.savefig('result_2.png')
def get_ration(data):
    total = sum(data)
    return [item / total for item in data] 

def draw_annotation_pie_bar():
    all_data = pd.read_csv('/mnt/analysis/map_res/structural_variation/annotation/final_annotation/annotation_summary.txt',sep='\t',header=None)
    sorted_data = all_data.sort_values(by=[1])
    values = sorted_data[1].tolist()
    labels = sorted_data[0].tolist()

    exnoic_data = pd.read_csv('/mnt/analysis/map_res/structural_variation/annotation/final_annotation/exon_summary_1.txt',sep='\t',header=None)
    sorted_data = exnoic_data.sort_values(by=[1])
    exonic_value = sorted_data[1].tolist()
    exonic_labels = sorted_data[0].tolist()
    print(exonic_labels)
    print(exonic_value)

    tmp_sum = 0
    for i,item in enumerate(values):
        tmp_sum += item
        if i > 5:
            break

    values = values[6:]
    labels = labels[6:]
    values.insert(0,tmp_sum)
    labels.insert(0,'Others')
    sorted_pair = sorted(zip(values,labels),reverse=True)
    values,labels = zip(*sorted_pair)
    explo = [0.01]*len(values)

    explo[-1] = 0.03
    explo[-2] = 0.06
    explo[-3] = 0.09
    explo[-4] = 0.12
    explo[-5] = 0.15
    explo[-6] = 0.18
    explo[-7] = 0.21
    # explo[-8] = 0.24


    total = sum(values)
    label_with_percent = [ f'{label} ({value / total * 100:.2f}%)' for label , value in zip(labels,values)]

    exnoic_values = get_ration(exonic_value)
    bottom = 1
    width = 0.1

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6),dpi=500)
    fig.subplots_adjust(wspace=0)
    wedges, texts =ax1.pie(values,explode=explo,labels=None,\
        rotatelabels=True,\
        startangle=30,\
            colors=['#95a2ff','#ffc076','#fae768','#87e885','#3cb9fc','#73abf5','#cb9bff','#434348','#90ed7d','#f74d4d'])
    
    ax1.legend(label_with_percent,loc='best',bbox_to_anchor=(0, 0.8),fontsize=8)
    wedges[0].set_alpha(0.5)
    wedges[1].set_alpha(0.6)
    wedges[2].set_alpha(0.7)

    print(exnoic_values)
    bar_height = sum(exnoic_values)
   

    for j,(height,label) in enumerate(zip(exnoic_values,exonic_labels)):
        bottom -= height
        bc = ax2.bar(0,height,bottom=bottom,width=width,label=label,color='C0',alpha=0.1 + 0.15 * j)
     # 添加百分比标签到条形右侧，并绘制连线
        base_offset = 0.20  # 基础偏移量
        decrement = 0.04    # 每次递减的偏移量

        # 添加百分比标签到条形右侧，并绘制连线
        percentage = f"{height:.2%}"
        for bar in bc:
            # 计算条形右侧的位置
            bar_x = bar.get_x() + bar.get_width()  # 条形右侧 x 坐标
            bar_y = bottom + height / 2  # 条形中部的 y 坐标
            
            # 动态计算连线终点（距离递减）
            label_x = bar_x + base_offset - j * decrement  # 随 j 递减偏移距离
            label_y = bar_y  # 标签 y 坐标与条形保持一致

            # 在条形右侧添加百分比标签
            ax2.text(label_x, label_y, percentage, 
                    ha='left', va='center', fontsize=6, rotation=0)

            # 绘制从条形右侧到标签的连线
            ax2.annotate('', xy=(label_x, label_y), xytext=(bar_x, bar_y),
                        arrowprops=dict(arrowstyle='-', color='black', lw=0.1))  # 连线样式为黑色细线

        # ax2.bar_label(bc, labels=[f"{height:.2%}"], label_type='center',fontsize=2)
    bar_legend = ax2.legend(bbox_to_anchor=(0.7, 1),fontsize=8,edgecolor='grey',frameon=True)
    bar_legend.get_frame().set_linewidth(0.5)
    ax2.axis('off')
    ax2.set_xlim(- 2.5 * width, 2.5 * width)
    


        # use ConnectionPatch to draw lines between the two plots
    theta1, theta2 = wedges[3].theta1, wedges[3].theta2
    center, r = wedges[3].center, wedges[3].r

    
    # draw top connecting line
    x = r * np.cos(np.pi / 180 * theta2) + center[0]
    y = r * np.sin(np.pi / 180 * theta2) + center[1]
    con = ConnectionPatch(xyA=(-width / 2, bar_height), coordsA=ax2.transData,
                        xyB=(x, y), coordsB=ax1.transData,connectionstyle="arc3")
    con.set_color([0, 0, 0])
    con.set_linewidth(1.5)
    con.set_color('grey')
    con.set_alpha(0.5)
    ax2.add_artist(con)

    # draw bottom connecting line
    x = r * np.cos(np.pi / 180 * theta1) + center[0]
    y = r * np.sin(np.pi / 180 * theta1) + center[1]
    con = ConnectionPatch(xyA=(-width / 2, 0), coordsA=ax2.transData,
                        xyB=(x, y), coordsB=ax1.transData,connectionstyle="arc3")
    con.set_color([0, 0, 0])
    ax2.add_artist(con)
    con.set_linewidth(1.5)
    con.set_color('grey')
    con.set_alpha(0.5)


    plt.tight_layout()

    plt.show()
    plt.savefig('pie_chart.png')
    png1=BytesIO()
    
    png2 = Image.open('pie_chart.png')
    png2.save("pie_chart.tiff")
    png1.close()