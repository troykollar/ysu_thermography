import numpy as np
import matplotlib.pyplot as plt
import np_vid_viewer
import np_vid_viewer.progress_bar as progress_bar


def generate_threshold_image(temp_filename: str, threshold=800):
    # Get temp data info
    temp_data = np.load(temp_filename, mmap_mode="r", allow_pickle=True)
    build_folder = temp_filename[:temp_filename.rfind('/')]
    build_number = build_folder[:build_folder.find('_')]
    build_number = build_number[(build_number.rfind('/') + 1):]

    # Get frame info
    num_frames = temp_data.shape[0]
    height = temp_data[0].shape[0]
    width = temp_data[0].shape[1]

    # Make blank image to increment
    threshold_img = np.zeros((height, width), dtype=np.float32)

    # Check each pixel, if pixel is over threshold, increment that pixel in theshold_img
    for i, frame in enumerate(temp_data):
        # Show progress
        progress_bar.printProgressBar(i,
                                      num_frames,
                                      prefix='Generating threshold image...')
        over_thresh_array = np.where(frame > threshold)

        if over_thresh_array[0].size > 0:
            for x_index, y in enumerate(over_thresh_array[0]):
                x = over_thresh_array[1][x_index]
                threshold_img[y, x] += 1

    # Generate a filename based on build_number and threshold used
    filename = build_folder + '/' + build_number + '_threshold' + str(
        threshold) + '.png'
    plt.imsave(filename, threshold_img, cmap='inferno')
    print('Threshold img saved as: ' + filename)
