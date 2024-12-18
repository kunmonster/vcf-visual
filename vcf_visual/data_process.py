import pandas as pd 
from natsort import natsorted
from plot import *

from vcftools import VCFINFO

ALLOWED_VARIABLES = {"CHR", "MAF", "LEN", "AAF", "TYPE", "MISSING_RATE"}
SUPPORTED_OPERATIONS = ["count", "sum", "mean", "density"]

class Axis:
    def __init__(self,x,y=None,stack=None) -> None:
        self.x = x
        self.y = y
        self.stack = stack
        self.x_type = None
        self.y_type = None
        self.stack_type = None
        self.validate_variable(self.x, "X")
        if self.y:
            self.validate_variable(self.y, "Y")
        if self.stack:
            self.validate_variable(self.stack, "Stack")
    
    def validate_variable(self, var, axis_name):
        """
        校验变量是否在允许范围内
        """
        if var not in ALLOWED_VARIABLES:
            raise ValueError(f"错误：{axis_name} 轴变量 '{var}' 不在允许的变量范围内！"
                             f" 允许的变量有：{', '.join(ALLOWED_VARIABLES)}")
    def determine_variable_type(self, data):
        
        """
        判断变量是分类还是连续类型
        """
        if self.x is None:
            raise ValueError("empty x axis!")
        if self.stack is not None and self.y is not None:
            raise ValueError("if you want to stack, y axis should be None!")
        
        self.x_type = "categorical" if data[self.x].dtype == "object" or data[self.x].dtype == "category" else "numerical"
        if self.y:
            self.y_type = "categorical" if data[self.y].dtype == "object" or data[self.y].dtype == "category" else "numerical"
            return
        if self.stack:
            self.stack_type = "categorical" if data[self.stack].dtype == "object" or data[self.stack].dtype == "category" else "numerical"
            if self.stack_type != "categorical":
                raise ValueError(f"error: stack variable '{self.stack}' must be categorical!")
            if self.stack_type == "categorical" and self.x_type != "categorical":
                raise ValueError(f"error: stack variable '{self.stack}' is categorical,but x '{self.x}' is not categorical!")


class Operation:
    def __init__(self,operation:str) -> None:
        if operation in SUPPORTED_OPERATIONS:
            raise ValueError(f"operation: '{operation}' is invalid!")
        self.operation_type = operation
    
class PlotType:
    @staticmethod
    def infer_plot_type(axis:Axis,operation:Operation):
          # axis检验已经在上级方法中完成
        if axis.stack is not None:
            return "stack_bar"
        if axis.y is not None:
            if operation.operation_type == "raw":
                if axis.y_type == "numerical" and axis.x_type == "numerical":
                    return "scatter"
                elif axis.x_type == "categorical" and axis.y_type == "numerical":
                    return "boxplot"
                else:
                    raise ValueError("UNKNOWN PLOT TYPE!")
            elif operation.operation_type == "mean":
                if axis.x_type == "categorical" and axis.y_type == "numerical":
                    return "mean_bar"
                else:
                    raise ValueError("UNKNOWN PLOT TYPE!")
            elif operation.operation_type == "density":
                # this situation is fit to multi-ax
                if axis.x_type == "categorical" and axis.y_type == "numerical":
                    return "multi_ax_density"
            else:
                raise ValueError("UNKNOWN PLOT TYPE!")        
        else:
            if operation.operation_type == "count" and axis.x_type == "categorical":
                return "count_bar"
            elif operation.operation_type == "density" and axis.x_type == "numerical":
                return "single_ax_density"
            else:
                raise ValueError("UNKNOWN PLOT TYPE!")
        

def data_to_plot(data:pd.DataFrame,axis:Axis,operation:Operation,plot_type):
    fig = None
    if plot_type == "stack_bar":
        plot_data = data.groupby([axis.stack,axis.x]).size().reset_index(name='COUNT')
        bar_labels = natsorted(plot_data[axis.x].unique())
        stack_labels = sorted(plot_data[axis.stack].unique())
        bar_data = {}
        for every_stack in stack_labels:
            bar_data[every_stack] = []
            for every_bar in bar_labels:
                count = plot_data[(plot_data[axis.x] == every_bar) & (plot_data[axis.stack] == every_stack)]['COUNT'].values[0]
                if count is None:
                    count = 0
                bar_data[every_stack].append(count)
        bar_data = dict(sorted(bar_data.items(),key=lambda item:sum(item[1])/len(item[1]),reverse=True))
        fig = plot_stack_bar(bar_labels,bar_data)
    elif plot_type == "scatter":
        fig = plot_scatter(data[axis.x],data[axis.y])
    elif plot_type == "single_ax_density":
        # just x is numerical and operation is density
        plot_data = data[axis.x].values.reshape(-1, 1)
        fig = plot_density(plot_data)
    elif plot_type == "multi_ax_density": 
        plot_data = data.groupby(axis.x)[axis.y].apply(list)
        fig = plot_density(plot_data,axis = axis)
    elif plot_type == "boxplot":
        sorted_key = natsorted(data[axis.x].unique())
        sorted_data = data.set_index(axis.x).loc[sorted_key]
        plot_data = [group[axis.y].dropna().to_list() for _,group in sorted_data.groupby(axis.x)]
        fig = plot_boxplot(sorted_key,plot_data)
    elif plot_type == "count_bar":
        sorted_key = natsorted(data[axis.x].unique())
        sorted_data = data.set_index(axis.x).loc[sorted_key]
        plot_data = sorted_data.groupby(axis.x).size().reset_index(name='COUNT')
        plot_bar(sorted_key,plot_data['COUNT'])
    elif plot_type == "mean_bar":
        sorted_key = natsorted(data[axis.x].unique())
        sorted_data = data.set_index(axis.x).loc[sorted_key]
        plot_data = sorted_data.groupby(axis.x)[axis.y].mean().reset_index(name='MEAN')
        plot_bar(sorted_key,plot_data['MEAN'])
    else :
        raise ValueError(f"Unsupported plot type: {plot_type}")
    return fig
    
    
def save_fig(fig,save_path):
    fig.savefig(save_path)
    return True


plot_data = VCFINFO('tests/data/all_without_bnd.vcf').get_vcf_info()

axis = Axis(x="LEN",y="MISSING_RATE")
axis.determine_variable_type(plot_data)
operation = Operation("raw")

plot_type = PlotType.infer_plot_type(axis,operation)

fig = data_to_plot(plot_data,axis,operation,plot_type)
save_fig(fig,"tests/test_pic/test.png")