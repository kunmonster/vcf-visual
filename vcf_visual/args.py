import argparse
from vcf_visual.utils import print_var_info
parser = argparse.ArgumentParser(description='VCF visual , a tool to visualize VCF file by user-defined plot type')

parser.add_argument('--support',help='show the supported variables and operations',action='store_true')
parser.add_argument('--vcf_file',type=str, help='[!!!Required!!!]    Specify the complete path of the VCF file to visualize')
parser.add_argument('--regions',type=str,help='specific the regions to visualize with bed file')
parser.add_argument('--plot_type',type=str,help='Type of plot to generate')
parser.add_argument('--plot_title',type=str,help='plot title')
parser.add_argument('--plot_path',type=str,help='the path of saving the plot')
parser.add_argument('--file_type',type=str,help='file type of the plot')
parser.add_argument('--exp',type=str,help='[!!! Required !!!]    expression to plot')