"""Utility to remove the heat reflection from an image"""
import numpy as np
import cv2

#TODO: Remove side reflections


def remove_top(frame, min_value=174, min_value_threshold=5):
    max_value = np.amax(frame)
    max_value_location = np.where(frame == max_value)
    max_value_y = max_value_location[0][0]

    mean = np.mean(frame[max_value_y])
    y = max_value_y
    while mean > min_value + min_value_threshold:
        if y == 0:
            break
        else:
            y -= 1
        mean = np.mean(frame[y])

    frame[:y] = min_value

    # Draw a line at top of piece (for debugging)
    #cv2.line(frame, (0, y), (frame.shape[1], y), int(np.amax(frame)), 1)


def remove_bottom(frame, min_value=174):
    max_value = np.amax(frame)
    max_value_location = np.where(frame == max_value)
    max_value_y = max_value_location[0][0]
    x = max_value_location[1][0]
    last_row_y = frame.shape[0] - 2

    y = max_value_y
    temp = frame[y, x]
    prev_temp = temp

    while y < last_row_y:
        temp = frame[y, x]
        if prev_temp < temp:
            if np.mean(frame[y]) > np.mean(frame[y + 1]):
                prev_temp = temp
                y += 1
            else:
                break
        else:
            prev_temp = temp
            y += 1

    #frame[y:] = min_value

    # Draw a line at bottom of piece (for debugging)
    cv2.line(frame, (0, y), (frame.shape[1], y), int(np.amax(frame)), 1)


def find_lower_bounds(temp_data):
    """Find the lower bounds of the piece.

        Returns
        -------
        max_locations
            List of the first points at the zero level below the each max temp.
        """
    temp_data
    i = 0
    # Find the x and y value of the max temp of first frame
    max_x = np.where(temp_data[0] == np.amax(temp_data[0]))[1][0]
    max_y = np.where(temp_data[0] == np.amax(temp_data[0]))[0][0]

    # Find the x value of the max temp of the next frame
    next_max_x = np.where(temp_data[1] == np.amax(temp_data[1]))[1][0]

    # Create lists of the x and y values of the max temperatures
    max_x_locations = []
    max_y_locations = []

    # While the laser is moving to the right. (i.e. the next location > current location)
    while max_x < next_max_x:
        max_x_locations.append([i, max_x])
        max_y_locations.append([i, max_y])
        i = i + 1
        max_x = np.where(temp_data[i] == np.amax(temp_data[i]))[1][0]
        next_max_x = np.where(temp_data[i + 1] == np.amax(temp_data[i +
                                                                    1]))[1][0]
        max_y = np.where(temp_data[i] == np.amax(temp_data[i]))[0][0]

    for frame in range(0, len(max_y_locations)):
        while temp_data[frame, max_y_locations[frame][1],
                        max_x_locations[frame][1]] > 174:
            max_y_locations[frame][1] += 1

    max_locations = []
    j = 0
    for i in range(max_x_locations[0][1], max_x_locations[-1][1]):
        if i > max_x_locations[j][1]:
            j = j + 1
        max_locations.append((i, max_y_locations[j][1]))
    return max_locations
