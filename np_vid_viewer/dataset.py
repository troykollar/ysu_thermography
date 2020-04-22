import cv2
import numpy as np
import np_vid_viewer
import np_vid_viewer.helper_functions as helpers


class dataset:
    def __init__(self,
                 data_directory: str,
                 remove_top_reflection=False,
                 remove_bottom_reflection=False):

        self.data_directory = data_directory
        self.remove_top_reflection = remove_top_reflection
        self.remove_bottom_reflection = remove_bottom_reflection

        # Load thermal cam temp data
        temp_data_fname = 'thermal_cam_temps.npy'
        self.temp_fname = data_directory + '/' + temp_data_fname
        self.frame_data = np.load(self.temp_fname,
                                  mmap_mode='r',
                                  allow_pickle=True)

        # Save index of last frame
        self.final_frame = self.frame_data.shape[0] - 1

        # Load merged dataset
        merged_data_fname = 'merged_data.npy'
        self.merged_data_fname = self.data_directory + '/' + merged_data_fname
        self.merged_data = np.load(self.merged_data_fname, allow_pickle=True)

        self.build_number = helpers.get_build_number(self.data_directory +
                                                     '/' + temp_data_fname)

    def get_frame(self, frame_num: int, scale_factor=1):
        """Remove reflections if neccesary and scale temperature frame data, then return frame.

        Returns
        -------
        frame : np.ndarray
            Frame data that has been edited, AND scaled.
        unscaled_frame : np.ndarray
            Frame data that has been edited, but not scaled.
        original_frame : np.ndarray
            Frame data of the original temperature data.
        """
        original_frame = self.frame_data[frame_num].copy()
        frame = original_frame

        if self.remove_top_reflection:
            np_vid_viewer.reflection_remover.remove_top(frame)

        if self.remove_bottom_reflection:
            np_vid_viewer.reflection_remover.remove_bottom(frame)

        width = int(frame.shape[1] * scale_factor)
        height = int(frame.shape[0] * scale_factor)
        size = (width, height)

        unscaled_frame = frame
        frame = cv2.resize(frame, size, interpolation=cv2.INTER_LINEAR)
        return frame, unscaled_frame, original_frame

    def get_meltpool_data(self, frame_num: int):
        """Return the data related to the meltpool for the given frame.

        Returns
        -------
        timestamp
            Timestamp of the given frame.
        mp_x
            x coordinate of the the meltpool for the given frame (NaN if not available).
        mp_y
            y coordinate of the the meltpool for the given frame (NaN if not available).
        mp_z
            z coordinate of the the meltpool for the given frame (NaN if not available).
        mp_area
            area of the meltpool for the given frame (NaN if not available).
        """

        timestamp = self.merged_data[frame_num][0]
        mp_x = self.merged_data[frame_num][1]
        mp_y = self.merged_data[frame_num][2]
        mp_z = self.merged_data[frame_num][3]
        mp_area = self.merged_data[frame_num][4]
        return timestamp, mp_x, mp_y, mp_z, mp_area

    def get_max_temp_data(self, frame_num: int):
        """Return data related to the max temperature of the given frame

        Returns
        -------
        max_temp
            Highest temperature of the frame.
        max_temp_x
            x coordinate of the highest temperature of the frame.
        max_temp_y
            x coordinate of the highest temperature of the frame.
        """
        frame = self.frame_data[frame_num]
        max_temp = np.amax(frame)
        max_temp_y = np.where(frame == max_temp)[0][0]
        max_temp_x = np.where(frame == max_temp)[1][0]

        return max_temp, max_temp_x, max_temp_y
