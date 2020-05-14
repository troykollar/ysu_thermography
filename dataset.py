import argparse
import cv2
import numpy as np
from helper_functions import printProgressBar


class DataSet:
    def __init__(self,
                 temps_file: str = None,
                 remove_top_reflection=False,
                 remove_bottom_reflection=False,
                 scale_factor=1):

        self.remove_top_reflection = remove_top_reflection
        self.remove_bottom_reflection = remove_bottom_reflection
        self.scale_factor = scale_factor

        # Load thermal cam temp data
        self.temp_fname = temps_file
        self.build_folder = self.get_build_folder()
        self.frame_data = np.load(self.temp_fname,
                                  mmap_mode='r',
                                  allow_pickle=True)
        self.cleaned_frame_data = np.empty(self.frame_data.shape,
                                           dtype=np.float32)

        if self.remove_top_reflection or self.remove_bottom_reflection:
            for i, frame in enumerate(self.frame_data):
                printProgressBar(i, self.frame_data.shape[0],
                                 'Removing reflections...')
                frame = frame.copy()
                if remove_top_reflection:
                    self.remove_top(frame)
                if remove_bottom_reflection:
                    self.remove_bottom(frame)

                self.cleaned_frame_data[i] = frame

        self.shape = self.frame_data.shape

    def __len__(self):
        return len(self.frame_data)

    def __getitem__(self, index: int):
        if self.remove_top_reflection or self.remove_bottom_reflection:
            frame = self.cleaned_frame_data[index]
        else:
            frame = self.frame_data[index]

        if self.scale_factor != 1:
            frame = self.scale_frame(frame)
        return frame

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

    def scale_frame(self, frame: np.ndarray):
        width = int(frame.shape[1] * self.scale_factor)
        height = int(frame.shape[0] * self.scale_factor)
        size = (width, height)
        frame = cv2.resize(frame, size, interpolation=cv2.INTER_LINEAR)
        return frame

    def get_build_folder(self):
        build_folder = self.temp_fname[:self.temp_fname.rfind('/')]
        return build_folder


def get_dataset_CLargs(parser: argparse.ArgumentParser):
    """Add dataset related CL arguments to given parser.

    Added Arguments
    ---------------
    temp_data: required
        filename (and location) of temp data
    top: optional
        0 or 1 specifying whether or not to remove top reflections.
    bot: optional
        0 or 1 specifying whether or not to remove bottom reflections.
    scale: optional
        int specifying the factor to scale frames by.
    """
    parser.add_argument('temp_data',
                        type=str,
                        help='filename (and location) of temp data')
    parser.add_argument(
        '-top',
        type=int,
        default=False,
        help=
        '0 or 1 specifying whether or not to remove top reflections from dataset.'
    )
    parser.add_argument(
        '-bot',
        type=int,
        default=False,
        help=
        '0 or 1 specifying whether or not to remove bottom reflections from dataset.'
    )
    parser.add_argument('-scale',
                        type=int,
                        default=1,
                        help='Factor to scale frames by.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=
        'Run a video of the dataset to ensure it is reading correctly')

    get_dataset_CLargs(parser)

    args = parser.parse_args()
    test_file = args.temp_data
    top = bool(args.top)
    bot = bool(args.bot)
    scale = args.scale

    dset = DataSet(test_file,
                   remove_top_reflection=top,
                   remove_bottom_reflection=bot,
                   scale_factor=scale)
    for frame in dset:
        frame = cv2.normalize(frame, frame, 0, 255, cv2.NORM_MINMAX,
                              cv2.CV_8UC1)
        frame = cv2.applyColorMap(frame, cv2.COLORMAP_INFERNO)
        cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
        cv2.imshow('Frame', frame)
        cv2.waitKey(1)
    cv2.destroyAllWindows()
