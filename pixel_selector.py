import argparse
import cv2
import numpy as np
from composite import get_threshold_img, save_threshold_img, get_composite_CLargs
from dataset import DataSet, get_dataset_CLargs
from plot import Plots


def on_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        param.append((x, y))


def select_pixels_and_gen_plots(temp_file: str,
                                threshold: int,
                                remove_reflections=False,
                                start_frame=-1,
                                end_frame=-1,
                                frame_cap=None):
    test_data = DataSet(temp_file,
                        remove_top_reflection=remove_reflections,
                        remove_bottom_reflection=remove_reflections,
                        start_frame=start_frame,
                        end_frame=end_frame)

    thresh_img = get_threshold_img(test_data, threshold, cap=frame_cap)
    save_threshold_img(temp_file, thresh_img, threshold)
    thresh_img = cv2.normalize(thresh_img,
                               thresh_img,
                               0,
                               255,
                               cv2.NORM_MINMAX,
                               dtype=cv2.CV_8UC1)
    thresh_img = cv2.applyColorMap(thresh_img, cv2.COLORMAP_INFERNO)

    pix_sel = PixelSelector()
    pix_sel.create_window('Select pixels to run analysis on', thresh_img)

    if len(pix_sel.location_list) < 3:
        print('No pixels selected for analysis!')
    else:
        for pixel in pix_sel.location_list[2:]:
            plot_maker = Plots(test_data, pixel, threshold, start, end)
            plot_maker.all()


class PixelSelector:
    def __init__(self):
        self.location_list = []
        self.close_window = False
        self.percents_from_right = []
        self.percents_from_bot = []

    def create_window(self, window_name: str, img: np.ndarray):
        yellow = (0, 255, 255)
        white = (255, 255, 255)
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.setMouseCallback(window_name, on_click, param=self.location_list)

        while not self.close_window:
            draw_img = img.copy()

            for i, pixel_location in enumerate(self.location_list):
                pixel_x = pixel_location[0]
                pixel_y = pixel_location[1]

                if i < 2:
                    color = yellow
                else:
                    color = white

                draw_img[pixel_y][pixel_x] = color

            if len(self.location_list) > 1:
                draw_img = cv2.rectangle(draw_img, self.location_list[0],
                                         self.location_list[1], yellow, 1)
                draw_img = self.highlight_rectangle_percents(draw_img)

            cv2.imshow(window_name, draw_img)
            key = cv2.waitKey(1) & 0xFF

            self.key_handler(key)

        self.percents_from_right, self.percents_from_bot = self.pixel_location_percents(
        )

        cv2.destroyAllWindows()

    def key_handler(self, key):
        if key == ord('q'):
            self.close_window = True
        elif key == ord('z'):
            if len(self.location_list) > 0:
                del self.location_list[-1]
        else:
            self.close_window = False

    def pixel_location_percents(self):
        if len(self.location_list) > 2:
            corners = self.location_list[0:2]
            corners.sort(key=lambda tup: tup[0])
            left_corner = corners[0]
            right_corner = corners[1]
            corners.sort(key=lambda tup: tup[1])
            top_corner = corners[0]
            bot_corner = corners[1]
            percent_from_bot = []
            percent_from_bot.append(0)  # 0% for left corner
            percent_from_bot.append(1)  # 100% for right corner

            percent_from_right = []
            percent_from_right.append(1)  # 100% for left corner
            percent_from_right.append(0)  # 0% for right corner

            for pixel in self.location_list[2:]:
                piece_length = right_corner[0] - left_corner[
                    0]  # Total length of the piece
                piece_height = bot_corner[1] - top_corner[
                    1]  # Total height of the piece
                bot_percent = (bot_corner[1] - pixel[1]) / piece_height
                percent_from_bot.append(round(bot_percent, 2))
                right_percent = (right_corner[0] - pixel[0]) / piece_length
                percent_from_right.append(round(right_percent, 2))

            return percent_from_right, percent_from_bot
        else:
            pass

    def highlight_rectangle_percents(self, draw_img: np.ndarray):
        if len(self.location_list) > 1:
            corners = self.location_list[0:2]
            corners.sort(key=lambda tup: tup[1])
            top_corner = corners[0]
            bot_corner = corners[1]
            corners.sort(key=lambda tup: tup[0])
            left_corner = corners[0]
            right_corner = corners[1]
            piece_length = right_corner[0] - left_corner[0]

            highlight_locs = [.25, .5, .75]
            for location in highlight_locs:
                x_cord = int(left_corner[0] + location * piece_length)
                draw_img[top_corner[1]][x_cord] = (255, 0, 0)
                draw_img[bot_corner[1]][x_cord] = (255, 0, 0)
        else:
            pass

        return draw_img


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Select pixels, and run analysis on those pixels.')
    get_dataset_CLargs(parser)
    get_composite_CLargs(parser)

    args = parser.parse_args()

    temp_data = args.temp_data
    top = bool(args.top)
    bot = bool(args.bot)
    rm_refl = top or bot
    THRESHOLD = args.THRESHOLD
    dst_folder = args.dst_folder
    cap = args.cap
    start = args.start
    end = args.end
    debug = args.debug

    select_pixels_and_gen_plots(temp_data,
                                THRESHOLD,
                                remove_reflections=rm_refl,
                                start_frame=start,
                                end_frame=end,
                                frame_cap=cap)
