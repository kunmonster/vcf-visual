from tkinter import font
import pandas as pd 
from natsort import natsorted
from plot import *

from vcftools import VCFINFO

ALLOWED_VARIABLES = {"CHR", "MAF", "LEN", "AAF", "TYPE", "MISSING_RATE","START"}
SUPPORTED_OPERATIONS = ["count", "sum", "mean", "density","stack","raw"]
PLOT_TYPE={"stack_bar","scatter","density","boxplot","bar","histogram"}


# filter operation for cateogrical and numerical variables


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
        if operation not in SUPPORTED_OPERATIONS:
            raise ValueError(f"operation: '{operation}' is invalid!")
        self.operation_type = operation
    
class PlotType:
    @staticmethod
    def validate_plot_type(plot_type:str,axis:Axis,operation:Operation):
        """this function accept the plot-type from user and check if it is valid
        Args:
            plot_type (str): the plot type from user
            axis (Axis): the axis object
            operation (Operation): the operation object
        """
        if plot_type not in PLOT_TYPE:
            raise ValueError(f"Unsupported plot type: {plot_type}")
        if plot_type == "stack_bar":
            if operation.operation_type != "stack":
                raise ValueError("stack bar plot only support stack operation!")
            if axis.stack is None:
                raise ValueError("stack bar plot need stack variable!")
            if axis.y is not None:
                raise ValueError("stack bar plot doesn't need y variable!")
            if axis.stack_type != "categorical" or axis.x_type != "categorical":
                raise ValueError("stack bar plot only support categorical variable!")
            return "stack_bar"
        
        # scatter plot
        elif plot_type == "scatter":
            if operation.operation_type != "raw":
                raise ValueError("scatter plot only support raw operation!")
            if axis.y is None:
                raise ValueError("scatter plot need y variable!")
            if axis.x_type != "numerical" or axis.y_type != "numerical":
                raise ValueError("scatter plot only support numerical variable!")
            return "scatter"
        
        # histogram plot
        elif plot_type == "histogram":
            if operation.operation_type != "density":
                raise ValueError("histogram plot only support density operation!")
            if axis.y is None:
                raise ValueError("histogram plot need y variable!")
            if axis.x_type != "categorical" or axis.y_type != "numerical":
                raise ValueError("histogram plot only support numerical variable!")
            return "histogram"
        
        # boxplot plot
        elif plot_type == "boxplot":
            if operation.operation_type != "raw":
                raise ValueError("boxplot plot only support raw operation!")
            if axis.y is None:
                raise ValueError("boxplot plot need y variable!")
            if axis.x_type != "categorical" or axis.y_type != "numerical":
                raise ValueError("boxplot plot only support numerical y variable and categorical x variable!")
            return "boxplot"
            
        # bar chart
        elif plot_type == "bar":
            if operation.operation_type == "count":
                if axis.y is not None:
                    raise ValueError("bar plot doesn't need y variable!")
                if axis.x_type != "categorical":
                    raise ValueError("bar plot only support categorical x variable!")
                return "count_bar"
            elif operation.operation_type == "mean":
                if axis.y is None:
                    raise ValueError("mean bar plot need y variable!")
                if axis.x_type != "categorical" or axis.y_type != "numerical":
                    raise ValueError("mean bar plot only support numerical y variable and categorical x variable!")
                return "mean_bar"
            else:
                raise ValueError("UNKNOWN PLOT TYPE!")
            
        elif plot_type == "density":
            if operation.operation_type == "density":
                if axis.x_type == "numerical" and axis.y is None:
                    return "single_ax_density"
                elif axis.x_type == "categorical" and axis.y_type == "numerical":
                    return "multi_ax_density"
                else:
                    raise ValueError("Density plot only support numerical x variable and numerical y variable or categorical y variable!")
            else:
                raise ValueError("Density plot is only supported with 'density' operation.")
        else:
            raise ValueError(f"Unknown plot type: {plot_type}")
        
 

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
        fig.suptitle(f"Stack Bar Plot of {axis.x} by {axis.stack}",fontsize=15)
    elif plot_type == "scatter":
        fig = plot_scatter(data[axis.x],data[axis.y])
        fig.suptitle(f"Scatter Plot of {axis.x} by {axis.y}",fontsize=15)
    elif plot_type == "single_ax_density":
        # just x is numerical and operation is density
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
    
    
def save_fig(fig,save_path):
    fig.tight_layout(rect=[0, 0, 0.98, 0.98])
    fig.savefig(save_path)
    return True 


plot_data = VCFINFO('/home/fkj/py_project/statvcf-sv/tests/data/all_without_bnd.vcf').get_vcf_info()

axis = Axis(x="CHR",y="START")
axis.determine_variable_type(plot_data)
operation = Operation("density")

# plot_type = PlotType.infer_plot_type(axis,operation)
plot_type = PlotType.validate_plot_type("histogram",axis,operation)

fig = data_to_plot(plot_data,axis,operation,plot_type)        
save_fig(fig,"tests/test_pic/test.png")