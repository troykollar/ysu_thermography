from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
import cv2
import numpy as np
import np_vid_viewer.reflection_remover
import np_vid_viewer.progress_bar as progress_bar


class NpVidTool:
    """NpVidViewer
    Stores information relating to a video to be able to easily display a video from a numpy array

    Attributes
    ----------
    video_array : list
        List of images that will be used for displaying/saving video.
        Images contain all adjustments and overlays.
    remove_top_reflection : bool
        Attempt to remove the top reflection if true.
    remove_bottom_reflection : bool
        Attempt to remove the bottom reflection if true.
    temp_data
        Numpy array of thermal cam temps loaded from the file.
    num_frames : int
        Number of frames in the video
    video_timestamps
        Numpy array of the thermal camera timestamps.
    meltpool_data
        Numpy array of the melt pool data.
    matched_array : list
        List containing the relevant data video and meltpool data after matching
    mp_data_on_vid : bool
        Overlay meltpool data on the video if true.
    """
    def __init__(self,
                 mp_data_on_vid=False,
                 remove_top_reflection=False,
                 remove_bottom_reflection=False):
        """Create an NpVidTool Object.

        Parameters
        ----------
        mp_data_on_vid : bool
            Add meltpool data on top of the video if true.
        remove_top_reflection : bool
            Run remove_top_reflection if true.
        remove_bottom_reflection : bool
            Run remove_bottom_reflection if true.
        """
        self.video_array = None
        self.remove_top_reflection = remove_top_reflection
        self.remove_bottom_reflection = remove_bottom_reflection
        self.mp_data_on_vid = mp_data_on_vid

        self.temp_data = None
        self.num_frames = 0
        self.merged_data = None

    def generate_video(self, temp_filename: str, data_filename: str):
        """Load temperature and meltpool data, match them, and create the video array"""
        # Load temperature data
        self.temp_data = np.load(temp_filename,
                                 mmap_mode="r",
                                 allow_pickle=True)
        self.num_frames = self.temp_data.shape[0]  # Save number of frames

        # Load merged data
        self.merged_data = np.load(data_filename, allow_pickle=True)

        self.video_array = []

        if self.remove_bottom_reflection:
            lower_bounds = np_vid_viewer.reflection_remover.find_lower_bounds(
                self.temp_data)

        # Loop through each frame of data
        i = 0
        for frame in self.temp_data:
            frame = frame.copy()  # Make copy since file is read-only

            progress_bar.printProgressBar(i,
                                          self.num_frames,
                                          prefix='Generating Video...',
                                          length=50)

            if self.remove_top_reflection:
                np_vid_viewer.reflection_remover.remove_top(
                    frame, zero_level_threshold=180, max_temp_threshold=700)

            if self.remove_bottom_reflection:
                np_vid_viewer.reflection_remover.remove_bottom(
                    frame, lower_bounds)
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

            i = i + 1

    def play_video(self, waitKey=1):
        """Create a window and play the video stored in video_array. 
        generate_video will be run automatically if it has not been run.
        
        Parameters
        -----------
        waitKey : int, optional
            Time (ms) delay between showing each frame.
        """
        if self.video_array is None:
            self.generate_video()
        # TODO: Automatically make the window name the name of the build
        cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Video", 640, 480)

        frame_num = 0
        pause = False
        while True:
            key = cv2.waitKey(waitKey)
            if key == ord("q"):
                break
            elif key == ord("k"):
                pause = not pause
            elif key == ord("l"):
                frame_num += 10
            elif key == ord("j"):
                frame_num -= 10

            if not pause:
                frame_num += 1
            else:
                pass

            frame = self.video_array[frame_num]
            cv2.imshow("Video", frame)

        cv2.destroyAllWindows()

    def save_video(self,
                   temp_filename: str,
                   data_filename: str,
                   playback_speed=15,
                   realtime_framerate=4):
        """Save the video as a .avi file.

        Parameters
        ----------
        playback_speed : int, optional
            Multiple of realtime speed to playback video at.
        realtime_framerate : int, optional
            Number of frames taken by the thermal camera in real time.
        """
        if self.video_array is None:
            self.generate_video(temp_filename, data_filename)

        framerate = playback_speed * realtime_framerate
        height = self.temp_data[0].shape[0]
        width = self.temp_data[0].shape[1]
        size = (width, height)
        filename = asksaveasfilename()

        video_writer = cv2.VideoWriter(filename,
                                       cv2.VideoWriter_fourcc(*'MPEG'),
                                       framerate, size)

        i = 0
        print("Saving video...")
        for frame in self.video_array:
            # Display completion percentage
            progress_bar.printProgressBar(i,
                                          self.num_frames,
                                          prefix='Saving Video...',
                                          length=50)

            video_writer.write(frame)

            i = i + 1

        video_writer.release()

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

    def max_temp(self, frame):
        """Return the max temp of the given frame"""
        return self.matched_array[frame][7]

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

    #TODO: Add Highlight max temp function

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
        img = cv2.putText(
            img,
            "Max Temp: " + str(self.max_temp(frame)),
            (50, int((5 / 16) * img_height)),
            font,
            font_size,
            font_color,
        )
