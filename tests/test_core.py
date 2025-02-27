import unittest
from vcf_visual.core import get_plot_data

class TestCore(unittest.TestCase):
    def test_plot_data(self):
        vcf_file = "/home/fkj/py_project/statvcf/example/data/delly_with_duphold.vcf"
        x = "CHROM"
        y = "SVTYPE"
        print(get_plot_data(x=x,y=y,vcf_file=vcf_file,sample=["A",'C','B','D']))

if __name__ == '__main__':
    unittest.main()