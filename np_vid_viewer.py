import os
import shutil
import time
import cv2
import matplotlib.pyplot as plt
import numpy as np

from helper_functions import *
from dataset import DataSet


def format_time(t):
    s = t.strftime('%Y-%m-%d %H:%M:%S.%f')
    return s[:-3]


class NpVidTool:
    def __init__(self,
                 data_directory,
                 r_top_refl=False,
                 r_bot_refl=False,
                 mp_data_on_vid=False,
                 follow_max_temp=0,
                 contour_threshold=0,
                 follow_contour=0,
                 contour_data_on_img=False):

        self.dataset = DataSet(data_directory, r_top_refl, r_bot_refl)
        self.mp_data_on_vid = mp_data_on_vid
        self.follow_max_temp = follow_max_temp
        self.framerate = None
        self.contour_threshold = contour_threshold
        self.follow_contour = follow_contour
        self.contour_data_on_img = contour_data_on_img

    def generate_img(self, frame_num, scale_factor=1):
        frame, unscaled_frame, original_frame = self.dataset.get_frame(
            frame_num, scale_factor)

        img = frame.copy()

        # Normalize the image to 8 bit color
        img = cv2.normalize(img, img, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)

        # Apply colormap to image
        img = cv2.applyColorMap(img, cv2.COLORMAP_INFERNO)

        # Find and draw contours if specified
        if self.contour_threshold != 0:
            thresh_img = cv2.inRange(frame, self.contour_threshold,
                                     int(np.amax(frame)))
            contours, _ = cv2.findContours(thresh_img, cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_TC89_KCOS)
            img = cv2.drawContours(img, contours, -1, (0, 255, 0), 1)

            cog_x = None
            cog_y = None
            contour_x = None
            contour_y = None
            contour_w = None
            contour_h = None
            for contour in contours:
                contour_x, contour_y, contour_w, contour_h = cv2.boundingRect(
                    contour)
                contour_area = float(cv2.contourArea(contour))
                M = cv2.moments(contour)
                if M['m00'] != 0:
                    cog_x = int(M['m10'] / M['m00'])  # center of gravity x
                    cog_y = int(M['m01'] / M['m00'])  # center of gravity y

            if self.follow_contour != 0:
                follow_size = self.follow_contour * scale_factor
                if cog_x is not None and cog_y is not None:
                    top_y, bottom_y, left_x, right_x = get_follow_contour_cords(
                        frame, follow_size, cog_x, cog_y)
                else:
                    top_y, bottom_y, left_x, right_x = get_follow_meltpool_cords(
                        frame, follow_size)

                img = img[top_y:bottom_y, left_x:right_x]

            if self.contour_data_on_img:
                img = add_white_border_on_img(img)
                if contour_x is not None:
                    img = self.add_contour_data_to_img(img, contour_x,
                                                       contour_y, contour_w,
                                                       contour_h, cog_x, cog_y)

        if self.follow_max_temp != 0 and self.follow_contour != 0:
            self.follow_max_temp = 0

        if self.follow_max_temp != 0:
            follow_size = self.follow_max_temp * scale_factor
            top_y, bottom_y, left_x, right_x = get_follow_meltpool_cords(
                frame, follow_size)

            img = img[top_y:bottom_y, left_x:right_x]

        # Add meltpool data onto the image
        if self.mp_data_on_vid:
            img = self.add_mp_data_to_img(img, frame_num)

        return img

    def save_frame16(self, start: int, end=0, scale_factor=1):
        build_folder = self.dataset.data_directory
        build_number = self.dataset.build_number
        if end != 0:
            frame_range_folder = build_folder + build_number + '_frames' + str(
                start) + '-' + str(end)
            if os.path.isdir(frame_range_folder):
                shutil.rmtree(frame_range_folder)
            os.mkdir(frame_range_folder)

            total = end - start
            progress = 0
            for i in range(start, end):
                # Display completion percentage
                printProgressBar(progress + 1,
                                 total,
                                 prefix='Saving frames ' + str(start) + '-' +
                                 str(end))
                frame_fname = frame_range_folder + '/frame_' + str(i) + '.png'
                unscaled_fname = frame_range_folder + '/frame_' + str(
                    i) + '_unscaled.png'
                original_fname = frame_range_folder + '/frame_' + str(
                    i) + '_original.png'
                frame, unscaled, original = self.dataset.get_frame(
                    i, scale_factor)
                plt.imsave(frame_fname, frame, cmap='inferno')
                plt.imsave(unscaled_fname, unscaled, cmap='inferno')
                plt.imsave(original_fname, original, cmap='inferno')

                progress += 1
            print('Saved frames ' + str(start) + '-' + str(end))
        else:
            frame_fname = build_folder + 'frame_' + str(start) + '.png'
            unscaled_fname = build_folder + 'frame_' + str(
                start) + '_unscaled.png'
            original_fname = build_folder + 'frame_' + str(
                start) + '_original.png'
            frame, unscaled, original = self.dataset.get_frame(
                start, scale_factor)
            plt.imsave(frame_fname, frame, cmap='inferno')
            plt.imsave(unscaled_fname, unscaled, cmap='inferno')
            plt.imsave(original_fname, original, cmap='inferno')
            print('Saved frame ' + str(start))

    def play_video(self, scale_factor=1, frame_delay=1):

        # Keep track of frame render times for framerate adjustment
        frame_start_time = None
        frame_end_time = None
        frame_render_time = None

        window_name = 'Build ' + str(self.dataset.build_number)
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, 1280, 720)

        print(
            "'K'/'Space' - Play/Pause\n" +
            "'J' - Rewind 10 frames \t\t| 'N' - Rewind 1 frame\t\t| 'I' - Rewind 100 frames\n"
            +
            "'L' - Fast Forward 10 frames \t| 'M' - Fast Forward 1 frame\t| 'O' - Fast-forward 100 frames\n"
            + "'F' - Jump to specific frame\n" + "'S' - Save frame as PNG\n" +
            "'Q' - Quit")

        frame_num = 0
        pause = False
        while True:
            # Get frame start time for FPS calculation
            frame_start_time = time.time()

            #TODO:  Change progressbar to show timestamp (relative to video)
            #       instead of percentage
            printProgressBar(frame_num,
                             self.dataset.final_frame,
                             prefix='Playing Video: ')
            key = cv2.waitKey(frame_delay)
            if key == ord("q"):
                break
            elif key == ord(
                    "k") or key == 32:  # key == 32 means spacebar is pressed
                pause = not pause
            elif key == ord("l"):
                if frame_num < self.dataset.final_frame - 10:
                    frame_num += 10
                else:
                    frame_num = self.dataset.final_frame
            elif key == ord("j"):
                if frame_num > 10:
                    frame_num -= 10
                else:
                    frame_num = 0
            elif key == ord('m'):
                if frame_num < self.dataset.final_frame:
                    frame_num += 1
                else:
                    frame_num = self.dataset.final_frame
            elif key == ord('n'):
                if frame_num > 0:
                    frame_num -= 1
                else:
                    frame_num = 0
            elif key == ord('o'):
                if frame_num < self.dataset.final_frame - 100:
                    frame_num += 100
                else:
                    frame_num = self.dataset.final_frame
            elif key == ord('i'):
                if frame_num > 100:
                    frame_num -= 100
                else:
                    frame_num = 0
            elif key == ord('s'):
                self.save_frame16(frame_num, scale_factor=scale_factor)
                print('Saved frame: ' + str(frame_num))
            elif key == ord('f'):
                pause = True
                input_frame = -1
                error = True
                while error:
                    input_frame = input("Enter a frame to jump to:\n")
                    if input_frame.isdigit():
                        error = False
                    else:
                        error = True
                frame_num = int(input_frame) - 1

            if not pause:
                frame_num += 1
            else:
                pass

            img = self.generate_img(frame_num, scale_factor)

            if frame_num == self.dataset.final_frame:
                frame_num = 0  #Start video over at end

            cv2.imshow(window_name, img)

            # FPS calculation
            frame_end_time = time.time()
            # frame render time in seconds
            frame_render_time = frame_end_time - frame_start_time

            self.framerate = int(1 / (frame_render_time +
                                      (frame_delay * .001)))

        print(
            '\n'
        )  # Print blank line to remove progressbar if video was quit before ending

        cv2.destroyAllWindows()

    def add_contour_data_to_img(self, img, contour_x, contour_y, contour_w,
                                contour_h, cog_x, cog_y):
        img_height = img.shape[0]
        img_width = img.shape[1]
        font = cv2.FONT_HERSHEY_DUPLEX
        font_size = img_height / 860
        font_color = (0, 0, 0)

        column1_x = 5
        column2_x = int(img_width * .4)
        if contour_x is not None:
            img = cv2.putText(
                img,
                'X: ' + str(contour_x),
                (column1_x, int((1 / 32) * img_height)),
                font,
                font_size,
                font_color,
            )
            img = cv2.putText(
                img,
                'Y: ' + str(contour_y),
                (column1_x, int((3 / 32) * img_height)),
                font,
                font_size,
                font_color,
            )
            img = cv2.putText(
                img,
                'Width: ' + str(contour_w),
                (column1_x, int((5 / 32) * img_height)),
                font,
                font_size,
                font_color,
            )
            img = cv2.putText(
                img,
                'Height: ' + str(contour_h),
                (column1_x, int((7 / 32) * img_height)),
                font,
                font_size,
                font_color,
            )
            img = cv2.putText(
                img,
                'Center of Gravity: (' + str(cog_x) + ',' + str(cog_y) + ')',
                (column1_x, int((9 / 32) * img_height)),
                font,
                font_size,
                font_color,
            )
        return img

    def save_hotspot_video(self, framerate=60, save_img=False):
        self.framerate = framerate
        height = self.temp_data[0].shape[0]
        width = self.temp_data[0].shape[1]
        size = (width, height)
        build_folder = get_build_folder(self.temp_filename)
        build_number = get_build_number(self.temp_filename)
        filename = build_folder + '/' + build_number + '_hotspot.avi'

        video_writer = cv2.VideoWriter(
            filename, cv2.VideoWriter_fourcc('F', 'M', 'P', '4'), framerate,
            size)

        hotspot_img = np.zeros((height, width), dtype=np.float32)

        for i, frame in enumerate(self.temp_data, 0):
            # Display completion percentage
            printProgressBar(
                i,
                self.num_frames,
                prefix='Saving Hotspot Video...',
            )

            current_max = np.amax(frame)
            current_max_y = np.where(frame == current_max)[0][0]
            current_max_x = np.where(frame == current_max)[1][0]

            hotspot_img[current_max_y, current_max_x] = current_max
            hotspot_img_frame = hotspot_img.copy()
            hotspot_img_frame = cv2.normalize(
                src=np.float32(hotspot_img_frame),
                dst=np.float32(hotspot_img_frame),
                alpha=0,
                beta=255,
                norm_type=cv2.NORM_MINMAX,
                dtype=cv2.CV_8UC1)
            hotspot_img_frame = cv2.applyColorMap(hotspot_img_frame,
                                                  cv2.COLORMAP_INFERNO)

            video_writer.write(hotspot_img_frame)

        video_writer.release()

        if save_img:
            cv2.imwrite(build_folder + '/' + build_number + '_hotspot_img.png',
                        hotspot_img_frame)

    """
    def circle_max_temp(self, frame_num: int, img: np.ndarray):
        frame = self.temp_data[frame_num]
        max_temp = np.amax(frame)
        if max_temp is not None:
            max_temp_x = np.where(frame == max_temp)[1][0] * self.scale_factor
            max_temp_y = np.where(frame == max_temp)[0][0] * self.scale_factor
            img = cv2.circle(img, (max_temp_x, max_temp_y),
                             radius=3,
                             color=(0, 0, 255),
                             thickness=2)
    """

    def add_mp_data_to_img(self, img, frame_num):
        img_height = img.shape[0]
        img_width = img.shape[1]
        font = cv2.FONT_HERSHEY_DUPLEX
        font_size = img_height / 860
        font_color = (0, 0, 0)

        # Add white border on top of img
        img = cv2.copyMakeBorder(img,
                                 int(img_height * (7 / 16)),
                                 0,
                                 0,
                                 0,
                                 cv2.BORDER_CONSTANT,
                                 value=(255, 255, 255))

        time_stamp, x, y, z, area = self.dataset.get_meltpool_data(frame_num)
        time_stamp = format_time(time_stamp)
        max_temp, max_x, max_y = self.dataset.get_max_temp_data(frame_num)

        column1_x = 5
        column2_x = int(img_width * .4)
        img = cv2.putText(
            img,
            'X: ' + str(x),
            (column1_x, int((1 / 32) * img_height)),
            font,
            font_size,
            font_color,
        )
        img = cv2.putText(
            img,
            'Y: ' + str(y),
            (column1_x, int((3 / 32) * img_height)),
            font,
            font_size,
            font_color,
        )
        img = cv2.putText(
            img,
            'Z: ' + str(z),
            (column1_x, int((5 / 32) * img_height)),
            font,
            font_size,
            font_color,
        )
        img = cv2.putText(
            img,
            "Area: " + str(area),
            (column2_x, int((1 / 32) * img_height)),
            font,
            font_size,
            font_color,
        )
        img = cv2.putText(
            img,
            "Max Temp: " + str(max_temp),
            (column2_x, int((3 / 32) * img_height)),
            font,
            font_size,
            font_color,
        )
        img = cv2.putText(
            img,
            "Frame: " + str(frame_num) + "/" + str(self.dataset.final_frame),
            (column2_x, int(
                (5 / 32) * img_height)), font, font_size, font_color)
        img = cv2.putText(img, 'Time: ' + str(time_stamp),
                          (column1_x, int((7 / 32) * img_height)), font,
                          font_size, font_color)

        if self.framerate is not None:
            img = cv2.putText(img, 'FPS: ' + str(self.framerate),
                              (column1_x, int((9 / 32) * img_height)), font,
                              font_size, font_color)

        img = cv2.putText(img, 'Build: ' + str(self.dataset.build_number),
                          (column2_x, int((9 / 32) * img_height)), font,
                          font_size, font_color)

        return img

    def save_video(self, scale_factor=1, framerate=60, start=0, end=0):
        filename = self.dataset.data_directory + str(self.dataset.build_number)

        if start < 0 or start > self.dataset.final_frame:
            start = 0

        if end <= 0 or end > self.dataset.final_frame:
            end = self.dataset.final_frame

        if start != 0 or end != self.dataset.final_frame:
            filename += '_frames' + str(start) + '-' + str(end)
        filename += '.avi'

        if start >= end:
            print('Invalid start and end frames.')
        else:
            # Generate a test img to get size of video
            test_img = self.generate_img(0, scale_factor)
            height = test_img.shape[0]
            width = test_img.shape[1]
            size = (width, height)

            # Create VideoWriter Object
            video_writer = cv2.VideoWriter(
                filename, cv2.VideoWriter_fourcc('F', 'M', 'P', '4'),
                framerate, size)

            progress = 0
            total = end - start
            for i in range(start, end):
                # Display completion percentage
                printProgressBar(progress, total, prefix='Saving Video...')

                img = self.generate_img(i, scale_factor)

                video_writer.write(img)
                progress += 1

            print('Video saved to : ' + filename)
            video_writer.release()
