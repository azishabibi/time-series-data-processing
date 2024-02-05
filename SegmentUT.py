import unittest
from FlokAlgorithmLocal import FlokDataFrame, FlokAlgorithmLocal
from SelectTimeseries import SelectTimeseries
from Segment import Segment


class SegmentUT(unittest.TestCase):

    def setUp(self):
        input_paths = ["root_test_d1"]
        input_types = ["csv"]
        input_location = ["local_fs"]
        output_paths = ["root_test_d1_out.csv"]
        output_types = ["csv"]
        self.dataset_ = FlokAlgorithmLocal().read(
            input_paths, input_types, input_location, output_paths, output_types)
        self.algorithm = Segment()

    def test_segment_1(self):
        self.timeseries = {"timeseries": "Time,s2"}
        self.params = {'output': 'first', 'error': 0.1}

    def test_segment_2(self):
        self.timeseries = {"timeseries": "Time,s2"}
        self.params = {'output': 'all', 'error': 1}

    def tearDown(self):
        dataset = SelectTimeseries().run(self.dataset_, self.timeseries)
        result = self.algorithm.run(dataset, self.params)
        print(result.get(0))


if __name__ == "__main__":
    unittest.main()
