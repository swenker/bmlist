__author__ = 'samsung'

from bmlist import serviceconfig
import unittest

class TestBmConfig(unittest.TestCase):
    def setUp(self):
        self.bmconfig = serviceconfig.bmconfig

    def test_get_config(self):

        self.assertEqual(self.bmconfig.dbn,"mysql")
        self.assertEqual(self.bmconfig.host,"localhost")
        self.assertEqual(self.bmconfig.db,"bmlist")
        self.assertEqual(self.bmconfig.user,"bmlist")
        self.assertEqual(self.bmconfig.passwd,"bmlist1")

    #@unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    def test_get_logger(self):
        logger = self.bmconfig.getlogger("BmService")
        self.assertTrue(logger)

        logger.info("Hello Python.")

    def tearDown(self):
        self.bmconfig = None


def run_test():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBmConfig)
    unittest.TextTestRunner(verbosity=3).run(suite)


if __name__=="__main__":
    unittest.main()
