import cv2
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from video_tools.reflection_remover import ReflectionRemover


class NpVidTool:
    """NpVidViewer
    Stores information relating to a video to be able to easily display a video from a numpy array

    Attributes
    ----------
    _remove_reflection : bool
        Whether or not to remove the reflection from each frame while playing the video.
    temp_data
        Numpy array of thermal cam temps loaded from the file.
    _speed : int
        Delay between each frame in ms.
    window_name : str
        Name of the window for the video to be displayed in.
    video_timestamps
        Numpy array of the thermal camera timestamps.
    meltpool_data
        Numpy array of the melt pool data.
    _mp_data_index : int
        Current index of `meltpool_data` numpy array.
    lower_bounds
        List of lower bounds of part. Used to remove the bottom reflection.
    """
    def __init__(self,
                 window_name="Video",
                 mp_data_on_img=False,
                 remove_reflection=False,
                 remove_lower=False):
        """Create an NpVidViewer Object.

        Parameters
        ----------
        window_name : str
            Name of the window that the video will be displayed in.
        remove_reflection : bool
            Run the remove reflection function if true.
        remove_lower : bool
            Run the remove_lower reflection function if true.
        """
        self.video_array = None
        self.remove_reflection = remove_reflection
        self.remove_lower = remove_lower
        self.speed = 1
        self.window_name = window_name

        self.max_temp = []
        self.mp_data_on_img = mp_data_on_img

    def generate_video(self, save_video=False):
        Tk().withdraw  #prevent tkinter from opening root window
        # Load temperature data
        self.temp_data = np.load(
            askopenfilename(title="Select thermal cam temperature data."),
            mmap_mode="r",
            allow_pickle=True)
        self.num_frames = self.temp_data.shape[0]  # Save number of frames

        # Load video timestamp data
        self.video_timestamps = np.load(
            askopenfilename(title="Select video timestamp data."),
            allow_pickle=True)

        # Load meltpool data
        self.meltpool_data = np.load(
            askopenfilename(title="Select meltpool data."), allow_pickle=True)

        self.video_array = []
        # Match the meltpool data to each frame of video
        self.match_vid_to_meltpool()

        if save_video:
            framerate = 60
            height = self.temp_data[0].shape[0]
            width = self.temp_data[0].shape[1]
            size = (width, height)
            filename = asksaveasfilename()
            video_writer = cv2.VideoWriter(
                filename, cv2.VideoWriter_fourcc("f", "m", "p", "4"),
                framerate, size)

        # Loop through each frame of data
        i = 0
        for frame in self.temp_data:
            print("Generating Video: " + str(i + 1) + "/" +
                  str(len(self.temp_data)))

            if self.remove_reflection:
                pass
            # Normalize the image to 8 bit color
            img = frame.copy()
            img = cv2.normalize(img, img, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)

            # Apply colormap to image
            img = cv2.applyColorMap(img, cv2.COLORMAP_INFERNO)

            # Add meltpool data onto the image
            if self.mp_data_on_img:
                self.add_mp_data_to_img(img, i)

            # Add image to video array
            self.video_array.append(img)

            if save_video:
                # Write image to current video file
                video_writer.write(img)
            i = i + 1

        # Release video_writer from memory
        video_writer.release()

    def play_video(self, waitKey=1):
        if self.video_array is None:
            self.generate_video()
        for frame in self.video_array:
            cv2.imshow("Video", frame)
            cv2.waitKey(waitKey)
        cv2.destroyAllWindows()

    def find_lower_bounds(self):
        """Find the lower bounds of the piece.

        Returns
        -------
        max_locations
            List of the first points at the zero level below the each max temp.
        """
        img_array = self.temp_data
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

    def match_vid_to_meltpool(self):
        """Shuffle the meltpool data and thermal camera data together based on timestamp"""
        self.matched_array = []
        self.mp_data_index = 0
        for i in range(0, self.temp_data.shape[0]):
            if self.mp_data_index + 1 < self.meltpool_data.shape[0]:
                if self.video_timestamps[i] >= self.meltpool_data[
                        self.mp_data_index + 1][0]:
                    self.mp_data_index = self.mp_data_index + 1
            self.matched_array.append([
                i, self.video_timestamps[i],
                self.meltpool_data[self.mp_data_index][0],
                self.meltpool_data[self.mp_data_index][1],
                self.meltpool_data[self.mp_data_index][2],
                self.meltpool_data[self.mp_data_index][3],
                self.meltpool_data[self.mp_data_index][4]
            ])

    def save_video(self, filename="Video.avi", framerate=60):
        """Generate video based on `temp_data` information, and save under `filename`.

        Parameters
        ----------
        filename : str
            Name to save the video file as.
        framerate : int
            Framerate to generate the video with.
        """
        height = self.temp_data[0].shape[0]
        width = self.temp_data[0].shape[1]
        size = (width, height)
        out = cv2.VideoWriter(filename,
                              cv2.VideoWriter_fourcc("f", "m", "p", "4"),
                              framerate, size)
        for i in range(0, self.temp_data.shape[0]):
            percent = (i / self.temp_data.shape[0]) * 100
            print("Saving video: " + str("%.2f" % percent) + "%")
            img = self.temp_data[i]
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
        img = self.temp_data[frame]
        self.max_temp.append(np.amax(self.temp_data[frame]))
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
        max_temp_y = np.where(self.temp_data[frame] == max_temp)[0][0]
        max_temp_x = np.where(self.temp_data[frame] == max_temp)[1][0]
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
