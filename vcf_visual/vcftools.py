from cyvcf2 import VCF
import pandas as pd
import allel

class VCFINFO:
    def __init__(self,vcf_path,var_array=[]) -> None:
        self.callset = allel.read_vcf(vcf_path,fields=var_array)
        if self.callset == {}:
            raise ValueError("the fileds you specified is not in the vcf file,please check it")
        pass
    def get_allele_freq(self):
        gt = allel.GenotypeArray(self.callset['calldata/GT'])
        allele_count = gt.count_alleles()
        return allele_count.to_frequencies()
    def get_maf(self):
        allele_freq = self.get_allele_freq()
        return allele_freq.min(axis=1)
    def get_var_len(self):
        pass
    def get_missing_rate(self):
        genotypes = allel.GenotypeArray(self.callset['calldata/GT'])

        missing_per_variant = genotypes.is_missing().sum(axis=1)
        # 计算总样本数
        n_samples = genotypes.n_samples
        # 计算缺失率（每个位点）
        missing_rate_per_variant = missing_per_variant / n_samples
        return missing_rate_per_variant
    def get_var_type(self):
        pass
    def get_var_chr(self):
        return self.callset["variants/CHROM"]
    def get_var_start(self):
        return self.callset["variants/POS"]
        


# class VCFINFO:
#     def __init__(self, vcf_path):
#         self.vcf = VCF(vcf_path,gts012=True)
#         self.header = self.vcf.raw_header
#         self.samples = self.vcf.samples
#     def get_vcf(self):
#         return self.vcf
#     def get_header(self):
#         return self.header
#     def get_samples(self):
#         return self.samples
#     def get_vcf_info(self)->pd.DataFrame:
#         chr_set = []
#         v_start = []
#         type_set = []
#         v_len = []
#         maf = []
#         aaf = []
#         missing_rate = []
#         for v in self.vcf:
#             chr_set.append(v.CHROM)
#             v_start.append(v.POS)
#             maf.append(min(v.aaf,1-v.aaf))
#             aaf.append(v.aaf)
#             if v.call_rate is not None:
#                 missing_rate.append((1-v.call_rate))
#             if v.is_sv:
#                 type_set.append(v.INFO.get('SVTYPE'))
#                 length = v.INFO.get('SVLEN')
#                 if length is not None:
#                     v_len.append(abs(int(length)))
#                 elif v.INFO.get('SVSIZE') is not None:
#                     v_len.append(int(v.INFO.get('SVSIZE')))
#                 else:
#                     v_len.append((int(v.INFO.get('END')) - v.POS))
#             elif v.is_indel:
#                 type_set.append('INDEL')
#                 v_len.append(0)
#             elif v.is_snp:
#                 type_set.append('SNP')
#                 v_len.append(1)
#             elif v.is_deletion:
#                 type_set.append('DEL')
#                 v_len.append(int(v.end) - v.POS)
#             elif v.is_transition:
#                 type_set.append('TRANSITION')
#                 v_len.append(0)
#             else:
#                 type_set.append('OTHER')
#                 v_len.append(0)
        
#         vcf_info = pd.DataFrame({'CHR':pd.Series(chr_set, dtype='category'), 
#                                  'START':v_start, 
#                                  'TYPE':pd.Series(type_set,dtype='category'),
#                                  'LEN':v_len,
#                                  'MAF':maf,
#                                  'AAF':aaf,
                                 
#                                  })
#         # breakpoint()
#         return vcf_info