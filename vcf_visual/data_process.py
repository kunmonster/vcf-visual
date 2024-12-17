from tarfile import SUPPORTED_TYPES
import pandas as pd 
from vcf_visual import plot
from vcf_visual.util.utils import validate_x_keys
from natsort import natsorted
from vcf_visual.plot import *

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
        pass
    
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
        if operation in SUPPORTED_TYPES:
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
                    return "bar"
                else:
                    raise ValueError("UNKNOWN PLOT TYPE!")
            else:
                raise ValueError("UNKNOWN PLOT TYPE!")        
        else:
            if operation.operation_type == "count":
                if axis.x_type == "categorical":
                    return "bar"
                else:
                    return "density"
            else:
                raise ValueError("UNKNOWN PLOT TYPE!")
            

def prepare_data(data:pd.DataFrame,axis:Axis,operation:Operation,plot_type):
    if plot_type == "stack_bar":
        prepare_data = data.groupby([axis.stack,axis.x]).size().reset_index(name='COUNT')
    elif plot_type == "scatter":
        return data[[axis.x, axis.y]]
    elif plot_type == "density":
        pass
    elif plot_type == "boxplot":
        pass
    elif plot_type == "bar":
        pass
    else: 
        pass


class VCFVISUAL:
    def __init__(self,data:pd.DataFrame,expression:str) -> None:
        self.data = data
        if expression is None or expression == "":
            raise ValueError("expression is empty")
        self.expression = expression


    def parse_expression(self):
        params = {}
        for param in self.expression.split(","):
            key, value = param.split("=")
            params[key.strip()] = value.strip()
        if len(params)  < 2:
            raise ValueError("expression is not enough")
        
        # validate_x_keys(params.keys())
        # checke values
        validate_x_keys(params.values())
        return params

    def prepare_data(self,x,y,agg_fun,stack=None,windows_size = 1000000):
        if stack is not None:
            # groupBy is not none
            grouped_data = self.data.groupby([stack,x]).size().reset_index(name='COUNT')
            bar_labels = natsorted(grouped_data[x].unique())
            stack_labels = sorted(grouped_data[stack].unique())
            bar_data = {}
            for every_stack in stack_labels:
                bar_data[every_stack] = []
                for every_bar in bar_labels:
                    count = grouped_data[(grouped_data[x] == every_bar) & (grouped_data[stack] == every_stack)]['COUNT'].values[0]
                    if count is None:
                        count = 0
                    bar_data[every_stack].append(count)
            bar_data = dict(sorted(bar_data.items(),key=lambda item:sum(item[1])/len(item[1]),reverse=True))
            return (0,bar_labels,bar_data)
        else:
            # stack is False
            if x  not in self.data:
                raise ValueError(f"{x} not found in data")
            
            if agg_fun == "COUNT":
                group_data = self.data.copy()
                plot_data = group_data.groupby(x).size().reset_index(name='COUNT')
                plot_data = plot_data.sort_values(by=x, key=lambda col: natsorted(col.unique()))
                x_data = plot_data[x].unique()
                y_data = plot_data['COUNT']
                return (1,x_data,y_data)
            else:
                if agg_fun == "DENSITY":
                    bin_data = self.data.copy()
                    bin_data["BIN"] = pd.cut(bin_data["START"], bins=range(0, bin_data["START"].max() + windows_size, windows_size), right=False, labels=range(0, bin_data["START"].max() , windows_size))
                    density = bin_data.groupby([x,"BIN"]).size().reset_index(name="COUNT")
                    # density = density.sort_values(by=x, key=lambda col: natsorted(col.unique()))
                    return (2,density,None)
                else:
                    pass

    def plot(self):
        params = self.parse_expression()
        x = params["x"]
        y = params["y"]
        agg_fun = params["agg_fun"]
        stack = params.get("stack",None)
        windows_size = params.get("windows_size",1000000)
        idx,data_1,data_2 = self.prepare_data(x,
                                              y,
                                              agg_fun,
                                              stack,
                                              windows_size)
        
        if idx == 0:
            plot.plot_stack_bar(data_1,data_2)
            pass
        elif idx == 1:
            plot.plot_bar(data_1,data_2)
            pass
        else:
            plot.plot_density(data_1,x,win_size=windows_size)
            pass
        