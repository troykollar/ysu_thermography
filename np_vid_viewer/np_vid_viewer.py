import cv2
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from np_vid_viewer import reflection_remover


class NpVidViewer:
    """NpVidViewer
    Stores information relating to a video to be able to easily display a video from a numpy array

    Attributes
    ----------
    _remove_reflection : bool
        Whether or not to remove the reflection from each frame while playing the video.
    _array
        Numpy array of thermal cam temps loaded from the file.
    _speed : int
        Delay between each frame in ms.
    _window_name : str
        Name of the window for the video to be displayed in.
    _timestamps
        Numpy array of the thermal camera timestamps.
    _melt_pool_data
        Numpy array of the melt pool data.
    _mp_data_index : int
        Current index of `_melt_pool_data` numpy array.
    _lower_bounds
        List of lower bounds of part. Used to remove the bottom reflection.
    """
    def __init__(self,
                 filename: str,
                 melt_pool_data,
                 tc_times,
                 window_name="Video",
                 remove_reflection=False,
                 remove_lower=False):
        """Create an NpVidViewer Object.

        Parameters
        ----------
        file_name : str
            Name of the numpy file that contains the thermal cam temps.
        window_name : str
            Name of the window that the video will be displayed in.
        melt_pool_data : str
            Name of the numpy file that contains the melt pool data.
        tc_times : str
            Name of the numpy file that contains the thermal camera timestamps.
        remove_reflection : bool
            Run the remove reflection function if true.
        remove_lower : bool
            Run the remove_lower reflection function if true.
        """
        Tk().withdraw  #prevent tkinter from opening root window
        self._array = np.load(
            askopenfilename(title="Select thermal cam temperature data."),
            mmap_mode="r",
            allow_pickle=True)
        self._timestamps = np.load(
            askopenfilename(title="Select video timestamp data."),
            allow_pickle=True)
        self._melt_pool_data = np.load(
            askopenfilename(title="Select meltpool data."), allow_pickle=True)

        self._remove_reflection = remove_reflection
        self._remove_lower = remove_lower
        self._speed = 1
        self._window_name = window_name
        self._num_frames = self.array.shape[0]
        self._mp_data_index = 0
        self.match_vid_to_meltpool()
        self._lower_bounds = self.find_lower_bounds()
        self.max_temp = []

    def find_lower_bounds(self):
        """Find the lower bounds of the piece.

        Returns
        -------
        max_locations
            List of the first points at the zero level below the each max temp.
        """
        img_array = self.array
        i = 0
        # Find the x and y value of the max temp of first frame
        max_x = np.where(img_array[0] == np.amax(img_array[0]))[1][0]
        max_y = np.where(img_array[0] == np.amax(img_array[0]))[0][0]

        # Find the x value of the max temp of the next frame
        next_max_x = np.where(img_array[1] == np.amax(img_array[1]))[1][0]

        # Create lists of the x and y values of the max temperatures
        max_x_locations = []
        max_y_locations = []

        # While the laser is moving to the right. (i.e. the next location > current location)
        while max_x < next_max_x:
            max_x_locations.append([i, max_x])
            max_y_locations.append([i, max_y])
            i = i + 1
            max_x = np.where(img_array[i] == np.amax(img_array[i]))[1][0]
            next_max_x = np.where(
                img_array[i + 1] == np.amax(img_array[i + 1]))[1][0]
            max_y = np.where(img_array[i] == np.amax(img_array[i]))[0][0]

        for frame in range(0, len(max_y_locations)):
            while img_array[frame, max_y_locations[frame][1],
                            max_x_locations[frame][1]] > 174:
                max_y_locations[frame][1] += 1

        max_locations = []
        j = 0
        for i in range(max_x_locations[0][1], max_x_locations[-1][1]):
            if i > max_x_locations[j][1]:
                j = j + 1
            max_locations.append((i, max_y_locations[j][1]))
        return max_locations

    @property
    def lower_bounds(self):
        """Return the lower bounds"""
        return self._lower_bounds

    def match_vid_to_meltpool(self):
        """Shuffle the meltpool data and thermal camera data together based on timestamp"""
        self._matched_array = []
        for i in range(0, self.array.shape[0]):
            if self.mp_data_index + 1 < self.melt_pool_data.shape[0]:
                if self.timestamps[i] >= self.melt_pool_data[self.mp_data_index
                                                             + 1][0]:
                    self.mp_data_index = self.mp_data_index + 1
            self._matched_array.append([
                i, self.timestamps[i],
                self.melt_pool_data[self.mp_data_index][0],
                self.melt_pool_data[self.mp_data_index][1],
                self.melt_pool_data[self.mp_data_index][2],
                self.melt_pool_data[self.mp_data_index][3],
                self.melt_pool_data[self.mp_data_index][4]
            ])

    def save_video(self, filename="Video.avi", framerate=60):
        """Generate video based on `_array` information, and save under `filename`.

        Parameters
        ----------
        filename : str
            Name to save the video file as.
        framerate : int
            Framerate to generate the video with.
        """
        height = self.array[0].shape[0]
        width = self.array[0].shape[1]
        size = (width, height)
        out = cv2.VideoWriter(filename,
                              cv2.VideoWriter_fourcc("f", "m", "p", "4"),
                              framerate, size)
        for i in range(0, self.array.shape[0]):
            percent = (i / self.array.shape[0]) * 100
            print("Saving video: " + str("%.2f" % percent) + "%")
            img = self.array[i]
            normalized_img = img.copy()
            if self.remove_reflection:
                ReflectionRemover.remove(normalized_img,
                                         zero_level_threshold=180,
                                         max_temp_threshold=700,
                                         remove_lower=self._remove_lower,
                                         lower_bounds=self.lower_bounds)

            normalized_img = cv2.normalize(normalized_img, normalized_img, 0,
                                           255, cv2.NORM_MINMAX, cv2.CV_8UC1)
            normalized_img = cv2.applyColorMap(normalized_img,
                                               cv2.COLORMAP_INFERNO)

            self.add_mp_data_to_img(normalized_img, i)

            out.write(normalized_img)

        out.release()

    @property
    def remove_reflection(self):
        """Return `_remove_reflection` attribute"""
        return self._remove_reflection

    @property
    def num_frames(self):
        """Return `_num_frames` attritbute. The number of frames in the video."""
        return self._num_frames

    def video_timestamp(self, frame):
        """Return the timestamp of the video based on the frame."""
        return self.matched_array[frame][1]

    def mp_timestamp(self, frame):
        """Return the timestamp of the melt pool data based on the frame."""
        return self.matched_array[frame][2]

    def mp_x(self, frame):
        """Return the meltpool x value based on the frame"""
        return self.matched_array[frame][3]

    def mp_y(self, frame):
        """Return the meltpool y value based on the frame"""
        return self.matched_array[frame][4]

    def mp_z(self, frame):
        """Return the meltpool z value based on the frame"""
        return self.matched_array[frame][5]

    def mp_area(self, frame):
        """Return the meltpool area value based on the frame"""
        return self.matched_array[frame][6]

    @property
    def matched_array(self):
        """Return the array of meltpool and video matched values"""
        return self._matched_array

    @property
    def mp_data_index(self):
        """Return the current index of the meltpool data array"""
        return self._mp_data_index

    @mp_data_index.setter
    def mp_data_index(self, value: int):
        """Set the `_mp_data_index` ensuring it is within bounds of the `_melt_pool_data` array."""
        if value < 0:
            self._mp_data_index = 0
        elif value > self._melt_pool_data.shape[0]:
            self._mp_data_index = self._melt_pool_data.shape[:0][0]
        else:
            self._mp_data_index = value

    @property
    def melt_pool_data(self):
        """Return the `_melt_pool_data` array"""
        return self._melt_pool_data

    @property
    def window_name(self):
        """Return the name of the window"""
        return self._window_name

    @property
    def array(self):
        """Return the array containing the thermal cam temp data"""
        return self._array

    @property
    def speed(self):
        """Return `_speed`"""
        return self._speed

    @speed.setter
    def speed(self, new_speed):
        """Set the speed, ensuring it is within OpenCV bounds of 1 <= speed <= 1000"""
        if new_speed < 1:
            self._speed = 1
        elif new_speed > 1000:
            self._speed = 1000
        else:
            self._speed = new_speed

    @property
    def timestamps(self):
        """Return the thermal camera timestamps"""
        return self._timestamps

    def print_info(self, frame):
        """Print the information about the current frame to console"""
        print(
            "Frame: " + str(frame),
            "| TC time: " +
            str(self.mp_timestamp(frame).replace(microsecond=0)),
            "| MP time: " +
            str(self.mp_timestamp(frame).replace(microsecond=0)),
            "| MP X: " + str(self.mp_x(frame)),
            "| MP Y: " + str(self.mp_y(frame)),
            "| MP Z: " + str(self.mp_z(frame)),
            "| MP Area: " + str(self.mp_area(frame)),
        )

    def update_image(self, frame: int):
        """Normalize the array data. Apply the colormap, and add meltpool data to the image.

        Parameters
        ----------
        frame : int
            The current frame of the video
        Returns
        -------
        normalized_img
            Numpy array of the updated image of the current frame.
        """
        img = self.array[frame]
        self.max_temp.append(np.amax(self.array[frame]))
        normalized_img = img.copy()
        if self.remove_reflection:
            reflection_remover.ReflectionRemover.remove(
                normalized_img,
                zero_level_threshold=180,
                max_temp_threshold=700,
                remove_lower=self._remove_lower,
                lower_bounds=self.lower_bounds,
            )

        normalized_img = cv2.normalize(normalized_img, normalized_img, 0, 255,
                                       cv2.NORM_MINMAX, cv2.CV_8UC1)
        normalized_img = cv2.applyColorMap(normalized_img,
                                           cv2.COLORMAP_INFERNO)

        self.add_mp_data_to_img(normalized_img, frame)
        self.highlight_max_temp(frame, normalized_img)

        self.print_info(frame)
        return normalized_img

    def highlight_max_temp(self, frame, img):
        max_temp = self.max_temp[frame]
        max_temp_y = np.where(self.array[frame] == max_temp)[0][0]
        max_temp_x = np.where(self.array[frame] == max_temp)[1][0]
        img[max_temp_y, max_temp_x] = (255, 255, 255)

    def add_mp_data_to_img(self, img, frame):
        """Add meltpool data to the image.
        
        Parameters
        ----------
        img
            Image to add the meltpool data text to
        frame : int
            Frame number to grab meltpool data for
        """
        img_height = img.shape[:1][0]
        font = cv2.FONT_HERSHEY_DUPLEX
        font_size = img_height / 480
        font_color = (255, 255, 255)
        img = cv2.putText(
            img,
            "X: " + str(self.mp_x(frame)),
            (50, int((1 / 16) * img_height)),
            font,
            font_size,
            font_color,
        )
        img = cv2.putText(
            img,
            "Y: " + str(self.mp_y(frame)),
            (50, int((2 / 16) * img_height)),
            font,
            font_size,
            font_color,
        )
        img = cv2.putText(
            img,
            "Z: " + str(self.mp_z(frame)),
            (50, int((3 / 16) * img_height)),
            font,
            font_size,
            font_color,
        )
        img = cv2.putText(
            img,
            "Area: " + str(self.mp_area(frame)),
            (50, int((4 / 16) * img_height)),
            font,
            font_size,
            font_color,
        )
        img = cv2.putText(img, "Max Temp: " + str(self.max_temp[frame]),
                          (50, int((5 / 16) * img_height)), font, font_size,
                          font_color)

    def play_video(self, speed=1):
        """Play the video.

        Arguments
        ---------
        speed : int
            Delay in ms between showing each frame. Must be 1-1000.
        """
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window_name, 640, 480)
        self.speed = speed
        pause = False
        frame = 0
        while True:
            key = cv2.waitKey(self.speed)
            if not pause:
                img = self.update_image(frame)
                cv2.imshow(self.window_name, img)
                frame = frame + 1
            elif pause:
                if key == ord("s"):
                    np.savetxt(
                        "tc_temps-" + str(frame + 1) + ".csv",
                        img,
                        fmt="%d",
                        delimiter=",",
                    )
                elif key == ord("l"):
                    frame = frame + 10
                    img = self.update_image(frame)
                    cv2.imshow(self.window_name, img)
                elif key == ord("j"):
                    if frame > 10:
                        frame = frame - 10
                    else:
                        frame = 0
                    img = self.update_image(frame)
                    cv2.imshow(self.window_name, img)

            if key == ord("q"):
                break
            elif key == ord("k"):
                pause = not pause
            elif frame >= self.num_frames:
                break
        cv2.destroyAllWindows()
