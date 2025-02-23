import unittest

from vcf_visual.vcftools import VCFINFO

class TestVcftools(unittest.TestCase):
    def test_get_var_type(self):
        vcfinfo = VCFINFO("/home/fkj/py_project/statvcf-sv/example/data/sample.vcf")
        arr = vcfinfo.get_var_type_info()
        self.assertEqual(arr[0], "TRANSVERSION")
        self.assertEqual(arr[3], "DEL")
if __name__ == '__main__':
    unittest.main()
