import cv2
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename


class NpVidTool:
    """NpVidViewer
    Stores information relating to a video to be able to easily display a video from a numpy array

    Attributes
    ----------
    video_array : list
        List of images that will be used for displaying/saving video.
        Images contain all adjustments/overlays.
    temp_data
        Numpy array of thermal cam temps loaded from the file.
    remove_top_reflection : bool
        Attempt to remove the top reflection if true.
    remove_bottom_reflection : bool
        Attempt to remove the bottom reflection if true.
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
                 mp_data_on_vid=False,
                 remove_top_reflection=False,
                 remove_bottom_reflection=False):
        """Create an NpVidViewer Object.

        Parameters
        ----------
        window_name : str
            Name of the window that the video will be displayed in.
        mp_data_on_vid : bool
            Add meltpool data on top of the video if true
        remove_reflection : bool
            Run the remove reflection function if true.
        remove_lower : bool
            Run the remove_lower reflection function if true.
        """
        self.video_array = None
        self.remove_top_reflection = remove_top_reflection
        self.remove_bottom_reflection = remove_bottom_reflection
        self.window_name = window_name

        self.max_temp = []
        self.mp_data_on_vid = mp_data_on_vid

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

            if self.remove_top_reflection:
                pass
            # Normalize the image to 8 bit color
            img = frame.copy()
            img = cv2.normalize(img, img, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)

            # Apply colormap to image
            img = cv2.applyColorMap(img, cv2.COLORMAP_INFERNO)

            # Add meltpool data onto the image
            if self.mp_data_on_vid:
                self.add_mp_data_to_img(img, i)

            # Add image to video array
            self.video_array.append(img)

            if save_video:
                # Write image to current video file
                video_writer.write(img)
            i = i + 1

        # Release video_writer from memory
        if save_video:
            video_writer.release()

    def play_video(self, waitKey=1):
        if self.video_array is None:
            self.generate_video()
        for frame in self.video_array:
            cv2.imshow("Video", frame)
            cv2.waitKey(waitKey)
        cv2.destroyAllWindows()

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
