import array
import unittest

from vcf_visual.vcftools import VCFINFO

class TestVcftools(unittest.TestCase):
    
    def test_var_type_transition(self):
        vcfinfo = VCFINFO("/home/fkj/py_project/statvcf/example/data/sample.vcf")
        arr = vcfinfo.get_var_type_info()
        
        # A-->G
        self.assertEqual(arr[0], "transition")
        # G-->A 
        self.assertEqual(arr[1], "transition")
        # C-->T
        self.assertEqual(arr[2], "transition")
        # T-->C
        self.assertEqual(arr[3], "transition")
    
    def test_var_type_transversion(self):
        vcfinfo = VCFINFO("/home/fkj/py_project/statvcf/example/data/sample.vcf")
        arr = vcfinfo.get_var_type_info()
        # A-->C
        self.assertEqual(arr[4], "transversion")
        # A-->T
        self.assertEqual(arr[5], "transversion")
        # G-->C
        self.assertEqual(arr[6], "transversion")
        # G-->T
        self.assertEqual(arr[7], "transversion")
        # C-->A
        self.assertEqual(arr[8], "transversion")
        # C-->G
        self.assertEqual(arr[9], "transversion")
        # T-->A
        self.assertEqual(arr[10], "transversion")
        # T-->G
        self.assertEqual(arr[11], "transversion")
    
    def test_var_type_complex(self):
        vcf_info = VCFINFO("/home/fkj/py_project/statvcf/example/data/sample.vcf")
        arr = vcf_info.get_var_type_info()
        # A-->G,A
        self.assertEqual(arr[12], "complex")
        # A-->A,GC,C
        self.assertEqual(arr[13], "complex")
    
    def test_var_type_deletion(self):
        vcf_info = VCFINFO("/home/fkj/py_project/statvcf/example/data/sample.vcf")
        arr = vcf_info.get_var_type_info()
        
        #AG --> A
        self.assertEqual(arr[14], "deletion")
        #AGT --> A
        self.assertEqual(arr[15], "deletion")
        #AGTCA --> AG
        self.assertEqual(arr[16], "deletion")
        
    def test_var_type_insertion(self):
        vcf_info = VCFINFO("/home/fkj/py_project/statvcf/example/data/sample.vcf")
        arr = vcf_info.get_var_type_info()
        
        #A --> AG
        self.assertEqual(arr[17], "insertion")
        #AG --> AGT
        self.assertEqual(arr[18], "insertion")
        #AGT --> AGATC
        self.assertEqual(arr[19], "insertion")
        # AGT-->AGGATA
        self.assertEqual(arr[20], "insertion")
        

if __name__ == '__main__':
    unittest.main()
