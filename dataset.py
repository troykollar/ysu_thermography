import argparse
import sys
import cv2
import numpy as np
from helper_functions import get_description_dict


class DataSet:
    def __init__(self,
                 temps_file: str,
                 meltpool_data: str = None,
                 remove_top_reflection: bool = False,
                 remove_bottom_reflection: bool = False,
                 scale_factor: int = 1,
                 start_frame: int = -1,
                 end_frame: int = -1):

        self.remove_top_reflection = remove_top_reflection
        self.remove_bottom_reflection = remove_bottom_reflection
        self.scale_factor = scale_factor
        self.contours = []

        # Load thermal cam temp data
        self.temp_fname = temps_file
        self.build_folder = self.get_build_folder()
        self.build_folder_name = self.build_folder[self.build_folder.
                                                   rfind('/') + 1:]
        self.frame_data = np.load(self.temp_fname,
                                  mmap_mode='c',
                                  allow_pickle=True)

        self.meltpool_data = None
        if meltpool_data is not None:
            self.meltpool_data = np.load(meltpool_data, allow_pickle=True)

        self.shape = self.frame_data.shape
        self.original_end_frame = self.frame_data.shape[0]
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.validate_frame_choice()

        self.frame_data = self.frame_data[self.start_frame:self.end_frame]
        if self.meltpool_data is not None:
            self.meltpool_data = self.meltpool_data[self.start_frame:self.
                                                    end_frame + 1]

    def __len__(self):
        return len(self.frame_data)

    def __getitem__(self, index: int):
        return self.clean_frame(index)

    def clean_frame(self, index: int):
        frame = self.frame_data[index]
        if self.remove_top_reflection:
            self.remove_top(frame)
        if self.remove_bottom_reflection:
            self.remove_bottom(frame)
        if self.scale_factor != 1:
            frame = self.scale_frame(frame)
        return frame

    def increase_scale(self, increase: int):
        self.scale_factor += increase

    def remove_top(self, frame: np.ndarray):
        """Attempt to remove reflection from above the piece."""
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
        """Attempt to remove reflection from below the piece."""
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
                    y += 1
                else:
                    break
            else:
                y += 1
            prev_temp = temp

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

    def find_contours(self, frame: np.ndarray, threshold: int):
        thresh_img = cv2.inRange(frame, threshold, int(np.amax(frame)))
        contours, _ = cv2.findContours(thresh_img, cv2.RETR_TREE,
                                       cv2.CHAIN_APPROX_TC89_KCOS)
        self.contours.append(contours)
        return contours

    def get_contour_geometry(self, contours):
        cog_x = None
        cog_y = None
        contour_x = None
        contour_y = None
        contour_w = None
        contour_h = None
        contour_area = None
        contour_moments = None
        if contours is not None:
            for contour in contours:
                contour_x, contour_y, contour_w, contour_h = cv2.boundingRect(
                    contour)
                contour_area = float(cv2.contourArea(contour))
                contour_moments = cv2.moments(contour)
                if contour_moments['m00'] != 0:
                    cog_x = int(contour_moments['m10'] /
                                contour_moments['m00'])
                    cog_y = int(contour_moments['m01'] /
                                contour_moments['m00'])

        geo_dict = {
            'cog_x': cog_x,
            'cog_y': cog_y,
            'x': contour_x,
            'y': contour_y,
            'width': contour_w,
            'height': contour_h,
            'area': contour_area
        }

        return geo_dict

    def get_max_temp(self, frame):
        max_temp = np.amax(frame)
        max_temp_y = np.where(frame == max_temp)[0][0]
        max_temp_x = np.where(frame == max_temp)[1][0]

        return max_temp, (max_temp_x, max_temp_y)

    def get_meltpool_data(self, index: int):
        date_time = self.meltpool_data[index][0]
        formatted_time = str(date_time.month) + '/' + str(
            date_time.day) + ' ' + str(date_time.hour) + ':' + str(
                date_time.minute) + ':' + str(date_time.second)
        meltpool_data = {
            'timestamp': formatted_time,
            'x': self.meltpool_data[index][1],
            'y': self.meltpool_data[index][2],
            'z': self.meltpool_data[index][3],
            'area': self.meltpool_data[index][4],
            'Build:': self.build_folder_name,
            'Max Temp': str(np.amax(self.frame_data[index]))
        }
        return meltpool_data

    def validate_frame_choice(self):
        valid = True
        if self.start_frame <= 0:
            self.start_frame = 0

        if self.end_frame <= 0:
            self.end_frame = self.shape[0]

        if self.end_frame >= self.shape[0]:
            self.end_frame = self.shape[0]

        if self.start_frame > self.end_frame:
            valid = False

        if not valid:
            print('Invalid range of frames.')
            sys.exit()
        else:
            self.shape = self.frame_data[self.start_frame:self.end_frame].shape


def get_dataset_CLargs(parser: argparse.ArgumentParser):
    """Add dataset related CL arguments to given parser.

    Added Arguments
    ---------------
    temp_data: required
        filename (and location) of thermal cam temps file.
    mp_data: optional
        filename (and location) of merged data file.
    top: optional
        0 or 1 specifying whether or not to remove top reflections.
    bot: optional
        0 or 1 specifying whether or not to remove bottom reflections.
    scale: optional
        int specifying the factor to scale frames by.
    range: optional
        start,end specifying frame range to use in dataset.
    """
    desc_dict = get_description_dict()
    parser.add_argument('temp_data', type=str, help=desc_dict['temp_data'])
    parser.add_argument('-top',
                        type=int,
                        default=False,
                        help=desc_dict['remove_top_CLarg'])
    parser.add_argument('-bot',
                        type=int,
                        default=False,
                        help=desc_dict['remove_bot_CLarg'])
    parser.add_argument('-scale',
                        type=int,
                        default=1,
                        help=desc_dict['scale_factor'])
    parser.add_argument('-mp_data',
                        type=str,
                        default=None,
                        help=desc_dict['mp_data'])
    parser.add_argument('-range',
                        default=None,
                        type=str,
                        help=desc_dict['range_CLarg'])


def validate_range_arg(range_arg: str):
    if range_arg is not None:
        comma_index = str(range_arg).find(',')
        if comma_index == -1:
            start_frame = range_arg
            end_frame = -1
        else:
            start_frame = int(range_arg[:comma_index])
            end_frame = int(range_arg[comma_index + 1:])
    else:
        start_frame = -1
        end_frame = -1

    return start_frame, end_frame


if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser(
        description=
        'Run a video of the dataset to ensure it is reading correctly')

    get_dataset_CLargs(argument_parser)

    args = argument_parser.parse_args()
    test_file = args.temp_data
    top = bool(args.top)
    bot = bool(args.bot)
    scale = args.scale

    merged_data = '/media/troy/TroyUSB/thermography/4-20_corrected/merged_data.npy'

    dset = DataSet(test_file,
                   meltpool_data=merged_data,
                   remove_top_reflection=top,
                   remove_bottom_reflection=bot,
                   scale_factor=scale)
    for data_frame in dset:
        data_frame = cv2.normalize(data_frame, data_frame, 0, 255,
                                   cv2.NORM_MINMAX, cv2.CV_8UC1)
        data_frame = cv2.applyColorMap(data_frame, cv2.COLORMAP_INFERNO)
        cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
        cv2.imshow('Frame', data_frame)
        cv2.waitKey(1)
    cv2.destroyAllWindows()
