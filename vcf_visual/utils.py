from numbers import Number
import time
from rich.console import Console
from rich.table import Table


COMPUTE_FILED = {
    "MAF":'get_maf',
    "AAF":'get_allele_freq',
    "MISSING_RATE":'get_missing_rate',
    "SNPTYPE":'get_snp_type',
    "SVLEN":'get_sv_len'
}

ALLOWED_VARIABLES = {
    "CHROM":'variants/CHROM', 
    "LEN":'variants/SVLEN',
    "START":'variants/POS',
    "FILTER":'variants/FILTER',
    "SVTYPE":'variants/SVTYPE',
    "QUAL":'variants/QUAL',
    "DEPTH":'variants/DP',
    "SVLEN":['variants/POS','variants/END'],
    "MAF":'calldata/GT',
    "AAF":'calldata/GT',
    "MISSING_RATE":'calldata/GT',
    "SNPTYPE":['variants/ALT','variants/REF']
    }

SUPPORTED_OPERATIONS = ["count", "sum", "mean", "density","stack","raw"]

PLOT_TYPE={"stack_bar","scatter","density","boxplot","bar","histogram"}

EXPRESSION_KEYS = {"x","y","stack","operation"}

def check_variable_type(var):
    if var in COMPUTE_FILED.keys():
        return 1
    elif var in ALLOWED_VARIABLES.keys():
        return 0
    else:
        return -1
    
def get_unit(num:Number)->str:
    """
    Get the unit of a number
    """
    if num < 1e3:
        return "bp"
    elif num < 1e6:
        return "Kb"
    elif num < 1e9:
        return "Mb"
    else:
        return "b"


def print_var_info():
    console = Console()
    table_var = Table(title="Variables", title_style="bold cyan")

    table_var.add_column("Supported X or Y ", style="green", justify="left")
    table_var.add_column("Type", style="cyan", justify="left")
    table_var.add_column("Description", style="magenta", justify="left")

    table_var.add_row("CHROM", "category","chromosome")
    table_var.add_row("SVTYPE","category" ,"the type of variation")
    table_var.add_row("START","numeric", "the start position of variation")   
    table_var.add_row("LEN","numeric", "the length of variation , SV length")
    table_var.add_row("AAF", "numeric","alternate allele frequency")
    table_var.add_row("MAF", "numeric","minor allele frequency")
    table_var.add_row("MISSING_RATE","numeric", "the missing rate of variation")
    table_var.add_row("SNPTYPE","category", "the type of snp, such as snp, indel, mnp, etc.")
    
    console.print(table_var)

    table_operation = Table(title="Operations", title_style="bold cyan")
    table_operation.add_column("Operation", style="green", justify="left")
    table_operation.add_column("Description", style="magenta", justify="left")
    table_operation.add_row("count", "count the number of variations")
    table_operation.add_row("sum", "sum the value of a variable")
    table_operation.add_row("mean", "calculate the mean value of a variable")
    table_operation.add_row("density", "calculate the density of a variable")
    table_operation.add_row("stack", "stack the value of a variable")
    table_operation.add_row("raw", "show the raw value of a variable")
    console.print(table_operation)
    
    
    table_plot_type = Table(title="Plot Types", title_style="bold cyan")
    table_plot_type.add_column("Plot Type", style="green", justify="left")
    table_plot_type.add_column("Description", style="magenta", justify="left")
    table_plot_type.add_row("stack_bar", "stack bar plot")
    table_plot_type.add_row("scatter", "scatter plot")
    table_plot_type.add_row("density", "density plot")
    table_plot_type.add_row("boxplot", "boxplot")
    table_plot_type.add_row("bar", "bar plot")
    table_plot_type.add_row("histogram", "histogram")
    console.print(table_plot_type)

    table_match = Table(title="Match", title_style="bold cyan")
    table_match.add_column("Ploy Type", style="green", justify="left")
    table_match.add_column("Operation", style="magenta", justify="left")
    table_match.add_column("Required", style="magenta", justify="left") 
    
    table_match.add_row("stack bar", "stack","x,stack")
    
    table_match.add_row("scatter", "raw","x,y")
    table_match.add_row("boxplot", "raw","x,y")
    table_match.add_row("density", "density","x,y")
    table_match.add_row("bar", "count or mean","x")
    table_match.add_row("histogram", "density","x,y")
    console.print(table_match)
    


def save_fig(fig,save_path,file_type=None):
    """ save the figure to a file in the specified format at the specified path
    Args:
        fig: the figure object to be saved
        save_path: the path to save the figure
        file_type: the format of the saved figure, e.g. "png", "pdf", "svg","tiff"
    return:
        True if the figure is saved successfully
    """
    fig.tight_layout(rect=[0, 0, 0.98, 0.98])
    if file_type is None or file_type.strip() == "":
        fig.savefig(save_path)
    else:
        fig.savefig(save_path, format=file_type)
    return True


def consume_time(func):
    """ A decorator to measure the running time of a function
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"The function {func.__name__} took {end_time - start_time:.2f} seconds to run")
        return result
    return wrapper