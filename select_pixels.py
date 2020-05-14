import cv2
from datetime import datetime
import numpy as np
import argparse
from np_vid_viewer.helper_functions import get_build_number, get_build_folder
from np_vid_viewer.composite import get_threshold_img
from Visualization_script import get_visualization
from bubble_plot_3d import plotBubble
from plot import Plots

PARSER = argparse.ArgumentParser(description='Generate plots from a dataset.')
PARSER.add_argument('temp_data',
                    type=str,
                    help='the file location/name of the temperature data')
PARSER.add_argument('THRESHOLD',
                    type=int,
                    help='temperature theshold of the image')
PARSER.add_argument('-start',
                    type=int,
                    default=0,
                    required=False,
                    help='First frame to consider.')
PARSER.add_argument('-end',
                    type=int,
                    default=-1,
                    required=False,
                    help='Last frame to consider.')
ARGS = PARSER.parse_args()
temp_file = ARGS.temp_data
composite_threshold = ARGS.THRESHOLD
start_frame = ARGS.start
end_frame = ARGS.end

temp_data = np.load(temp_file, allow_pickle=True, mmap_mode='r')

img1 = get_threshold_img(temp_data,
                         composite_threshold,
                         show_progress=True,
                         start=start_frame,
                         end=end_frame)
img1 = cv2.normalize(img1, img1, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
img1 = cv2.applyColorMap(img1, cv2.COLORMAP_INFERNO)

pixel_locations = []
corner_locations = []

select_corners = True


def on_click(event, x, y, flags, param):
    x_loc = x
    y_loc = y
    if event == cv2.EVENT_LBUTTONDOWN:
        if select_corners:
            corner_locations.append((x, y))
        else:
            pixel_locations.append((x, y))


window_name = get_build_number(temp_file)
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setMouseCallback(window_name, on_click)

while True:
    if len(corner_locations) < 4:
        select_corners = True
    else:
        select_corners = False

    draw_img = img1.copy()

    if select_corners:
        for corner_pixel in corner_locations:
            corner_x = corner_pixel[0]
            corner_y = corner_pixel[1]
            draw_img[corner_y][corner_x] = [0, 255, 255]
    else:
        draw_img = cv2.polylines(draw_img, np.int32([corner_locations]), True,
                                 (0, 255, 255), 1)

    for pixel in pixel_locations:
        pixel_x = pixel[0]
        pixel_y = pixel[1]
        draw_img[pixel_y][pixel_x] = [255, 255, 255]

    cv2.imshow(window_name, draw_img)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    elif key == ord('z'):
        if len(pixel_locations) > 0:
            del pixel_locations[-1]
        elif len(corner_locations) > 0:
            del corner_locations[-1]
        else:
            pass

cv2.destroyAllWindows()

savetime = str(datetime.now().month) + '-' + str(
    datetime.now().day) + '_' + str(datetime.now().hour) + '-' + str(
        datetime.now().minute)

path = get_build_folder(temp_file)

if len(corner_locations) == 4:
    if len(pixel_locations) > 0:
        corner_locations.sort()
        pixel_locations.sort()
        loc_file = open('pixel_locations' + savetime + '.txt', 'w')
        loc_file.write('Corner locations:\n')
        for corner_pixel in corner_locations:
            loc_file.write(str(corner_pixel) + '\n')
        loc_file.write('\nSelected Pixels:\n')
        for pixel in pixel_locations:
            loc_file.write(str(pixel) + '\n')

        loc_file.close()

        for pixel in pixel_locations:
            print(temp_data.shape)
            print('\nGenerating 2D plots for: ' + str(pixel))
            plot = Plots(temp_data,
                         (pixel_y, pixel_x),
                         threshold=composite_threshold,
                         start_frame=start_frame,
                         end_frame=end_frame)
            plot.all()
