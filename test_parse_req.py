import unittest
from parse_req import parse_req_string 

class TestParseReq(unittest.TestCase):
    
    def test_basic_and(self)
        in_str = "1.00, 1.01, 1.02"

        expected = ReqList(["1.00", "1.01", "1.02"], True)

        assertEqual(expected, parse_req_string(in_str))
        
