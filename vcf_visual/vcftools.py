from cyvcf2 import VCF
import pandas as pd
import pysam
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
    

def process_per_var(v):
    type_set = []
    for i in v : 
        type_set.append(get_var_type(i))
    return type_set

def process_vcf_file_parallel(vcf_file, chunk_size=1000000):
    with pysam.VariantFile(vcf_file) as vcf:
        with ThreadPoolExecutor() as executor:
            vcf_chunk = []
            futures = []
            
            # 遍历 VCF 文件，将记录按块分配给线程处理
            for record in vcf:
                vcf_chunk.append(record)
                if len(vcf_chunk) >= chunk_size:
                    futures.append(executor.submit(process_per_var, vcf_chunk))
                    vcf_chunk = []  # 重置块

            # 如果最后的块不足 `chunk_size`，也要处理
            if vcf_chunk:
                futures.append(executor.submit(process_per_var, vcf_chunk))
            
            # 等待所有线程完成并收集返回的 DataFrame
            all_results = []
            for future in futures:
                all_results.extend(future.result())  # 合并返回的所有类型
            
            return all_results




def get_var_type(variant: pysam.VariantRecord):
    ref = variant.ref
    alts = variant.alts
    Svtype = ["INV","DEL","INS","DUP","CNV"] 
    matching_svtypes = [svtype for svtype in Svtype if svtype in alts[0]]
    if "SVTYPE" in  variant.info or len(matching_svtypes) > 0:
        return variant.info["SVTYPE"] if "SVTYPE" in variant.info else matching_svtypes[0]
    if len(ref) == 1:
        # check the alt allele
        if len(alts[0]) == 1:
            return "SNP"
        else:
            return "INDEL"
    if len(ref) > 1:
        if len(alts[0]) < len(ref):
            return "DEL"
        else:
            return "INS"
    return "OTHER"


process_vcf_file_parallel("/home/fkj/py_project/statvcf-sv/test/data/HG002_GRCh38_TandemRepeats_v1.0.1.vcf.gz")

