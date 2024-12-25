import argparse
parser = argparse.ArgumentParser(description='VCF visual , a tool to visualize VCF file by user-defined plot type')

parser.add_argument('--support',help='show the supported variables and operations',action='store_true')


parser.add_argument('--vcf_file',type=str, help='Specify the complete path of the VCF file to visualize [!!!Required!!!]')
parser.add_argument('--exp',type=str,help='expression to plot [!!! Required !!!]')
parser.add_argument('--plot_type',type=str,help='Type of plot to generate [!!! Required !!!]')


parser.add_argument('--plot_title',type=str,help='plot title')
parser.add_argument('--plot_path',type=str,help='the wholepath of saving the plot,carrying the file name and extension')
parser.add_argument('--filter',type=str,help='filter the vcf file')