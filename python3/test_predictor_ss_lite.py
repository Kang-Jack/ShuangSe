import unittest
from predictor_ss_lite import predictor_ss

class Duration_Test(unittest.TestCase):
    def setUp(self):
        rs = []
        self.sut = predictor_ss()
        self.sut.init_data()
    def test_random_draw(self):

        self.rs=self.sut.print_random()
        top_line = self.rs[:6]
        bottom_line = self.rs[6:7]
        print (len(str (top_line)))
        print (len(str(bottom_line)))
        self.assertAlmostEqual(len(self.rs), 7)

    def test_format_str_random(self,):
        rs=[11,12,13,14,15,16,17]
        top_line,bottom_line = self.sut.format_str(rs,"RAND")
        print (str (top_line))
        print (str(bottom_line))
        print (len(str (top_line)))
        print (len(str(bottom_line)))
        self.assertTrue(len(top_line)>0 and len(top_line)<17)
        self.assertTrue(len(bottom_line) > 0 and len(bottom_line) < 17)

    def test_format_str_max(self, ):
            rs = [11, 12, 13, 14, 15, 16, 17]
            top_line, bottom_line = self.sut.format_str(rs, "MAX")
            print(str(top_line))
            print(str(bottom_line))
            print(len(str(top_line)))
            print(len(str(bottom_line)))
            self.assertTrue(len(top_line) > 0 and len(top_line) < 17)
            self.assertTrue(len(bottom_line) > 0 and len(bottom_line) < 17)
if __name__ == '__main__':
    unittest.main()