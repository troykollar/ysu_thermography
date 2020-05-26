"""Functions to generate composite images and videos for thermal data analysis"""
from abc import ABC, abstractmethod
import time
import argparse
import cv2
import numpy as np
import matplotlib.pyplot as plt
from helper_functions import printProgressBar, get_description_dict
from dataset import DataSet, get_dataset_CLargs, validate_range_arg


class Composite(ABC):
    def __init__(self, dataset: DataSet):
        self.dataset = dataset
        self._img = None
        self.plot_title = None
        self.colorbar_label = None
        self.filename = None

    @property
    def img(self):
        if self._img is None:
            self._img = self.get_img()
        return self._img

    def save_img(self):
        fig, ax = plt.subplots()
        fig.suptitle(self.plot_title)
        im = ax.imshow(self.img, cmap='inferno')
        _ = ax.figure.colorbar(im, ax=ax, label=self.colorbar_label)

        plt.savefig(self.filename + '.png')
        plt.imsave(self.filename + '_raw.png', self.img, cmap='inferno')

        plt.close()
        print('Saved to: ' + str(self.filename))

    @abstractmethod
    def get_img(self):
        pass


class Threshold(Composite):
    def __init__(self, dataset: DataSet, threshold: int):
        super().__init__(dataset)
        self.threshold = threshold
        self.plot_title = 'Build: ' + self.dataset.build_folder_name + ' Threshold: ' + str(
            self.threshold)
        self.colorbar_label = '# frames above ' + str(self.threshold)
        self.filename = self.dataset.build_folder + '/' + self.dataset.build_folder_name + '_threshold' + str(
            self.threshold)

    def get_img(self):
        # Get frame size info
        height, width = self.dataset[0].shape[0], self.dataset[0].shape[1]

        # Make blank image to increment
        img = np.zeros((height, width), dtype=np.float32)

        for i, frame in enumerate(self.dataset):
            printProgressBar(i - self.dataset.start_frame,
                             self.dataset.end_frame - self.dataset.start_frame,
                             "Generating threshold image...")
            img = np.where(frame > self.threshold, img + 1, img)

        return img


class MaxImg(Composite):
    def __init__(self, dataset: DataSet):
        super().__init__(dataset)
        self.plot_title = 'Build: ' + self.dataset.build_folder_name + ' Maximum Temperatures'
        self.colorbar_label = 'Temperature (C)'
        self.filename = self.dataset.build_folder + '/' + self.dataset.build_folder_name + '_max_temps'

    def get_img(self):
        # Get frame size info
        height, width = self.dataset[0].shape[0], self.dataset[0].shape[1]

        # Make blank image to update
        max_temp_img = np.zeros((height, width), dtype=np.float32)

        for i, frame in enumerate(self.dataset):
            printProgressBar(i, self.dataset.end_frame,
                             'Creating max temp composite...')
            max_temp_img = np.maximum(max_temp_img, frame)

        return max_temp_img


class Integration(Composite):
    pass


""" Deprecated threshold image functions
def increment_from_thresh(img: np.ndarray, data_frame: np.ndarray,
                          threshold: int):
    over_thresh_array = cv2.threshold(data_frame, threshold, 1,
                                      cv2.THRESH_BINARY)
    over_thresh_array = over_thresh_array[1]
    img += over_thresh_array


def get_threshold_img(dataset: DataSet, threshold: int, cap=None):
    start_time = time.time()
    # Get frame size info
    height = dataset[0].shape[0]
    width = dataset[0].shape[1]

    # Make blank image to increment
    threshold_img = np.zeros((height, width), dtype=np.float32)

    for i, frame in enumerate(dataset):
        printProgressBar(i - dataset.start_frame,
                         dataset.end_frame - dataset.start_frame,
                         "Generating threshold image...")
        frame = dataset[i]
        increment_from_thresh(threshold_img, frame, threshold)

    if cap is not None:
        over_cap = np.where(threshold_img > cap)
        for y, x in zip(over_cap[0], over_cap[1]):
            threshold_img[y, x] = cap

    end_time = time.time()
    print('Og Run time:', end_time - start_time)
    return threshold_img


def save_threshold_img(dataset: DataSet, threshold: int, cap=None):
    img = get_threshold_img(dataset, threshold, cap)
    filename = dataset.build_folder + '/' + dataset.build_folder_name + '_threshold' + str(
        threshold)
    title = 'Build: ' + dataset.build_folder_name + ' Threshold: ' + str(
        threshold)
    colorbar_label = '# frames above ' + str(threshold)
    get_fig(img, title, colorbar_label)

    plt.savefig(filename + '.png')
    plt.imsave(filename + '_raw.png', img, cmap='inferno')

    plt.close()
    print_success_msg(filename)
"""


def get_max_temp_img(dataset: DataSet):
    # Get frame size info
    height = dataset[0].shape[0]
    width = dataset[0].shape[1]

    # Make blank image to update
    max_temp_img = np.zeros((height, width), dtype=np.float32)

    for i, frame in enumerate(dataset):
        printProgressBar(i, dataset.end_frame,
                         'Creating max temp composite...')
        max_temp_img = np.maximum(max_temp_img, frame)

    return max_temp_img


def save_max_temp_img(dataset: DataSet):
    img = get_max_temp_img(dataset)
    filename = dataset.build_folder + '/' + dataset.build_folder_name + '_max_temps'
    title = 'Build: ' + dataset.build_folder_name + ' Maximum temperatures'
    colorbar_label = 'Max temp (C) '
    get_fig(img, title, colorbar_label)

    plt.savefig(filename + '.png')
    plt.imsave(filename + '_raw.png', img, cmap='inferno')

    plt.close()

    print_success_msg(filename)


def get_avg_temp_img(dataset: DataSet):
    # Get frame size info
    height = dataset[0].shape[0]
    width = dataset[0].shape[1]

    # Make blank image to update
    avg_temp_img = np.zeros((height, width), dtype=np.float32)

    num_pixels = (height + 1) * (width + 1)

    cur_pix_num = 0
    for row_num, _ in enumerate(avg_temp_img):
        for col_num, _ in enumerate(avg_temp_img[row_num]):
            printProgressBar(cur_pix_num, num_pixels,
                             'Generating avg temp composite...')
            avg_temp_img[row_num, col_num] = np.mean(dataset[:, row_num,
                                                             col_num])
            cur_pix_num += 1

    return avg_temp_img


def save_avg_temp_img(dataset: DataSet):
    img = get_avg_temp_img(dataset)
    filename = dataset.build_folder + '/' + dataset.build_folder_name + '_avg_temps'
    title = 'Build: ' + dataset.build_folder_name + ' Average temperatures'
    colorbar_label = 'Avg temp (C) '
    get_fig(img, title, colorbar_label)

    plt.savefig(filename + '.png')
    plt.imsave(filename + '_raw.png', img, cmap='inferno')

    plt.close()

    print_success_msg(filename)


def get_fig(img: np.ndarray, title: str, colorbar_label: str):
    fig, ax = plt.subplots()
    fig.suptitle(title)
    im = ax.imshow(img, cmap='inferno')
    _ = ax.figure.colorbar(im, ax=ax, label=colorbar_label)


def print_success_msg(filename):
    print('Saved to: ' + str(filename))


def get_composite_CLargs(parser: argparse.ArgumentParser):
    """Add composite related CL arguments to given parser.

    Added Arguments
    ---------------
    threshold: optional
        int specifying the threshold to be used for the composite image.
    dst_folder: optional
        str specifying where to save the composite image. Defaults to build folder.
    cap: optional
        int specifying the max number of frames to use for composite.
    max: optional
        0 or 1 specifying whether or not to generate a max temperature composite image.
    """
    desc_dict = get_description_dict()
    parser.add_argument('-threshold',
                        type=int,
                        help=desc_dict['threshold'],
                        default=None)
    parser.add_argument('-dst_folder',
                        type=str,
                        default=None,
                        help=desc_dict['thresh_dst_folder'])
    parser.add_argument('-cap', type=int, help=desc_dict['thresh_cap'])
    parser.add_argument('-max',
                        type=int,
                        help=desc_dict['max_temp_composite_CLarg'],
                        default=0)
    parser.add_argument('-avg',
                        type=int,
                        help=desc_dict['avg_composite_CLarg'],
                        default=0)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        description='Generate a composite image.')

    get_dataset_CLargs(arg_parser)
    get_composite_CLargs(arg_parser)

    args = arg_parser.parse_args()

    temp_data = args.temp_data
    top = bool(args.top)
    bot = bool(args.bot)
    composite_threshold = args.threshold

    destination_folder = args.dst_folder
    frame_cap = args.cap

    max_composite = bool(args.max)
    avg_composite = bool(args.avg)

    start_frame, end_frame = validate_range_arg(args.range)

    data_set = DataSet(temp_data,
                       remove_top_reflection=top,
                       remove_bottom_reflection=bot,
                       start_frame=start_frame,
                       end_frame=end_frame)
    if composite_threshold is not None:
        #save_threshold_img(data_set, composite_threshold, frame_cap)
        Threshold(data_set, composite_threshold).save_img()

    if max_composite:
        save_max_temp_img(data_set)

    if avg_composite:
        save_avg_temp_img(data_set)
