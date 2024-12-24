import unittest
from vcf_visual.vcftools import VCFINFO
from vcf_visual.core import Axis
class TestAxis(unittest.TestCase):
    def setUp(self) -> None:
        print("======test start======")
    def tearDown(self) -> None:
        print("=======test end=======")
    def test_axis_normal_init(self):
        axis = Axis(x="CHR",stack="LEN")
        self.assertEqual(axis.x,"CHR")
        self.assertEqual(axis.y,None)
        self.assertEqual(axis.stack,"LEN")
    def test_axis_validation(self):
        with self.assertRaises(ValueError) as context:
            axis = Axis(x="CHR",y="test",stack="test")
    def test_axis_determine_variable_type(self):
        vcf = VCFINFO('tests/data/all_without_bnd.vcf')
        # with self.assertRaises(ValueError) as context:
        axis = Axis(x="CHR",stack="TYPE")
        axis.determine_variable_type(vcf.get_vcf_info())
        self.assertEqual(axis.x_type,"categorical")
        self.assertEqual(axis.stack_type,"categorical")

        
if __name__ == '__main__':
    unittest.main()