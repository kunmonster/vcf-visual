from cyvcf2 import VCF
import pandas as pd
import pysam
import numpy as np
from concurrent.futures import ThreadPoolExecutor

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
            if v.is_sv:
                type_set.append(v.INFO.get('SVTYPE'))
                length = v.INFO.get('SVLEN')
                if length is not None:
                    v_len.append(abs(int(length)))
                elif v.INFO.get('SVSIZE') is not None:
                    v_len.append(int(v.INFO.get('SVSIZE')))
                else:
                    v_len.append((int(v.INFO.get('END')) - v.POS))
            elif v.is_indel:
                type_set.append('INDEL')
                v_len.append(0)
            elif v.is_snp:
                type_set.append('SNP')
                v_len.append(1)
            elif v.is_deletion:
                type_set.append('DEL')
                v_len.append(int(v.end) - v.POS)
            elif v.is_transition:
                type_set.append('TRANSITION')
                v_len.append(0)
            else:
                type_set.append('OTHER')
                v_len.append(0)
        vcf_info = pd.DataFrame({'CHR':pd.Series(chr_set, dtype='category'), 
                                 'START':v_start, 
                                 'TYPE':pd.Series(type_set,dtype='category'), 
                                 'LEN':v_len})
        return vcf_info