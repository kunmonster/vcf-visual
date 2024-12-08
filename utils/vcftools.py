from cyvcf2 import VCF
import pandas as pd
class VCFINFO:
    def __init__(self, vcf_path):
        self.vcf = VCF(vcf_path)
        self.header = self.vcf.raw_header
        self.samples = self.vcf.samples
    def get_vcf(self):
        return self.vcf
    def get_header(self):
        return self.header
    def get_samples(self):
        return self.samples
    def get_vcf_info(self)->pd.DataFrame:
        chr_set = []
        v_start = []
        type_set = []
        v_len = []
        for v in self.vcf:
            chr_set.append(v.CHROM)
            v_start.append(v.POS)
            type_set.append(v.INFO.get('SVTYPE'))
            length = v.INFO.get('SVLEN')
            if length is not None:
                v_len.append(abs(int(length)))
            else:
                v_len.append(int(v.end) - v.POS)
        vcf_info = pd.DataFrame({'CHR':pd.Series(chr_set, dtype='category'), 
                                 'START':v_start, 
                                 'TYPE':pd.Series(type_set,dtype='category'), 
                                 'LEN':v_len})
        return vcf_info