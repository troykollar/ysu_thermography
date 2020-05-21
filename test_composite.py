import unittest
import numpy as np
from composite import increment_from_thresh
from composite import get_threshold_img, get_max_temp_img
from dataset import DataSet


class TestThresholdIncrementer(unittest.TestCase):
    def test_zero_img_creation(self):
        """Test that a zero image is created properly"""
        dataset = DataSet('test_dataset.npy')

        height = dataset[0].shape[0]
        width = dataset[0].shape[1]

        # Zero image create from np.zeros with datset dimensions
        zero_frame = np.zeros((height, width), dtype=np.float32)

        # Actual zero img of same dimensions as dataset
        theoretical_zero_frame = np.array(
            ([0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]), dtype=np.float32)

        np.testing.assert_array_equal(zero_frame, theoretical_zero_frame)

    def test_increment_from_thresh(self):
        """Test that a threshold image is properly incremented when given a threshold"""
        full_dataset = DataSet('test_dataset.npy')
        data_array = full_dataset[0]
        height = full_dataset[0].shape[0]
        width = data_array.shape[1]
        threshold_img = np.zeros((height, width), dtype=np.float32)

        # Increment threshold_img
        increment_from_thresh(threshold_img, data_array, 3)

        # What threshold_img should be after incrementing
        theoretical_incremented_img = np.array(
            ([0, 0, 1, 0, 0, 0], [1, 1, 1, 0, 1, 1]), dtype=np.float32)
        np.testing.assert_array_equal(threshold_img,
                                      theoretical_incremented_img)

    def test_get_threshold_img(self):
        """Test that a threshold image can be correctly generated"""
        full_dataset = DataSet(temps_file='test_dataset.npy')

        threshold = 3
        threshold_img = get_threshold_img(full_dataset, threshold)
        theoretical_threshold_img = np.array(
            ([0, 0, 5, 0, 0, 0], [5, 5, 5, 0, 5, 5]), dtype=np.float32)
        np.testing.assert_array_equal(threshold_img, theoretical_threshold_img)

    def test_get_max_temp_img(self):
        """Test that a max temp composite can be correctly generated"""
        dataset = DataSet(temps_file='test_dataset.npy')

        max_temp_img = get_max_temp_img(dataset)
        theoretical_max_temp_img = np.array(
            ([1, 1, 5, 1, 1, 1], [5, 5, 5, 1, 5, 5]), dtype=np.float32)
        np.testing.assert_array_equal(max_temp_img, theoretical_max_temp_img)

    def test_avg_temp_img(self):
        """Test that an average temp composite can be correctly generated"""
        dataset = DataSet(temps_file='test_dataset.npy')

        avg_temp_img = get_avg_temp_img(dataset)
        theoretical_avg_temp_img = np.array(
            ([1, 1, 5, 1, 1, 1], [5, 5, 5, 1, 5, 5]), dtype=np.float32)
        np.testing.assert_array_equal(avg_temp_img, theoretical_avg_temp_img)


def create_test_dataset():
    data_frame = np.array(([1, 1, 5, 1, 1, 1], [5, 5, 5, 1, 5, 5]),
                          dtype=np.float32)
    data = np.stack(
        (data_frame, data_frame, data_frame, data_frame, data_frame))

    np.save('test_dataset.npy', data, allow_pickle=True)


if __name__ == '__main__':
    unittest.main()