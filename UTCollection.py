import unittest

import SelectTimeseriesUT

if __name__ == "__main__":
    suite = unittest.TestSuite()

    suite.addTest(SelectTimeseriesUT.SelectTimeseriesUT('test_SelectTimeseries_1'))
    suite.addTest(SelectTimeseriesUT.SelectTimeseriesUT('test_SelectTimeseries_2'))

    r = unittest.TextTestRunner()
    r.run(suite)
