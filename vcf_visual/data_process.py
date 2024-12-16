import pandas as pd 
from vcf_visual import plot
from vcf_visual.util.utils import validate_x_keys
from natsort import natsorted
from vcf_visual.plot import *

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
        