import os
import shutil
import argparse
import cv2
import numpy as np
import matplotlib.pyplot as plt
from dataset import DataSet, get_dataset_CLargs
from helper_functions import printProgressBar


class Viewer:
    def __init__(self, dataset: DataSet, contour_threshold: int = None):
        self.dataset = dataset
        self.quit = False
        self.cur_frame = None
        self.pause = False
        self.update_frame = True
        self.contour_threshold = contour_threshold

    def play_video(self):
        window_name = self.dataset.build_folder
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        self.cur_frame = 0
        while not self.quit:
            if self.update_frame:
                frame = self.dataset[self.cur_frame]
                frame = self.colormap_frame(frame)
                if self.contour_threshold is not None:
                    frame = self.draw_contour(self.cur_frame, frame,
                                              self.contour_threshold)
            if self.quit:
                break
            cv2.imshow(window_name, frame)
            if not self.pause:
                self.advance_frame(1)
            else:
                self.update_frame = False
            key = cv2.waitKey(1) & 0xFF
            self.key_handler(key)
        cv2.destroyAllWindows()

    def colormap_frame(self, frame):
        frame = cv2.normalize(frame,
                              frame,
                              0,
                              255,
                              cv2.NORM_MINMAX,
                              dtype=cv2.CV_8UC1)
        frame = cv2.applyColorMap(frame, cv2.COLORMAP_INFERNO)
        return frame

    def save_frame16(self, start: int, end=-1):
        # TODO: Add frame choice validation
        # Save only one frame
        if end < 0:
            savename = self.dataset.build_folder + '/frame' + str(
                start) + '.png'
            plt.imsave(savename, dataset[start], cmap='inferno')
            print('Saved to: ' + savename)
        else:
            # Create folder to save frames in
            frame_range_folder = self.dataset.build_folder + '/frames' + str(
                start) + '-' + str(end - 1)

            if os.path.isdir(frame_range_folder):
                shutil.rmtree(frame_range_folder)
            os.mkdir(frame_range_folder)

            for i in range(start, end):
                printProgressBar(
                    i - start, end - start,
                    'Saving frame range ' + str(start) + '-' + str(end))
                savename = frame_range_folder + '/frame' + str(i) + '.png'
                plt.imsave(savename, self.dataset[i], cmap='inferno')
            print('Frame range saved in: ' + frame_range_folder)

    def key_handler(self, key):
        # TODO: Add ability to jump forward and back different amounts of frames
        if key == ord('q'):
            self.quit = True
        elif key == ord('s'):
            self.save_frame16(self.cur_frame)
        elif key == ord('p') or key == 32 or key == ord('k'):
            self.pause = not self.pause
        elif key == ord('l'):
            self.advance_frame(10)
        elif key == ord('j'):
            self.rewind_frame(10)
        else:
            pass

    def advance_frame(self, advancement: int):
        if self.cur_frame + advancement >= self.dataset.shape[0] - 1:
            self.cur_frame = self.dataset.shape[0] - 1
        else:
            self.cur_frame += advancement

        self.update_frame = True

    def rewind_frame(self, rewind_amount: int):
        if self.cur_frame - rewind_amount <= 0:
            self.cur_frame = 0
        else:
            self.cur_frame -= rewind_amount

        self.update_frame = True

    def draw_contour(self, frame_index: int, colormapped_frame: np.ndarray,
                     contour_threshold: int):
        frame = self.dataset[frame_index]
        contours = self.dataset.find_contours(frame, contour_threshold)
        colormapped_frame = cv2.drawContours(colormapped_frame, contours, -1,
                                             (0, 255, 0), 1)
        return colormapped_frame

    def add_info_pane(self):
        # TODO: Add info pane function
        pass


def get_viewer_CLargs(parser: argparse.ArgumentParser):
    """Add viewer related CL arguments to given parser

    Added Arguments
    ---------------
    play: optional
        Play the video using OpenCV.
    frame: optional
        int specifying a frame to save in 16 bit color using matplotlib.
    framerange: optional
        start,end specifying frame range to save in 16 bit color using matplotlib.
    contour: optional
        int specifying the threshold to use if drawing a contour
    """
    parser.add_argument(
        '-play',
        type=int,
        help='0 or 1 specifying whether to play the video using OpenCV.')
    parser.add_argument(
        '-frame',
        default=None,
        type=int,
        help='int specifying a frame to save in 16 bit color using matplotlib.'
    )
    parser.add_argument(
        '-framerange',
        default=None,
        type=str,
        help=
        'start,end specifying frame range to save in 16 bit color using matplotlib.'
    )
    parser.add_argument(
        '-contour',
        type=int,
        default=None,
        help='int specifying threshold to use to find contours in dataset.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Play a video from the given dataset.')

    get_viewer_CLargs(parser)
    get_dataset_CLargs(parser)

    args = parser.parse_args()

    play = bool(args.play)
    temp_data = str(args.temp_data)
    top = bool(args.top)
    bot = bool(args.bot)
    scale = args.scale
    frame = args.frame
    framerange = args.framerange
    contour = args.contour

    dataset = DataSet(temp_data, top, bot, int(scale))
    thermal_viewer = Viewer(dataset, contour)

    if frame is not None:
        thermal_viewer.save_frame16(int(frame))
    if framerange is not None:
        comma_index = str(framerange).find(',')
        start = int(framerange[:comma_index])
        end = int(framerange[comma_index + 1:])
        thermal_viewer.save_frame16(start=start, end=end)
    if play:
        thermal_viewer.play_video()