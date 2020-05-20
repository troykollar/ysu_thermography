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
            'Quit': [ord('q'), 27],
            'Save': [ord('s')],
            'Adv 1 Frame': [ord('m')],
            'Adv 10 Frame': [ord('l')],
            'Adv 100 Frame': [ord('o')],
            'Rew 1 Frame': [ord('n')],
            'Rew 10 Frame': [ord('j')],
            'Rew 100 Frame': [ord('i')]
        }

    def play_video(self, frame_delay: int = 1):
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
            key = cv2.waitKey(frame_delay) & 0xFF
            self.key_handler(key)
        cv2.destroyAllWindows()

    def save_video(self, start: int = -1, end: int = -1, framerate: int = 60):
        start, end, valid_inputs = self.dataset.validate_start_end(start, end)
        if valid_inputs:
            # Generate the filename based on what frames are used
            filename = self.dataset.build_folder + 'video'
            if start != 0 or end != self.dataset.shape[0]:
                filename += str(start) + '-' + str(end)

            filename += '.avi'

            # Generate a reference frame to get height and width
            ref_frame = self.generate_frame(self.dataset[0])
            height = ref_frame.shape[0]
            width = ref_frame.shape[1]
            video_writer = cv2.VideoWriter(
                filename, cv2.VideoWriter_fourcc('F', 'M', 'P', '4'),
                framerate, (width, height))

            for i in range(start, end):
                frame = self.dataset[i]
                printProgressBar(i - start, end - start, 'Saving Video...')
                generated_frame = self.generate_frame(frame)
                video_writer.write(generated_frame)

            video_writer.release()

            print('\nVideo saved as :', filename)

    def generate_frame(self, frame_data: np.ndarray):
        generated_frame = colormap_frame(frame_data)
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

        if self.info_pane == 'contour':
            generated_frame = self.add_info_pane(generated_frame,
                                                 contour_geo_dict)
        elif self.info_pane == 'mp':
            meltpool_dict = self.dataset.get_meltpool_data(self.cur_frame)
            generated_frame = self.add_info_pane(generated_frame,
                                                 meltpool_dict)

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

    def save_frame16(self, start: int, end=-1):
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
        int specifying frame delay in ms to play the video using OpenCV.
    save: optional
        int specifying the framerate to save the video in using OpenCV.
    frame: optional
        int specifying a frame to save in 16 bit color using matplotlib.
    range: optional
        start,end specifying frame range to save in 16 bit color using matplotlib.
    contour: optional
        int specifying the threshold to use if drawing a contour.
    follow: optional
        str specifying what to focus the frame on.
        follow = 'max' centers the frame on the max temperature.
        follow = 'contour' centers the frame on the center of gravity of the contour (if present).
    fsize: optional
        int specifying the size of the window when following max temp or contour.
    info: optional
        'mp' or 'contour' to display an info pane with relevant info above video.
    """
    parser.add_argument(
        '-play',
        type=int,
        help='int specifying frame delay in ms to play the video using OpenCV.',
        default=None)
    parser.add_argument(
        '-save',
        type=int,
        help='int specifying the framerate to save the video in using OpenCV.',
        default=None)
    parser.add_argument(
        '-frame',
        default=None,
        type=int,
        help=
        '0 or 1 specifying whether to save a frame in 16 bit color using matplotlib. Must also use range arg to specify frame numbers.'
    )
    parser.add_argument(
        '-range',
        default=None,
        type=str,
        help=
        "'start,end' specifying frame range to save in 16 bit color using matplotlib. Or just 'frame' to specify a single frame."
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
    parser.add_argument(
        '-info',
        type=str,
        default=None,
        help=
        "'mp' or 'contour' to display an info pane with relevant info above video"
    )


def colormap_frame(frame):
    frame = cv2.normalize(frame,
                          frame,
                          0,
                          255,
                          cv2.NORM_MINMAX,
                          dtype=cv2.CV_8UC1)
    frame = cv2.applyColorMap(frame, cv2.COLORMAP_INFERNO)
    return frame


if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser(
        description='Play a video from the given dataset.')

    get_viewer_CLargs(argument_parser)
    get_dataset_CLargs(argument_parser)

    args = argument_parser.parse_args()

    play = args.play
    temp_data = str(args.temp_data)
    top = bool(args.top)
    bot = bool(args.bot)
    scale = args.scale
    save_frame = args.frame
    framerange = args.range
    contour = args.contour
    follow_arg = args.follow
    fsize = args.fsize
    save_framerate = args.save
    info_arg = args.info
    merged_data = args.mp_data

    # Validate follow argument
    acceptable_follow_args = ['max', 'contour']
    if follow_arg is not None:
        if not follow_arg in acceptable_follow_args:
            follow_arg = None

    # Validate info argument
    acceptable_info_args = ['contour', 'mp']
    if info_arg is not None:
        if not info_arg in acceptable_info_args:
            info_arg = None

    data = DataSet(temps_file=temp_data,
                   meltpool_data=merged_data,
                   remove_top_reflection=top,
                   remove_bottom_reflection=bot,
                   scale_factor=int(scale))
    thermal_viewer = Viewer(dataset=data,
                            contour_threshold=contour,
                            follow=follow_arg,
                            follow_size=fsize,
                            info_pane=info_arg)

    if framerange is not None:
        comma_index = str(framerange).find(',')
        if comma_index == -1:
            start_frame = framerange
            end_frame = -1
        else:
            start_frame = int(framerange[:comma_index])
            end_frame = int(framerange[comma_index + 1:])
    else:
        start_frame = -1
        end_frame = -1

    if save_frame is not None:
        if framerange is not None:
            if end_frame == -1:
                thermal_viewer.save_frame16(int(start_frame))
            else:
                thermal_viewer.save_frame16(int(start_frame), int(end_frame))
        else:
            print("Must specify frames to save using '-range' argument!")
    if play is not None:
        thermal_viewer.play_video(play)

    if save_framerate is not None:
        thermal_viewer.save_video(start=start_frame,
                                  end=end_frame,
                                  framerate=save_framerate)
