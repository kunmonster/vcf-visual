from vcf_visual.vcftools import VCFINFO
from vcf_visual.data_process import VCFVISUAL

Vcf = VCFINFO('tests/data/all_without_bnd.vcf')
VCFVISUAL(Vcf.get_vcf_info(),"x=LEN,y=DENSITY,agg_fun=COUNT").plot()