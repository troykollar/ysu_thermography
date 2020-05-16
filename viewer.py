import os
import shutil
import argparse
import cv2
import numpy as np
import matplotlib.pyplot as plt
from dataset import DataSet, get_dataset_CLargs
from helper_functions import printProgressBar


class Viewer:
    """Contains functions related to viewing and saving video/images of thermal data"""
    def __init__(self,
                 dataset: DataSet,
                 contour_threshold: int = None,
                 follow: str = None,
                 follow_size: int = 20,
                 info_pane=None):
        self.dataset = dataset
        self.quit = False
        self.cur_frame = None
        self.pause = False
        self.update_frame = True
        self.contour_threshold = contour_threshold
        self.follow = follow
        self.follow_size = follow_size
        self.info_pane = info_pane

        # Keycodes stored as list so multiple keys can be assigned to a function w/o other changes
        # Could be made simpler using ASCII lookup and keycodes, but apparently keycodes are
        # different depending on platform
        self.keys = {
            'Play/Pause': ['P', 'Space', 'K'],
            'Quit': ['Q', 'Esc'],
            'Save': ['S'],
            'Adv 1 Frame': ['M'],
            'Adv 10 Frame': ['L'],
            'Adv 100 Frame': ['O'],
            'Rew 1 Frame': ['N'],
            'Rew 10 Frame': ['J'],
            'Rew 100 Frame': ['I'],
        }

        self.keycodes = {
            'Play/Pause': [ord('p'), 32, ord('k')],
            # TODO: Add keycode for Esc
            'Quit': [ord('q')],
            'Save': [ord('s')],
            'Adv 1 Frame': [ord('m')],
            'Adv 10 Frame': [ord('l')],
            'Adv 100 Frame': [ord('o')],
            'Rew 1 Frame': [ord('n')],
            'Rew 10 Frame': [ord('j')],
            'Rew 100 Frame': [ord('i')]
        }

    def play_video(self):
        for item in self.keys:
            print(item + ':', *self.keys[item], sep=' | ')
        window_name = self.dataset.build_folder
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        self.cur_frame = 0
        while not self.quit:
            if self.update_frame:
                video_frame = self.generate_frame(self.dataset[self.cur_frame])
            if self.quit:
                break
            cv2.imshow(window_name, video_frame)
            if not self.pause:
                self.advance_frame(1)
            else:
                self.update_frame = False
            key = cv2.waitKey(1) & 0xFF
            self.key_handler(key)
        cv2.destroyAllWindows()

    def generate_frame(self, frame_data: np.ndarray):
        generated_frame = self.colormap_frame(frame_data)
        if self.contour_threshold is not None:
            contours = self.dataset.find_contours(frame_data,
                                                  self.contour_threshold)
            generated_frame = self.draw_contour(contours, generated_frame)
            contour_geo_dict = self.dataset.get_contour_geometry(contours)
        frame_size = self.follow_size * self.dataset.scale_factor
        if self.follow == 'max':
            _, max_temp_location = self.dataset.get_max_temp(generated_frame)
            if max_temp_location is not None:
                generated_frame = self.center_frame(generated_frame,
                                                    max_temp_location,
                                                    frame_size)
        elif self.follow == 'contour':
            if self.contour_threshold is not None:
                center_x = contour_geo_dict['cog_x']
                center_y = contour_geo_dict['cog_y']
                if center_x is not None and center_y is not None:
                    generated_frame = self.center_frame(
                        generated_frame, (center_x, center_y), frame_size)
                else:
                    _, max_temp_location = self.dataset.get_max_temp(
                        generated_frame)
                    generated_frame = self.center_frame(
                        generated_frame, max_temp_location, frame_size)

        # Change conditional to be specific for mp data or contour data
        # TODO: Add conditional for meltpool info pane
        if self.info_pane == 'contour':
            generated_frame = self.add_info_pane(generated_frame,
                                                 contour_geo_dict)

        return generated_frame

    def center_frame(self, frame: np.ndarray, point: tuple, frame_size: int):
        center_x = point[0]
        center_y = point[1]

        # Decide if too far left or right
        if center_x < frame_size:
            left_x = 0
            right_x = frame_size * 2
        elif center_x + frame_size > frame.shape[1]:
            right_x = frame.shape[1]
            left_x = right_x - (2 * frame_size)
        else:
            left_x = center_x - frame_size
            right_x = center_x + frame_size

        # Decide if too far up or down
        if center_y < frame_size:
            top_y = 0
            bot_y = frame_size * 2
        elif center_y + (frame_size * 2) > frame.shape[0]:
            bot_y = frame.shape[0]
            top_y = bot_y - (frame_size * 2)
        else:
            top_y = center_y - frame_size
            bot_y = center_y + frame_size

        return frame[top_y:bot_y, left_x:right_x]

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
            plt.imsave(savename, self.dataset[start], cmap='inferno')
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
        if key in self.keycodes['Quit']:
            self.quit = True
        elif key in self.keycodes['Save']:
            self.save_frame16(self.cur_frame)
        elif key in self.keycodes['Play/Pause']:
            self.pause = not self.pause
        elif key in self.keycodes['Adv 1 Frame']:
            self.advance_frame(1)
        elif key in self.keycodes['Adv 10 Frame']:
            self.advance_frame(10)
        elif key in self.keycodes['Adv 100 Frame']:
            self.advance_frame(100)
        elif key in self.keycodes['Rew 1 Frame']:
            self.rewind_frame(1)
        elif key in self.keycodes['Rew 10 Frame']:
            self.rewind_frame(10)
        elif key in self.keycodes['Rew 100 Frame']:
            self.rewind_frame(100)
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

    def draw_contour(self, contours, colormapped_frame: np.ndarray):
        colormapped_frame = cv2.drawContours(colormapped_frame, contours, -1,
                                             (0, 255, 0), 1)
        return colormapped_frame

    def add_info_pane(self, colormapped_frame: np.ndarray, info: dict):
        frame_height = colormapped_frame.shape[0]
        frame_width = colormapped_frame.shape[1]
        font = cv2.FONT_HERSHEY_DUPLEX
        font_size = .002 * frame_height
        font_color = (0, 0, 0)
        #pane_height = 30 * len(info) * self.dataset.scale_factor
        pane_height = int(len(info) * .08 * frame_height)

        if font_size < .35:
            self.dataset.increase_scale(1)

        # Add white pane
        colormapped_frame = cv2.copyMakeBorder(src=colormapped_frame,
                                               top=pane_height,
                                               bottom=0,
                                               left=0,
                                               right=0,
                                               borderType=cv2.BORDER_CONSTANT,
                                               value=(255, 255, 255))

        # Add text
        for i, item in enumerate(info):
            text_y = int(.07 * frame_height * (i + 1))
            text_x = int(.01 * frame_width)
            colormapped_frame = cv2.putText(
                colormapped_frame,
                item + ': ' + str(info[item]), (text_x, text_y),
                font,
                font_size,
                font_color,
                thickness=int(.05 * self.dataset.scale_factor))

        return colormapped_frame


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
    follow: optional
        str specifying what to focus the frame on.
        follow = 'max' centers the frame on the max temperature.
        follow = 'contour' centers the frame on the center of gravity of the contour (if present).
    fsize: optional
        int specifying the size of the window when following max temp or contour
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
    parser.add_argument(
        '-follow',
        type=str,
        default=None,
        help=
        "str, 'max' or 'contour' will center the frame on the max temp or the contour center of gravity, respectively"
    )
    parser.add_argument(
        '-fsize',
        type=int,
        default=20,
        help=
        'int specifying the size of the window when following max temp or contour'
    )


if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser(
        description='Play a video from the given dataset.')

    get_viewer_CLargs(argument_parser)
    get_dataset_CLargs(argument_parser)

    args = argument_parser.parse_args()

    play = bool(args.play)
    temp_data = str(args.temp_data)
    top = bool(args.top)
    bot = bool(args.bot)
    scale = args.scale
    save_frame = args.frame
    framerange = args.framerange
    contour = args.contour
    follow_arg = args.follow
    fsize = args.fsize

    # Validate follow argument
    acceptable_follow_args = ['max', 'contour']
    if follow_arg is not None:
        if not follow_arg in acceptable_follow_args:
            follow_arg = None

    data = DataSet(temp_data, top, bot, int(scale))
    thermal_viewer = Viewer(data,
                            contour,
                            follow=follow_arg,
                            follow_size=fsize,
                            info_pane='contour')

    if save_frame is not None:
        thermal_viewer.save_frame16(int(save_frame))
    if framerange is not None:
        comma_index = str(framerange).find(',')
        start_frame = int(framerange[:comma_index])
        end_frame = int(framerange[comma_index + 1:])
        thermal_viewer.save_frame16(start=start_frame, end=end_frame)
    if play:
        thermal_viewer.play_video()
