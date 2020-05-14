import argparse
import cv2
import numpy as np
import matplotlib.pyplot as plt
from dataset import DataSet, get_dataset_CLargs


class Viewer:
    def __init__(self, dataset: DataSet):
        self.dataset = dataset
        self.quit = False
        self.cur_frame = None
        self.pause = False

    def play_video(self):
        window_name = self.dataset.build_folder
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        self.cur_frame = 0
        while not self.quit:
            if not self.pause:
                frame = self.dataset[self.cur_frame]
                if self.quit:
                    break
                frame = self.colormap_frame(frame)
                self.advance_frame(1)
            cv2.imshow(window_name, frame)
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
        # TODO: Add ability to save range of frames
        # Save only one frame
        if end < 0:
            savename = self.dataset.build_folder + '/frame' + str(
                start) + '.png'
            plt.imsave(savename, dataset[start], cmap='inferno')
            print('Saved to: ' + savename)

    def key_handler(self, key):
        # TODO: Add ability to jump forward and back frames
        if key == ord('q'):
            self.quit = True
        elif key == ord('s'):
            self.save_frame16(self.cur_frame)
        elif key == ord('p') or key == 32:
            self.pause = not self.pause
        else:
            pass

    def advance_frame(self, advancement: int):
        if self.cur_frame + advancement >= self.dataset.shape[0] - 1:
            self.cur_frame = self.dataset.shape[0] - 1
        else:
            self.cur_frame += advancement

    def rewind_frame(self, rewind_amount: int):
        if self.cur_frame - rewind_amount <= 0:
            self.cur_frame = 0
        else:
            self.cur_frame -= rewind_amount

    def draw_contour(self):
        # TODO: Add contour drawing
        pass

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

    dataset = DataSet(temp_data, top, bot, int(scale))
    thermal_viewer = Viewer(dataset)

    if frame is not None:
        thermal_viewer.save_frame16(int(frame))
    if play:
        thermal_viewer.play_video()