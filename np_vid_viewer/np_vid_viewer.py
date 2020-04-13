import os
import shutil
import time
import cv2
import matplotlib.pyplot as plt
import numpy as np

import np_vid_viewer.reflection_remover
import np_vid_viewer.progress_bar as progress_bar
import np_vid_viewer.helper_functions as helper_functions

#TODO: Update documenation


def format_time(t):
    s = t.strftime('%Y-%m-%d %H:%M:%S.%f')
    return s[:-3]


class NpVidTool:
    def __init__(self,
                 data_directory: str,
                 mp_data_on_vid=False,
                 scale_factor=1,
                 remove_top_reflection=False,
                 remove_bottom_reflection=False,
                 follow_meltpool=False,
                 circle_max_temp=False):

        self.follow_meltpool = follow_meltpool
        self.highlight_max_temp = circle_max_temp
        self.remove_top_reflection = remove_top_reflection
        self.remove_bottom_reflection = remove_bottom_reflection
        self.mp_data_on_vid = mp_data_on_vid
        self.framerate = 0

        # Load temperature data
        temp_filename = 'thermal_cam_temps.npy'
        self.temp_filename = data_directory + '/' + temp_filename
        self.temp_data = np.load(self.temp_filename,
                                 mmap_mode="r",
                                 allow_pickle=True)
        self.num_frames = self.temp_data.shape[0]  # Save number of frames

        # Load merged data
        data_filename = data_directory + '/' + 'merged_data.npy'
        self.merged_data = np.load(data_filename, allow_pickle=True)

        # Find lower bounds of piece if remove_lower reflection is selected
        if self.remove_bottom_reflection:
            self.lower_bounds = np_vid_viewer.reflection_remover.find_lower_bounds(
                self.temp_data)
        else:
            self.lower_bounds = None

        # Set scale factor for resizing frames of video
        self.scale_factor = scale_factor
        if self.scale_factor == 1:
            self.scale_factor = helper_functions.min_scale_factor(
                self.temp_data[0])

    def save_frame_range16(self, start, end):
        build_folder = helper_functions.get_build_folder(self.temp_filename)
        build_number = helper_functions.get_build_number(self.temp_filename)
        frame_range_folder = build_folder + '/' + build_number + '_frames' + str(
            start) + '-' + str(end)
        if os.path.isdir(frame_range_folder):
            shutil.rmtree(frame_range_folder)
        os.mkdir(frame_range_folder)
        total = end + 1 - start

        progress = 0
        for i in range(start, end + 1):
            # Display completion percentage
            progress_bar.printProgressBar(progress + 1,
                                          total,
                                          prefix='Saving frames ' +
                                          str(start) + '-' + str(end))
            self.save_frame16(i, frame_range_folder)
            progress += 1

        print('Saved frames ' + str(start) + '-' + str(end))

    def generate_frame(self, frame_num):
        frame = self.temp_data[frame_num].copy()

        # Remove the top reflection of specified
        if self.remove_top_reflection:
            np_vid_viewer.reflection_remover.remove_top(
                frame, zero_level_threshold=180, max_temp_threshold=700)

        # Remove the bottom reflection if specififed
        if self.remove_bottom_reflection:
            np_vid_viewer.reflection_remover.remove_bottom(
                frame, self.lower_bounds)

        # Normalize the image to 8 bit color
        img = frame.copy()
        img = cv2.normalize(img, img, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)

        # Apply colormap to image
        img = cv2.applyColorMap(img, cv2.COLORMAP_INFERNO)

        # Focus on meltpool if specified
        if self.follow_meltpool:
            follow_size = 20
            max_temp = np.amax(frame)
            max_temp_y = np.where(frame == max_temp)[0][0]
            max_temp_x = np.where(frame == max_temp)[1][0]

            if max_temp_x < follow_size:
                left_x = 0
                right_x = follow_size * 2
            elif max_temp_x > frame.shape[1] - follow_size:
                right_x = frame.shape[1]
                left_x = right_x - (follow_size * 2)
            else:
                left_x = max_temp_x - follow_size
                right_x = max_temp_x + follow_size

            if max_temp_y < follow_size:
                top_y = 0
                bottom_y = follow_size * 2
            elif max_temp_y > img.shape[0] - follow_size:
                bottom_y = img.shape[0]
                top_y = img.shape[0] - (follow_size * 2)
            else:
                top_y = max_temp_y - follow_size
                bottom_y = max_temp_y + follow_size

            img = img[top_y:bottom_y, left_x:right_x]

        # Scale image according to scale_factor
        width = int(img.shape[1] * self.scale_factor)
        height = int(img.shape[0] * self.scale_factor)
        size = (width, height)

        img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)

        # Circle max temperature if selected
        if self.highlight_max_temp:
            self.circle_max_temp(frame_num, img)

        # Extend frame for mp_data
        if self.mp_data_on_vid:
            img = cv2.copyMakeBorder(img,
                                     int(height * (7 / 16)),
                                     0,
                                     0,
                                     0,
                                     cv2.BORDER_CONSTANT,
                                     value=(255, 255, 255))

        # Add meltpool data onto the image
        if self.mp_data_on_vid:
            self.add_mp_data_to_img(img, frame_num)

        return img

    def play_video(self, frame_delay: int):
        temp_filename = self.temp_filename

        window_name = temp_filename[(temp_filename.rfind('/') + 1):]
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
            start_frame_time = time.time()
            #TODO:  Change progressbar to show timestamp (relative to video)
            #       instead of percentage
            progress_bar.printProgressBar(frame_num,
                                          self.num_frames - 1,
                                          prefix='Playing Video: ')
            key = cv2.waitKey(frame_delay)
            if key == ord("q"):
                break
            elif key == ord(
                    "k") or key == 32:  # key == 32 means spacebar is pressed
                pause = not pause
            elif key == ord("l"):
                if frame_num < self.num_frames - 11:
                    frame_num += 10
                else:
                    frame_num = self.num_frames - 1
            elif key == ord("j"):
                if frame_num > 10:
                    frame_num -= 10
                else:
                    frame_num = 0
            elif key == ord('m'):
                if frame_num < self.num_frames - 2:
                    frame_num += 1
                else:
                    frame_num = self.num_frames - 1
            elif key == ord('n'):
                if frame_num > 0:
                    frame_num -= 1
                else:
                    frame_num = 0
            elif key == ord('o'):
                if frame_num < self.num_frames - 101:
                    frame_num += 100
                else:
                    frame_num = self.num_frames - 1
            elif key == ord('i'):
                if frame_num > 100:
                    frame_num -= 100
                else:
                    frame_num = 0
            elif key == ord('s'):
                folder = helper_functions.get_build_folder(self.temp_filename)
                self.save_frame16(frame_num, folder)
                print('Saved frame: ' + folder + '/frame_' + str(frame_num))
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

            img = self.generate_frame(frame_num)

            if frame_num == self.num_frames - 1:
                frame_num = 0  #Start video over at end

            cv2.imshow(window_name, img)
            render_time = time.time() - start_frame_time
            self.framerate = int(1 / (render_time + (frame_delay * .001)))

        print(
            '\n'
        )  # Print blank line to remove progressbar if video was quit before ending

        cv2.destroyAllWindows()

    def save_frame16(self, frame_num: int, folder: str):
        filename = folder + "/frame_" + str(frame_num) + ".png"
        plt.imsave(filename, self.temp_data[frame_num], cmap='inferno')

    def save_video(self, framerate=60):
        # generate a test frame to save correct height and width for videowriter
        test_img = self.generate_frame(0)
        height = test_img.shape[0]
        width = test_img.shape[1]
        self.framerate = framerate

        size = (width, height)
        build_folder = helper_functions.get_build_folder(self.temp_filename)
        build_number = helper_functions.get_build_number(self.temp_filename)
        filename = build_folder + build_number + '_video.avi'

        video_writer = cv2.VideoWriter(
            filename, cv2.VideoWriter_fourcc('F', 'M', 'P', '4'), framerate,
            size)

        for i, frame in enumerate(self.temp_data):
            # Display completion percentage
            progress_bar.printProgressBar(i,
                                          self.num_frames,
                                          prefix='Saving Video...')

            img = self.generate_frame(i)

            video_writer.write(img)
        print('\n')  #print a newline to get rid of progress bar

        video_writer.release()

    def save_hotspot_video(self, framerate=60, save_img=False):
        self.framerate = framerate
        height = self.temp_data[0].shape[0]
        width = self.temp_data[0].shape[1]
        size = (width, height)
        build_folder = helper_functions.get_build_folder(self.temp_filename)
        build_number = helper_functions.get_build_number(self.temp_filename)
        filename = build_folder + '/' + build_number + '_hotspot.avi'

        video_writer = cv2.VideoWriter(
            filename, cv2.VideoWriter_fourcc('F', 'M', 'P', '4'), framerate,
            size)

        hotspot_img = np.zeros((height, width), dtype=np.float32)

        for i, frame in enumerate(self.temp_data, 0):
            # Display completion percentage
            progress_bar.printProgressBar(
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

    def timestamp(self, frame):
        """Return the timestamp of the video based on the frame."""
        return self.merged_data[frame][0]

    def mp_x(self, frame):
        """Return the meltpool x value based on the frame"""
        return self.merged_data[frame][1]

    def mp_y(self, frame):
        """Return the meltpool y value based on the frame"""
        return self.merged_data[frame][2]

    def mp_z(self, frame):
        """Return the meltpool z value based on the frame"""
        return self.merged_data[frame][3]

    def mp_area(self, frame):
        """Return the meltpool area value based on the frame"""
        return self.merged_data[frame][4]

    def max_temp(self, frame):
        return np.amax(self.temp_data[frame])

    def print_info(self, frame):
        """Print the information about the current frame to console"""
        print(
            "Frame: " + str(frame),
            "| Timestamps: " +
            str(self.timestamp(frame).replace(microsecond=0)),
            "| MP X: " + str(self.mp_x(frame)),
            "| MP Y: " + str(self.mp_y(frame)),
            "| MP Z: " + str(self.mp_z(frame)),
            "| MP Area: " + str(self.mp_area(frame)),
        )

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

    def add_mp_data_to_img(self, img, frame):
        img_height = img.shape[:1][0]
        img_width = img.shape[1]
        font = cv2.FONT_HERSHEY_DUPLEX
        font_size = img_height / 860
        font_color = (0, 0, 0)
        column1_x = 5
        column2_x = int(img_width * .4)
        img = cv2.putText(
            img,
            "X: " + str(self.mp_x(frame)),
            (column1_x, int((1 / 32) * img_height)),
            font,
            font_size,
            font_color,
        )
        img = cv2.putText(
            img,
            "Y: " + str(self.mp_y(frame)),
            (column1_x, int((3 / 32) * img_height)),
            font,
            font_size,
            font_color,
        )
        img = cv2.putText(
            img,
            "Z: " + str(self.mp_z(frame)),
            (column1_x, int((5 / 32) * img_height)),
            font,
            font_size,
            font_color,
        )
        img = cv2.putText(
            img,
            "Area: " + str(self.mp_area(frame)),
            (column2_x, int((1 / 32) * img_height)),
            font,
            font_size,
            font_color,
        )
        img = cv2.putText(
            img,
            "Max Temp: " + str(self.max_temp(frame)),
            (column2_x, int((3 / 32) * img_height)),
            font,
            font_size,
            font_color,
        )
        img = cv2.putText(img,
                          "Frame: " + str(frame) + "/" + str(self.num_frames),
                          (column2_x, int((5 / 32) * img_height)), font,
                          font_size, font_color)
        time_stamp = format_time(self.timestamp(frame))
        img = cv2.putText(img, 'Time: ' + str(time_stamp),
                          (column1_x, int((7 / 32) * img_height)), font,
                          font_size, font_color)
        img = cv2.putText(img, 'Framerate: ' + str(self.framerate),
                          (column1_x, int((9 / 32) * img_height)), font,
                          font_size, font_color)
        img = cv2.putText(
            img, 'Build: ' +
            str(helper_functions.get_build_folder_name(self.temp_filename)),
            (column2_x, int(
                (9 / 32) * img_height)), font, font_size, font_color)

    def save_partial_video(self, start, end, framerate=60):
        # generate a test frame to save correct height and width for videowriter
        test_img = self.generate_frame(0)
        height = test_img.shape[0]
        width = test_img.shape[1]
        self.framerate = framerate

        size = (width, height)

        temp_filename = self.temp_filename
        filename = temp_filename[:temp_filename.rfind(
            '/')] + "/partial_" + str(start) + "-" + str(end) + ".avi"

        video_writer = cv2.VideoWriter(
            filename, cv2.VideoWriter_fourcc('F', 'M', 'P', '4'), framerate,
            size)

        progress = 0
        total = end - start
        for i in range(start, end):
            # Display completion percentage
            progress_bar.printProgressBar(progress,
                                          total,
                                          prefix='Saving Video...')

            img = self.generate_frame(i)

            video_writer.write(img)
            progress += 1

        print("Partial video saved as: '" + str(filename) +
              "'")  #print a newline to get rid of progress bar

        video_writer.release()
