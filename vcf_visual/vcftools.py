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
    def __init__(self,vcf_path,var_array = "*",sample=None,region=None) -> None:
        self.callset = allel.read_vcf(vcf_path,fields=var_array,samples=sample,region=region)    
        if self.callset == {}:
            raise ValueError("the fileds you specified is not in the vcf file,please check it")
        self.all_keys = self.callset.keys()
        
    def get_allele_freq(self):
        assert 'calldata/GT' in self.all_keys, "please check if the vcf file has 'calldata/GT' field"
        gt = allel.GenotypeArray(self.callset['calldata/GT'])
        allele_count = gt.count_alleles()
        # attention: the frequency will not calculate the missing genotype
        print(allele_count[6])
        return allele_count.to_frequencies()
    
    def get_maf(self):
        allele_freq = self.get_allele_freq()
        return allele_freq.min(axis=1)
    
    def get_missing_rate(self):
        genotypes = allel.GenotypeArray(self.callset['calldata/GT'])
        # get the number of the missing samples
        missing_per_variant = genotypes.count_missing(axis=1)
        n_samples = genotypes.n_samples 
        missing_rate_per_variant = missing_per_variant / n_samples
        return missing_rate_per_variant
    
    # sv about
    def get_sv_type(self):
        assert 'variants/SVTYPE' in self.all_keys, "please check if the vcf file has 'variants/SVTYPE' field"
        return self.callset["variants/SVTYPE"]
    
    def get_sv_len(self):
        ''' get sv length by variants
        return : a list of sv length for each variant
        '''
        assert 'variants/POS', "please check if the vcf file has 'variants/POS' field"
        assert 'variants/END', "please check if the vcf file has 'variants/END' field"
        return self.callset["variants/END"]-self.callset["variants/POS"]
    
    
    def get_var_chr(self):
        assert 'variants/CHROM' in self.all_keys, "please check if the vcf file has 'variants/CHROM' field"
        return self.callset["variants/CHROM"]
    
    def get_var_start(self):
        ''' get the start position of each variant
        return: a list of start position for each variant
        '''
        assert 'variants/POS' in self.all_keys, "please check if the vcf file has 'variants/POS' field"
        return self.callset["variants/POS"]
    def trans_param_to_fileds(self,var_array):
        return var_array

    def get_depth_info(self):
        ''' get the depth info of the vcf file
        return: a list of depth for each sample
        '''
        assert 'variants/DP', "please check if the vcf file has 'INFO/DP' field"
        return self.callset['variants/DP']
    
    
    def get_het(self):
        # TODO等待测试
        ''' get the het by variants
        return: a list of het for each variant
        '''
        assert 'calldata/GT' in self.all_keys, "please check if the vcf file has 'calldata/GT' field"
        gt = allel.GenotypeArray(self.callset['calldata/GT'])
        return gt.count_het(axis=1)
    
    # def get_het_by_sample(self,sample_name):
    #     # TODO等待测试
    #     ''' get the het and hom by sample'''
    #     assert 'calldata/GT' in self.all_keys, "please check if the vcf file has 'calldata/GT' field"
    #     sample_idx = self.callset['samples'].index(sample_name)
    #     if sample_idx is None:
    #         raise ValueError("the sample name you specified is not in the vcf file,please check it")
    #     gt = allel.GenotypeArray(self.callset['calldata/GT'])
    #     return gt.count_het(axis=0)[sample_idx]

    
    
    # SNP about
    def get_snp_type(self):
        '''get snp type 
        return: a list of snp type for each variant
        '''
        assert 'variants/REF' in self.all_keys , "please check if the vcf file has 'variants/REF' field"
        assert 'variants/ALT' in self.all_keys , "please check if the vcf file has 'variants/ALT' field"
        ref = self.callset['variants/REF']
        alt = self.callset['variants/ALT']
        var_type = []
        for ref_str , alt_arr in zip(ref,alt):
            alt_arr = list(filter(None,alt_arr))
            if len(alt_arr) > 1:
                # multi allele
                var_type.append('complex')
            else:
                # just one allele
                if len(ref_str) > len(alt_arr[0]):
                    var_type.append('deletion')
                elif len(ref_str) < len(alt_arr[0]):
                    var_type.append('insertion')
                elif is_transition(ref_str,alt_arr[0]):
                    var_type.append('transition')
                else:
                    var_type.append('transversion')
        return var_type