"""Utility to remove the heat reflection from an image"""
import numpy as np

#TODO: Remove side reflections


def remove_top(frame,
               distance=3,
               min_value=174,
               max_temp_threshold=1900,
               zero_level_threshold=176):

    max_value = np.amax(frame)
    max_value_location = np.where(frame == max_value)

    distance_from_max_val = distance
    if max_value_location[0][0] > distance_from_max_val:
        remove_to = max_value_location[0][0] - distance_from_max_val
    else:
        remove_to = 0

    frame[:remove_to] = min_value


def remove_bottom(img, lower_bounds, min_value=174):
    for i in range(0, len(lower_bounds)):
        x = lower_bounds[i][0]
        y = lower_bounds[i][1]
        img[y:, x] = min_value
        if i == 0:
            img[y:, :x] = min_value
        elif i == len(lower_bounds) - 1:
            img[y:, x:] = min_value


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
