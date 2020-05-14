import unittest
import numpy as np
import cv2
from composite import increment_from_thresh
from composite import get_threshold_img
from dataset import DataSet


class TestThresholdIncrementer(unittest.TestCase):
    def test_zero_img_creation(self):
        """Test that a zero image is created properly"""
        data_array = np.array(([1, 1, 5, 1, 5, 1], [5, 5, 1, 5, 1, 5]),
                              dtype=np.float32)
        height = data_array.shape[0]
        width = data_array.shape[1]

        # Zero image create from np.zeros with datset dimensions
        threshold_img = np.zeros((height, width), dtype=np.float32)

        # Actual zero img of same dimensions as dataset
        test_zero_img = np.array(([0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]),
                                 dtype=np.float32)
        np.testing.assert_array_equal(threshold_img, test_zero_img)

    def test_increment_from_thresh(self):
        """Test that a threshold image is properly incremented when given a threshold"""
        data_array = np.array(([1, 1, 5, 1, 5, 1], [5, 5, 1, 5, 1, 5]),
                              dtype=np.float32)
        height = data_array.shape[0]
        width = data_array.shape[1]
        threshold_img = np.zeros((height, width), dtype=np.float32)

        # Increment threshold_img
        increment_from_thresh(threshold_img, data_array, 3)

        # What threshold_img should be after incrementing
        theoretical_incremented_img = np.array(
            ([0, 0, 1, 0, 1, 0], [1, 1, 0, 1, 0, 1]), dtype=np.float32)
        np.testing.assert_array_equal(threshold_img,
                                      theoretical_incremented_img)

    def test_get_threshold_img(self):
        """Test that a threshold image can be correctly generated"""
        data_array1 = np.array(([1, 1, 5, 1, 5, 1], [5, 5, 1, 5, 1, 5]),
                               dtype=np.float32)
        data_array2 = np.array(([1, 1, 5, 1, 5, 1], [5, 5, 1, 5, 1, 5]),
                               dtype=np.float32)
        data_array3 = np.array(([1, 1, 5, 1, 5, 1], [5, 5, 1, 5, 1, 5]),
                               dtype=np.float32)
        full_dataset = np.stack((data_array1, data_array2, data_array3))

        threshold = 3
        threshold_img = get_threshold_img(full_dataset, threshold)
        theoretical_threshold_img = np.array(
            ([0, 0, 3, 0, 3, 0], [3, 3, 0, 3, 0, 3]), dtype=np.float32)
        np.testing.assert_array_equal(threshold_img, theoretical_threshold_img)

    def test_get_threshold_img_with_start_end(self):
        """Test that a threshold image is properly created with a different start and end frame"""
        data_array1 = np.array(([1, 1, 5, 1, 5, 1], [5, 5, 1, 5, 1, 5]),
                               dtype=np.float32)
        data_array2 = np.array(([1, 1, 5, 1, 5, 1], [5, 5, 1, 5, 1, 5]),
                               dtype=np.float32)
        data_array3 = np.array(([1, 1, 5, 1, 5, 1], [5, 5, 1, 5, 1, 5]),
                               dtype=np.float32)
        data_array4 = np.array(([1, 1, 5, 1, 5, 1], [5, 5, 1, 5, 1, 5]),
                               dtype=np.float32)
        data_array5 = np.array(([1, 1, 5, 1, 5, 1], [5, 5, 1, 5, 1, 5]),
                               dtype=np.float32)
        full_dataset = np.stack(
            (data_array1, data_array2, data_array3, data_array4, data_array5))

        threshold = 3
        threshold_img1 = get_threshold_img(full_dataset,
                                           threshold,
                                           start=0,
                                           end=3)
        theoretical_threshold_img1 = np.array(
            ([0, 0, 4, 0, 4, 0], [4, 4, 0, 4, 0, 4]), dtype=np.float32)
        np.testing.assert_array_equal(threshold_img1,
                                      theoretical_threshold_img1)

        threshold_img2 = get_threshold_img(full_dataset,
                                           threshold,
                                           start=3,
                                           end=4)
        theoretical_threshold_img2 = np.array(
            ([0, 0, 2, 0, 2, 0], [2, 2, 0, 2, 0, 2]), dtype=np.float32)
        np.testing.assert_array_equal(threshold_img2,
                                      theoretical_threshold_img2)