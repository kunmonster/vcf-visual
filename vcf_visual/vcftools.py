from cyvcf2 import VCF
import allel



transition = {'A':'G','G':'A','C':'T','T':'C'}
transversion = {'A':['C','T'],'G':['C','T'],'C':['A','G'],'T':['A','G']}

def is_transition(ref,alt):
    if alt == transition.get(ref):
        return True
    elif alt in transversion.get(ref):
        return False
    return False

class VCFINFO:
    def __init__(self,vcf_path,var_array = "*") -> None:
        self.callset = allel.read_vcf(vcf_path,fields=var_array)    
        if self.callset == {}:
            raise ValueError("the fileds you specified is not in the vcf file,please check it")
        self.all_keys = self.callset.keys()
        
    def get_allele_freq(self):
        gt = allel.GenotypeArray(self.callset['calldata/GT'])
        allele_count = gt.count_alleles()
        return allele_count.to_frequencies()
    def get_maf(self):
        allele_freq = self.get_allele_freq()
        return allele_freq.min(axis=1)
    def get_var_len(self):
        # 只对SV类型变异有效，对于其他类型变异，返回0
        return self.callset["variants/END"]-self.callset["variants/POS"]
    def get_missing_rate(self):
        genotypes = allel.GenotypeArray(self.callset['calldata/GT'])
        missing_per_variant = genotypes.count_missing(axis=1)
        # 计算总样本数
        n_samples = genotypes.n_samples
        # 计算缺失率（每个位点）
        missing_rate_per_variant = missing_per_variant / n_samples
        return missing_rate_per_variant
    def get_var_type(self):
        # TODO: TYPE只针对结构变异而言的，对于其他类型变异，返回None
        return self.callset["variants/SVTYPE"]
    def get_var_chr(self):
        return self.callset["variants/CHROM"]
    def get_var_start(self):
        return self.callset["variants/POS"]
    def trans_param_to_fileds(self,var_array):
        return var_array
    def get_transition_transversion(self):
        ''' # TODO: 获取变异位点的过渡/颠换比例,针对SNP变异'''
        
        pass
    def get_depth_info(self):
        '''# TODO: 获取深度信息'''
        pass
    def get_het_hom(self):
        '''# TODO: 获取杂合纯合数量'''
        pass
    def get_var_type_info(self):
        '''# TODO: 获取变异类型信息,返回list'''
        assert 'variants/REF' in self.all_keys , "please check if the vcf file has 'variants/REF' field"
        assert 'variants/ALT' in self.all_keys , "please check if the vcf file has 'variants/ALT' field"
        ref = self.callset['variants/REF']
        alt = self.callset['variants/ALT']
        var_type = []
        for item in zip(ref,alt):
            if len(item[1]) > 1:
                # multi allele
                var_type.append('COMPLEX')
            else:
                # just one allele
                if len(item[0]) > len(item[1]):
                    var_type.append('DEL')
                elif len(item[0]) < len(item[1]):
                    var_type.append('INS')
                elif is_transition(item[0],item[1]):
                    var_type.append('TRANSITION')
                else:
                    var_type.append('TRANSVERSION')
        return var_type
    def get_var_info(self):
        pass
    


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