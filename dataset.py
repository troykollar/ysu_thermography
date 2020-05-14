import cv2
import numpy as np
from helper_functions import printProgressBar


class DataSet:
    def __init__(self,
                 temps_file: str,
                 remove_top_reflection=False,
                 remove_bottom_reflection=False,
                 scale_factor=1):

        self.remove_top_reflection = remove_top_reflection
        self.remove_bottom_reflection = remove_bottom_reflection
        self.scale_factor = scale_factor

        # Load thermal cam temp data
        self.temp_fname = temps_file
        self.frame_data = np.load(self.temp_fname,
                                  mmap_mode='r',
                                  allow_pickle=True)
        self.cleaned_frame_data = np.empty(self.frame_data.shape,
                                           dtype=np.float32)

        if remove_top_reflection or remove_bottom_reflection:
            for i, frame in enumerate(self.frame_data):
                printProgressBar(i, self.frame_data.shape[0],
                                 'Removing reflections...')
                frame = frame.copy()
                if remove_top_reflection:
                    self.remove_top(frame)
                if remove_bottom_reflection:
                    self.remove_bottom(frame)
                self.cleaned_frame_data[i] = frame

        # Save index of last frame
        self.final_frame = self.frame_data.shape[0] - 1

    def __len__(self):
        return len(self.frame_data)

    def __getitem__(self, index: int):
        return self.cleaned_frame_data[index]

    def remove_top(self, frame: np.ndarray):
        min_value = 174
        min_value_threshold = 5
        max_value = np.amax(frame)
        max_value_location = np.where(frame == max_value)
        max_value_y = max_value_location[0][0]

        mean = np.mean(frame[max_value_y])
        y = max_value_y
        while mean > min_value + min_value_threshold:
            if y == 0:
                break
            else:
                y -= 1
            mean = np.mean(frame[y])

        frame[:y] = min_value

        # Draw a line at top of piece (for debugging)
        #cv2.line(frame, (0, y), (frame.shape[1], y), int(np.amax(frame)), 1)

    def remove_bottom(self, frame: np.ndarray):
        min_value = 174
        max_value = np.amax(frame)
        max_value_location = np.where(frame == max_value)
        max_value_y = max_value_location[0][0]
        x = max_value_location[1][0]
        last_row_y = frame.shape[0] - 2

        y = max_value_y
        temp = frame[y, x]
        prev_temp = temp

        while y < last_row_y:
            temp = frame[y, x]
            if prev_temp < temp:
                if np.mean(frame[y]) > np.mean(frame[y + 1]):
                    prev_temp = temp
                    y += 1
                else:
                    break
            else:
                prev_temp = temp
                y += 1

        frame[y:] = min_value

        # Draw a line at bottom of piece (for debugging)
        #cv2.line(frame, (0, y), (frame.shape[1], y), int(np.amax(frame)), 1)


if __name__ == '__main__':
    test_file = '/home/troy/thermography/4-20_corrected/thermal_cam_temps.npy'
    dset = DataSet(test_file)
    dset_noRefl = DataSet(test_file,
                          remove_top_reflection=True,
                          remove_bottom_reflection=True)
    for frame in dset_noRefl:
        frame = cv2.normalize(frame, frame, 0, 255, cv2.NORM_MINMAX,
                              cv2.CV_8UC1)
        frame = cv2.applyColorMap(frame, cv2.COLORMAP_INFERNO)
        cv2.imshow('Frame', frame)
        cv2.waitKey(1)
    cv2.destroyAllWindows()
