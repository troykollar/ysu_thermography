import cv2
import numpy as np
from composite import get_threshold_img
from dataset import DataSet


def on_click(event, x, y, flags, param):
    x_loc = x
    y_loc = y
    if event == cv2.EVENT_LBUTTONDOWN:
        param.append((x, y))


class PixelSelector:
    def __init__(self):
        self.location_list = []
        self.close_window = False

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

            cv2.imshow(window_name, draw_img)
            key = cv2.waitKey(1) & 0xFF

            self.key_handler(key)

        cv2.destroyAllWindows()

    def key_handler(self, key):
        if key == ord('q'):
            self.close_window = True
        elif key == ord('z'):
            if len(self.location_list) > 0:
                del self.location_list[-1]
        else:
            self.close_window = False


if __name__ == '__main__':
    test_data = DataSet(
        '/home/troy/thermography/4-20_corrected/thermal_cam_temps.npy')

    thresh_img = get_threshold_img(test_data, 700)
    thresh_img = cv2.normalize(thresh_img,
                               thresh_img,
                               0,
                               255,
                               cv2.NORM_MINMAX,
                               dtype=cv2.CV_8UC1)
    thresh_img = cv2.applyColorMap(thresh_img, cv2.COLORMAP_INFERNO)

    pix_sel = PixelSelector()
    pix_sel.create_window('test_window', thresh_img)
