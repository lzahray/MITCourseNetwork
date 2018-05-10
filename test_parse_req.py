import unittest
from parse_req import parse_req_string
from prereqDataParser import ReqList
import pdb

class TestParseReq(unittest.TestCase):

    def test_basic_and(self):
        in_str = "1.00, 1.01, 1.02"

        expected = ReqList(["1.00", "1.01", "1.02"], True)

        self.assertEqual(expected, parse_req_string(in_str))

    def test_basic_or_with_oxford_comma(self):
        in_str = "1.00, 2.00C, or 6.006"

        expected = ReqList(["1.00", "2.00C", "6.006"], False)
        result = parse_req_string(in_str)


        self.assertEqual(expected, parse_req_string(in_str))

    def test_basic_or_without_oxford_comma(self):
        in_str = "1.00, 2.00C or 6.006"

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

        self.assertEqual(expected, result)

    def test_binary_or_no_comma(self):
        in_str = "12.001 or 12.002"

        expected = ReqList(["12.001", "12.002"], False)

        result = parse_req_string(in_str)

        self.assertEqual(expected, result)

    def test_comma_clause_with_perm_and_with_binary_and(self):
        in_str = "2.006, or 2.041 and 2.06, or permission of instructor"

        expected = ReqList(["2.006", ReqList(["2.041", "2.06"], True), "permission"], False)

        result = parse_req_string(in_str)

        self.assertEqual(expected, result)

    def test_2_clauses_one_singleton_one_implicit_and(self):
        in_str = "2.005; or 2.051, 2.06"

        expected = ReqList(["2.005", ReqList(["2.051", "2.06"], True)], False)

        result = parse_req_string(in_str)

        self.assertEqual(expected, result)

    def test_2_clauses_binary_or_and_singleton_gir(self):
        in_str = "18.03 or 18.032; GIR:PHY2"

        expected = ReqList([ReqList(["18.03", "18.032"], False), "GIR:PHY2"], True)

        result = parse_req_string(in_str)

        self.assertEqual(expected, result)

if __name__ == '__main__':
    unittest.main()
