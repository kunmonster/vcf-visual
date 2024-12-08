from utils.vcftools import VCFINFO
from utils.visualize import visual_by_chr,distribution_by_chr,visual_by_var_len


# draw_annotation_pie_bar()
Vcf = VCFINFO('test/data/bos_taurus_structural_variations.vcf.gz')
# visual_by_chr(Vcf.get_vcf_info())
# distribution_by_chr(Vcf.get_vcf_info())
visual_by_var_len(Vcf.get_vcf_info())
