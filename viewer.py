import argparse
import cv2
import numpy as np
import matplotlib.pyplot as plt
from dataset import DataSet, get_dataset_CLargs


class Viewer:
    def __init__(self, dataset: DataSet):
        self.dataset = dataset

    def play_video(self):
        window_name = self.dataset.build_folder
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        for frame in self.dataset:
            frame = self.colormap_frame(frame)
            cv2.imshow(window_name, frame)
            cv2.waitKey(1)
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

    def save_frame16(self, frame):
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Play a video from the given dataset.')

    get_dataset_CLargs(parser)
    args = parser.parse_args()

    temp_data = args.temp_data
    top = bool(args.top)
    bot = bool(args.bot)
    scale = args.scale

    dataset = DataSet(temp_data, top, bot, scale)
    thermal_viewer = Viewer(dataset)
    thermal_viewer.play_video()