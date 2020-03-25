from tkinter.filedialog import asksaveasfilename
import cv2
import numpy as np
import np_vid_viewer.reflection_remover
import np_vid_viewer.progress_bar as progress_bar
import np_vid_viewer.draw_line as draw_line
import os
import math
import matplotlib.pyplot as plt
import seaborn as sns

#TODO: Update documenation

# Random test comment


class NpVidTool:
    """NpVidViewer
    Stores information relating to a video to be able to easily display a video from a numpy array

    Attributes
    ----------
    build : str
        Name of the build to create the dir of images for
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
                 build: str,
                 temp_filename: str,
                 data_filename: str,
                 mp_data_on_vid=False,
                 scale_factor=1,
                 frame_delay=1,
                 remove_top_reflection=False,
                 remove_bottom_reflection=False):
        """Create an NpVidTool Object.

        Parameters
        ----------
        build : str
            directory to create for frame images
        mp_data_on_vid : bool
            Add meltpool data on top of the video if true.
        remove_top_reflection : bool
            Run remove_top_reflection if true.
        remove_bottom_reflection : bool
            Run remove_bottom_reflection if true.
        """
        self.imgdir = build
        self.video_array = None
        self.remove_top_reflection = remove_top_reflection
        self.remove_bottom_reflection = remove_bottom_reflection
        self.mp_data_on_vid = mp_data_on_vid
        self.maxTemps = []
        self.building = False
        if build is not None:
            self.building = True
            try:
                os.mkdir(build)
            except OSError:
                print ("Creation of the directory %s failed" % build)
            else:
                print ("Successfully created the directory %s " % build)


        # Load temperature data
        self.temp_filename = temp_filename
        self.temp_data = np.load(temp_filename,
                                 mmap_mode="r",
                                 allow_pickle=True)
        self.num_frames = self.temp_data.shape[0]  # Save number of frames

        # Load merged data
        self.merged_data = np.load(data_filename, allow_pickle=True)

        # Find lower bounds of piece if remove_lower reflection is selected
        if self.remove_bottom_reflection:
            self.lower_bounds = np_vid_viewer.reflection_remover.find_lower_bounds(
                self.temp_data)
        else:
            self.lower_bounds = None

        # Set scale factor for resizing frames of video
        self.scale_factor = scale_factor

        # Set frame delay for playing video
        self.frame_delay = frame_delay

    def generate_frame(self, frame_num):
        frame = self.temp_data[frame_num].copy()

        if self.remove_top_reflection:
            np_vid_viewer.reflection_remover.remove_top(
                frame, zero_level_threshold=180, max_temp_threshold=700)

        if self.remove_bottom_reflection:
            np_vid_viewer.reflection_remover.remove_bottom(
                frame, self.lower_bounds)

        # Normalize the image to 8 bit color
        img = frame.copy()
        maxpoint = self.findHottestPoint(img)
        endpoint = self.findCoolestAdjacent(img, maxpoint)
        points = draw_line.findline(img, maxpoint)
        #img = self.drawHeatDisArrows(img)
        img = cv2.normalize(img, img, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
        img = cv2.circle(img, maxpoint, 1,(0,255,0),1)
        img = draw_line.drawline(img, points)
        #img = cv2.arrowedLine(img, maxpoint, endpoint, (0,0,0),1)
        # Apply colormap to image
        img = cv2.applyColorMap(img, cv2.COLORMAP_INFERNO)

        # Scale image according to scale_factor
        width = int(img.shape[1] * self.scale_factor)
        height = int(frame.shape[0] * self.scale_factor)
        size = (width, height)

        img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)

        # Extend frame for mp_data
        if self.mp_data_on_vid:
            img = cv2.copyMakeBorder(img,
                                     int(height * (11 / 16)),
                                     0,
                                     0,
                                     0,
                                     cv2.BORDER_CONSTANT,
                                     value=(255, 255, 255))

        # Add meltpool data onto the image
        if self.mp_data_on_vid:
            self.add_mp_data_to_img(img, frame_num)

        return img

    def play_video(self):
        """Create a window and play the video stored in video_array.
        generate_video will be run automatically if it has not been run.

        Parameters
        -----------
        waitKey : int, optional
            Time (ms) delay between showing each frame.
        """
        temp_filename = self.temp_filename

        window_name = temp_filename[(temp_filename.rfind('/') + 1):]
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, 640, 480)

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
            #TODO:  Change progressbar to show timestamp (relative to video)
            #       instead of percentage
            progress_bar.printProgressBar(frame_num,
                                          self.num_frames - 1,
                                          prefix='Playing Video: ')
            key = cv2.waitKey(self.frame_delay)
            if key == ord("q"):
                break
            elif key == ord(
                    "k") or key == 32:  # key == 32 means spacebar is pressed
                self.heatFluxDraw(img)
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
                filename = temp_filename[:temp_filename.rfind(
                    '/')] + "/frame_" + str(frame_num + 1) + ".png"
                print("Saved image to: " + filename)
                cv2.imwrite(filename, self.generate_frame(frame_num))
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


            #self.heatFluxDraw(img)
            #img = cv2.imread("tmp.png")

            cv2.imshow(window_name, img)
            if self.building:
                path = self.imgdir + "/" + str(frame_num) + ".png"
                cv2.imwrite(path, img)

        print(
            '\n'
        )  # Print blank line to remove progressbar if video was quit before ending

        cv2.destroyAllWindows()

    def save_video(self, playback_speed=15, realtime_framerate=4):
        """Save the video as a .avi file.

        Parameters
        ----------
        playback_speed : int, optional
            Multiple of realtime speed to playback video at.
        realtime_framerate : int, optional
            Number of frames taken by the thermal camera in real time.
        """

        framerate = playback_speed * realtime_framerate
        height = self.temp_data[0].shape[0] * self.scale_factor
        width = self.temp_data[0].shape[1] * self.scale_factor
        size = (width, height)
        filename = asksaveasfilename()

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

        video_writer.release()

    def save_hotspot_video(self,
                           playback_speed=15,
                           realtime_framerate=4,
                           save_img=False):
        framerate = playback_speed * realtime_framerate
        height = self.temp_data[0].shape[0] * self.scale_factor
        width = self.temp_data[0].shape[1] * self.scale_factor
        size = (width, height)
        filename = asksaveasfilename()

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
            cv2.imwrite('hotspot_img.png', hotspot_img_frame)

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
        img_width = img.shape[1]
        font = cv2.FONT_HERSHEY_DUPLEX
        font_size = img_height / 480
        font_color = (0, 0, 0)
        column1_x = 25
        column2_x = int(img_width * .5)
        img = cv2.putText(
            img,
            "X: " + str(self.mp_x(frame)),
            (column1_x, int((1 / 16) * img_height)),
            font,
            font_size,
            font_color,
        )
        img = cv2.putText(
            img,
            "Y: " + str(self.mp_y(frame)),
            (column1_x, int((2 / 16) * img_height)),
            font,
            font_size,
            font_color,
        )
        img = cv2.putText(
            img,
            "Z: " + str(self.mp_z(frame)),
            (column1_x, int((3 / 16) * img_height)),
            font,
            font_size,
            font_color,
        )
        img = cv2.putText(
            img,
            "Area: " + str(self.mp_area(frame)),
            (column1_x, int((4 / 16) * img_height)),
            font,
            font_size,
            font_color,
        )
        img = cv2.putText(
            img,
            "Max Temp: " + str(self.max_temp(frame)),
            (column1_x, int((5 / 16) * img_height)),
            font,
            font_size,
            font_color,
        )
        img = cv2.putText(
            img, "Frame: " + str(frame + 1) + "/" + str(self.num_frames),
            (column1_x, int(
                (6 / 16) * img_height)), font, font_size, font_color)

    def generate_threshold_image(self, threshold=800):
        height = self.temp_data[0].shape[0] * self.scale_factor
        width = self.temp_data[0].shape[1] * self.scale_factor
        threshold_img = np.zeros((height, width), dtype=np.float32)
        for i, frame in enumerate(self.temp_data, 0):
            # Show progress
            progress_bar.printProgressBar(
                i, self.num_frames, prefix='Generating threshold image...')

            # Check each pixel, if pixel is over threshold, increment that pixel in theshold_img
            for y, row in enumerate(frame):
                for x, pixel in enumerate(row):
                    if pixel > threshold:
                        threshold_img[y, x] += 1

        threshold_img = cv2.normalize(src=threshold_img,
                                      dst=threshold_img,
                                      alpha=0,
                                      beta=255,
                                      norm_type=cv2.NORM_MINMAX,
                                      dtype=cv2.CV_8UC1)
        threshold_img = cv2.applyColorMap(threshold_img, cv2.COLORMAP_INFERNO)

        cv2.imwrite("threshold_img.png", threshold_img)


    def heatFluxDraw(self, image):

        print(image[125,150,:])

        vertical_max, horizontal_max, colorValues = np.shape(image)

        horizontal_min, horizontal_stepsize = 0, 1 #set bounds for plot
        vertical_min, vertical_stepsize = 0, 1

        horizontal_dist = horizontal_max-horizontal_min
        vertical_dist = vertical_max-vertical_min

        horizontal_stepsize = horizontal_dist / float(math.ceil(horizontal_dist/float(horizontal_stepsize)))
        vertical_stepsize = vertical_dist / float(math.ceil(vertical_dist/float(vertical_stepsize)))

        xv, yv =np.meshgrid(np.arange(horizontal_min, horizontal_max, horizontal_stepsize),
                            np.arange(vertical_min, vertical_max, vertical_stepsize))

        xv+=horizontal_stepsize/2.0 #Arrow placed in center of each pixel
        yv+=vertical_stepsize/2.0
        result_matrix = np.asmatrix(image[:,:,0]) #convert data to np matrix
        yd, xd = np.gradient(result_matrix)

        skip = (slice(None, None, 2), slice(None, None, 2)) #sets amount of arrows shown


        def func_to_vectorize(x, y, dx, dy, scaling=0.01):
            plt.arrow(x, y, dx*scaling, dy*scaling, fc="k", ec="k", head_width=0.2, head_length=0.2) #scales arrow size

        vectorized_arrow_drawing = np.vectorize(func_to_vectorize)

        fig = plt.imshow(np.flip(result_matrix,0), extent=[horizontal_min, horizontal_max, vertical_min, vertical_max])
        vectorized_arrow_drawing(xv[skip], yv[skip], -xd[skip], -yd[skip], 0.001) #scale of vector magnitude



        sns.heatmap(image[:,:,0], fmt="d")
        #plt.colorbar()
        plt.axis("off")
        fig.axes.get_xaxis().set_visible(False)
        fig.axes.get_yaxis().set_visible(False)
        plt.savefig("tmp.png", bbox='tight', pad_inches=0)
        #plt.show()


    def findHottestPoint(self, image):
        color = (0, 0, 0)
        thickness = 1
        tmpmax = 0
        x = 0
        for row in image:
            y = 0
            for cell in row:
                if int(cell) > tmpmax:
                    tmpmax = int(cell)
                    maxpoint = (y,x)
                y = y + 1
            x = x + 1
        self.maxTemps.append(tmpmax)
        return maxpoint

    def findCoolestAdjacent(self, image, maxpoint):
        adjacent = np.arange(-3, 4)
        tmpmin = 999999
        minpoint = maxpoint
        for i in range(adjacent.size):
            for z in range(adjacent.size):
                if maxpoint[0]-adjacent[i] > (image.shape[0] - 1) or maxpoint[1]-adjacent[z] > (image.shape[1] - 1):
                    continue
                if int(image[maxpoint[0]-adjacent[i],maxpoint[1]-adjacent[z]]) < tmpmin:
                    tmpmin = int(image[maxpoint[0]-adjacent[i],maxpoint[1]-adjacent[z]])
                    minpoint = (maxpoint[0]-adjacent[i],maxpoint[1]-adjacent[z])

        return minpoint


    def drawHeatDisArrows(self, image):
        color = (0, 255, 0)
        thickness = 1

        x = 0
        for row in image:
            y = 0
            for cell in row:

                if int(cell) > 174:
                    #print(cell)
                    tmp = 999999
                    start = (y,x)

                    adjacent = [-2, -1, 0, 1, 2]
                    for i in range(5):
                        for z in range(5):
                            if int(image[x-adjacent[i],y-adjacent[z]]) < tmp:
                                #print(image[x-i, y-z])
                                end = (y-adjacent[z],x-adjacent[i])
                                tmp = int(image[y-adjacent[z],x-adjacent[i]])
                    print("Start: " + str(start) + "End: " + str(end))
                    image = cv2.arrowedLine(image, start, end, color, thickness)
                y = y + 1
            x = x + 1
        return image

