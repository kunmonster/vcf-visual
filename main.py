from utils.vcftools import VCFINFO
from utils.visualize import draw_annotation_pie_bar,visual_by_chr,distribution_by_chr,visual_by_var_len
import matplotlib.pyplot as plt
import csv
import pandas as pd

# draw_annotation_pie_bar()

# Vcf =  VCFINFO('/mnt/analysis/map_res/structural_variation/split_single_sample/final_res/chr_X/filtered_chrx.vcf')
# type_numbers(Vcf.get_vcf_info())
Vcf =  VCFINFO('/mnt/analysis/map_res/structural_variation/split_single_sample/final_res/autochr_without_bnd/filtered_missgin_gre_0.1.recode.vcf')

# visual_by_chr(Vcf.get_vcf_info())
# distribution_by_chr(Vcf.get_vcf_info())
visual_by_var_len(Vcf.get_vcf_info())
