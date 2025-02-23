
import allel

vcf_path = "/home/fkj/py_project/statvcf-sv/example/data/delly_with_duphold.vcf"
vcf_capra_path = "/home/fkj/py_project/statvcf-sv/example/data/capra_hircus.vcf.gz"
vcf_path_a = "/home/fkj/py_project/statvcf-sv/example/data/sample.vcf"

call_set = allel.read_vcf(vcf_path_a,fields="*")
# print(call_set.keys())
print(call_set["variants/REF"].shape)
print(call_set["variants/ALT"][:20])
 
# call_set = allel.read_vcf(vcf_path_a,fields="*")
# print(call_set.keys())
# print(call_set["variants/REF"])