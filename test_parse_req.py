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
        
    
        self.assertEqual(expected, parse_req_string(in_str))    

    def test_one_multi_or_one_singular_and(self):
        in_str = "18.404, 18.200, or 6.046; 6.046"

        expected = ReqList([ReqList(["18.404", "18.200", "6.046"], False), "6.046"], True)

        self.assertEqual(expected, parse_req_string(in_str))

    def test_one_multi_and_one_multi_or(self):
        in_str = "18.404, 18.200, 6.046; 6.046, or 12.001"

        expected = ReqList([ReqList(["18.404", "18.200", "6.046"], True), ReqList(["6.046", "12.001"], False)], True)
        result = parse_req_string(in_str)

        self.assertEqual(expected, result)

    def test_one_multi_or_with_nested_and(self):
        in_str = "18.404, 6.046, or 12.001 and 12.002"

        expected = ReqList(["18.404", "6.046", ReqList(["12.001", "12.002"], True)], False)
        result = parse_req_string(in_str)

        self.assertEqual(expected, result)

    def test_multi_and_with_permission_of_instructor(self):
        in_str = "6.00, 18.03, 5.12; or permission of instructor"

        expected = ReqList([ReqList(["6.00", "18.03", "5.12"], True), "permission"], False)

        result = parse_req_string(in_str)

        self.assertEqual(expected, result)

    def test_only_with_permission_of_instructor(self):
        in_str = "permission of instructor"

        expected = ReqList(["permission"], False)

        result = parse_req_string(in_str)

        self.assertEqual(expected.items, ["permission"])

        
        



        
if __name__ == '__main__':
    unittest.main()
