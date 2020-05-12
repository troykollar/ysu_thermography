import unittest
import numpy as np
from plot_gen import PlotGen


class TestPlotGenMethods(unittest.TestCase):
    def test_validate_start_end_frames_no_input(self):
        test_array = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
        last_frame = test_array.shape[0]
        pg = PlotGen(test_array, None, None)
        self.assertEqual(pg.start_frame, 0)
        self.assertEqual(pg.end_frame, last_frame)

    def test_validate_start_end_frames_invalid_input(self):
        test_array = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
        last_frame = test_array.shape[0]
        pg = PlotGen(test_array, None, None, start_frame=4000, end_frame=78945)
        self.assertEqual(pg.start_frame, 0)
        self.assertEqual(pg.end_frame, last_frame)