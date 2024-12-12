from vcf_visual.vcftools import VCFINFO
from vcf_visual.visualize import visual_by_chr,distribution_by_chr,visual_by_var_len


# draw_annotation_pie_bar()
Vcf = VCFINFO('test/data/HG002_GRCh38_TandemRepeats_v1.0.1.vcf.gz')
# Vcf=VCFINFO('/home/fkj/py_project/statvcf-sv/test/data/bos_taurus_structural_variations.vcf.gz')


visual_by_chr(Vcf.get_vcf_info())
# distribution_by_chr(Vcf.get_vcf_info())
# visual_by_var_len(Vcf.get_vcf_info())
 