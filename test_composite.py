import unittest
import numpy as np
from dataset import DataSet
from composite import ThresholdImg, MaxImg, AvgImg, IntegrationImg

# TODO: Implement more complex test data


class TestThresholdIncrementer(unittest.TestCase):
    def setUp(self):
        self.simple_dataset = DataSet('test_dataset.npy')

    def tearDown(self):
        pass

    def test_threshold_img(self):
        threshold = ThresholdImg(self.simple_dataset, 3)
        theoretical_threshold_img = np.array(
            ([0, 0, 5, 0, 0, 0], [5, 5, 5, 0, 5, 5]), dtype=np.float32)

        np.testing.assert_array_equal(threshold.img, theoretical_threshold_img)

    def test_max_img(self):
        max_img = MaxImg(self.simple_dataset).img
        theoretical_max_img = np.array(
            ([1, 1, 5, 1, 1, 1], [5, 5, 5, 1, 5, 5]), dtype=np.float32)

        np.testing.assert_array_equal(max_img, theoretical_max_img)

    def test_avg_img(self):
        avg_img = AvgImg(self.simple_dataset).img
        theoretical_avg_img = np.array(
            ([1, 1, 5, 1, 1, 1], [5, 5, 5, 1, 5, 5]), dtype=np.float32)

        np.testing.assert_array_equal(avg_img, theoretical_avg_img)

    def test_integration_img(self):
        int_img = IntegrationImg(self.simple_dataset, 3).img
        theoretical_integration_img = np.array(
            ([0, 0, 10, 0, 0, 0], [10, 10, 10, 0, 10, 10]), dtype=np.float32)

        np.testing.assert_array_equal(int_img, theoretical_integration_img)


def create_test_dataset():
    data_frame = np.array(([1, 1, 5, 1, 1, 1], [5, 5, 5, 1, 5, 5]),
                          dtype=np.float32)
    data = np.stack(
        (data_frame, data_frame, data_frame, data_frame, data_frame))

    np.save('test_dataset.npy', data, allow_pickle=True)


if __name__ == '__main__':
    unittest.main()