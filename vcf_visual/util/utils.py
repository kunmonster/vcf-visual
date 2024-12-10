

def sort_ucsc_chromosomes(chrom_list):
    """ sort the UCSC chromosomes\n
    Args:
        chrom_list: list of chromosomes
    Returns:
        sorted(list): sorted list of chromosomes
    """

    def parse_key(chrom):
        # 去掉 "chr" 前缀，判断内容
        chrom = str(chrom[3:]).lower()
        if chrom.isdigit():
            return (0, int(chrom))  # 数字染色体
        elif chrom == 'x':
            return (1, float('inf'))  # X 染色体
        elif chrom == 'y':
            return (2, float('inf'))  # Y 染色体
        elif chrom == 'm' or chrom == 'mt':
            return (3, float('inf'))  # 线粒体
        else:
            return (4, chrom)  # 其他未识别染色体

    return sorted(chrom_list, key=parse_key)

def sort_nc_chromosomes(chrom_list):
    """ sort the NCBI chromosomes\n
    Args:
        chrom_list: list of chromosomes
    Returns:
        sorted(list): sorted list of chromosomes
    """
    def parse_key(chrom):
        # 去掉 "NC_" 前缀，提取编号和后缀
        main_part, _, version = chrom[3:].partition(".")
        number = int(main_part)  
        return number
    return sorted(chrom_list, key=parse_key)     

def sort_genebank_chromosomes(chrom_list):
    """ sort the GENE_BANK chromosomes\n
    Args:
        chrom_list: list of chromosomes
    Returns:
        sorted(list): sorted list of chromosomes
    """
    def parse_key(chrom):
        # 去掉 "CM" 前缀，提取编号和后缀
        main_part, _, version = chrom[2:].partition(".")
        number = int(main_part)  
        return number
    return sorted(chrom_list, key=parse_key)


def sort_ensembl_chromosomes(chrom_list):
    """ sort the ENSEMBL chromosomes\n
    Args:
        chrom_list: list of chromosomes
    Returns:
        sorted(list): sorted list of chromosomes
    """
    def parse_key(chrom):
        if chrom.isdigit():  # 数字染色体
            return (0, int(chrom))  # 优先级 0，按数字排序
        elif chrom == "X":  # 性染色体 X
            return (1, float('inf'))
        elif chrom == "Y":  # 性染色体 Y
            return (2, float('inf'))
        elif chrom == "MT":  # 线粒体
            return (3, float('inf'))
        else:  # 未分配染色体
            return (4, chrom)  # 按字母排序，放在最后
    return sorted(chrom_list, key=parse_key)


def sort_chromosome(chrom:list):
    """ this function sorts the chromosomes naturally\n
        ensemble chrs: 1,2,3 ... 
        ucsc chrs: chrN ... 
        ncbi chrs: NC_xxxx.x ...
        genebank chrs: CMxxxx.x ...
        
        Args:
            chrom: list of chromosomes
        Returns: 
            sorted(list): sorted list of chromosomes
    """
    if chrom:
        element = str(chrom[0])
        # check the patten of the first element
        if element.startswith("chr"):
            # ucsc style
            chrom = sort_ucsc_chromosomes(chrom)
        elif element.startswith("NC_"):
            # ncbi style
            chrom = sort_nc_chromosomes(chrom)
        elif element.startswith("CM"):
            # genebank style
            chrom = sort_genebank_chromosomes(chrom)
        elif element.isdigit():
            # ensemble style
            chrom = sort_ensembl_chromosomes(chrom)
        else:
            # unknown style
            chrom = sorted(chrom)
        return chrom
    return None