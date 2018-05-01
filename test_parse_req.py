import unittest
from parse_req import parse_req_string 
from prereqDataParser import ReqList
import pdb

class TestParseReq(unittest.TestCase):
    
    def test_basic_and(self):
        in_str = "1.00, 1.01, 1.02"

        expected = ReqList(["1.00", "1.01", "1.02"], True)
       
        self.assertEqual(expected, parse_req_string(in_str))

    def test_basic_or(self):
        in_str = "1.00, 2.00C, or 6.006"

        expected = ReqList(["1.00", "2.00C", "6.006"], False)
        result = parse_req_string(in_str)
        
    
        print(expected)
        print(result)
        self.assertEqual(expected, parse_req_string(in_str))    

    def test_one_multi_or_one_singular_and(self):
        in_str = "18.404, 18.200, or 6.046; 6.046"

        expected = ReqList([ReqList(["18.404", "18.200", "6.046"], False), "6.046"], True)

        self.assertEqual(expected, parse_req_string(in_str))
        


        
if __name__ == '__main__':
    unittest.main()
