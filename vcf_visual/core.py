import sys
from tkinter import ALL
import pandas as pd 
from natsort import natsorted
import matplotlib as mpl
from .vcftools import VCFINFO
from .plot import *
from .models import Axis,Operation,Expression,PlotType
from .utils import COMPUTE_FILED, consume_time, save_fig,ALLOWED_VARIABLES,check_variable_type
from .args import parser
from .utils import print_var_info

def get_plot_data(x,y=None,stack=None,filter_field=None,sample=None,region=None,vcf_file=None):
    # TODO : 实现filter_filed的解析
    vcf_field = []
    base_param = [x,y,stack]
    if filter_field is not None and isinstance(filter_field,list):
        base_param.extend(filter_field)
    for item in base_param:
        if item is None:
            continue
        value = ALLOWED_VARIABLES.get(item)
        if value is None:
            raise ValueError(f"Unsupported variable: {item}")
        elif isinstance(value,str):
            vcf_field.append(value)
        else:
            vcf_field.extend(value)
    
    print("==== start reading vcf file ====")
    vcf_info = VCFINFO(vcf_file,sample=sample,region=region,var_array=vcf_field)
    print("=====   vcf reading done   =====")
    
    if x == None:
        raise ValueError("x is required!")
    x_type = check_variable_type(x)
    if x_type == 0:
        x_data = vcf_info.callset[ALLOWED_VARIABLES[x]]
    else:
        x_data = getattr(vcf_info,COMPUTE_FILED[x])()
    if y != None:
        y_type = check_variable_type(y)
        if y_type == 0:
            y_data = vcf_info.callset[ALLOWED_VARIABLES[y]]
        else:
            y_data = getattr(vcf_info,COMPUTE_FILED[y])()
        return pd.DataFrame({x:x_data,y:y_data})
    if stack != None:
        stack_type = check_variable_type(stack)
        if stack_type == 0:
            print(stack)
            print(ALLOWED_VARIABLES[stack])
            stack_data = vcf_info.callset[ALLOWED_VARIABLES[stack]]
        else:
            stack_data = getattr(vcf_info,COMPUTE_FILED[stack])()
        return pd.DataFrame({x:x_data,stack:stack_data})
    return pd.DataFrame({x:x_data})


def data_to_plot(data:pd.DataFrame,axis:Axis,operation:Operation,plot_type):
    fig = None
    mpl.use("Agg")
    if plot_type == "stack_bar":
        plot_data = data.groupby([axis.stack,axis.x]).size().reset_index(name='COUNT')
        bar_labels = natsorted(plot_data[axis.x].unique())
        stack_labels = sorted(plot_data[axis.stack].unique())
        bar_data = {}
        for every_stack in stack_labels:
            bar_data[every_stack] = []
            for every_bar in bar_labels:
                                
                if plot_data[(plot_data[axis.x] == every_bar)][(plot_data[axis.stack] == every_stack)].empty:
                    count = 0
                else:
                    count = plot_data[(plot_data[axis.x] == every_bar)][(plot_data[axis.stack] == every_stack)]['COUNT'].values[0]
                
                # count = plot_data[(plot_data[axis.x] == every_bar) & (plot_data[axis.stack] == every_stack)]['COUNT'].values[0]
                if count is None:
                    count = 0
                bar_data[every_stack].append(count)
        bar_data = dict(sorted(bar_data.items(),key=lambda item:sum(item[1])/len(item[1]),reverse=True))
        fig = plot_stack_bar(bar_labels,bar_data)
        fig.suptitle(f"Stack Bar Plot of {axis.x} by {axis.stack}",fontsize=15)
    elif plot_type == "scatter":
        fig = plot_scatter(data[axis.x],data[axis.y])
        fig.suptitle(f"Scatter Plot of {axis.x} by {axis.y}",fontsize=15)
    elif plot_type == "single_ax_density":
        # just x is numerical and operation is density
        print(data[axis.x].shape)
        plot_data = data[axis.x].values.reshape(-1, 1)
        
        fig = plot_density(plot_data)
    elif plot_type == "multi_ax_density": 
        plot_data = data.groupby(axis.x)[axis.y].apply(list).reset_index(name='DENSITY')
        
        fig = plot_density(plot_data,axis = axis)
        fig.suptitle(f'Density Plot of {axis.y} by {axis.x}',fontsize=15)
    elif plot_type == "boxplot":
        sorted_key = natsorted(data[axis.x].unique())
        sorted_data = data.set_index(axis.x).loc[sorted_key]
        plot_data = [group[axis.y].dropna().to_list() for _,group in sorted_data.groupby(axis.x)]
        fig = plot_boxplot(sorted_key,plot_data)
        fig.suptitle(f'Boxplot of {axis.y} by {axis.x}',fontsize=15)
    elif plot_type == "count_bar":
        sorted_key = natsorted(data[axis.x].unique())
        sorted_data = data.set_index(axis.x).loc[sorted_key]
        plot_data = sorted_data.groupby(axis.x).size().reset_index(name='COUNT')
        fig = plot_bar(sorted_key,plot_data['COUNT'])
        fig.suptitle(f'Count by {axis.x}',fontsize=15)
    elif plot_type == "mean_bar":
        sorted_key = natsorted(data[axis.x].unique())
        sorted_data = data.set_index(axis.x).loc[sorted_key]
        plot_data = sorted_data.groupby(axis.x)[axis.y].mean().reset_index(name='MEAN')
        fig = plot_bar(sorted_key,plot_data['MEAN'])
        fig.suptitle(f'Mean of {axis.y} by {axis.x}',fontsize=15)
    elif plot_type == "histogram":
        data["BIN"] = pd.cut(data[axis.y], bins=range(0, data[axis.y].max() + 1_000_000, 1_000_000), right=False, labels=range(0, data[axis.y].max(), 1_000_000))
        density = data.groupby(["CHR", "BIN"]).size().reset_index(name="COUNT")
        fig = plot_histogram(density,axis.x,1_000_000)
        fig.suptitle(f'Distribution by {axis.x}',fontsize=15)
    else :
        raise ValueError(f"Unsupported plot type: {plot_type}")
    return fig

@consume_time
def plot_save(vcf_file:str,exp:str,plot_path:str,plot_type:str,plot_title:str=None,file_type:str=None):
    if plot_type is None:
        raise ValueError("plot type is required!")
    exp_class = Expression(exp)
    params  = exp_class.parse_expression()
    x = params.get("x")
    y = params.get("y")
    
    stack = params.get("stack")
    operation = Operation(params.get("operation"))
    axis = Axis(x=x,y=y,stack=stack)
    
    
    # TODO: 解析filter表达式
    
    
    plot_data = get_plot_data(x,y,vcf_file=vcf_file,stack=stack)

    axis.determine_variable_type(plot_data)
    plot_type = PlotType.validate_plot_type(plot_type,axis,operation)
    fig = data_to_plot(plot_data,axis,operation,plot_type)  
    if plot_title is not None:
        fig.suptitle(plot_title,fontsize=15)
    save_fig(fig,plot_path)
    

def main_fun(argv):
    if argv is None or len(argv) == 0:
        parser.print_help()
        sys.exit(1)
    params, _ = parser.parse_known_args(argv)
    # 检查是否提供 --help
    if params.support:
        print_var_info()
        sys.exit(0)
    if "file_type"  not in params:
        params.file_type = None
    
    try:
        plot_save(params.vcf_file,params.exp,params.plot_path,params.plot_type,params.plot_title,params.file_type)
    except Exception as e:
         print(f"Error: {e}")
         sys.exit(1)
        
        
