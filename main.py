# from vcf_visual.vcftools import VCFINFO
# from vcf_visual.data_process import VCFVISUAL,Axis


# Vcf = VCFINFO('tests/data/all_without_bnd.vcf')
# # VCFVISUAL(Vcf.get_vcf_info(),"x=LEN,y=DENSITY,agg_fun=COUNT").plot()
# Axis(x="CHR",stack="LEN").determine_variable_type(Vcf.get_vcf_info())



if __name__ == "__main__":
    args = parser.parse_args()
    print(args.vcf_file)
    print(args.regions)