
from operator import call
import allel

vcf_path = "/home/fkj/py_project/statvcf/example/data/delly_with_duphold.vcf"
vcf_capra_path = "/home/fkj/py_project/statvcf/example/data/capra_hircus.vcf.gz"
vcf_path_a = "/home/fkj/py_project/statvcf/example/data/sample.vcf"

call_set = allel.read_vcf(vcf_path_a,fields="*")
genotypes = allel.GenotypeArray(call_set['calldata/GT'])
missing_data = genotypes.count_missing(axis=1)
print(missing_data[4])

# samples_list = call_set['samples']
# sample_idx = samples_list.tolist().index('C')
# print(sample_idx)
# sample_gts = genotypes[:,sample_idx ,:]
# print(sample_gts)
# print(call_set["variants/REF"].shape)
# print(call_set["variants/ALT"][:20])
 
# call_set = allel.read_vcf(vcf_path_a,fields="*")
# print(call_set.keys())
# print(call_set["variants/REF"])