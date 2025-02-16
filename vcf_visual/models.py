from utils import ALLOWED_VARIABLES,SUPPORTED_OPERATIONS,EXPRESSION_KEYS,PLOT_TYPE

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
        """ this function validate the variable name
        Args:
            var (str): the variable name
            axis_name (str): the axis name
        """
        if var not in ALLOWED_VARIABLES:
            raise ValueError(f"error: {axis_name} variable '{var}' is not allowed!"
                             f" allowed variables:{', '.join(ALLOWED_VARIABLES)}")
    def determine_variable_type(self, data):
        
        """ this function determine the type of x,y and stack variable from the data
        Args:
            data (pd.DataFrame): the data frame
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

class Expression:
    def __init__(self,expression:str) -> None:
        if expression is None or expression == "":
            raise ValueError("empty expression!")
        self.expression = expression
    
    def parse_expression(self):
        """this function parse the expression and return the axis and operation object
        """
        expression_list = self.expression.split(',')
        expression_dict = {}
        for expr in expression_list:
            key, value = expr.split('=')
            if key not in EXPRESSION_KEYS:
                raise ValueError(f"Unsupported expression key: {key}")
            expression_dict[key] = value
        return expression_dict
        
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
        
 