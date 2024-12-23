import argparse

parser = argparse.ArgumentParser(description='VCF visual , a tool to visualize VCF file by user-defined plot type')
parser.add_argument('--vcf_file', type=str, help='the complete path of the VCF file to visualize',required=True)
parser.add_argument('--regions',type=str,help='specific the regions to visualize with bed file')
parser.add_argument('--plot_type',type=str,help='Type of plot to generate')
parser.add_argument('--plot_title',type=str,help='plot title')
parser.add_argument('--plot_path',type=str,help='the path of saving the plot\n')
parser.add_argument('--file_type',type=str,help='file type of the plot\n')
parser.add_argument('--exp',type=str,help='expression to plot',required=True)